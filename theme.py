from copy import deepcopy
from typing import Any, Dict, Optional
from yaml import safe_load, safe_dump

"""
flags:
  - light
  - dark
main:
  light:
    window_bg_color: "#eed5ee"
    window_fg_color: "#6d507b"
    accent_color: "#d9aeae"
    accent_bg_color: "#d9aeae"
    accent_fg_color: "#1e0742"
    headerbar_bg_color: "#f5dee3"
    headerbar_fg_color: "#6d507b"
    headerbar_backdrop_color: "#fde3e7"
    popover_bg_color: "#fde3e7"
    popover_fg_color: "#1e0742"
    view_bg_color: "#fde3e7"
    view_fg_color: "#1e0742"
    card_bg_color: "#eed5ee"
    card_fg_color: "#1e0742"
  dark:
    accent_color: "#6d507b"
    accent_bg_color: "#612778"
    accent_fg_color: "#eed5ee"
    window_bg_color: "#331052"
    window_fg_color: "#eed5ee"
    headerbar_bg_color: "#28073b"
    headerbar_fg_color: "#eee8d5"
    headerbar_backdrop_color: "#331052"
    popover_bg_color: "#2e1244"
    popover_fg_color: "#eed5ee"
    view_bg_color: "#1e0742"
    view_fg_color: "#eed5ee"
    card_bg_color: "#2e1244"
    card_fg_color: "#fde3e7"
  global:
    dialog_bg_color: "@popover_bg_color"
    dialog_fg_color: "@popover_fg_color"
    warning_bg_color: "#cc791a"
    warning_fg_color: "#eee8d5"
    warning_color: "#cc791a"
    error_bg_color: "#dc2f2f"
    error_fg_color: "#eed5ee"
    error_color: "#dc2f2f"
    success_bg_color: "#00991c"
    success_fg_color: "#eed5ee"
    success_color: "#00991c"
    destructive_bg_color: "#c93e81"
    destructive_fg_color: "#eed5ee"
    destructive_color: "#c93e81"





"""

FLAGS = "flags"
MAIN = "main"
GLOBAL = "global"


def apply_transforms(base: str, transformations: Dict[str, str]) -> str:
    for old, new in transformations.items():
        base = base.replace(old, new)
    return base


def display_text(prop: str) -> str:
    return " ".join(
        map(
            lambda word: word.capitalize(),
            apply_transforms(
                prop,
                {
                    "bg": "background",
                    "fg": "foreground",
                },
            ).split("_"),
        )
    )


def validate_props(props: Any, section: Optional[str] = None):
    for_section = "" if section is None else f"for section {section} "
    if not isinstance(props, dict):
        raise ValueError(
            f"Invalid yaml format, props {for_section}must be key value pairs"
        )
    for key, value in props.items():
        if not isinstance(key, str):
            raise ValueError(f"Key {key} must be a valid string")
        if "properties" in key:
            continue
        if not isinstance(value, str):
            raise ValueError(f"Value {value} must be a valid string")


class Theme:
    """
    Logic and state for an rTheme.
    """

    valid_props = [
        "popover_bg_color",
        "accent_color",
        "success_color",
        "accent_bg_color",
        "success_bg_color",
        "headerbar_backdrop_color",
        "headerbar_fg_color",
        "headerbar_border_color",
        "headerbar_shade_color",
        "warning_fg_color",
        "window_fg_color",
        "card_bg_color",
        "error_bg_color",
        "accent_fg_color",
        "warning_color",
        "headerbar_bg_color",
        "view_bg_color",
        "success_fg_color",
        "error_fg_color",
        "dialog_fg_color",
        "card_shade_color",
        "destructive_bg_color",
        "error_color",
        "destructive_fg_color",
        "panel_color",
        "shade_color",
        "warning_bg_color",
        "popover_fg_color",
        "scrollbar_outline_color",
        "view_fg_color",
        "card_fg_color",
        "window_bg_color",
        "destructive_color",
        "dialog_bg_color",
    ]

    def __init__(self, file: Optional[str] = None) -> None:
        self.file = file
        self.flags: Dict[str, Dict[str, str]] = {}
        self.global_props: Dict[str, str] = {}
        self.variants: Dict[str, Dict[str, str]] = {}

        if self.file != None:
            with open(self.file, "r") as f:
                yaml = safe_load(f.read())
                self._default = deepcopy(yaml)

            if not isinstance(yaml, dict):
                raise ValueError(
                    "Invalid yaml format, must have top level key declarations"
                )

            if FLAGS in yaml and isinstance(yaml[FLAGS], list):
                for flag in yaml[FLAGS]:
                    self.flags[flag] = {}

            if MAIN in yaml and isinstance(yaml[MAIN], dict):
                for section, props in yaml[MAIN].items():
                    validate_props(props, section)
                    if section == GLOBAL:
                        self.global_props = props
                    elif section in self.flags:
                        self.flags[section] = props
            if FLAGS in yaml:
                del yaml[FLAGS]
            if MAIN in yaml:
                del yaml[MAIN]

            for variant, flags in yaml.items():
                if not isinstance(flags, dict):
                    raise ValueError(
                        f"Flags/global sections must contain key/value props in variant {variant}"
                    )
                for flag, props in flags.items():
                    validate_props(props, f"{variant}.{flag}")
            self.variants = yaml

    def _as_dict(self) -> dict:
        return {
            FLAGS: list(self.flags.keys()),
            MAIN: {**self.flags, GLOBAL: self.global_props},
            **self.variants,
        }

    def export(self):
        if not self.file:
            return
        with open(self.file, "w") as f:
            safe_dump(self._as_dict(), f)

    def is_default(self) -> bool:
        return self._default == self._as_dict()
