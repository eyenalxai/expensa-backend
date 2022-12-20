"""Module with helper functions for the settings class."""


def parse_boolean(string: str | None) -> bool:
    """
    Parse a string to a boolean.

    Args:
        string (str | None): The string to parse.

    Returns:
        bool: The parsed boolean.
    """
    if not string:
        return False

    if string.lower() == "true":
        return True

    if string.lower() == "1":
        return True

    return string.lower() == "yes"
