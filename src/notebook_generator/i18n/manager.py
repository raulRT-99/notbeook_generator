import gettext
from pathlib import Path

DOMAIN = "app"
LOCALEDIR = Path(__file__).resolve().parent / "locales"


def load_language(lang_code: str):
    translation = gettext.translation(
        DOMAIN,
        localedir=str(LOCALEDIR),
        languages=[lang_code],
        fallback=True
    )
    translation.install()
    return translation.gettext