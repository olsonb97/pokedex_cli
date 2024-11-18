from src.cmd.pokemon_cmd import PokemonCommands

class PokemonCLI(PokemonCommands):
    """CLI for a Pokemon"""

    def __init__(self, pokemon, pokemon_url, client):
        self.client = client
        self.prompt= f"{pokemon}> "
        self.original_prompt = self.prompt
        super().__init__(pokemon, pokemon_url, self.client)