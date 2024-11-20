from traceback import print_exc
from src.cmd.pokedex_cmd import PokedexCommands

class PokedexCLI(PokedexCommands):
    """CLI for the Pokedex"""
    intro = "Welcome to the Pokedex! Use '?' for help."

    def __init__(self, client):
        self.prompt= "pokedex> "
        self.client = client
        self.doc_header = "Pokedex commands: (Use 'help' on any command for more info)"
        self.ruler = "="
        try:
            super().__init__(self.client) # Initialize Pokedex commands
        except Exception as e:
            print_exc()
            print(f"\nInitialization error: {str(e)}")
            input("Press Enter to exit...")
            exit(1)