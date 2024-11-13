from src.cmd.base import BaseCommands

class PokemonCLI(BaseCommands):
    """CLI for a Pokemon"""

    def __init__(self, pokemon):
        super().__init__()
        self.pokemon = pokemon
        self.prompt = f"{pokemon}> "