from traceback import print_exc
from src.cmd.pokedex_cmd import PokedexCommands

class PokedexCLI(PokedexCommands):
    """CLI for the Pokedex"""
    intro = "Welcome to the Pokedex! Use '?' for help."

    def __init__(self, client):
        self.prompt= "pokedex> "
        self.original_prompt = self.prompt
        self.client = client
        try:
            super().__init__(self.client) # Initialize Pokedex commands
        except Exception as e:
            print_exc()
            print(f"\nInitialization error: {str(e)}")
            input("Press Enter to exit...")
            exit(1)