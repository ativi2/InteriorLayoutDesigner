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
    design_type = FLOOR_DESIGNS.get(floor_design_name, "solid")
    
    if design_type == "wooden":
        return {
            "primary": "#8B4513",
            "secondary": "#A0522D",
            "accent": "#704214"
        }
    elif design_type == "tile":
        return {
            "primary": "#E5E5E5",
            "secondary": "#CCCCCC",
            "accent": "#AAAAAA"
        }
    elif design_type == "carpet":
        return {
            "primary": "#6495ED",
            "secondary": "#5A86D7",
            "accent": "#4A76C7"
        }
    elif design_type == "checkered":
        return {
            "primary": "#F5F5DC",
            "secondary": "#D2B48C",
            "accent": "#C2A47C"
        }
    else:  # solid
        return {
            "primary": "#F5F5DC",
            "secondary": "#F5F5DC",
            "accent": "#F5F5DC"
        }
