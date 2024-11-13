from traceback import print_exc
from src.cmd.base import BaseCommands
from src.cmd.pokedex import PokedexCommands

class PokedexCLI(BaseCommands, PokedexCommands):
    """CLI for the Pokedex"""
    intro = "Welcome to the Pokedex! Use '?' for help."

    def __init__(self):
        self.prompt= "pokedex> "
        self.original_prompt = self.prompt
        try:
            BaseCommands.__init__(self) # Initialize Cmd parent
            PokedexCommands.__init__(self) # Initialize Pokedex commands
        except Exception as e:
            print_exc()
            print(f"Initialization error: {str(e)}")
            input("Press Enter to exit...")
            exit(1)