import streamlit as st
import numpy as np
import pandas as pd
import json
from PIL import Image, ImageDraw
from io import BytesIO
import base64

from room import Room
from furniture import Furniture, FurnitureItem
from utils import generate_room_image, get_mouse_pos_in_canvas
from assets.furniture_items import FURNITURE_ITEMS
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
    
    # Furniture selection section
    st.header("Furniture")
    
    furniture_category = st.selectbox("Category", ["All"] + list(set(item.category for item in FURNITURE_ITEMS)))
    
    filtered_items = FURNITURE_ITEMS
    if furniture_category != "All":
        filtered_items = [item for item in FURNITURE_ITEMS if item.category == furniture_category]
    
    # Create a selection grid for furniture items
    cols = st.columns(2)
    for i, item in enumerate(filtered_items):
        with cols[i % 2]:
            if st.button(f"{item.name}", key=f"btn_{item.id}"):
                new_furniture = Furniture(
                    item_id=item.id,
                    name=item.name,
                    width=item.width,
                    height=item.height,
                    x=50,
                    y=50,
                    color=item.default_color,
                    rotation=0
                )
                st.session_state.room.add_furniture(new_furniture)
    
    # Controls for selected furniture
    if st.session_state.selected_furniture is not None:
        st.subheader("Selected Furniture")
        furniture = st.session_state.room.get_furniture_by_id(st.session_state.selected_furniture)
        
        if furniture:
            st.write(f"**{furniture.name}**")
            
            # Color selection for furniture
            if hasattr(furniture, 'item') and hasattr(furniture.item, 'available_colors') and furniture.item.available_colors:
                selected_color = st.selectbox("Color", furniture.item.available_colors, 
                                           index=furniture.item.available_colors.index(furniture.color) if furniture.color in furniture.item.available_colors else 0)
                if selected_color != furniture.color:
                    furniture.color = selected_color
            
            # Manual position adjustment
            st.number_input("X Position (cm)", min_value=0, max_value=st.session_state.room.width, 
                         value=int(furniture.x), key=f"x_pos_{furniture.id}", 
                         on_change=lambda: st.session_state.room.update_furniture_position(
                             st.session_state.selected_furniture, 
                             st.session_state[f"x_pos_{furniture.id}"], 
                             furniture.y))
            
            st.number_input("Y Position (cm)", min_value=0, max_value=st.session_state.room.height, 
                         value=int(furniture.y), key=f"y_pos_{furniture.id}", 
                         on_change=lambda: st.session_state.room.update_furniture_position(
                             st.session_state.selected_furniture, 
                             furniture.x, 
                             st.session_state[f"y_pos_{furniture.id}"]))
            
            # Rotation control
            rotation = st.slider("Rotation (degrees)", 0, 359, int(furniture.rotation), key=f"rotation_{furniture.id}")
            if rotation != furniture.rotation:
                furniture.rotation = rotation
            
            # Scale control
            scale = st.slider("Scale", 0.5, 2.0, float(furniture.scale), 0.1, key=f"scale_{furniture.id}")
            if scale != furniture.scale:
                furniture.scale = scale
            
            # Remove furniture button
            if st.button("Remove", key=f"remove_{furniture.id}"):
                st.session_state.room.remove_furniture(st.session_state.selected_furniture)
                st.session_state.selected_furniture = None
                st.rerun()
    
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
    # Main canvas for room visualization
    st.header("Room View")
    
    # Generate room image
    room_img = generate_room_image(st.session_state.room)
    
    # Convert the PIL image to a data URL
    buffered = BytesIO()
    room_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Create a clickable image using HTML/CSS
    canvas_html = f"""
    <div style="position: relative; width: 100%; max-width: {st.session_state.room.width}px;">
        <img src="data:image/png;base64,{img_str}" width="100%" id="room_canvas">
    </div>
    <script>
        const img = document.getElementById('room_canvas');
        
        img.addEventListener('click', function(e) {{
            const rect = e.target.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const canvas_width = this.clientWidth;
            const canvas_height = this.clientHeight;
            
            // Send click coordinates to Streamlit
            const data = {{
                x: x / canvas_width,
                y: y / canvas_height,
                width: canvas_width,
                height: canvas_height
            }};
            
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: data
            }}, '*');
        }});
        
        img.addEventListener('mousedown', function(e) {{
            const rect = e.target.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const canvas_width = this.clientWidth;
            const canvas_height = this.clientHeight;
            
            // Send mousedown coordinates to Streamlit
            const data = {{
                event: 'mousedown',
                x: x / canvas_width,
                y: y / canvas_height,
                width: canvas_width,
                height: canvas_height
            }};
            
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: data
            }}, '*');
        }});
        
        img.addEventListener('mousemove', function(e) {{
            if (e.buttons === 1) {{  // Left mouse button is pressed
                const rect = e.target.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const canvas_width = this.clientWidth;
                const canvas_height = this.clientHeight;
                
                // Send mousemove coordinates to Streamlit
                const data = {{
                    event: 'mousemove',
                    x: x / canvas_width,
                    y: y / canvas_height,
                    width: canvas_width,
                    height: canvas_height
                }};
                
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: data
                }}, '*');
            }}
        }});
        
        img.addEventListener('mouseup', function(e) {{
            const data = {{
                event: 'mouseup'
            }};
            
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: data
            }}, '*');
        }});
    </script>
    """
    
    # Display the custom HTML
    from streamlit.components.v1 import html
    room_interaction = html(canvas_html, height=int(st.session_state.room.height * 0.8))
    
    # Process clicks and interactions
    if room_interaction:
        if 'event' in room_interaction:
            if room_interaction['event'] == 'mousedown':
                # Get coordinates in actual room dimensions
                room_x, room_y = get_mouse_pos_in_canvas(
                    room_interaction['x'],
                    room_interaction['y'],
                    room_interaction['width'],
                    room_interaction['height'],
                    st.session_state.room.width,
                    st.session_state.room.height
                )
                
                # Check if a furniture item was clicked
                clicked_furniture = st.session_state.room.get_furniture_at_position(room_x, room_y)
                
                if clicked_furniture:
                    st.session_state.selected_furniture = clicked_furniture.id
                    st.session_state.dragging = True
                    st.session_state.drag_start_pos = (room_x, room_y)
                else:
                    st.session_state.selected_furniture = None
                
                st.rerun()
            
            elif room_interaction['event'] == 'mousemove' and st.session_state.dragging and st.session_state.selected_furniture is not None:
                # Get coordinates in actual room dimensions
                room_x, room_y = get_mouse_pos_in_canvas(
                    room_interaction['x'],
                    room_interaction['y'],
                    room_interaction['width'],
                    room_interaction['height'],
                    st.session_state.room.width,
                    st.session_state.room.height
                )
                
                # Update furniture position
                furniture = st.session_state.room.get_furniture_by_id(st.session_state.selected_furniture)
                if furniture:
                    furniture.x = room_x
                    furniture.y = room_y
                
                st.rerun()
            
            elif room_interaction['event'] == 'mouseup':
                st.session_state.dragging = False
                st.session_state.rotating = False
                st.rerun()
        else:
            # Handle regular clicks
            room_x, room_y = get_mouse_pos_in_canvas(
                room_interaction['x'],
                room_interaction['y'],
                room_interaction['width'],
                room_interaction['height'],
                st.session_state.room.width,
                st.session_state.room.height
            )
            
            clicked_furniture = st.session_state.room.get_furniture_at_position(room_x, room_y)
            
            if clicked_furniture:
                st.session_state.selected_furniture = clicked_furniture.id
            else:
                st.session_state.selected_furniture = None
            
            st.rerun()
    
    # Instructions
    st.markdown("""
    ### Instructions:
    - Click on furniture in the side panel to add it to the room
    - Click and drag furniture to move it around
    - Select furniture to adjust properties (color, rotation, scale)
    - Change wall color and floor design from the control panel
    - Save your designs for later use
    """)
