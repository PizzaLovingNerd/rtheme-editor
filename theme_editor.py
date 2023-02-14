import os.path
from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Adw  # type: ignore

from typing import Optional
from theme import Theme

_HOME = os.path.expanduser("~")


class ThemeEditor(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.project: Optional[Theme] = None

        # Titlebar
        self.titlebar = Adw.HeaderBar()
        self.save_button = Gtk.Button(icon_name="document-save-symbolic")
        self.save_button.set_tooltip_text("Save Project")
        self.save_button.set_valign(Gtk.Align.CENTER)
        self.save_button.connect("clicked", self.save_project)
        self.titlebar.pack_end(self.save_button)

    def save_project(self, button):
        self.metadata_page.save_project()
        self.repositories_page.save_project()
        self.packages_page.save_project()
        # self.project.export_yaml()
        self.save_button.set_sensitive(False)

    def set_project(self, project):
        self.project = project
        self.metadata_page.set_project(project)
        self.repositories_page.set_project(project)
        self.packages_page.set_project(project)

    def check_savable(self) -> bool:
        savable = False
        if self.is_valid():
            if self.metadata_page.check_savable():
                savable = True
            if self.repositories_page.check_savable():
                savable = True
            if self.packages_page.check_savable():
                savable = True
        self.save_button.set_sensitive(savable)
        return savable

    def is_valid(self) -> bool:
        valid = True
        if not self.metadata_page.check_valid():
            valid = False
        if not self.repositories_page.check_valid():
            valid = False
        return valid
