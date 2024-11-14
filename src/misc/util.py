def pretty_print(items, columns=5):
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
                row_items.append(f"{sorted_items[index]:<25}")  # Adjust width as needed
        print(" ".join(row_items))
    print()
