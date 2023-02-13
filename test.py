import yaml

with open("risi.rtheme", "r") as f:
    print(yaml.safe_load(f.read()))


h = {
    "flags": ["light", "dark"],
    "main": {
        "light": {
            "accent_color": "#ed4a3f",
            "destructive_color": "#d81c1c",
            "destructive_bg_color": "#e01b24",
            "success_color": "#26a269",
            "success_bg_color": "#2ec27e",
            "warning_color": "#ae7b03",
            "warning_bg_color": "#e5a50a",
            "error_color": "#c01c28",
            "error_bg_color": "#e01b24",
            "window_bg_color": "#f6f5f4",
            "window_fg_color": "rgba(0, 0, 0, 0.8)",
            "view_bg_color": "#ffffff",
            "view_fg_color": "rgba(0, 0, 0, 0.8)",
            "headerbar_bg_color": "#d9d9d9",
            "headerbar_fg_color": "rgba(0, 0, 0, 0.8)",
            "headerbar_border_color": "rgba(0, 0, 0, 0.8)",
            "headerbar_backdrop_color": "#f6f5f4",
            "headerbar_shade_color": "rgba(0, 0, 0, 0.07)",
            "card_bg_color": "#ffffff",
            "card_fg_color": "rgba(0, 0, 0, 0.8)",
            "card_shade_color": "rgba(0, 0, 0, 0.07)",
            "popover_bg_color": "#ffffff",
            "popover_fg_color": "rgba(0, 0, 0, 0.8)",
            "shade_color": "rgba(0, 0, 0, 0.07)",
            "scrollbar_outline_color": "#ffffff",
        },
        "dark": {
            "accent_color": "#cb3f40",
            "destructive_color": "#ff7b63",
            "destructive_bg_color": "#c01c28",
            "success_color": "#8ff0a4",
            "success_bg_color": "#26a269",
            "warning_color": "#f0c05a",
            "warning_bg_color": "#f8e45c",
            "error_color": "#ff7b63",
            "error_bg_color": "#c01c28",
            "window_bg_color": "#353535",
            "window_fg_color": "#ffffff",
            "view_bg_color": "#2d2d2d",
            "view_fg_color": "#ffffff",
            "headerbar_bg_color": "#292929",
            "headerbar_fg_color": "#ffffff",
            "headerbar_border_color": "#ffffff",
            "headerbar_backdrop_color": "#242424",
            "headerbar_shade_color": "rgba(0, 0, 0, 0.36)",
            "card_bg_color": "rgba(255, 255, 255, 0.08)",
            "card_fg_color": "#ffffff",
            "card_shade_color": "rgba(0, 0, 0, 0.36)",
            "popover_bg_color": "#1e1e1e",
            "popover_fg_color": "#ffffff",
            "shade_color": "rgba(0, 0, 0, 0.36)",
            "scrollbar_outline_color": "rgba(0, 0, 0, 0.5)",
        },
        "global": {
            "accent_bg_color": "#ff4033",
            "accent_fg_color": "#ffffff",
            "destructive_fg_color": "#ffffff",
            "success_fg_color": "#ffffff",
            "warning_fg_color": "rgba(0, 0, 0, 0.8)",
            "error_fg_color": "#ffffff",
            "plugin_properties": {
                "gnome_shell": {
                    "panel_color": "#292929",
                    "custom_css": "#dash .dash-background {\n    background-color: transparent;}\n#overviewGroup {\n    background-color: #292929; }\n",
                }
            },
        },
    },
    "blue": {
        "light": {"accent_color": "#1c71d8"},
        "dark": {"accent_color": "#3584e4"},
        "global": {"accent_bg_color": "#62a0ea"},
    },
    "green": {
        "light": {"accent_color": "#26a269"},
        "dark": {"accent_color": "#26a269"},
        "global": {"accent_bg_color": "#26a269"},
    },
    "yellow": {
        "light": {"accent_color": "#e5a50a"},
        "dark": {"accent_color": "#e5a50a"},
        "global": {"accent_bg_color": "#e5a50a"},
    },
    "orange": {
        "light": {"accent_color": "#e66100"},
        "dark": {"accent_color": "#ffa348"},
        "global": {"accent_bg_color": "#f8c45c"},
    },
    "red": {
        "light": {"accent_color": "#ed333b"},
        "dark": {"accent_color": "#e01b24"},
        "global": {"accent_bg_color": "#c01c28"},
    },
    "purple": {
        "light": {"accent_color": "#c061cb"},
        "dark": {"accent_color": "#9141ac"},
        "global": {"accent_bg_color": "#813d9c"},
    },
    "brown": {
        "light": {"accent_color": "#b5835a"},
        "dark": {"accent_color": "#986a44"},
        "global": {"accent_bg_color": "#865e3c"},
    },
}
