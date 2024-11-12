from traceback import print_exc
from src.commands.base import BaseCommands
from src.commands.pokemon import PokemonCommands

class PokedexCLI(BaseCommands, PokemonCommands):
    """CLI for the Pokedex"""
    intro = "Welcome to the Pokedex! Use '?' for help."
    prompt = "pokedex> "

    def __init__(self):
        try:
            BaseCommands.__init__(self)  # Initialize Cmd parent
            PokemonCommands.__init__(self)  # Initialize with service
        except Exception as e:
            print_exc()
            print(f"Initialization error: {str(e)}")
            input("Press Enter to exit...")
            exit(1)

if __name__ == "__main__":
    PokedexCLI().cmdloop()