from src.misc.util import *
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
        self.stats = self.client.get_stats(pokemon_name)
        self.available_versions = self._get_available_versions()
        self.version = None

    def precmd(self, line):
       """Override precmd so that version is set before anything else."""
       if self.version is None:
           disallowed_commands = ['move', 'moves', 'abilities']
           command = line.split()[0] if line.strip() else ''
           if command in disallowed_commands:
               pretty_message("""This command requires setting the game version first using the 'version' command.
\nAvailabe versions:""")
               pretty_print_list(self.available_versions)
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

    def complete_move(self, text, line, begidx, endidx):
        return [move["move"]["name"] for move in self.pokemon["moves"] if move["move"]["name"].startswith(text)]

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
            print(f"Moves for {pretty_string(self.pokemon_name)} in {self.version}{f' with method {method}' if method else ''}:")
            pretty_print_list(moves)
        else:
            print("No moves found! Check version or method.")

    def do_stats(self, arg):
        """List the stats for chosen pokemon of chosen game version"""
        if arg:
            print("Argument not supported!")
            return
        pretty_print_dict(self.stats, f"{self.pokemon_name} Stats")

    @BaseCommands.noargs
    def do_abilities(self, arg):
        abilities = self.pokemon["abilities"]
        totals = {}

        for ability in abilities:
            name = ability["ability"]["name"]
            num = ability["slot"]
            hidden = ability["is_hidden"]
            effects = self.client.get_ability(name)
            if not (desc := effects.get(self.version, None)):
                print("No abilities found! Try changing game version.")
                return
            totals[pretty_string(name)] = {
                "Ability Slot": num,
                "Hidden Ability": hidden,
                "Effect": desc
            }

        pretty_print_dict(totals, f"{self.pokemon_name} Abilities")