from typing import Dict, Any, List
from room import Room
from furniture import Furniture, get_furniture_item_by_id

# Define room templates
ROOM_TEMPLATES = {
    "Empty Room": {
        "width": 500,
        "height": 400,
        "wall_color": "White",
        "floor_design": "Hardwood",
        "furniture": []
    },
    "Living Room": {
        "width": 600,
        "height": 500,
        "wall_color": "Beige",
        "floor_design": "Hardwood",
        "furniture": [
            {
                "item_id": "sofa_3seater",
                "x": 50,
                "y": 300,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "armchair",
                "x": 300,
                "y": 300,
                "color": "#A52A2A",
                "rotation": 45,
                "scale": 1.0
            },
            {
                "item_id": "coffee_table",
                "x": 150,
                "y": 200,
                "color": "#D2B48C",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "tv_stand",
                "x": 220,
                "y": 50,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "plant",
                "x": 50,
                "y": 50,
                "color": "#228B22",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "rug_rectangular",
                "x": 150,
                "y": 200,
                "color": "#DEB887",
                "rotation": 0,
                "scale": 1.2
            }
        ]
    },
    "Bedroom": {
        "width": 500,
        "height": 400,
        "wall_color": "Light Blue",
        "floor_design": "Carpet",
        "furniture": [
            {
                "item_id": "double_bed",
                "x": 150,
                "y": 200,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "nightstand",
                "x": 100,
                "y": 150,
                "color": "#D2B48C",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "nightstand",
                "x": 350,
                "y": 150,
                "color": "#D2B48C",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "wardrobe",
                "x": 50,
                "y": 50,
                "color": "#D2B48C",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "dresser",
                "x": 350,
                "y": 50,
                "color": "#D2B48C",
                "rotation": 0,
                "scale": 1.0
            }
        ]
    },
    "Dining Room": {
        "width": 550,
        "height": 450,
        "wall_color": "Cream",
        "floor_design": "Tile",
        "furniture": [
            {
                "item_id": "dining_table",
                "x": 200,
                "y": 200,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "dining_chair",
                "x": 150,
                "y": 150,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "dining_chair",
                "x": 250,
                "y": 150,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "dining_chair",
                "x": 150,
                "y": 280,
                "color": "#8B4513",
                "rotation": 180,
                "scale": 1.0
            },
            {
                "item_id": "dining_chair",
                "x": 250,
                "y": 280,
                "color": "#8B4513",
                "rotation": 180,
                "scale": 1.0
            },
            {
                "item_id": "sideboard",
                "x": 50,
                "y": 50,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "plant",
                "x": 400,
                "y": 50,
                "color": "#228B22",
                "rotation": 0,
                "scale": 1.2
            }
        ]
    },
    "Office": {
        "width": 450,
        "height": 400,
        "wall_color": "Light Gray",
        "floor_design": "Hardwood",
        "furniture": [
            {
                "item_id": "desk",
                "x": 150,
                "y": 100,
                "color": "#D2B48C",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "office_chair",
                "x": 200,
                "y": 200,
                "color": "#000000",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "bookcase",
                "x": 50,
                "y": 300,
                "color": "#D2B48C",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "filing_cabinet",
                "x": 350,
                "y": 100,
                "color": "#808080",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "plant",
                "x": 50,
                "y": 50,
                "color": "#228B22",
                "rotation": 0,
                "scale": 0.8
            }
        ]
    },
    "Kitchen": {
        "width": 500,
        "height": 400,
        "wall_color": "Light Yellow",
        "floor_design": "Tile",
        "furniture": [
            {
                "item_id": "kitchen_counter",
                "x": 50,
                "y": 50,
                "color": "#D3D3D3",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "kitchen_island",
                "x": 200,
                "y": 200,
                "color": "#D3D3D3",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "refrigerator",
                "x": 400,
                "y": 50,
                "color": "#C0C0C0",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "stove",
                "x": 320,
                "y": 50,
                "color": "#C0C0C0",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "dining_chair",
                "x": 180,
                "y": 300,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "dining_chair",
                "x": 240,
                "y": 300,
                "color": "#8B4513",
                "rotation": 0,
                "scale": 1.0
            }
        ]
    },
    "Bathroom": {
        "width": 350,
        "height": 300,
        "wall_color": "Light Blue",
        "floor_design": "Tile",
        "furniture": [
            {
                "item_id": "toilet",
                "x": 50,
                "y": 50,
                "color": "#FFFFFF",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "sink",
                "x": 250,
                "y": 50,
                "color": "#FFFFFF",
                "rotation": 0,
                "scale": 1.0
            },
            {
                "item_id": "bathtub",
                "x": 50,
                "y": 200,
                "color": "#FFFFFF",
                "rotation": 0,
                "scale": 1.0
            }
        ]
    }
}

def load_room_template(template_name: str) -> Room:
    """Load a room template by name."""
    if template_name not in ROOM_TEMPLATES:
        return Room()
    
    template = ROOM_TEMPLATES[template_name]
    room = Room(
        width=template["width"],
        height=template["height"],
        wall_color=template["wall_color"],
        floor_design=template["floor_design"]
    )
    
    # Add furniture
    for i, furniture_data in enumerate(template["furniture"]):
        item_id = furniture_data["item_id"]
        item = get_furniture_item_by_id(item_id)
        
        if item:
            furniture = Furniture(
                id=i+1,  # Give it a unique ID
                item_id=item_id,
                name=item.name,
                width=item.width,
                height=item.height,
                x=furniture_data["x"],
                y=furniture_data["y"],
                color=furniture_data["color"],
                rotation=furniture_data["rotation"],
                scale=furniture_data["scale"]
            )
            room.add_furniture(furniture)
    
    return room

def get_room_template_names() -> List[str]:
    """Get a list of available room template names."""
    return list(ROOM_TEMPLATES.keys())