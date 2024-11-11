from converse_agent import ConverseAgent
from converse_tools import ConverseToolManager
from register_tools import register_game_tools
from game_state import GameState

class Game:
    def __init__(self, model_id='anthropic.claude-3-5-haiku-20241022-v1:0', display_callback=None):
        self.display_callback = display_callback
        self.state = GameState(display_callback=self.game_state_display_callback)
        self.tools = ConverseToolManager()

        # Setup agent
        register_game_tools(self.tools, self.state)
        self.agent = ConverseAgent(model_id=model_id)
        self.agent.system_prompt = open("system.txt", "r").read()
        self.agent.tools = self.tools
        self.agent.response_output_tags = ['<response>', '</response>']

    def game_state_display_callback(self, message):
        """Callback to handle displaying tool responses to the user"""
        try:

            if message['tool_name'] == 'roll_dice':
                if 'response' in message:
                    self.display_callback(f"🎲 {message['response']}", "dice")

        except Exception as e:
            print(f"Error in display callback: {str(e)}")

    def start_game(self, theme):
        """Initialize and start a new game with the given theme"""
        start_prompt = f"Start a {theme} themed adventure game."
        return self.agent.invoke_with_prompt(start_prompt)

    def process_command(self, command):
        """Process a player command and return the response"""
        if not command:
            return None, None
            
        response = self.agent.invoke_with_prompt(command)
        
        # Get current info if available
        room_info = ""
        inventory_info = ""
        if self.state.player_id:
            current_room = self.state.get_player_room(self.state.player_id)
            if current_room:
                room_desc = self.state.get_room_description(current_room)
                room_info = f"{current_room}: {room_desc}"

            # Get current player inventory
            player_inventory = self.state.get_player_objects(self.state.player_id)
            if player_inventory:
                inventory_info += f"Inventory: {player_inventory}"
                
        return response, room_info, player_inventory
