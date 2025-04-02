import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import math

from room import Room
from utils import get_wall_color_hex, get_floor_design_color
from assets.wall_colors import WALL_COLORS
from assets.floor_designs import FLOOR_DESIGNS

# Set page configuration
st.set_page_config(
    page_title="Interior Design Simulator",
    page_icon="🏠",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'room' not in st.session_state:
    st.session_state.room = Room(width=500, height=400)
if 'selected_furniture' not in st.session_state:
    st.session_state.selected_furniture = None
if 'dragging' not in st.session_state:
    st.session_state.dragging = False
if 'rotating' not in st.session_state:
    st.session_state.rotating = False
if 'drag_start_pos' not in st.session_state:
    st.session_state.drag_start_pos = (0, 0)
if 'designs' not in st.session_state:
    st.session_state.designs = {}
if 'current_design_name' not in st.session_state:
    st.session_state.current_design_name = "Untitled Design"
if 'scale_factor' not in st.session_state:
    st.session_state.scale_factor = 1.0

# Title and description
st.title("Interior Design Simulator")
st.markdown("Experiment with furniture placement, wall colors, and floor designs in a virtual room.")

# Main layout
col1, col2 = st.columns([3, 1])

with col2:
    # Room settings section
    st.header("Room Settings")
    
    room_width = st.slider("Room Width (cm)", 300, 800, st.session_state.room.width)
    room_height = st.slider("Room Height (cm)", 300, 800, st.session_state.room.height)
    
    if room_width != st.session_state.room.width or room_height != st.session_state.room.height:
        st.session_state.room.width = room_width
        st.session_state.room.height = room_height
    
    # Wall color selection
    st.subheader("Wall Color")
    wall_color_options = list(WALL_COLORS.keys())
    selected_wall_color = st.selectbox("Select Wall Color", wall_color_options, 
                                     index=wall_color_options.index(st.session_state.room.wall_color) if st.session_state.room.wall_color in wall_color_options else 0)
    
    if selected_wall_color != st.session_state.room.wall_color:
        st.session_state.room.wall_color = selected_wall_color
    
    # Floor design selection
    st.subheader("Floor Design")
    floor_design_options = list(FLOOR_DESIGNS.keys())
    selected_floor_design = st.selectbox("Select Floor Design", floor_design_options,
                                      index=floor_design_options.index(st.session_state.room.floor_design) if st.session_state.room.floor_design in floor_design_options else 0)
    
    if selected_floor_design != st.session_state.room.floor_design:
        st.session_state.room.floor_design = selected_floor_design
    
    # Camera controls for 3D view
    st.header("3D View Controls")
    
    camera_angle = st.slider("Camera Angle", 0, 359, st.session_state.camera_angle)
    if camera_angle != st.session_state.camera_angle:
        st.session_state.camera_angle = camera_angle
    
    camera_height = st.slider("Camera Height", 100, 400, st.session_state.camera_height)
    if camera_height != st.session_state.camera_height:
        st.session_state.camera_height = camera_height
    
    # Save and load design section
    st.header("Save & Load")
    
    design_name = st.text_input("Design Name", value=st.session_state.current_design_name)
    
    col_save, col_load = st.columns(2)
    
    with col_save:
        if st.button("Save Design"):
            if design_name:
                st.session_state.designs[design_name] = st.session_state.room.to_dict()
                st.session_state.current_design_name = design_name
                st.success(f"Design '{design_name}' saved!")
    
    with col_load:
        if st.session_state.designs:
            design_options = list(st.session_state.designs.keys())
            selected_design = st.selectbox("Load Design", design_options)
            
            if st.button("Load"):
                if selected_design in st.session_state.designs:
                    room_data = st.session_state.designs[selected_design]
                    st.session_state.room = Room.from_dict(room_data)
                    st.session_state.current_design_name = selected_design
                    st.success(f"Design '{selected_design}' loaded!")
                    st.rerun()
        else:
            st.write("No saved designs")
    
    # Export design
    if st.button("Export Design as JSON"):
        room_data = st.session_state.room.to_dict()
        room_json = json.dumps(room_data, indent=2)
        
        b64 = base64.b64encode(room_json.encode()).decode()
        href = f'<a href="data:application/json;base64,{b64}" download="{design_name}.json">Download JSON File</a>'
        st.markdown(href, unsafe_allow_html=True)

with col1:
    # Main 3D room visualization
    st.header("3D Room View")
    
    # Get the wall color
    wall_color_hex = get_wall_color_hex(st.session_state.room.wall_color)
    
    # Get floor design colors
    floor_colors = get_floor_design_color(st.session_state.room.floor_design)
    
    # Create 3D visualization using Plotly
    fig = go.Figure()
    
    # Room dimensions
    width = st.session_state.room.width / 100  # Convert to meters for better 3D scale
    height = st.session_state.room.height / 100
    room_height = 2.5  # Standard room height in meters
    
    # Calculate camera position based on angle and height
    camera_angle_rad = math.radians(st.session_state.camera_angle)
    camera_distance = max(width, height) * 1.5
    camera_x = camera_distance * math.sin(camera_angle_rad)
    camera_y = camera_distance * math.cos(camera_angle_rad)
    camera_z = st.session_state.camera_height / 100
    
    # Add floor
    vertices = [
        [0, 0, 0],  # bottom left
        [width, 0, 0],  # bottom right
        [width, height, 0],  # top right
        [0, height, 0],  # top left
    ]
    
    i = [0, 0, 0, 0]
    j = [1, 2, 3, 0]
    k = [2, 3, 0, 1]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color=floor_colors["primary"],
            name="Floor"
        )
    )
    
    # Add walls
    # Wall 1 (left)
    vertices = [
        [0, 0, 0],  # bottom left
        [0, height, 0],  # bottom right
        [0, height, room_height],  # top right
        [0, 0, room_height],  # top left
    ]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color=wall_color_hex,
            name="Left Wall"
        )
    )
    
    # Wall 2 (back)
    vertices = [
        [0, 0, 0],  # bottom left
        [width, 0, 0],  # bottom right
        [width, 0, room_height],  # top right
        [0, 0, room_height],  # top left
    ]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color=wall_color_hex,
            name="Back Wall"
        )
    )
    
    # Wall 3 (right)
    vertices = [
        [width, 0, 0],  # bottom left
        [width, height, 0],  # bottom right
        [width, height, room_height],  # top right
        [width, 0, room_height],  # top left
    ]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color=wall_color_hex,
            name="Right Wall"
        )
    )
    
    # Wall 4 (front)
    vertices = [
        [0, height, 0],  # bottom left
        [width, height, 0],  # bottom right
        [width, height, room_height],  # top right
        [0, height, room_height],  # top left
    ]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color=wall_color_hex,
            name="Front Wall"
        )
    )
    
    # Add room ceiling
    vertices = [
        [0, 0, room_height],  # bottom left
        [width, 0, room_height],  # bottom right
        [width, height, room_height],  # top right
        [0, height, room_height],  # top left
    ]
    
    fig.add_trace(
        go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color="#FFFFFF",
            opacity=0.8,
            name="Ceiling"
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
        height=600
    )
    
    # Display the 3D visualization
    st.plotly_chart(fig, use_container_width=True)
    
    # Instructions
    st.markdown("""
    ### Instructions:
    - Click on furniture in the side panel to add it to the room
    - Click and drag furniture to move it around
    - Select furniture to adjust properties (color, rotation, scale)
    - Change wall color and floor design from the control panel
    - Save your designs for later use
    """)
