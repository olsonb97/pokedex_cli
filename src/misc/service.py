import requests
from src.config.config import API

class ServiceError(Exception):
    def __init__(self, message="No error message provided"):
        super().__init__(message)

def try_again_wrapper(func):
    """Wrapper to handle try again logic"""
    def wrapper(*args, **kwargs):
        while True:
            try:
                result = func(*args, **kwargs)
                return result
            except ServiceError as e:
                print(f"Error: {str(e)}")
                choice = input("Do you want to try again? (y/n): ")
                if choice.lower().strip() != "y":
                    return None
    return wrapper

def get_pokemon_iterator(chunk_size = 100):
    """Generator to fetch Pokemon data in chunks"""
    try:
        print("Catching Pokemon...")
        total = 0
        offset = 0
        while True:
            url = f"{API.pokemon}?offset={offset}&limit={chunk_size}"
            response = requests.get(url)
            response.raise_for_status()
            
            chunk_data = response.json()["results"]
            if not chunk_data: # Caught all pokemon
                break
                
            for pokemon in chunk_data:
                yield pokemon
                total += 1
            offset += chunk_size
            print(f"Caught {total} Pokemon...")
        print("Caught em all!")
            
    except requests.RequestException as e:
        raise ServiceError(f"Failed to fetch Pokemon: {str(e)}")
    except (KeyError, ValueError) as e:
        raise ServiceError(f"Invalid response format: {str(e)}")

@try_again_wrapper
def get_initial_pokemon():
    """Create a dictionary of Pokemon names for quick lookup"""
    try:
        return {
            pokemon["name"]: pokemon["url"] 
            for pokemon in get_pokemon_iterator()
        }
        
    except ServiceError as e:
        raise ServiceError(f"Failed to process Pokemon data: {str(e)}")