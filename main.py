from src.context.pokedex_cli import PokedexCLI
from src.misc.client import PokeApiClient

if __name__ == "__main__":
    client = PokeApiClient()
    PokedexCLI(client).cmdloop()