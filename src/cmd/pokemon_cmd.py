from src.misc.util import pretty_print_list, pretty_print_dict
from src.cmd.base import BaseCommands
import yaml

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
        self.available_versions = self._get_available_versions()
        self.version = None
        self.cmdloop()

    def precmd(self, line):
       """Override precmd so that version is set before anything else."""
       if self.version is None:
           allowed_commands = ['version', 'help', 'exit', 'EOF']
           command = line.split()[0] if line.strip() else ''
           if command not in allowed_commands:
               print("You must set the game version first using the 'version' command.")
               return ''
       return line

    def _get_available_versions(self):
        """Retrieve available versions based on the Pokémon's moves"""
        version_groups = {
            detail["version_group"]["name"]
            for move in self.pokemon["moves"]
            for detail in move["version_group_details"]
        }
        return list(self.client.versions.intersection(version_groups))

    def complete_version(self, text, line, begidx, endidx):
        """Provide auto-completion for game versions."""
        return [version for version in self.available_versions if version.startswith(text)]

    def do_version(self, arg):
        """Choose a game version: 'version scarlet-violet'"""
        if not arg:
            print(f"Current game version: {self.version}")
            return
        arg = arg.strip().lower()
        if arg not in self.available_versions:
            print("Unknown version!")
            return
        print(f"Game version set to {arg}!")
        self.version = arg

    def do_move(self, arg):
        """Get details about a move: 'move <move name>'"""
        if not arg:
            print("Please provide a move!")
            return
        arg = arg.strip().lower()
        found_move = None
        for move in self.pokemon["moves"]:
            if move["move"]["name"] == arg:
                for detail in move["version_group_details"]:
                    if detail["version_group"]["name"] == self.version:
                        found_move = move["move"]["name"]
                        details = detail
                        break
                if found_move:
                    break
        if not found_move:
            print("Unknown move for this pokemon or game version!")
            return
        move_build = self.client.get_usable_move(found_move)
        move_build | {
            "level_learned_at": details["level_learned_at"],
            "move_learn_method": details["move_learn_method"]["name"]
        }
        pretty_print_dict(move_build, found_move)

    def do_moves(self, arg):
        """\nList all moves for the chosen Pokemon: 'moves'
Available methods:
Use 'moves level' to list level-up moves
Use 'moves machine' to list machine moves
Use 'moves tutor' to list tutored moves
Use 'moves egg' to list egg moves\n"""
        arg = arg.strip().lower()
        move_flags = {
            "": None,
            "level": "level-up",
            "machine": "machine",
            "tutor": "tutor",
            "egg": "egg"
        }

        if arg not in move_flags:
            print("Unknown argument!")
            return

        method = move_flags[arg]
        moves = []
        for move in self.pokemon["moves"]:
            # Lengthy way to check if the move is available in the chosen version
            for move_details in move["version_group_details"]:
                if (method is None or move_details["move_learn_method"]["name"] == method) and \
                    move_details["version_group"]["name"] == self.version: # Verify version
                    moves.append(move["move"]["name"]) # Append the move name
                    break  # Continue once a match is found

        if moves:
            print(f"Moves for {self.pokemon_name} in {self.version}{f" with method '{method}'" if method else ""}:")
            pretty_print_list(moves)
        else:
            print("No moves found! Check version or method.")