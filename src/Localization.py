"""Translated messages."""
import gettext

gettext.install("all", "localization")

TUTORIAL_MOVEMENT = _("Use arrows (←, ↑, →, ↓) to move your tank.")
TUTORIAL_SHOOTING = _("space")
MAIN_MENU_TUTORIAL = _("Tutorial")
MAIN_MENU_PLAY = _("Play")
MAIN_MENU_LANGUAGE = _("Language")
MAIN_MENU_APPLY = _("Apply")

SUPPORTED_LANGUAGES = {"English": "en", "Русский": "ru"}
