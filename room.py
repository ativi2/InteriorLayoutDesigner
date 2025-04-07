import json
from typing import List, Optional, Dict, Any, Tuple
from furniture import Furniture, get_furniture_item_by_id

class Room:
    def __init__(self, width: int = 500, height: int = 400, wall_color: str = "White", floor_design: str = "Hardwood"):
        self.width = width
        self.height = height
        self.wall_color = wall_color
        # Individual wall colors (initialized to match the main wall color)
        self.left_wall_color = wall_color
        self.right_wall_color = wall_color
        self.front_wall_color = wall_color
        self.back_wall_color = wall_color
        self.floor_design = floor_design
        self.furniture: List[Furniture] = []
        self.next_furniture_id = 1
    
    def add_furniture(self, furniture: Furniture) -> Tuple[bool, str]:
        """Add a furniture item to the room with a unique ID.
        Returns (success, message) tuple. If success is False, message contains the reason."""
        furniture.id = self.next_furniture_id
        self.next_furniture_id += 1
        
        # Load the furniture item data
        furniture.item = get_furniture_item_by_id(furniture.item_id)
        
        # Constrain furniture position to stay within room boundaries
        self._constrain_furniture_position(furniture)
        
        # Check for overlaps with existing furniture
        # Skip this check for doors and windows as they are placed on walls
        if not (furniture.item_id.startswith('door') or furniture.item_id.startswith('window')):
            overlapping_furniture = self._check_furniture_overlap(furniture)
            if overlapping_furniture:
                # Reset the furniture ID counter since we're not adding this item
                self.next_furniture_id -= 1
                return False, f"Cannot place {furniture.name} here. It overlaps with {overlapping_furniture.name}."
        
        self.furniture.append(furniture)
        return True, f"Added {furniture.name} to the room."
    
    def _constrain_furniture_position(self, furniture: Furniture) -> None:
        """Make sure furniture stays within room boundaries."""
        # Calculate effective dimensions based on rotation
        effective_width = furniture.width
        effective_height = furniture.height
        
        # Constrain x coordinate
        furniture.x = max(0, min(self.width - effective_width, furniture.x))
        
        # Constrain y coordinate
        furniture.y = max(0, min(self.height - effective_height, furniture.y))
    
    def remove_furniture(self, furniture_id: int) -> bool:
        """Remove a furniture item from the room by ID."""
        for i, furniture in enumerate(self.furniture):
            if furniture.id == furniture_id:
                del self.furniture[i]
                return True
        return False
    
    def get_furniture_by_id(self, furniture_id: int) -> Optional[Furniture]:
        """Get a furniture item by its ID."""
        for furniture in self.furniture:
            if furniture.id == furniture_id:
                return furniture
        return None
    
    def get_furniture_at_position(self, x: float, y: float) -> Optional[Furniture]:
        """Get furniture at the given position (if any)."""
        # Check furniture in reverse order (top items first)
        for furniture in reversed(self.furniture):
            if furniture.contains_point(x, y):
                return furniture
        return None
    
    def update_furniture_position(self, furniture_id: int, x: float, y: float) -> bool:
        """Update the position of a furniture item."""
        furniture = self.get_furniture_by_id(furniture_id)
        if furniture:
            # Store the original position in case we need to revert
            original_x, original_y = furniture.x, furniture.y
            
            # Update position
            furniture.x = x
            furniture.y = y
            self._constrain_furniture_position(furniture)
            
            # Check for overlaps (except for doors and windows)
            if not (furniture.item_id.startswith('door') or furniture.item_id.startswith('window')):
                overlapping_furniture = self._check_furniture_overlap(furniture)
                if overlapping_furniture and overlapping_furniture.id != furniture.id:
                    # Revert to original position if overlap detected
                    furniture.x, furniture.y = original_x, original_y
                    return False
            
            return True
        return False
    
    def _check_furniture_overlap(self, furniture: Furniture) -> Optional[Furniture]:
        """Check if furniture overlaps with any existing furniture in the room.
        Returns the first overlapping furniture item or None if no overlap."""
        for existing_furniture in self.furniture:
            # Skip checking against itself or doors/windows
            if (existing_furniture.id == furniture.id or 
                existing_furniture.item_id.startswith('door') or 
                existing_furniture.item_id.startswith('window')):
                continue
                
            # Simple bounding box collision detection using corners
            # Get corners for both furniture items
            furniture_corners = furniture.get_corners()
            existing_furniture_corners = existing_furniture.get_corners()
            
            # Get bounding boxes (min/max coordinates) for both items
            f_min_x = min(corner[0] for corner in furniture_corners)
            f_max_x = max(corner[0] for corner in furniture_corners)
            f_min_y = min(corner[1] for corner in furniture_corners)
            f_max_y = max(corner[1] for corner in furniture_corners)
            
            e_min_x = min(corner[0] for corner in existing_furniture_corners)
            e_max_x = max(corner[0] for corner in existing_furniture_corners)
            e_min_y = min(corner[1] for corner in existing_furniture_corners)
            e_max_y = max(corner[1] for corner in existing_furniture_corners)
            
            # Check for overlap using AABB (Axis-Aligned Bounding Box) collision detection
            if (f_min_x <= e_max_x and f_max_x >= e_min_x and
                f_min_y <= e_max_y and f_max_y >= e_min_y):
                return existing_furniture
                
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the room to a dictionary for serialization."""
        return {
            "width": self.width,
            "height": self.height,
            "wall_color": self.wall_color,
            "left_wall_color": self.left_wall_color,
            "right_wall_color": self.right_wall_color,
            "front_wall_color": self.front_wall_color,
            "back_wall_color": self.back_wall_color,
            "floor_design": self.floor_design,
            "furniture": [f.to_dict() for f in self.furniture],
            "next_furniture_id": self.next_furniture_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Room':
        """Create a room from a dictionary."""
        room = cls(
            width=data.get("width", 500),
            height=data.get("height", 400),
            wall_color=data.get("wall_color", "White"),
            floor_design=data.get("floor_design", "Hardwood")
        )
        
        # Set individual wall colors if available
        room.left_wall_color = data.get("left_wall_color", room.wall_color)
        room.right_wall_color = data.get("right_wall_color", room.wall_color)
        room.front_wall_color = data.get("front_wall_color", room.wall_color)
        room.back_wall_color = data.get("back_wall_color", room.wall_color)
        
        room.next_furniture_id = data.get("next_furniture_id", 1)
        
        # Add furniture
        for f_data in data.get("furniture", []):
            furniture = Furniture.from_dict(f_data)
            # Don't use add_furniture as we want to preserve IDs
            furniture.item = get_furniture_item_by_id(furniture.item_id)
            room.furniture.append(furniture)
        
        return room
