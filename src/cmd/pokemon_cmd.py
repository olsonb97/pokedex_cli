from src.misc.util import pretty_print
from src.cmd.base import BaseCommands

class PokemonError(Exception):
    """Exception raised for errors in the Pokemon commands."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokemon error: {message}")

class PokemonCommands(BaseCommands):
    def __init__(self, pokemon_name, pokemon_url, client):
        super().__init__()
        self.pokemon_name = pokemon_name
        self.pokemon_url = pokemon_url
        self.client = client
        print(f"Catching {pokemon_name}...")
        self.pokemon = self.client.get_pokemon(pokemon_name)

    def do_moves(self, arg):
        """\nList all moves for the chosen Pokemon: 'moves'
Use 'moves -l' to list learned moves
Use 'moves -m' to list machine moves
Use 'moves -t' to list tutored moves
Use 'moves -e' to list egg moves\n"""
        arg = arg.strip().lower()
        move_flags = {
            "": None,
            "-l": "level-up",
            "-m": "machine",
            "-t": "tutor",
            "-e": "egg"
        }

        if arg not in move_flags:
            print("Unknown argument!")
            return

        method = move_flags[arg]
        moves = [
            move["move"]["name"] for move in self.pokemon["moves"]
            if method is None or 
            move["version_group_details"][-1]["move_learn_method"]["name"] == method
        ]

        if moves:
            pretty_print(moves)
        else:
            print("No moves found!")