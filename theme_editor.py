import os.path
from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Adw  # type: ignore

_HOME = os.path.expanduser("~")

# Stack with Basic and Advanced pages
# Basic Pages:
# - Metadata
# - Repositories
# - Packages
# - Kickstart
# - Gsettings
# - Branding


class ThemeEditor(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.project = None

        # Titlebar
        self.titlebar = Adw.HeaderBar()
        self.save_button = Gtk.Button(icon_name="document-save-symbolic")
        self.save_button.set_tooltip_text("Save Project")
        self.save_button.set_valign(Gtk.Align.CENTER)
        self.save_button.connect("clicked", self.save_project)
        self.titlebar.pack_end(self.save_button)

        # Stack and StackSwitcher
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)
        self.titlebar.set_title_widget(self.stack_switcher)
        self.append(self.titlebar)
        self.append(self.stack)

        # Basic Stack
        basic_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.basic_stack = Gtk.Stack()
        self.basic_stack.set_margin_top(20)
        self.basic_stack.set_margin_start(20)
        self.basic_stack.set_margin_end(20)
        self.basic_stack.set_margin_bottom(20)
        self.basic_stack.set_vexpand(True)
        self.basic_stack.set_hexpand(True)
        self.basic_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.basic_stack.set_transition_duration(500)
        basic_sidebar = Gtk.StackSidebar()
        basic_sidebar.set_stack(self.basic_stack)
        basic_sidebar.set_size_request(175, -1)
        basic_sidebar.add_css_class("sidebar")
        basic_box.append(basic_sidebar)
        basic_box.append(self.basic_stack)
        self.stack.add_titled(basic_box, "basic", "Basic")

        # Advanced Stack
        advanced_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.advanced_stack = Gtk.Stack()
        self.advanced_stack.set_margin_top(20)
        self.advanced_stack.set_margin_start(20)
        self.advanced_stack.set_margin_end(20)
        self.advanced_stack.set_margin_bottom(20)
        self.advanced_stack.set_vexpand(True)
        self.advanced_stack.set_hexpand(True)
        self.advanced_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.advanced_stack.set_transition_duration(500)
        advanced_sidebar = Gtk.StackSidebar()
        advanced_sidebar.set_stack(self.advanced_stack)
        advanced_sidebar.set_size_request(175, -1)
        advanced_sidebar.add_css_class("sidebar")
        advanced_box.append(advanced_sidebar)
        advanced_box.append(self.advanced_stack)
        self.stack.add_titled(advanced_box, "advanced", "Advanced")

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
