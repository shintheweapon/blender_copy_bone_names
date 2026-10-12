# Every report text of the add-on, as templates with named fields; plain Python.
# The templates are also the keys of the translations.

COPIED = "Copied {count} bone names from {name}"
NO_BONES = "{name} has no bones"


def templates() -> dict:
    """
    List every message template of this module.

    Returns
    -------
    dict
        Constant name to template, for every upper-case string constant.
    """
    return {name: value for name, value in globals().items()
            if name.isupper() and isinstance(value, str)}
