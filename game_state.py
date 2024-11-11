import networkx as nx
import random

class GameState:
    def __init__(self, display_callback=None):
        self.graph = nx.MultiDiGraph()
        self.player_id = None
        self.display_callback = display_callback

    def tool_response(func):
        """Decorator to format tool responses when callback is defined"""
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if self.display_callback:
                self.display_callback({
                    "tool_name": func.__name__,
                    "response": result
                })
            return result
        return wrapper

    @tool_response
    def create_room(self, room_id, description=''):
        """Create a room with a unique ID and optional description."""
        if self.graph.has_node(room_id):
            raise ValueError(f"Room '{room_id}' already exists.")
        self.graph.add_node(room_id, type='room', description=description) #, image_path=image_path)
        return(f"Room '{room_id}' created.")

    @tool_response
    def connect_rooms(self, room1_id, room2_id, direction, reverse_direction=None):
        """
        Connect two rooms in a specified direction.
        Optionally, connect them in the reverse direction.
        """
        if not (self.graph.has_node(room1_id) and self.graph.has_node(room2_id)):
            raise ValueError("Both rooms must exist to create a connection.")
        self.graph.add_edge(room1_id, room2_id, type='connected_to', direction=direction)
        if reverse_direction:
            self.graph.add_edge(room2_id, room1_id, type='connected_to', direction=reverse_direction)
        return(f"Rooms '{room1_id}' and '{room2_id}' connected ({direction}).")
    
    @tool_response
    def create_player(self, player_id, name):
        """Create the player character with a unique ID and name."""
        if self.player_id is not None:
            raise Exception("Player already exists.")
        if self.graph.has_node(player_id):
            raise ValueError(f"Entity '{player_id}' already exists.")
        self.player_id = player_id
        self.graph.add_node(player_id, type='player', name=name)
        return(f"Player '{name}' with ID '{player_id}' created.")
    
    @tool_response
    def move_player(self, player_id, to_room_id):
        """Move the player to a specified room."""
        if not self.graph.has_node(to_room_id):
            raise ValueError(f"Room '{to_room_id}' does not exist.")
        # Remove existing 'located_in' edges from player to any room
        for edge in list(self.graph.edges(player_id, data=True, keys=True)):
            if edge[3]['type'] == 'located_in':
                self.graph.remove_edge(*edge[:3])
        # Add new 'located_in' edge from player to room
        self.graph.add_edge(player_id, to_room_id, type='located_in')
        return(f"Player '{player_id}' moved to room '{to_room_id}'.")
    
    @tool_response
    def create_npc(self, npc_id, name):
        """Create a non-player character (NPC) with a unique ID and name."""
        if self.graph.has_node(npc_id):
            raise ValueError(f"Entity '{npc_id}' already exists.")
        self.graph.add_node(npc_id, type='npc', name=name)
        return(f"NPC '{name}' with ID '{npc_id}' created.")
    
    @tool_response
    def move_npc(self, npc_id, to_room_id):
        """Move an NPC to a specified room."""
        if not self.graph.has_node(to_room_id):
            raise ValueError(f"Room '{to_room_id}' does not exist.")
        # Remove existing 'located_in' edges from NPC to any room
        for edge in list(self.graph.edges(npc_id, data=True, keys=True)):
            if edge[3]['type'] == 'located_in':
                self.graph.remove_edge(*edge[:3])
        # Add new 'located_in' edge from NPC to room
        self.graph.add_edge(npc_id, to_room_id, type='located_in')
        return(f"NPC '{npc_id}' moved to room '{to_room_id}'.")
    
    @tool_response
    def create_object(self, object_id, name):
        """Create an object with a unique ID and name."""
        if self.graph.has_node(object_id):
            raise ValueError(f"Entity '{object_id}' already exists.")
        self.graph.add_node(object_id, type='object', name=name)
        return(f"Object '{name}' with ID '{object_id}' created.")
    
    @tool_response
    def add_object_to_room(self, object_id, room_id):
        """Place an object in a specified room."""
        if not (self.graph.has_node(object_id) and self.graph.has_node(room_id)):
            raise ValueError(f"Both object and room must exist. object: {object_id}, room: {room_id}")
        # Remove existing 'located_in' or 'held_by' edges from object
        for edge in list(self.graph.edges(object_id, data=True, keys=True)):
            if edge[3]['type'] in ('located_in', 'held_by'):
                self.graph.remove_edge(*edge[:3])
        self.graph.add_edge(object_id, room_id, type='located_in')
        return(f"Object '{object_id}' placed in room '{room_id}'.")
    
    @tool_response
    def player_take_object(self, player_id, object_id):
        """Player picks up an object."""
        if not (self.graph.has_node(player_id) and self.graph.has_node(object_id)):
            raise ValueError("Both player and object must exist.")
        # Check if object is in the same room as the player
        player_room = self.get_player_room(player_id)
        object_room = self.get_object_location(object_id)
        if player_room != object_room:
            raise ValueError("Object is not in the same room as the player.")
        # Remove existing 'located_in' or 'held_by' edges from object
        for edge in list(self.graph.edges(object_id, data=True, keys=True)):
            if edge[3]['type'] in ('located_in', 'held_by'):
                self.graph.remove_edge(*edge[:3])
        self.graph.add_edge(player_id, object_id, type='holds')
        return(f"Player '{player_id}' took object '{object_id}'.")
    
    @tool_response
    def player_drop_object(self, player_id, object_id):
        """Player drops an object in their current room."""
        if not (self.graph.has_node(player_id) and self.graph.has_node(object_id)):
            raise ValueError("Both player and object must exist.")
        # Remove 'holds' edge from player to object
        for edge in list(self.graph.edges(player_id, data=True, keys=True)):
            if edge[1] == object_id and edge[3]['type'] == 'holds':
                self.graph.remove_edge(*edge[:3])
                break
        else:
            raise ValueError(f"Player '{player_id}' does not hold object '{object_id}'.")
        # Add 'located_in' edge from object to player's current room
        room_id = self.get_player_room(player_id)
        self.graph.add_edge(object_id, room_id, type='located_in')
        return(f"Player '{player_id}' dropped object '{object_id}' in room '{room_id}'.")
    
    @tool_response
    def get_player_room(self, player_id):
        """Get the room where the player is currently located."""
        for edge in self.graph.edges(player_id, data=True):
            if edge[2]['type'] == 'located_in':
                return edge[1]
        return 'None'
    
    @tool_response
    def get_object_location(self, object_id):
        """Get the room where the object is currently located."""
        for edge in self.graph.edges(object_id, data=True):
            if edge[2]['type'] == 'located_in':
                return edge[1]
        return 'None'
    
    @tool_response
    def get_room_players(self, room_id):
        """List all players in a specified room."""
        players = []
        for edge in self.graph.in_edges(room_id, data=True):
            if edge[2]['type'] == 'located_in':
                node = edge[0]
                if self.graph.nodes[node]['type'] == 'player':
                    players.append(node)
        return ','.join(players)
    
    @tool_response
    def get_room_npcs(self, room_id):
        """List all NPCs in a specified room."""
        npcs = []
        for edge in self.graph.in_edges(room_id, data=True):
            if edge[2]['type'] == 'located_in':
                node = edge[0]
                if self.graph.nodes[node]['type'] == 'npc':
                    npcs.append(node)
        return ','.join(npcs)
    
    @tool_response
    def get_player_objects(self, player_id):
        """List all objects the player is currently holding."""
        objects = []
        for edge in self.graph.edges(player_id, data=True):
            if edge[2]['type'] == 'holds':
                objects.append(edge[1])
        return ','.join(objects)
    
    @tool_response
    def get_room_objects(self, room_id):
        """List all objects in a specified room."""
        objects = []
        for edge in self.graph.in_edges(room_id, data=True):
            if edge[2]['type'] == 'located_in':
                node = edge[0]
                if self.graph.nodes[node]['type'] == 'object':
                    objects.append(node)
        return ','.join(objects)
    
    @tool_response
    def get_room_description(self, room_id):
        """Get the description of a specified room."""
        if self.graph.has_node(room_id):
            return self.graph.nodes[room_id].get('description', 'None')
        return 'None'
    
    @tool_response
    def get_player_name(self, player_id):
        """Get the name of the player."""
        return self.graph.nodes[player_id].get('name', '')
    
    @tool_response
    def get_npc_name(self, npc_id):
        """Get the name of an NPC."""
        return self.graph.nodes[npc_id].get('name', '')
    
    @tool_response
    def get_object_name(self, object_id):
        """Get the name of an object."""
        return self.graph.nodes[object_id].get('name', '')
    
    @tool_response
    def get_room_exits(self, room_id):
        """List all exits from a specified room."""
        exits = {}
        for edge in self.graph.edges(room_id, data=True):
            if edge[2]['type'] == 'connected_to':
                direction = edge[2]['direction']
                exits[direction] = edge[1]  # edge[1] is the connected room
        return exits
    
    @tool_response
    def move_player_direction(self, player_id, direction):
        """Move the player in a specified direction if possible."""
        current_room = self.get_player_room(player_id)
        exits = self.get_room_exits(current_room)
        if direction in exits:
            self.move_player(player_id, exits[direction])
            return True
        else:
            print(f"No exit in direction '{direction}' from room '{current_room}'.")
            return False  # Can't move in that direction
    
    @tool_response
    def roll_dice(self, num_dice=1, num_sides=20):
        """Roll a number of dice with a given number of sides."""
        rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(rolls)
        result = f"Rolled {total} ({num_dice}d{num_sides})"
        if num_dice > 1:
            result += f" [rolls: {', '.join(map(str, rolls))}]"
        return result