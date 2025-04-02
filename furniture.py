import math
from typing import Dict, Any, List, Optional, Tuple

class FurnitureItem:
    """Class representing a furniture item template."""
    def __init__(self, id: str, name: str, category: str, width: int, height: int, 
                 default_color: str, available_colors: List[str] = None, shape: str = "rectangle"):
        self.id = id
        self.name = name
        self.category = category
        self.width = width
        self.height = height
        self.default_color = default_color
        self.available_colors = available_colors or [default_color]
        self.shape = shape  # "rectangle", "circle", "custom", etc.

class Furniture:
    """Class representing a furniture instance in the room."""
    def __init__(self, item_id: str, name: str, width: int, height: int, 
                 x: float, y: float, color: str, rotation: float = 0, scale: float = 1.0, id: int = None):
        self.id = id  # This will be set by the Room when added
        self.item_id = item_id
        self.name = name
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.rotation = rotation  # In degrees
        self.scale = scale
        self.item = None  # Will be set when added to a room
    
    def contains_point(self, px: float, py: float) -> bool:
        """Check if the furniture contains the given point."""
        # Get center of furniture
        center_x = self.x + (self.width * self.scale) / 2
        center_y = self.y + (self.height * self.scale) / 2
        
        # Get point relative to center
        rel_x = px - center_x
        rel_y = py - center_y
        
        # Rotate point in opposite direction
        rad = math.radians(-self.rotation)
        rot_x = rel_x * math.cos(rad) - rel_y * math.sin(rad)
        rot_y = rel_x * math.sin(rad) + rel_y * math.cos(rad)
        
        # Check if point is within bounds
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2
        
        return (abs(rot_x) <= half_width and 
                abs(rot_y) <= half_height)
    
    def get_corners(self) -> List[Tuple[float, float]]:
        """Get the four corners of the furniture accounting for rotation and scale."""
        # Get center of furniture
        center_x = self.x + (self.width * self.scale) / 2
        center_y = self.y + (self.height * self.scale) / 2
        
        # Calculate half-width and half-height
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2
        
        # Calculate corners relative to center
        corners_rel = [
            (-half_width, -half_height),
            (half_width, -half_height),
            (half_width, half_height),
            (-half_width, half_height)
        ]
        
        # Rotate corners
        rad = math.radians(self.rotation)
        corners = []
        for rel_x, rel_y in corners_rel:
            rot_x = rel_x * math.cos(rad) - rel_y * math.sin(rad)
            rot_y = rel_x * math.sin(rad) + rel_y * math.cos(rad)
            corners.append((center_x + rot_x, center_y + rot_y))
        
        return corners
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the furniture to a dictionary for serialization."""
        return {
            "id": self.id,
            "item_id": self.item_id,
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "rotation": self.rotation,
            "scale": self.scale
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Furniture':
        """Create a furniture item from a dictionary."""
        return cls(
            id=data.get("id"),
            item_id=data.get("item_id"),
            name=data.get("name"),
            width=data.get("width"),
            height=data.get("height"),
            x=data.get("x"),
            y=data.get("y"),
            color=data.get("color"),
            rotation=data.get("rotation", 0),
            scale=data.get("scale", 1.0)
        )

# Dictionary to store furniture items
_furniture_items: Dict[str, FurnitureItem] = {}

def register_furniture_item(item: FurnitureItem) -> None:
    """Register a furniture item template."""
    _furniture_items[item.id] = item

def get_furniture_item_by_id(item_id: str) -> Optional[FurnitureItem]:
    """Get a furniture item template by ID."""
    return _furniture_items.get(item_id)
