from PIL import Image, ImageDraw
import math
import numpy as np
from typing import Tuple, Dict

from assets.wall_colors import WALL_COLORS
from assets.floor_designs import FLOOR_DESIGNS



def get_mouse_pos_in_canvas(rel_x: float, rel_y: float, canvas_width: int, canvas_height: int, 
                           room_width: int, room_height: int) -> Tuple[float, float]:
    """Convert mouse position from canvas coordinates to room coordinates."""
    room_x = rel_x * room_width
    room_y = rel_y * room_height
    
    return room_x, room_y

def get_wall_color_hex(wall_color_name: str) -> str:
    """Get the hex color code for a wall color name."""
    return WALL_COLORS.get(wall_color_name, "#FFFFFF")

def get_floor_design_color(floor_design_name: str) -> Dict[str, str]:
    """Get the colors for a floor design."""
    # Get floor design colors directly from the updated FLOOR_DESIGNS dictionary
    design_colors = FLOOR_DESIGNS.get(floor_design_name)
    
    # If design not found, use a default
    if not design_colors:
        return {
            "primary": "#F5F5DC",
            "secondary": "#F5F5DC",
            "accent": "#F5F5DC"
        }
    
    # Add accent color if not provided in the design
    if "accent" not in design_colors:
        # Create an accent color based on primary
        design_colors["accent"] = design_colors.get("secondary", design_colors["primary"])
    
    return design_colors
