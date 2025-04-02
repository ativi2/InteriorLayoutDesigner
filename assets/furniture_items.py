from furniture import FurnitureItem, register_furniture_item

# Define furniture items
FURNITURE_ITEMS = [
    # Living Room
    FurnitureItem(
        id="sofa_3seater",
        name="3-Seater Sofa",
        category="Living Room",
        width=200,
        height=90,
        default_color="#8B4513",
        available_colors=["#8B4513", "#654321", "#A52A2A", "#D2B48C", "#808080", "#000080"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="sofa_2seater",
        name="2-Seater Sofa",
        category="Living Room",
        width=150,
        height=90,
        default_color="#8B4513",
        available_colors=["#8B4513", "#654321", "#A52A2A", "#D2B48C", "#808080", "#000080"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="armchair",
        name="Armchair",
        category="Living Room",
        width=90,
        height=90,
        default_color="#A52A2A",
        available_colors=["#8B4513", "#A52A2A", "#D2B48C", "#808080", "#000080"],
        shape="chair"
    ),
    FurnitureItem(
        id="coffee_table",
        name="Coffee Table",
        category="Living Room",
        width=120,
        height=60,
        default_color="#D2B48C",
        available_colors=["#8B4513", "#D2B48C", "#808080", "#000000", "#FFFFFF"],
        shape="table"
    ),
    FurnitureItem(
        id="tv_stand",
        name="TV Stand",
        category="Living Room",
        width=160,
        height=40,
        default_color="#8B4513",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="side_table",
        name="Side Table",
        category="Living Room",
        width=50,
        height=50,
        default_color="#D2B48C",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="table"
    ),
    
    # Dining Room
    FurnitureItem(
        id="dining_table",
        name="Dining Table",
        category="Dining Room",
        width=180,
        height=100,
        default_color="#8B4513",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="table"
    ),
    FurnitureItem(
        id="dining_chair",
        name="Dining Chair",
        category="Dining Room",
        width=45,
        height=45,
        default_color="#8B4513",
        available_colors=["#8B4513", "#A52A2A", "#D2B48C", "#000000"],
        shape="chair"
    ),
    FurnitureItem(
        id="sideboard",
        name="Sideboard",
        category="Dining Room",
        width=160,
        height=50,
        default_color="#8B4513",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="rectangle"
    ),
    
    # Bedroom
    FurnitureItem(
        id="double_bed",
        name="Double Bed",
        category="Bedroom",
        width=160,
        height=200,
        default_color="#8B4513",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="bed"
    ),
    FurnitureItem(
        id="single_bed",
        name="Single Bed",
        category="Bedroom",
        width=100,
        height=200,
        default_color="#8B4513",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="bed"
    ),
    FurnitureItem(
        id="wardrobe",
        name="Wardrobe",
        category="Bedroom",
        width=100,
        height=60,
        default_color="#D2B48C",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="dresser",
        name="Dresser",
        category="Bedroom",
        width=120,
        height=50,
        default_color="#D2B48C",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="nightstand",
        name="Nightstand",
        category="Bedroom",
        width=45,
        height=45,
        default_color="#D2B48C",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="table"
    ),
    
    # Office
    FurnitureItem(
        id="desk",
        name="Desk",
        category="Office",
        width=140,
        height=70,
        default_color="#D2B48C",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="table"
    ),
    FurnitureItem(
        id="office_chair",
        name="Office Chair",
        category="Office",
        width=50,
        height=50,
        default_color="#000000",
        available_colors=["#000000", "#808080", "#A52A2A", "#000080"],
        shape="chair"
    ),
    FurnitureItem(
        id="bookcase",
        name="Bookcase",
        category="Office",
        width=100,
        height=40,
        default_color="#D2B48C",
        available_colors=["#8B4513", "#D2B48C", "#000000", "#FFFFFF"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="filing_cabinet",
        name="Filing Cabinet",
        category="Office",
        width=50,
        height=60,
        default_color="#808080",
        available_colors=["#808080", "#000000", "#FFFFFF"],
        shape="rectangle"
    ),
    
    # Bathroom
    FurnitureItem(
        id="toilet",
        name="Toilet",
        category="Bathroom",
        width=60,
        height=70,
        default_color="#FFFFFF",
        available_colors=["#FFFFFF"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="sink",
        name="Sink",
        category="Bathroom",
        width=60,
        height=45,
        default_color="#FFFFFF",
        available_colors=["#FFFFFF"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="bathtub",
        name="Bathtub",
        category="Bathroom",
        width=160,
        height=70,
        default_color="#FFFFFF",
        available_colors=["#FFFFFF"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="shower",
        name="Shower",
        category="Bathroom",
        width=90,
        height=90,
        default_color="#FFFFFF",
        available_colors=["#FFFFFF"],
        shape="rectangle"
    ),
    
    # Kitchen
    FurnitureItem(
        id="kitchen_counter",
        name="Kitchen Counter",
        category="Kitchen",
        width=180,
        height=60,
        default_color="#D3D3D3",
        available_colors=["#D3D3D3", "#FFFFFF", "#000000"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="kitchen_island",
        name="Kitchen Island",
        category="Kitchen",
        width=120,
        height=80,
        default_color="#D3D3D3",
        available_colors=["#D3D3D3", "#FFFFFF", "#000000"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="refrigerator",
        name="Refrigerator",
        category="Kitchen",
        width=75,
        height=75,
        default_color="#C0C0C0",
        available_colors=["#C0C0C0", "#FFFFFF", "#000000"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="stove",
        name="Stove",
        category="Kitchen",
        width=60,
        height=60,
        default_color="#C0C0C0",
        available_colors=["#C0C0C0", "#FFFFFF", "#000000"],
        shape="rectangle"
    ),
    
    # Decorative Items
    FurnitureItem(
        id="plant",
        name="Plant",
        category="Decor",
        width=40,
        height=40,
        default_color="#228B22",
        available_colors=["#228B22", "#006400", "#008000"],
        shape="circle"
    ),
    FurnitureItem(
        id="rug_rectangular",
        name="Rectangular Rug",
        category="Decor",
        width=160,
        height=120,
        default_color="#DEB887",
        available_colors=["#DEB887", "#8B4513", "#D2B48C", "#800020", "#000080", "#808080"],
        shape="rectangle"
    ),
    FurnitureItem(
        id="rug_round",
        name="Round Rug",
        category="Decor",
        width=120,
        height=120,
        default_color="#DEB887",
        available_colors=["#DEB887", "#8B4513", "#D2B48C", "#800020", "#000080", "#808080"],
        shape="circle"
    ),
    FurnitureItem(
        id="floor_lamp",
        name="Floor Lamp",
        category="Decor",
        width=40,
        height=40,
        default_color="#C0C0C0",
        available_colors=["#C0C0C0", "#000000", "#FFFFFF", "#8B4513"],
        shape="circle"
    )
]

# Register all furniture items
for item in FURNITURE_ITEMS:
    register_furniture_item(item)
