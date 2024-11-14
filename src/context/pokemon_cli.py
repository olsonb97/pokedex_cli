from src.cmd.base import BaseCommands
from src.cmd.pokemon_cmd import PokemonCommands

class PokemonCLI(BaseCommands, PokemonCommands):
    """CLI for a Pokemon"""
    categories = {
            "Pokemon": ["moves"],
            "System": ["exit", "help"]
        }

    def __init__(self, pokemon, pokemon_url):
        super().__init__()
        self.pokemon_url = pokemon_url
        self.pokemon = pokemon
        self.prompt = f"{pokemon}> "