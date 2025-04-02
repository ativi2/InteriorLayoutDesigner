from PIL import Image, ImageDraw
import math
import numpy as np
from typing import Tuple

from room import Room
from assets.wall_colors import WALL_COLORS
from assets.floor_designs import FLOOR_DESIGNS

def generate_room_image(room: Room) -> Image.Image:
    """Generate an image of the room with furniture."""
    # Create a blank image with white background
    img = Image.new('RGB', (room.width, room.height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw the floor
    draw_floor(img, draw, room)
    
    # Draw the walls
    draw_walls(draw, room)
    
    # Draw the furniture
    for furniture in room.furniture:
        draw_furniture(draw, furniture)
    
    # Draw selection highlight for selected furniture
    if hasattr(room, 'selected_furniture_id') and room.selected_furniture_id is not None:
        selected_furniture = room.get_furniture_by_id(room.selected_furniture_id)
        if selected_furniture:
            draw_selection_highlight(draw, selected_furniture)
    
    return img

def draw_walls(draw: ImageDraw.Draw, room: Room) -> None:
    """Draw the walls of the room."""
    wall_color = WALL_COLORS.get(room.wall_color, "#FFFFFF")
    
    # Draw wall border (we'll just draw a border around the room)
    border_width = 10
    draw.rectangle([0, 0, room.width, room.height], outline=wall_color, width=border_width)

def draw_floor(img: Image.Image, draw: ImageDraw.Draw, room: Room) -> None:
    """Draw the floor of the room."""
    floor_pattern = FLOOR_DESIGNS.get(room.floor_design, "solid")
    floor_color = "#F5F5DC"  # Default beige if pattern not found
    
    if floor_pattern == "solid":
        # Solid color floor
        draw.rectangle([0, 0, room.width, room.height], fill=floor_color)
    
    elif floor_pattern == "checkered":
        # Checkered floor pattern
        square_size = 40
        for x in range(0, room.width, square_size):
            for y in range(0, room.height, square_size):
                if (x // square_size + y // square_size) % 2 == 0:
                    draw.rectangle([x, y, x + square_size, y + square_size], fill="#F5F5DC")
                else:
                    draw.rectangle([x, y, x + square_size, y + square_size], fill="#D2B48C")
    
    elif floor_pattern == "wooden":
        # Wooden floor pattern
        plank_width = 40
        plank_color1 = "#8B4513"
        plank_color2 = "#A0522D"
        
        for y in range(0, room.height, plank_width):
            draw.rectangle([0, y, room.width, y + plank_width], fill=plank_color1 if (y // plank_width) % 2 == 0 else plank_color2)
            
            # Add wood grain lines
            for x in range(0, room.width, 80):
                offset = (y // plank_width) % 3 * 20
                draw.line([x + offset, y, x + offset, y + plank_width], fill="#704214", width=1)
    
    elif floor_pattern == "tile":
        # Tile floor pattern
        tile_size = 50
        for x in range(0, room.width, tile_size):
            for y in range(0, room.height, tile_size):
                draw.rectangle([x, y, x + tile_size, y + tile_size], fill="#E5E5E5", outline="#CCCCCC", width=1)
    
    elif floor_pattern == "carpet":
        # Carpet floor pattern
        draw.rectangle([0, 0, room.width, room.height], fill="#6495ED")
        
        # Add carpet texture dots
        for x in range(10, room.width, 20):
            for y in range(10, room.height, 20):
                draw.ellipse([x-1, y-1, x+1, y+1], fill="#5A86D7")

def draw_furniture(draw: ImageDraw.Draw, furniture) -> None:
    """Draw a piece of furniture on the canvas."""
    # Determine shape based on furniture type
    if not furniture.item:
        # Fallback for furniture without item data
        shape = "rectangle"
    else:
        shape = furniture.item.shape if hasattr(furniture.item, 'shape') else "rectangle"
    
    # Get furniture color
    color = furniture.color
    
    # Calculate center point for rotation
    center_x = furniture.x + (furniture.width * furniture.scale) / 2
    center_y = furniture.y + (furniture.height * furniture.scale) / 2
    
    if shape == "rectangle":
        # Get the four corners with rotation applied
        corners = furniture.get_corners()
        draw.polygon(corners, fill=color, outline="#000000")
        
        # Draw a line to indicate front direction
        front_x = center_x + math.cos(math.radians(furniture.rotation)) * (furniture.width * furniture.scale) / 3
        front_y = center_y + math.sin(math.radians(furniture.rotation)) * (furniture.width * furniture.scale) / 3
        draw.line([center_x, center_y, front_x, front_y], fill="#000000", width=2)
        
    elif shape == "circle":
        # Calculate radius based on the smaller dimension
        radius = min(furniture.width, furniture.height) * furniture.scale / 2
        
        # Draw circle
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius], 
            fill=color, 
            outline="#000000"
        )
        
        # Draw a line to indicate front direction
        front_x = center_x + math.cos(math.radians(furniture.rotation)) * radius * 0.8
        front_y = center_y + math.sin(math.radians(furniture.rotation)) * radius * 0.8
        draw.line([center_x, center_y, front_x, front_y], fill="#000000", width=2)
    
    elif shape == "bed":
        # Specialized shape for beds
        corners = furniture.get_corners()
        draw.polygon(corners, fill=color, outline="#000000", width=2)
        
        # Add mattress detail
        mattress_color = "#FFFFFF"
        mattress_padding = furniture.width * furniture.scale * 0.1
        
        # Get mattress corners (inset from main corners)
        # This is a simplified approach that doesn't handle rotation properly for the mattress
        # For a proper implementation we'd need more complex transformation
        corners_mattress = [
            (corners[0][0] + mattress_padding, corners[0][1] + mattress_padding),
            (corners[1][0] - mattress_padding, corners[1][1] + mattress_padding),
            (corners[2][0] - mattress_padding, corners[2][1] - mattress_padding),
            (corners[3][0] + mattress_padding, corners[3][1] - mattress_padding)
        ]
        draw.polygon(corners_mattress, fill=mattress_color, outline="#CCCCCC")
        
        # Add pillow
        pillow_width = furniture.width * furniture.scale * 0.3
        pillow_height = furniture.height * furniture.scale * 0.2
        
        # Calculate pillow position based on rotation
        # This is a simplified approach
        rad = math.radians(furniture.rotation)
        pillow_offset_x = math.cos(rad) * (furniture.height * furniture.scale * 0.35)
        pillow_offset_y = math.sin(rad) * (furniture.height * furniture.scale * 0.35)
        
        # Draw the pillow as a rectangle
        pillow_center_x = center_x - pillow_offset_x
        pillow_center_y = center_y - pillow_offset_y
        
        # Calculate pillow corners
        pillow_corners = []
        for dx, dy in [(-pillow_width/2, -pillow_height/2), 
                       (pillow_width/2, -pillow_height/2), 
                       (pillow_width/2, pillow_height/2), 
                       (-pillow_width/2, pillow_height/2)]:
            rotated_dx = dx * math.cos(rad) - dy * math.sin(rad)
            rotated_dy = dx * math.sin(rad) + dy * math.cos(rad)
            pillow_corners.append((pillow_center_x + rotated_dx, pillow_center_y + rotated_dy))
        
        draw.polygon(pillow_corners, fill="#EEEEEE", outline="#DDDDDD")
    
    elif shape == "table":
        # Specialized shape for tables
        corners = furniture.get_corners()
        draw.polygon(corners, fill=color, outline="#000000", width=2)
        
        # Add table leg details
        leg_width = furniture.width * furniture.scale * 0.1
        leg_offset = furniture.width * furniture.scale * 0.25
        
        # Draw simplified table legs
        for corner in corners:
            draw.rectangle([corner[0] - leg_width/2, corner[1] - leg_width/2, 
                           corner[0] + leg_width/2, corner[1] + leg_width/2], 
                          fill="#333333", outline="#000000")
    
    elif shape == "chair":
        # Specialized shape for chairs
        corners = furniture.get_corners()
        draw.polygon(corners, fill=color, outline="#000000", width=2)
        
        # Draw chair back
        back_width = furniture.width * furniture.scale * 0.8
        back_height = furniture.height * furniture.scale * 0.3
        
        # Calculate back position based on rotation
        rad = math.radians(furniture.rotation)
        back_offset_x = math.cos(rad) * (furniture.height * furniture.scale * 0.35)
        back_offset_y = math.sin(rad) * (furniture.height * furniture.scale * 0.35)
        
        back_center_x = center_x - back_offset_x
        back_center_y = center_y - back_offset_y
        
        # Calculate back corners
        back_corners = []
        for dx, dy in [(-back_width/2, -back_height/2), 
                      (back_width/2, -back_height/2), 
                      (back_width/2, back_height/2), 
                      (-back_width/2, back_height/2)]:
            rotated_dx = dx * math.cos(rad) - dy * math.sin(rad)
            rotated_dy = dx * math.sin(rad) + dy * math.cos(rad)
            back_corners.append((back_center_x + rotated_dx, back_center_y + rotated_dy))
        
        draw.polygon(back_corners, fill=color, outline="#000000")
    
    else:
        # Default to rectangle for unknown shapes
        corners = furniture.get_corners()
        draw.polygon(corners, fill=color, outline="#000000")

def draw_selection_highlight(draw: ImageDraw.Draw, furniture) -> None:
    """Draw a highlight around selected furniture."""
    # Get the corners with a slightly larger bounds
    center_x = furniture.x + (furniture.width * furniture.scale) / 2
    center_y = furniture.y + (furniture.height * furniture.scale) / 2
    
    # Add small padding for highlight
    padding = 5
    highlighted_width = furniture.width * furniture.scale + padding * 2
    highlighted_height = furniture.height * furniture.scale + padding * 2
    
    # Calculate corners of the highlight rectangle
    half_width = highlighted_width / 2
    half_height = highlighted_height / 2
    
    corners_rel = [
        (-half_width, -half_height),
        (half_width, -half_height),
        (half_width, half_height),
        (-half_width, half_height)
    ]
    
    # Rotate corners
    rad = math.radians(furniture.rotation)
    corners = []
    for rel_x, rel_y in corners_rel:
        rot_x = rel_x * math.cos(rad) - rel_y * math.sin(rad)
        rot_y = rel_x * math.sin(rad) + rel_y * math.cos(rad)
        corners.append((center_x + rot_x, center_y + rot_y))
    
    # Draw dashed outline
    draw_dashed_polygon(draw, corners, "#FF0000", dash_length=5)

def draw_dashed_polygon(draw: ImageDraw.Draw, points, color, dash_length=5):
    """Draw a dashed polygon outline."""
    for i in range(len(points)):
        start = points[i]
        end = points[(i + 1) % len(points)]
        
        # Calculate line length
        line_length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        
        # Calculate number of dashes
        num_dashes = int(line_length / dash_length)
        
        # Draw dashes
        for j in range(num_dashes):
            # Calculate dash start and end positions
            t1 = j / num_dashes
            t2 = (j + 0.5) / num_dashes
            
            dash_start = (start[0] + (end[0] - start[0]) * t1, 
                         start[1] + (end[1] - start[1]) * t1)
            dash_end = (start[0] + (end[0] - start[0]) * t2, 
                       start[1] + (end[1] - start[1]) * t2)
            
            # Draw dash
            draw.line([dash_start, dash_end], fill=color, width=2)

def get_mouse_pos_in_canvas(rel_x: float, rel_y: float, canvas_width: int, canvas_height: int, 
                           room_width: int, room_height: int) -> Tuple[float, float]:
    """Convert mouse position from canvas coordinates to room coordinates."""
    room_x = rel_x * room_width
    room_y = rel_y * room_height
    
    return room_x, room_y
