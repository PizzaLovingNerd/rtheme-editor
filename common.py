from typing import Any, Callable, Tuple
from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Adw  # type: ignore

APP_NAME = "<b>rTheme Editor</b>"


class Content(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_vexpand(True)
        self.set_hexpand(True)

        # Add Titlebar
        self.titlebar = Adw.HeaderBar()
        self.titlebar.add_css_class("flat")
        self.titlebarLabel = Gtk.Label()
        self.titlebarLabel.set_markup(APP_NAME)
        self.titlebar.set_title_widget(self.titlebarLabel)
        self.append(self.titlebar)


def file_picker(
    window: Adw.ApplicationWindow,
    handler: Callable[..., None],
    action: Gtk.FileChooserAction,
    desc: str = "",
):
    dialog = Gtk.FileChooserNative.new(
        parent=window,
        title=desc,
        action=action,
    )
    dialog.connect("response", handler)

    filefilter = Gtk.FileFilter()
    filefilter.add_pattern("*.rtheme")
    dialog.set_filter(filefilter)
    return dialog
