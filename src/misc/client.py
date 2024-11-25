import requests
from src.misc.util import pretty_string

class PokeApiError(Exception):
    """Exception raised for errors in the PokeAPI."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokedex error: {message}")

# Retry wrapper for PokeAPI requests
def poke_api_retry(func):
    """Wrapper to handle PokeAPI retries"""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.RequestException as e:
                choice = input(f"{str(e)} - Retry API request? (y/n): ")
                if choice.lower().strip() != "y":
                    raise e
    return wrapper

# PokeAPI client
class PokeApiClient:
    def __init__(self, base_url = "https://pokeapi.co/api/v2"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self._load_pokemon()
        self._load_versions()

    def _load_pokemon(self):
        """Initial load of all Pokemon names from the API"""
        self.pokemon_dict = self.get_initial_pokemon()
        if not self.pokemon_dict:
            raise PokeApiError("Failed to load Pokemon from PokeAPI")
        self.pokemon_names = set(self.pokemon_dict.keys())

    def _load_versions(self):
        """Initial load of all available versions from the API"""
        response = self.get_versions()
        self.versions = {version["name"] for version in response["results"]}
        if not self.versions:
            raise PokeApiError("Failed to load versions from PokeAPI")

    @poke_api_retry
    # Make a request to the PokeAPI
    def _make_request(self, endpoint, params = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # Pokemon endpoints
    def get_pokemon(self, name_or_id):
        return self._make_request(f"pokemon/{name_or_id}")
    
    # Pokemon list endpoint
    def get_pokemon_list(self, limit= 20, offset= 0):
        return self._make_request("pokemon", params={"limit": limit, "offset": offset})

    # Berry endpoints
    def get_berry(self, name_or_id):
        return self._make_request(f"berry/{name_or_id}")

    # Item endpoints
    def get_item(self, name_or_id):
        return self._make_request(f"item/{name_or_id}")
    
    # Generator to fetch Pokemon data in chunks
    def _get_pokemon_iterator(self, chunk_size = 100):
        """Generator to fetch Pokemon data in chunks"""
        print("Catching Pokemon...")
        total = 0
        offset = 0
        while True:
            response = self.get_pokemon_list(chunk_size, offset)
            
            chunk_data = response["results"]
            if not chunk_data: # Caught all pokemon
                break
                
            for pokemon in chunk_data:
                yield pokemon
                total += 1
            offset += chunk_size
            print(f"Caught {total} Pokemon...")
        print("Caught em all!")

    # Create a dictionary of {Pokemon: url}
    def get_initial_pokemon(self):
        """Create a dictionary of Pokemon names for quick lookup"""
        return {
            pokemon["name"]: pokemon["url"] 
            for pokemon in self._get_pokemon_iterator()
        }
    
    # Get a list of available versions
    def get_versions(self):
        return self._make_request("version-group?limit=100")
    
    def get_move(self, name_or_id):
        return self._make_request(f"move/{name_or_id}")

    def get_usable_move(self, name_or_id):
        move = self.get_move(name_or_id)
        move["damage_class"] = move["damage_class"]["name"]
        move["effects"] = [effect["short_effect"] for effect in move["effect_entries"]]
        keys_to_del = [
            "contest_combos",
            "contest_effect",
            "contest_type",
            "effect_changes",
            "effect_entries",
            "flavor_text_entries",
            "generation",
            "id",
            "learned_by_pokemon",
            "meta",
            "name",
            "names",
            "past_values",
            "stat_changes",
            "super_contest_effect",
            "target",
            "type"
        ]
        for key in keys_to_del:
            move.pop(key, None)
        if move["effect_chance"] is None:
            move.pop("effect_chance", None)
        move["machines"] = self._prettify_machines(move["machines"])
        return move
    
    def get_machine(self, id):
        return self._make_request(f"machine/{id}")
    
    def _prettify_machines(self, mach_list):
        new_machines = {}
        for machine in mach_list:
            id = machine["machine"]["url"].split("/")[-2]
            api_dict = self.get_machine(id)
            name = api_dict["item"]["name"]
            game = pretty_string(api_dict["version_group"]["name"])
            new_machine = {
                name: {
                    "Game": game
                }
            }
            new_machines.update(new_machine)
        return new_machines