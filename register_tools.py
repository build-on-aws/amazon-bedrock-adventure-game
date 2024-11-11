from converse_tools import ConverseToolManager

from game_state import GameState

def register_game_tools(tools: ConverseToolManager, game_state: GameState):
    # Create Room Tool
    tools.register_tool(
        name="create_room",
        func=game_state.create_room,
        description="Create a new room with a unique ID and optional description",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "room_id": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["room_id"]
            }
        }
    )
    
    # Connect Rooms Tool
    tools.register_tool(
        name="connect_rooms",
        func=game_state.connect_rooms,
        description="Connect two rooms with directional paths",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "room1_id": {"type": "string"},
                    "room2_id": {"type": "string"},
                    "direction": {"type": "string"},
                    "reverse_direction": {"type": "string"}
                },
                "required": ["room1_id", "room2_id", "direction"]
            }
        }
    )

    # Create Player Tool
    tools.register_tool(
        name="create_player",
        func=game_state.create_player,
        description="Create a new player character",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "player_id": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["player_id", "name"]
            }
        }
    )

    # Move Player Tool
    tools.register_tool(
        name="move_player",
        func=game_state.move_player,
        description="Move a player to a specific room",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "player_id": {"type": "string"},
                    "to_room_id": {"type": "string"}
                },
                "required": ["player_id", "to_room_id"]
            }
        }
    )

    # Create Object Tool
    tools.register_tool(
        name="create_object",
        func=game_state.create_object,
        description="Create a new object with a unique ID and name",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "object_id": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["object_id", "name"]
            }
        }
    )

    # Add Object to Room Tool
    tools.register_tool(
        name="add_object_to_room",
        func=game_state.add_object_to_room,
        description="Add an object to a specific room",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "object_id": {"type": "string"},
                    "room_id": {"type": "string"}
                },
                "required": ["object_id", "room_id"]
            }
        }
    )

    # Player Take Object Tool
    tools.register_tool(
        name="player_take_object",
        func=game_state.player_take_object,
        description="Player picks up an object from their current room",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "player_id": {"type": "string"},
                    "object_id": {"type": "string"}
                },
                "required": ["player_id", "object_id"]
            }
        }
    )

    # Player Drop Object Tool
    tools.register_tool(
        name="player_drop_object",
        func=game_state.player_drop_object,
        description="Player drops an object in their current room",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "player_id": {"type": "string"},
                    "object_id": {"type": "string"}
                },
                "required": ["player_id", "object_id"]
            }
        }
    )

    # Get Room Description Tool
    tools.register_tool(
        name="get_room_description",
        func=game_state.get_room_description,
        description="Get the description of a specific room",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "room_id": {"type": "string"}
                },
                "required": ["room_id"]
            }
        }
    )

    # Get Room Exits Tool
    tools.register_tool(
        name="get_room_exits",
        func=game_state.get_room_exits,
        description="Get all available exits from a specific room",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "room_id": {"type": "string"}
                },
                "required": ["room_id"]
            }
        }
    )

    # Move Player Direction Tool
    tools.register_tool(
        name="move_player_direction",
        func=game_state.move_player_direction,
        description="Move a player in a specific direction if possible",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "player_id": {"type": "string"},
                    "direction": {"type": "string"}
                },
                "required": ["player_id", "direction"]
            }
        }
    )

    # Create NPC Tool
    tools.register_tool(
        name="create_npc",
        func=game_state.create_npc,
        description="Create a new NPC with a unique ID and name",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "npc_id": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["npc_id", "name"]
            }
        }
    )

    # Move NPC Tool
    tools.register_tool(
        name="move_npc",
        func=game_state.move_npc,
        description="Move an NPC to a specific room",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "npc_id": {"type": "string"},
                    "to_room_id": {"type": "string"}
                },
                "required": ["npc_id", "to_room_id"]
            }
        }
    )

    # Roll Dice Tool
    tools.register_tool(
        name="roll_dice",
        func=game_state.roll_dice,
        description="Roll a number of dice with a given number of sides",
        input_schema={
            'json': {
                "type": "object",
                "properties": {
                    "num_dice": {"type": "integer"},
                    "num_sides": {"type": "integer"}
                },
                "required": []
            }
        }
    )