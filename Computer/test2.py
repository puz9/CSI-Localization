from typing import List

def greet_users(names: List[int]) -> None:
    """
    Greets each user in the list of names.

    Args:
        names (List[int]): A list of integers representing user IDs.
    
    Returns:
        None
    """
    for name in names:
        print(f"Hello, {name}!")

# Example usage
user_list = ["Alice", "Bob", "Charlie"]
greet_users(user_list)
