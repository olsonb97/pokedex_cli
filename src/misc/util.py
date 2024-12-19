import yaml
from colorama import init, Fore, Style

init(autoreset=True)

def pretty_print_list(items, columns=5):
    sorted_items = sorted(items)
    
    # Calculate the number of rows needed
    num_rows = (len(sorted_items) + columns - 1) // columns
    
    # Print the items in a grid format
    print()
    for row in range(num_rows):
        row_items = []
        for col in range(columns):
            index = row + col * num_rows
            if index < len(sorted_items):
                row_items.append(f"{sorted_items[index]:<25}")
        print(" ".join(row_items))
    print()

def pretty_string(string):
    """Convert a string from 'name_test' to 'Name Test'."""
    string = string.replace("-", " ").replace("_", " ")
    return ' '.join(word.capitalize() for word in string.split())

def rename_dict(d):
    """Recursively rename only the string keys in a dictionary."""
    if isinstance(d, dict):
        return {rename_dict(pretty_string(k)): rename_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [rename_dict(item) for item in d]
    else:
        return d
    
def pretty_print_dict(d, message=""):
    d = rename_dict(d)
    dict_string = yaml.dump(d, width=70, allow_unicode=True).rstrip()
    max_len = max((len(line) for line in dict_string.splitlines()), default=0)
    if message:
        message = pretty_string(message)
        max_len = max(max_len, len(message) + 4)
        header = message.center(max_len, '-')
    else:
        header = '-' * max_len
    footer = '-' * max_len
    print(header)
    print(dict_string)
    print(footer)

def pretty_message(msg, num=70):
    print("-"*num)
    print(msg)
    print("-"*num)
    
def highlight_value(value, high, low, width):
    if not isinstance(value, (int, float)):
        return str(value).ljust(width)
    color = (
        Fore.YELLOW if (value == high and value == low) else
        Fore.GREEN if value == high else
        Fore.RED if value == low else ""
    )
    return f"{color}{str(value).ljust(width)}{Style.RESET_ALL}" 

def pretty_compare(stats_dict):
    pokemons = list(stats_dict.keys())
    stats = next(iter(stats_dict.values())).keys()
    col_width = max(max(len(p) for p in pokemons), 8)

    header = f"{'Base Stats'.ljust(15)} | {' | '.join(p.ljust(col_width) for p in pokemons)}"
    print(f"{header}\n{'-' * len(header)}")

    for stat in stats:
        values = [stats_dict[p][stat] for p in pokemons]
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        high, low = (max(numeric_values), min(numeric_values)) if numeric_values else (None, None)

        row = f"{stat.ljust(15)} | " + " | ".join(
            highlight_value(stats_dict[p][stat], high, low, col_width) for p in pokemons
        )
        print(row)