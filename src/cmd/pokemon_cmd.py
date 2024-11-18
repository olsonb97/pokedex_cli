from src.misc.util import pretty_print
from src.cmd.base import BaseCommands

class PokemonError(Exception):
    """Exception raised for errors in the Pokemon commands."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokemon error: {message}")

class PokemonCommands(BaseCommands):
    def __init__(self, pokemon_name, pokemon_url, client):
        super().__init__()
        self.doc_header = f"{pokemon_name.title()} commands:"
        self.ruler = "="
        self.pokemon_name = pokemon_name
        self.pokemon_url = pokemon_url
        self.client = client
        print(f"Catching {pokemon_name}...")
        self.pokemon = self.client.get_pokemon(pokemon_name)

    def do_moves(self, arg):
        """List all moves for the chosen Pokemon: moves"""
        if arg:
            print("Please use <moves> without arguments!")
            return
        else:
            moves = [
                move["move"]["name"] for move in self.pokemon["moves"]
            ]
            pretty_print(moves)

            