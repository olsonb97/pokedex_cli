import requests

class PokeApiError(Exception):
    """Exception raised for errors in the PokeAPI."""
    def __init__(self, message="No error message provided"):
        super().__init__(f"Pokedex error: {message}")

class PokeApiClient:
    def __init__(self, base_url = "https://pokeapi.co/api/v2"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self._load_pokemon_names()

    def _load_pokemon_names(self):
        """Initial load of all Pokemon names from the API"""
        self.pokemon_dict = service.get_initial_pokemon()
        if not self.pokemon_dict:
            raise PokeApiError("Failed to load Pokemon from PokeAPI")
        self.pokemon_names = set(self.pokemon_dict.keys())

    def _make_request(self, endpoint, params = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # Pokemon endpoints
    def get_pokemon(self, name_or_id):
        return self._make_request(f"pokemon/{name_or_id}")
    
    def list_pokemon(self, limit= 20, offset= 0):
        return self._make_request("pokemon", params={"limit": limit, "offset": offset})

    # Berry endpoints
    def get_berry(self, name_or_id):
        return self._make_request(f"berry/{name_or_id}")

    # Item endpoints
    def get_item(self, name_or_id):
        return self._make_request(f"item/{name_or_id}")