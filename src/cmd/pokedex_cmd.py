from src.context.pokemon_cli import PokemonCLI
from src.cmd.base import BaseCommands
from src.misc.util import *

class PokedexError(Exception):
    """Exception raised for errors in the Pokedex commands."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokedex error: {message}")

class PokedexCommands(BaseCommands):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def _is_pokemon(self, name):
        """Check if a Pokemon exists by name"""
        return name.lower() in self.client.pokemon_names
        
    def do_search(self, arg):
        """Search for a Pokemon by name: search <pokemon>"""
        arg = arg.lower().strip()
        if not arg:
            print("Please provide a Pokemon name")
            return
            
        if self._is_pokemon(arg):
            print(f"Found {arg.capitalize()}!")
        else:
            print(f"Pokemon not found: {arg}")
            
    def complete_search(self, text, line, begidx, endidx):
        """Autocomplete Pokemon names for search"""
        text = text.lower().strip()
        if not text:
            return list(self.client.pokemon_names)[:50]
        return [name for name in self.client.pokemon_names 
                if name.startswith(text.lower())]
    
    def do_move(self, arg):
        """Get details about a move: 'move <move name>'"""
        if not arg:
            print("Please provide a move!")
            return
        arg = arg.strip().lower()
        move_dict = self.client.get_usable_move(arg)
        pretty_print_dict(move_dict, arg)
    
    def do_choose(self, arg):
        """Choose a Pokemon: choose <pokemon>"""
        arg = arg.lower().strip()
        if not arg:
            print("Please provide a Pokemon name")
            return

        if self._is_pokemon(arg):
            pokemon_url = self.client.pokemon_dict[arg]
            PokemonCLI(arg, pokemon_url, self.client).cmdloop()
        else:
            print(f"Pokemon not found: {arg}")

    def complete_choose(self, text, line, begidx, endidx):
        """Autocomplete Pokemon names for choose"""
        text = text.lower().strip()
        if not text:
            return list(self.client.pokemon_names)[:50]
        return [name for name in self.client.pokemon_names 
                if name.startswith(text.lower())]

    def do_compare(self, args):
        """Compare two stats of two or more pokemon: compare <pokemon1> <pokemon2> ..."""
        pokemon_names = [poke.lower().strip() for poke in args.split()]
        pokemon_stats = {}

        for pokemon in pokemon_names:
            if not self._is_pokemon(pokemon):
                print(f"'{pokemon}' is not a valid Pokemon!")
                return
            stats = self.client.get_stats(pokemon)
            pokemon_stats[pokemon] = stats
        
        if len(pokemon_stats) < 2:
            print("Please provide at least two Pokémon to compare!")
            return
        
        all_stats = set()
        for stats in pokemon_stats.values():
            all_stats.update(stats.keys())
        for pokemon, stats in pokemon_stats.items():
            for all_stat in all_stats:
                stats.setdefault(all_stat, "None")

        pretty_compare(pokemon_stats)

    def complete_compare(self, text, line, begidx, endidx):
        """Autocomplete Pokemon names for search"""
        text = text.lower().strip().split()
        if not text[0]:
            return list(self.client.pokemon_names)[:50]
        for pokemon in text:
            if not self._is_pokemon(pokemon):
                names = [name for name in self.client.pokemon_names 
                if name.startswith(pokemon.lower())]
                if not names:
                    print(f"{pokemon} is not a valid Pokemon!")
                    return
                else:
                    return names
    
    def do_moves(self, arg):
        """List all moves for a Pokemon: moves <pokemon>"""
        arg = arg.lower().strip()
        if not arg:
            print("Please provide a Pokemon name")
            return
        
        if not self._is_pokemon(arg):
            print(f"Pokemon not found: {arg}")
            return
        
        print("Learning moves...")
        pokemon = self.client.get_pokemon(arg)
        moves = [move["move"]["name"] for move in pokemon["moves"]]
        pretty_print_list(moves)