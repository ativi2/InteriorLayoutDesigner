import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional, Tuple
import os
import random
import uuid

from utils import get_mouse_pos_in_canvas, get_wall_color_hex, get_floor_design_color
from room import Room
from furniture import Furniture, get_furniture_item_by_id
from room_templates import load_room_template, get_room_template_names
from assets.wall_colors import WALL_COLORS
from assets.floor_designs import FLOOR_DESIGNS
from assets.furniture_items import FURNITURE_ITEMS

# Set page config
st.set_page_config(
    page_title="Interior Design Simulator",
    page_icon="🏠",
    layout="wide"
)

# Initialize session state for room
if 'room' not in st.session_state:
    st.session_state.room = Room(width=500, height=400, wall_color="White", floor_design="Hardwood")
    
if 'camera_x' not in st.session_state:
    st.session_state.camera_x = 1.5
    
if 'camera_y' not in st.session_state:
    st.session_state.camera_y = 1.5
    
if 'camera_z' not in st.session_state:
    st.session_state.camera_z = 1.5

def main():
    # ===== HEADER SECTION =====
    # Top header with site name and details
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #2c3e50; border-radius: 10px; margin-bottom: 20px; color: #ecf0f1;">
        <h1 style="color: #e74c3c;">Interior Design Simulator</h1>
        <p style="color: #ecf0f1; font-size: 18px;">An interactive tool for visualizing and planning interior spaces in 3D</p>
        <p style="color: #ecf0f1; font-size: 16px;">Design your dream space with customizable walls, floors, and furniture</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== 3D VISUALIZATION SECTION =====
    # This section will contain only the 3D view of the room for maximum visibility
    st.markdown("<h2 style='text-align: center;'>3D Room Visualization</h2>", unsafe_allow_html=True)
    
    # Get room dimensions
    width = st.session_state.room.width
    height = st.session_state.room.height
    room_height = 250 / 100  # Default room height in meters
    
    # Get camera settings from session state
    camera_x = st.session_state.camera_x
    camera_y = st.session_state.camera_y
    camera_z = st.session_state.camera_z
    
    # Convert room dimensions from cm to meters for visualization
    width_m = width / 100
    height_m = height / 100
    
    # Create 3D visualization
    fig = go.Figure()
    
    # Get floor design colors
    floor_colors = get_floor_design_color(st.session_state.room.floor_design)
    
    # Add floor with pattern
    floor_primary_color = floor_colors["primary"]
    floor_secondary_color = floor_colors.get("secondary", floor_primary_color)
    
    # Create floor with visible pattern based on floor design
    if st.session_state.room.floor_design == "Hardwood":
        # Hardwood pattern - add strips
        plank_width = 0.1  # width of each plank in meters
        num_planks = int(width_m / plank_width)
        
        for i in range(num_planks):
            x_start = i * plank_width
            x_end = (i + 1) * plank_width
            if x_end > width_m:
                x_end = width_m
                
            vertices = [
                [x_start, 0, 0],
                [x_end, 0, 0],
                [x_end, height_m, 0],
                [x_start, height_m, 0]
            ]
            
            i_indices = [0]
            j_indices = [1]
            k_indices = [2]
            
            color = floor_primary_color if i % 2 == 0 else floor_secondary_color
            
            fig.add_trace(
                go.Mesh3d(
                    x=[v[0] for v in vertices],
                    y=[v[1] for v in vertices],
                    z=[v[2] for v in vertices],
                    i=i_indices, j=j_indices, k=k_indices,
                    color=color,
                    flatshading=True,
                    name=f"Floor Plank {i}"
                )
            )
    elif st.session_state.room.floor_design == "Tile":
        # Tile pattern - add grid
        tile_size = 0.2  # size of each tile in meters
        for x_idx in range(int(width_m / tile_size) + 1):
            for y_idx in range(int(height_m / tile_size) + 1):
                x_start = x_idx * tile_size
                y_start = y_idx * tile_size
                x_end = min((x_idx + 1) * tile_size, width_m)
                y_end = min((y_idx + 1) * tile_size, height_m)
                
                if x_start >= width_m or y_start >= height_m:
                    continue
                
                vertices = [
                    [x_start, y_start, 0],
                    [x_end, y_start, 0],
                    [x_end, y_end, 0],
                    [x_start, y_end, 0]
                ]
                
                i_indices = [0]
                j_indices = [1]
                k_indices = [2]
                
                color = floor_primary_color if (x_idx + y_idx) % 2 == 0 else floor_secondary_color
                
                fig.add_trace(
                    go.Mesh3d(
                        x=[v[0] for v in vertices],
                        y=[v[1] for v in vertices],
                        z=[v[2] for v in vertices],
                        i=i_indices, j=j_indices, k=k_indices,
                        color=color,
                        flatshading=True,
                        name=f"Tile {x_idx}-{y_idx}"
                    )
                )
    elif st.session_state.room.floor_design == "Stripes":
        # Stripes pattern - horizontal stripes
        stripe_width = 0.15  # width of each stripe in meters
        num_stripes = int(height_m / stripe_width)
        
        for i in range(num_stripes):
            y_start = i * stripe_width
            y_end = (i + 1) * stripe_width
            if y_end > height_m:
                y_end = height_m
                
            vertices = [
                [0, y_start, 0],
                [width_m, y_start, 0],
                [width_m, y_end, 0],
                [0, y_end, 0]
            ]
            
            i_indices = [0]
            j_indices = [1]
            k_indices = [2]
            
            color = floor_primary_color if i % 2 == 0 else floor_secondary_color
            
            fig.add_trace(
                go.Mesh3d(
                    x=[v[0] for v in vertices],
                    y=[v[1] for v in vertices],
                    z=[v[2] for v in vertices],
                    i=i_indices, j=j_indices, k=k_indices,
                    color=color,
                    flatshading=True,
                    name=f"Stripe {i}"
                )
            )
    elif st.session_state.room.floor_design == "Zigzag":
        # Zigzag pattern
        zigzag_width = 0.2  # width of each zigzag section in meters
        zigzag_height = 0.2  # height of each zigzag row
        
        num_zigzag_rows = int(height_m / zigzag_height)
        num_zigzag_cols = int(width_m / zigzag_width) * 2  # Double for zigzag effect
        
        for row in range(num_zigzag_rows):
            for col in range(num_zigzag_cols):
                # Calculate zigzag position
                x_start = (col // 2) * zigzag_width
                y_start = row * zigzag_height
                
                # Zigzag pattern - alternate between forward and backward slant
                if col % 2 == 0:  # Forward slant \
                    vertices = [
                        [x_start, y_start, 0],
                        [x_start + zigzag_width, y_start + zigzag_height, 0],
                        [x_start, y_start + zigzag_height, 0]
                    ]
                else:  # Backward slant /
                    vertices = [
                        [x_start, y_start + zigzag_height, 0],
                        [x_start, y_start, 0],
                        [x_start - zigzag_width, y_start + zigzag_height, 0]
                    ]
                
                # Skip if outside room boundaries
                if any(v[0] < 0 or v[0] > width_m or v[1] < 0 or v[1] > height_m for v in vertices):
                    continue
                
                i_indices = [0]
                j_indices = [1]
                k_indices = [2]
                
                # Alternate colors
                color = floor_primary_color if (row + col) % 2 == 0 else floor_secondary_color
                
                fig.add_trace(
                    go.Mesh3d(
                        x=[v[0] for v in vertices],
                        y=[v[1] for v in vertices],
                        z=[v[2] for v in vertices],
                        i=i_indices, j=j_indices, k=k_indices,
                        color=color,
                        flatshading=True,
                        name=f"Zigzag {row}-{col}"
                    )
                )
    else:
        # Default solid floor for other designs
        vertices = [
            [0, 0, 0],  # bottom left
            [width_m, 0, 0],  # bottom right
            [width_m, height_m, 0],  # top right
            [0, height_m, 0],  # top left
        ]
        
        i = [0]
        j = [1]
        k = [2]
        
        fig.add_trace(
            go.Mesh3d(
                x=[v[0] for v in vertices],
                y=[v[1] for v in vertices],
                z=[v[2] for v in vertices],
                i=i, j=j, k=k,
                color=floor_primary_color,
                name="Floor",
                flatshading=True
            )
        )
    
    # Get wall colors (individual wall colors if available)
    left_wall_color = get_wall_color_hex(getattr(st.session_state.room, 'left_wall_color', st.session_state.room.wall_color))
    back_wall_color = get_wall_color_hex(getattr(st.session_state.room, 'back_wall_color', st.session_state.room.wall_color))
    right_wall_color = get_wall_color_hex(getattr(st.session_state.room, 'right_wall_color', st.session_state.room.wall_color))
    front_wall_color = get_wall_color_hex(getattr(st.session_state.room, 'front_wall_color', st.session_state.room.wall_color))
    
    # Add walls with full rectangles (no partial walls)
    # Wall 1 (left)
    left_wall_vertices = [
        [0, 0, 0],  # bottom left
        [0, height_m, 0],  # bottom right
        [0, height_m, room_height],  # top right
        [0, 0, room_height],  # top left
    ]
    
    # For full rectangles, we need to define all triangular faces
    i = [0, 0]
    j = [1, 2]
    k = [2, 3]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in left_wall_vertices],
            y=[v[1] for v in left_wall_vertices],
            z=[v[2] for v in left_wall_vertices],
            i=i, j=j, k=k,
            color=left_wall_color,
            opacity=0.95,  # Slightly transparent to make it look like interior wall
            name="Left Wall",
            flatshading=True
        )
    )
    
    # Wall 2 (back)
    back_wall_vertices = [
        [0, 0, 0],  # bottom left
        [width_m, 0, 0],  # bottom right
        [width_m, 0, room_height],  # top right
        [0, 0, room_height],  # top left
    ]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in back_wall_vertices],
            y=[v[1] for v in back_wall_vertices],
            z=[v[2] for v in back_wall_vertices],
            i=i, j=j, k=k,
            color=back_wall_color,
            opacity=0.95,
            name="Back Wall",
            flatshading=True
        )
    )
    
    # Wall 3 (right)
    right_wall_vertices = [
        [width_m, 0, 0],  # bottom left
        [width_m, height_m, 0],  # bottom right
        [width_m, height_m, room_height],  # top right
        [width_m, 0, room_height],  # top left
    ]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in right_wall_vertices],
            y=[v[1] for v in right_wall_vertices],
            z=[v[2] for v in right_wall_vertices],
            i=i, j=j, k=k,
            color=right_wall_color,
            opacity=0.95,
            name="Right Wall",
            flatshading=True
        )
    )
    
    # Wall 4 (front)
    front_wall_vertices = [
        [0, height_m, 0],  # bottom left
        [width_m, height_m, 0],  # bottom right
        [width_m, height_m, room_height],  # top right
        [0, height_m, room_height],  # top left
    ]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in front_wall_vertices],
            y=[v[1] for v in front_wall_vertices],
            z=[v[2] for v in front_wall_vertices],
            i=i, j=j, k=k,
            color=front_wall_color,
            opacity=0.95,
            name="Front Wall",
            flatshading=True
        )
    )
    
    # Ceiling removed as requested
    
    # Add furniture items in 3D
    if hasattr(st.session_state.room, 'furniture') and st.session_state.room.furniture:
        for furniture in st.session_state.room.furniture:
            # Convert furniture dimensions to meters
            f_width = furniture.width / 100 * furniture.scale
            f_height = furniture.height / 100 * furniture.scale
            f_thickness = 0.05  # Standard thickness in meters
            
            # Calculate furniture position in meters
            f_x = furniture.x / 100
            f_y = furniture.y / 100
            f_z = 0  # Place on the floor
            
            # Create a box for the furniture
            x_values = []
            y_values = []
            z_values = []
            
            # Bottom face
            x_values.extend([f_x, f_x + f_width, f_x + f_width, f_x, f_x])
            y_values.extend([f_y, f_y, f_y + f_height, f_y + f_height, f_y])
            z_values.extend([f_z, f_z, f_z, f_z, f_z])
            
            # Top face
            x_values.extend([f_x, f_x + f_width, f_x + f_width, f_x, f_x])
            y_values.extend([f_y, f_y, f_y + f_height, f_y + f_height, f_y])
            z_values.extend([f_z + f_thickness, f_z + f_thickness, f_z + f_thickness, f_z + f_thickness, f_z + f_thickness])
            
            # Connect bottom to top
            x_values.extend([f_x, f_x, f_x + f_width, f_x + f_width])
            y_values.extend([f_y, f_y, f_y, f_y])
            z_values.extend([f_z, f_z + f_thickness, f_z + f_thickness, f_z])
            
            x_values.extend([f_x + f_width, f_x + f_width, f_x, f_x])
            y_values.extend([f_y, f_y, f_y + f_height, f_y + f_height])
            z_values.extend([f_z, f_z + f_thickness, f_z + f_thickness, f_z])
            
            x_values.extend([f_x, f_x, f_x + f_width, f_x + f_width])
            y_values.extend([f_y + f_height, f_y + f_height, f_y + f_height, f_y + f_height])
            z_values.extend([f_z, f_z + f_thickness, f_z + f_thickness, f_z])
            
            # Add furniture as a 3D line
            fig.add_trace(
                go.Scatter3d(
                    x=x_values,
                    y=y_values,
                    z=z_values,
                    mode='lines',
                    line=dict(color=furniture.color, width=4),
                    name=furniture.name
                )
            )
            
            # Add furniture name label
            fig.add_trace(
                go.Scatter3d(
                    x=[f_x + f_width/2],
                    y=[f_y + f_height/2],
                    z=[f_z + f_thickness + 0.1],  # Position slightly above the furniture
                    mode='text',
                    text=[furniture.name],
                    textposition='top center',
                    textfont=dict(
                        size=12,
                        color='black'
                    ),
                    name=f"{furniture.name} Label"
                )
            )
    
    # Set up the 3D scene
    fig.update_layout(
        scene=dict(
            xaxis=dict(showticklabels=False, title=""),
            yaxis=dict(showticklabels=False, title=""),
            zaxis=dict(showticklabels=False, title=""),
            aspectmode='data',
            camera=dict(
                eye=dict(x=camera_x, y=camera_y, z=camera_z),
                up=dict(x=0, y=0, z=1)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=700  # Make the 3D visualization larger
    )
    
    # Display the 3D visualization
    st.plotly_chart(fig, use_container_width=True)
    
    # ===== ROOM EDITING OPTIONS SECTION =====
    st.markdown("<h2 style='text-align: center;'>Room Editing Options</h2>", unsafe_allow_html=True)
    
    # Create tabs for different editing categories
    edit_tabs = st.tabs(["Room Dimensions", "Wall Colors", "Floor Design", "Furniture", "Camera Control", "Save/Load"])
    
    with edit_tabs[0]:  # Room Dimensions
        st.subheader("Room Dimensions")
        col1, col2 = st.columns(2)
        
        with col1:
            new_width = st.slider("Room Width (cm)", 200, 800, st.session_state.room.width)
        
        with col2:
            new_height = st.slider("Room Height (cm)", 200, 800, st.session_state.room.height)
        
        if st.button("Apply Dimensions"):
            st.session_state.room.width = new_width
            st.session_state.room.height = new_height
            st.success("Room dimensions updated")
            st.rerun()
        
        # Room templates
        st.subheader("Room Templates")
        template_names = ["Custom"] + get_room_template_names()
        selected_template = st.selectbox("Select a template", template_names)
        
        if selected_template != "Custom" and st.button("Load Template"):
            st.session_state.room = load_room_template(selected_template)
            st.success(f"Loaded template: {selected_template}")
            st.rerun()
    
    with edit_tabs[1]:  # Wall Colors
        st.subheader("Wall Colors")
        # Create tabs for wall colors
        wall_color_tabs = st.tabs(["All Walls", "Left Wall", "Back Wall", "Right Wall", "Front Wall"])
        
        with wall_color_tabs[0]:  # All Walls tab
            # Add color picker with pre-defined colors
            wall_color_options = list(WALL_COLORS.keys())
            wall_color = st.selectbox("Select Wall Color", wall_color_options, 
                                     index=wall_color_options.index(st.session_state.room.wall_color) 
                                     if st.session_state.room.wall_color in wall_color_options else 0)
            
            if st.button("Apply to All Walls"):
                st.session_state.room.wall_color = wall_color
                # Also set individual wall colors
                st.session_state.room.left_wall_color = wall_color
                st.session_state.room.back_wall_color = wall_color
                st.session_state.room.right_wall_color = wall_color
                st.session_state.room.front_wall_color = wall_color
                st.success(f"Applied {wall_color} to all walls")
                st.rerun()
        
        with wall_color_tabs[1]:  # Left Wall tab
            left_wall_color_options = list(WALL_COLORS.keys())
            left_wall_color = st.selectbox("Select Left Wall Color", left_wall_color_options, 
                                         index=left_wall_color_options.index(getattr(st.session_state.room, 'left_wall_color', st.session_state.room.wall_color)) 
                                         if getattr(st.session_state.room, 'left_wall_color', st.session_state.room.wall_color) in left_wall_color_options else 0)
            
            if st.button("Apply to Left Wall"):
                st.session_state.room.left_wall_color = left_wall_color
                st.success(f"Applied {left_wall_color} to left wall")
                st.rerun()
        
        with wall_color_tabs[2]:  # Back Wall tab
            back_wall_color_options = list(WALL_COLORS.keys())
            back_wall_color = st.selectbox("Select Back Wall Color", back_wall_color_options, 
                                         index=back_wall_color_options.index(getattr(st.session_state.room, 'back_wall_color', st.session_state.room.wall_color)) 
                                         if getattr(st.session_state.room, 'back_wall_color', st.session_state.room.wall_color) in back_wall_color_options else 0)
            
            if st.button("Apply to Back Wall"):
                st.session_state.room.back_wall_color = back_wall_color
                st.success(f"Applied {back_wall_color} to back wall")
                st.rerun()
        
        with wall_color_tabs[3]:  # Right Wall tab
            right_wall_color_options = list(WALL_COLORS.keys())
            right_wall_color = st.selectbox("Select Right Wall Color", right_wall_color_options, 
                                          index=right_wall_color_options.index(getattr(st.session_state.room, 'right_wall_color', st.session_state.room.wall_color)) 
                                          if getattr(st.session_state.room, 'right_wall_color', st.session_state.room.wall_color) in right_wall_color_options else 0)
            
            if st.button("Apply to Right Wall"):
                st.session_state.room.right_wall_color = right_wall_color
                st.success(f"Applied {right_wall_color} to right wall")
                st.rerun()
        
        with wall_color_tabs[4]:  # Front Wall tab
            front_wall_color_options = list(WALL_COLORS.keys())
            front_wall_color = st.selectbox("Select Front Wall Color", front_wall_color_options, 
                                          index=front_wall_color_options.index(getattr(st.session_state.room, 'front_wall_color', st.session_state.room.wall_color)) 
                                          if getattr(st.session_state.room, 'front_wall_color', st.session_state.room.wall_color) in front_wall_color_options else 0)
            
            if st.button("Apply to Front Wall"):
                st.session_state.room.front_wall_color = front_wall_color
                st.success(f"Applied {front_wall_color} to front wall")
                st.rerun()
    
    with edit_tabs[2]:  # Floor Design
        st.subheader("Floor Design")
        floor_design_options = list(FLOOR_DESIGNS.keys())
        floor_design = st.selectbox("Select Floor Design", floor_design_options,
                                  index=floor_design_options.index(st.session_state.room.floor_design) 
                                  if st.session_state.room.floor_design in floor_design_options else 0)
        
        if st.button("Apply Floor Design"):
            st.session_state.room.floor_design = floor_design
            st.success(f"Applied {floor_design} floor design")
            st.rerun()
    
    with edit_tabs[3]:  # Furniture
        # Add Furniture Tab
        st.subheader("Add Furniture")
        
        # Group items by category
        furniture_categories = {}
        for item in FURNITURE_ITEMS:
            if item.category not in furniture_categories:
                furniture_categories[item.category] = []
            furniture_categories[item.category].append(item)
        
        selected_category = st.selectbox("Furniture Category", list(furniture_categories.keys()))
        
        # Show items for selected category
        if selected_category:
            category_items = furniture_categories[selected_category]
            item_names = [item.name for item in category_items]
            selected_item_name = st.selectbox("Select Furniture", item_names)
            
            selected_item = next((item for item in category_items if item.name == selected_item_name), None)
            
            if selected_item:
                st.write(f"Size: {selected_item.width}cm x {selected_item.height}cm")
                
                # Color options for the selected item
                color_options = selected_item.available_colors or ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]
                selected_color = st.selectbox("Color", color_options, 
                                             index=color_options.index(selected_item.default_color) if selected_item.default_color in color_options else 0)
                
                # Position information
                st.write("Position (where to place the furniture):")
                pos_col1, pos_col2 = st.columns(2)
                
                with pos_col1:
                    x_pos = st.slider("X Position", 0, st.session_state.room.width, st.session_state.room.width // 2)
                
                with pos_col2:
                    y_pos = st.slider("Y Position", 0, st.session_state.room.height, st.session_state.room.height // 2)
                
                if st.button("Add to Room"):
                    new_furniture = Furniture(
                        item_id=selected_item.id,
                        name=selected_item.name,
                        width=selected_item.width,
                        height=selected_item.height,
                        x=x_pos,
                        y=y_pos,
                        color=selected_color
                    )
                    
                    st.session_state.room.add_furniture(new_furniture)
                    st.success(f"Added {selected_item.name} to the room")
                    st.rerun()
        
        # Furniture Management
        st.subheader("Manage Existing Furniture")
        
        if hasattr(st.session_state.room, 'furniture') and st.session_state.room.furniture:
            furniture_list = [(f.id, f.name) for f in st.session_state.room.furniture]
            selected_furniture_id = st.selectbox("Select Furniture to Move or Delete", 
                                               options=[id for id, _ in furniture_list],
                                               format_func=lambda x: next((name for id, name in furniture_list if id == x), ""))
            
            selected_furniture = st.session_state.room.get_furniture_by_id(selected_furniture_id)
            
            if selected_furniture:
                col_move, col_delete = st.columns(2)
                
                with col_move:
                    st.text(f"Current Position: ({selected_furniture.x}, {selected_furniture.y})")
                    new_x = st.slider("X Position", 0, st.session_state.room.width, int(selected_furniture.x))
                    new_y = st.slider("Y Position", 0, st.session_state.room.height, int(selected_furniture.y))
                    
                    if st.button("Move Furniture"):
                        st.session_state.room.update_furniture_position(selected_furniture_id, new_x, new_y)
                        st.success(f"Moved {selected_furniture.name} to ({new_x}, {new_y})")
                        st.rerun()
                
                with col_delete:
                    if st.button("Delete Furniture"):
                        if st.session_state.room.remove_furniture(selected_furniture_id):
                            st.success(f"Removed {selected_furniture.name} from the room")
                            st.rerun()
        else:
            st.write("No furniture in the room. Add furniture using the controls above.")
    
    with edit_tabs[4]:  # Camera Control
        st.subheader("Camera Control")
        camera_col1, camera_col2 = st.columns(2)
        with camera_col1:
            new_camera_x = st.slider("Camera Angle X", 0.5, 3.0, st.session_state.camera_x, step=0.1)
            new_camera_y = st.slider("Camera Angle Y", 0.5, 3.0, st.session_state.camera_y, step=0.1)
        
        with camera_col2:
            new_camera_z = st.slider("Camera Height", 0.5, 3.0, st.session_state.camera_z, step=0.1)
            
            if st.button("Apply Camera Settings"):
                st.session_state.camera_x = new_camera_x
                st.session_state.camera_y = new_camera_y
                st.session_state.camera_z = new_camera_z
                st.rerun()
    
    with edit_tabs[5]:  # Save/Load
        st.subheader("Save/Load Design")
        save_name = st.text_input("Design Name", "my_room_design")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Design"):
                room_data = st.session_state.room.to_dict()
                room_json = json.dumps(room_data)
                
                # Create a download link for the JSON data
                st.download_button(
                    label="Download Design",
                    data=room_json,
                    file_name=f"{save_name}.json",
                    mime="application/json"
                )
        
        with col2:
            uploaded_file = st.file_uploader("Upload Design", type=["json"])
            if uploaded_file is not None:
                try:
                    room_data = json.loads(uploaded_file.read())
                    st.session_state.room = Room.from_dict(room_data)
                    st.success("Room design loaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading room design: {e}")
    
    # ===== FOOTER SECTION =====
    st.markdown("""
    <div style="background-color: #34495e; padding: 20px; border-radius: 10px; margin-top: 30px; color: #ecf0f1;">
        <h2 style="text-align: center; color: #e74c3c;">How to Use the Interior Design Simulator</h2>
        <ul style="color: #ecf0f1; font-size: 16px;">
            <li><strong style="color: #f39c12;">Visualize:</strong> The 3D room visualization shows your current design with all selected options</li>
            <li><strong style="color: #f39c12;">Room Dimensions:</strong> Adjust the width and height of your room or load a template</li>
            <li><strong style="color: #f39c12;">Wall Colors:</strong> Choose different colors for each wall separately</li>
            <li><strong style="color: #f39c12;">Floor Design:</strong> Select from various floor patterns like Hardwood, Tile, Stripes, and Zigzag</li>
            <li><strong style="color: #f39c12;">Furniture:</strong> Add furniture items from different categories and position them in the room</li>
            <li><strong style="color: #f39c12;">Camera Control:</strong> Adjust the viewing angle to see the room from different perspectives</li>
            <li><strong style="color: #f39c12;">Save/Load:</strong> Export your design as a JSON file to share or save it for later use</li>
        </ul>
        <div style="text-align: center; margin-top: 20px; background-color: #2c3e50; padding: 15px; border-radius: 8px;">
            <p style="color: #ecf0f1; font-size: 16px;">Contact: <a href="mailto:support@interiordesignsimulator.com" style="color: #3498db; text-decoration: none; font-weight: bold;">support@interiordesignsimulator.com</a></p>
            <p style="color: #ecf0f1; font-size: 14px;">&copy; 2025 Interior Design Simulator. All rights reserved.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()