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
        self.available_versions = self._get_available_versions()
        self.version = None
        self.prompt_version()

    def _get_available_versions(self):
        """Retrieve available versions based on the Pokémon's moves"""
        version_groups = {
            detail["version_group"]["name"]
            for move in self.pokemon["moves"]
            for detail in move["version_group_details"]
        }

        # Find common versions
        return list(self.client.versions.intersection(version_groups))

    def prompt_version(self):
        """Prompt the user to enter a valid game version."""
        print(f"Available game versions for {self.pokemon_name}:")
        pretty_print(self.available_versions)
        while not self.version:
            try:
                user_input = input("Please enter a game version to use: ").strip().lower()
                self.do_version(user_input)
            except KeyboardInterrupt:
                print("\nInitialization aborted by user.")
                raise PokemonError("Version selection aborted.")

    def complete_version(self, text, line, begidx, endidx):
        """Provide auto-completion for game versions."""
        return [version for version in self.client.versions if version.startswith(text)]

    def do_version(self, arg):
        """\nChoose a game version: 'version scarlet-violet'"""
        arg = arg.strip().lower()
        if arg not in self.available_versions:
            print("Unknown version!")
            return
        print(f"Game version set to {arg}!")
        self.version = arg

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
            for move_details in move["version_group_details"]:
                if (method is None or move_details["move_learn_method"]["name"] == method) and \
                    move_details["version_group"]["name"] == self.version: # Verify version
                    moves.append(move["move"]["name"]) # Append the move name
                    break  # Continue once a match is found

        if moves:
            print(f"Moves for {self.pokemon_name} in {self.version} with method '{method}':")
            pretty_print(moves)
        else:
            print("No moves found! Check version or method.")