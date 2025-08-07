import re


def slugify(text: str) -> str:
    """
    Convert a string to a slug.
    """

    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")
