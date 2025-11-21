def extract_title(markdown: str) -> str:
    """
    Extract the H1 title (# ...) from a markdown string.
    Raises ValueError if no H1 header is found.
    """
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):          # presne jeden #
            return stripped[2:].strip()
        if stripped.startswith("#") and not stripped.startswith("##"):
            # podporí aj "#Title" bez medzery
            return stripped[1:].strip()

    raise ValueError("No H1 header ('# ...') found in markdown")
