from src.cmd.base import BaseCommands
from src.cmd.pokemon import PokemonCommands

class PokemonCLI(BaseCommands, PokemonCommands):
    """CLI for a Pokemon"""

    def __init__(self, pokemon, pokemon_url):
        super().__init__()
        self.pokemon_url = pokemon_url
        self.pokemon = pokemon
        self.prompt = f"{pokemon}> "