from src.context.pokemon_cli import PokemonCLI
from src.cmd.base import BaseCommands
from src.misc.util import pretty_print

class PokedexError(Exception):
    """Exception raised for errors in the Pokedex commands."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokedex error: {message}")

class PokedexCommands(BaseCommands):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def _search_pokemon(self, name):
        """Check if a Pokemon exists by name"""
        return name.lower() in self.client.pokemon_names
        
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
            return list(self.client.pokemon_names)[:50]
        return [name for name in self.client.pokemon_names 
                if name.startswith(text.lower())]
    
    def do_choose(self, arg):
        """Choose a Pokemon: choose <pokemon>"""
        arg = arg.lower().strip()
        if not arg:
            print("Please provide a Pokemon name")
            return
        
        if self._search_pokemon(arg):
            pokemon_url = self.client.pokemon_dict[arg]
            PokemonCLI(arg, pokemon_url, self.client).cmdloop()
        else:
            print(f"Pokemon not found: {arg}")

    def complete_choose(self, text, line, begidx, endidx):
        """Override Cmd.complete to autocomplete Pokemon names"""
        text = text.lower().strip()
        if not text:
            return list(self.client.pokemon_names)[:50]
        return [name for name in self.client.pokemon_names 
                if name.startswith(text.lower())]
    
    def do_moves(self, arg):
        """List all moves for a Pokemon: moves <pokemon>"""
        arg = arg.lower().strip()
        if not arg:
            print("Please provide a Pokemon name")
            return
        
        if not self._search_pokemon(arg):
            print(f"Pokemon not found: {arg}")
            return
        
        print("Learning moves...")
        pokemon = self.client.get_pokemon(arg)
        moves = [move["move"]["name"] for move in pokemon["moves"]]
        pretty_print(moves)