from src.misc import service
from src.context.pokemon_cli import PokemonCLI
from src.cmd.base import BaseCommands

class PokedexError(Exception):
    """Exception raised for errors in the Pokedex commands."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokedex error: {message}")

class PokedexCommands(BaseCommands):
    def __init__(self):
        super().__init__()
        self._load_pokemon_names()

    def _load_pokemon_names(self):
        """Initial load of all Pokemon names from the API"""
        self.pokemon_dict = service.get_initial_pokemon()
        if not self.pokemon_dict:
            raise PokedexError("Failed to load Pokemon from PokeAPI")
        self.pokemon_names = set(self.pokemon_dict.keys())
        
    def _search_pokemon(self, name):
        """Check if a Pokemon exists by name"""
        return name.lower() in self.pokemon_names
        
    def do_search(self, arg):
        """Search for a Pokemon by name: search <pokemon>"""
        arg = arg.lower().strip()
        if not arg:
            print("Please provide a Pokemon name")
            return
            
        if self._search_pokemon(arg):
            print(f"Found {arg.capitalize()}!")
        else:
            print(f"Pokemon not found: {arg}")
            
    def complete_search(self, text, line, begidx, endidx):
        """Override Cmd.complete to autocomplete Pokemon names"""
        text = text.lower().strip()
        if not text:
            return list(self.pokemon_names)[:50]
        return [name for name in self.pokemon_names 
                if name.startswith(text.lower())]
    
    def do_choose(self, arg):
        """Choose a Pokemon: choose <pokemon>"""
        arg = arg.lower().strip()
        if not arg:
            print("Please provide a Pokemon name")
            return
        
        if self._search_pokemon(arg):
            pokemon_url = self.pokemon_dict[arg]
            PokemonCLI(arg, pokemon_url).cmdloop()
            self.prompt = self.original_prompt
            self.pokemon = None
        else:
            print(f"Pokemon not found: {arg}")

    def complete_choose(self, text, line, begidx, endidx):
        """Override Cmd.complete to autocomplete Pokemon names"""
        text = text.lower().strip()
        if not text:
            return list(self.pokemon_names)[:50]
        return [name for name in self.pokemon_names 
                if name.startswith(text.lower())]