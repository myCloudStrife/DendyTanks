"""Translated messages."""
import gettext

gettext.install("all", "localization")

TUTORIAL_MOVEMENT = _("Use arrows (←, ↑, →, ↓) to move your tank.")
TUTORIAL_SHOOTING = _("Use the spacebar to shoot. This way you can "
                      "destroy enemy tanks and break walls.")
TUTORIAL_KILL = _("Kill enemies.")
MAIN_MENU_TUTORIAL = _("Tutorial")
MAIN_MENU_PLAY = _("Play")
MAIN_MENU_LANGUAGE = _("Language")
MAIN_MENU_APPLY = _("Apply")
STATS_HP = _("HP")
STATS_KILLS = _("Kills")

SUPPORTED_LANGUAGES = {"English": "en", "Русский": "ru"}
