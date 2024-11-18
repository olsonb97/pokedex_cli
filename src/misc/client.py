import requests

class PokeApiError(Exception):
    """Exception raised for errors in the PokeAPI."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokedex error: {message}")

def poke_api_retry(func):
    """Wrapper to handle PokeAPI retries"""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.RequestException as e:
                print(f"API Error: {str(e)}")
                choice = input("Connection failed! Retry API request? (y/n): ")
                if choice.lower().strip() != "y":
                    raise PokeApiError(f"API request failed: {str(e)}")
    return wrapper

class PokeApiClient:
    def __init__(self, base_url = "https://pokeapi.co/api/v2"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self._load_pokemon()

    def _load_pokemon(self):
        """Initial load of all Pokemon names from the API"""
        self.pokemon_dict = self.get_initial_pokemon()
        if not self.pokemon_dict:
            raise PokeApiError("Failed to load Pokemon from PokeAPI")
        self.pokemon_names = set(self.pokemon_dict.keys())

    @poke_api_retry
    def _make_request(self, endpoint, params = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # Pokemon endpoints
    def get_pokemon(self, name_or_id):
        return self._make_request(f"pokemon/{name_or_id}")
    
    def get_pokemon_list(self, limit= 20, offset= 0):
        return self._make_request("pokemon", params={"limit": limit, "offset": offset})

    # Berry endpoints
    def get_berry(self, name_or_id):
        return self._make_request(f"berry/{name_or_id}")

    # Item endpoints
    def get_item(self, name_or_id):
        return self._make_request(f"item/{name_or_id}")
    
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

    def get_initial_pokemon(self):
        """Create a dictionary of Pokemon names for quick lookup"""
        return {
            pokemon["name"]: pokemon["url"] 
            for pokemon in self._get_pokemon_iterator()
        }