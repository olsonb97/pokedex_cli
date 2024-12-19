import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from src.misc.util import *

class PokeApiError(Exception):
    """Exception raised for errors in the PokeAPI."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"API error: {message}")

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
    def __init__(self, base_url="https://pokeapi.co/api/v2"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.verify_ssl = True
        self.ssl_warnings_suppressed = False
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

    def _handle_ssl_error(self):
        """Handle SSL errors dynamically"""
        if not self.verify_ssl:
            return  # SSL verification already disabled
        print("-"*50)
        while True:
            choice = input("SSL verification failed. Disable SSL verification for all future requests? (y/n): ").lower().strip()
            if choice == "y":
                self.verify_ssl = False
                self.ssl_warnings_suppressed = True
                print("SSL verification disabled for all future requests.")
                print("-"*50)
                break
            elif choice == "n":
                print("-"*50)
                raise requests.RequestException("SSL verification is required but failed.")
            else:
                print("Invalid choice.")

    def _suppress_ssl_warnings(self):
        """Suppress SSL warnings if warnings are disabled"""
        if self.ssl_warnings_suppressed:
            disable_warnings(InsecureRequestWarning)

    @poke_api_retry
    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._suppress_ssl_warnings()  # Suppress warnings if needed

        try:
            response = self.session.get(url, params=params, verify=self.verify_ssl)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.json()
        except requests.exceptions.SSLError as e:
            print(f"SSL Error: {e}")
            self._handle_ssl_error()
            return self._make_request(endpoint, params)  # Retry with updated SSL

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
        if not mach_list:
            return None
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

    def get_stats(self, id):
        pokemon = self.get_pokemon(id)
        stats = pokemon["stats"]
        types = pokemon["types"]
        totals = {}

        for stat in stats:
            name = pretty_string(stat["stat"]["name"])
            num = stat["base_stat"]
            totals[name] = num

        for i, type in enumerate(types):
            totals[f"Type {i+1}"] = pretty_string(type["type"]["name"])

        return totals
    
    def get_ability(self, id):
        ability = self._make_request(f"ability/{id}")
        entries = ability["flavor_text_entries"]
        effects = {}

        for entry in entries:
            if entry["language"]["name"] == "en":
                version = entry["version_group"]["name"]
                effect = entry["flavor_text"].replace("\n", " ")
                effects[version] = effect
        
        return effects