from src.misc import service

class PokemonError(Exception):
    """Exception raised for errors in the Pokemon commands."""
    def __init__(self, message="No error message provided"):
        super().__init__(message)

class PokemonCommands:
    def __init__(self):
        self._load_pokemon_names()

    def _load_pokemon_names(self):
        """Initial load of all Pokemon names from the API"""
        self.pokemon_dict = service.get_initial_pokemon()
        if not self.pokemon_dict:
            raise PokemonError("Failed to load Pokemon from PokeAPI")
        self.pokemon_names = set(self.pokemon_dict.keys())
        
    def _search_pokemon(self, name):
        """Check if a Pokemon exists by name"""
        return name.lower() in self.pokemon_names
        
    def do_search(self, arg):
        """Search for a Pokemon by name: search <pokemon>"""
        if not arg:
            print("Please provide a Pokemon name")
            return
            
        if self._search_pokemon(arg):
            print(f"Found {arg.capitalize()}!")
        else:
            print(f"Pokemon not found: {arg}")
            
    def complete_search(self, text, line, begidx, endidx):
        """Override Cmd.complete to autocomplete Pokemon names"""
        if not text:
            return list(self.pokemon_names)[:10]
        return [name for name in self.pokemon_names 
                if name.startswith(text.lower())]