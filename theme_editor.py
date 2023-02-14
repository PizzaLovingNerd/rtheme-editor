import os.path
from gi import require_version

from common import APP_NAME, Content, file_picker

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Adw  # type: ignore

from typing import Optional
from theme import Theme

_HOME = os.path.expanduser("~")


class ThemeEditor(Content):
    def __init__(self, window=Adw.ApplicationWindow):
        super().__init__()
        self.window = window
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.theme: Optional[Theme] = None

        # Titlebar
        self.save_button = Gtk.Button(icon_name="document-save-symbolic")
        self.save_button.set_tooltip_text("Save Project")
        self.save_button.set_valign(Gtk.Align.CENTER)
        self.save_button.connect("clicked", self.save_theme)
        self.titlebar.pack_end(self.save_button)
        self.check_savable()

        # File Save Picker
        self.save_picker = file_picker(
            window,
            self.choose_file,
            Gtk.FileChooserAction.SAVE,
            "Choose where to save the rtheme",
        )

        # Test button
        open_button = Gtk.Button(label="Test")
        open_button.connect("clicked", lambda _: self.check_savable())
        self.append(open_button)

    def choose_file(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT and self.theme:
            file = str(widget.get_file().get_path())
            if not file.endswith(".rtheme"):
                file += ".rtheme"
            self.theme.file = file
            self.window.stack.set_visible_child_name("themeEditor")
            self.window.theme_editor.theme = self.theme
            self.save_theme(None)

    def save_theme(self, _):
        if self.theme and self.theme.file is not None:
            self.theme.export()
            self.check_savable()
        else:
            self.save_picker.show()

    def check_savable(self) -> bool:
        savable = (
            self.theme is not None
            and self.theme.file is not None
            and os.path.exists(self.theme.file)
            and not self.theme.is_default()
        )
        self.save_button.set_sensitive(savable)
        return savable
