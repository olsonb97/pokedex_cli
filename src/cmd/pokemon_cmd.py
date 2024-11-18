from src.misc.service import get_pokemon_moves
from src.misc.util import pretty_print
from src.cmd.base import BaseCommands

class PokemonError(Exception):
    """Exception raised for errors in the Pokemon commands."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokemon error: {message}")

class PokemonCommands(BaseCommands):
    def __init__(self, pokemon, pokemon_url):
        super().__init__()
        self.pokemon = pokemon
        self.pokemon_url = pokemon_url

    def do_moves(self, arg):
        """List all moves for the chosen Pokemon: moves"""
        if arg:
            print("Please use <moves> without arguments!")
            return
        else:
            moves = get_pokemon_moves(self.pokemon_url)
            pretty_print(moves)