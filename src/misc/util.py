import yaml

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
    """Recursively rename all string keys and values in a dictionary."""
    if isinstance(d, dict):
        return {rename_dict(pretty_string(k)): rename_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [rename_dict(item) for item in d]
    elif isinstance(d, str):
        return pretty_string(d)
    else:
        return d
    
def pretty_print_dict(d, message=""):
    d = rename_dict(d)
    dict_string = yaml.dump(d, default_flow_style=False).rstrip()
    max_len = max(len(line) for line in dict_string.splitlines()) if dict_string else 0
    if not message:
        header = "-" * max_len
    else:
        message = pretty_string(message)
        mes_len = len(message)
        pre_header = "-" * (max_len - mes_len)
        mid = max_len // 2
        header = pre_header[:mid] + message + pre_header[mid:]

    footer = "-" * max_len
    print(header, dict_string, footer, sep="\n")