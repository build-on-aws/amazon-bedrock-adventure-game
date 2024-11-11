from game import Game
from colorama import init, Fore, Style

# Initialize colorama
init()

def create_box(message):
    width = len(message) + 4
    return (
        f"╭─{'─' * width}╮\n"
        f"│  {message}  │\n"
        f"╰─{'─' * width}╯"
    )

def display(message, type='info'):
    if type == 'info':
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
    elif type == 'dice':
        boxed_message = create_box(message)
        print(f"{Fore.YELLOW}{boxed_message}{Style.RESET_ALL}")

def main():
    game = Game(display_callback=display)

    # Get game theme from user
    display("What theme would you like for your adventure game?\n(e.g. Fantasy, Star Fighter, Fantasy, Cyberpunk, Space Horror, etc.)")
    theme = input(f"{Fore.GREEN}➜ {Style.RESET_ALL}").strip()

    # Start the game
    response = game.start_game(theme)
    display(response)

    # Main game loop
    while True:
        display("\nCommand (type 'exit' to quit)")
        player_input = input(f"\n{Fore.GREEN}➜ {Style.RESET_ALL}").strip()

        if player_input != '':

            if player_input == 'exit':
                break

            response, room_info, inventory_info = game.process_command(player_input)
            display(response)
            # if room_info:
            #     display(room_info)
            # if inventory_info:
            #     display(inventory_info)

if __name__ == "__main__":
    main()
