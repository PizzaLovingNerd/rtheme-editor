from new_dialog import NewDialog
from theme import Theme
from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Adw  # type: ignore

APP_NAME = "<b>rTheme Editor</b>"


class Editor(Gtk.Box):
    def __init__(self, window=Adw.ApplicationWindow):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # Content Box
        self.contentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.contentBox.set_vexpand(True)
        self.contentBox.set_hexpand(True)

        # Add welcome content
        window_handle = Gtk.WindowHandle()
        window_handle.set_vexpand(True)
        window_handle.set_hexpand(True)
        welcome_content = WelcomeContent(window)
        window_handle.set_child(welcome_content)
        self.contentBox.append(window_handle)

        self.append(self.contentBox)


class WelcomeContent(Gtk.Box):
    def __init__(self, window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.window = window
        self.set_vexpand(True)
        self.set_hexpand(True)

        # Add Titlebar
        self.titlebar = Adw.HeaderBar()
        self.titlebar.add_css_class("flat")
        self.titlebarLabel = Gtk.Label()
        self.titlebarLabel.set_markup(APP_NAME)
        self.titlebar.set_title_widget(self.titlebarLabel)
        self.append(self.titlebar)

        # Text Box
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        text_box.set_vexpand(True)
        text_box.set_hexpand(True)
        text_box.set_valign(Gtk.Align.CENTER)
        text_box.set_halign(Gtk.Align.CENTER)
        self.append(text_box)

        big_welcome = Gtk.Label()
        big_welcome.set_markup(f"<big>{APP_NAME}</big>")
        text_box.append(big_welcome)

        small_welcome = Gtk.Label()
        small_welcome.set_label("Either create or open a project to start.")
        small_welcome.set_margin_bottom(5)
        text_box.append(small_welcome)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        new_button = Gtk.Button(label="New Theme")
        new_button.connect("clicked", self.new_theme)
        open_button = Gtk.Button(label="Open Existing Theme")
        open_button.connect("clicked", self.open_theme)
        button_box.append(new_button)
        button_box.append(open_button)
        text_box.append(button_box)

        self.open_dialog = Gtk.FileChooserNative.new(
            parent=window,
            title="Please choose a *.rtheme file",
            action=Gtk.FileChooserAction.OPEN,
        )
        self.open_dialog.connect("response", self.theme_picker_response)

        filefilter = Gtk.FileFilter()
        filefilter.add_pattern("*.rtheme")
        self.open_dialog.set_filter(filefilter)

    def new_theme(self, widget):
        new_window = NewDialog(self.window)
        new_window.present()

    def open_theme(self, widget):
        self.open_dialog.show()

    def theme_picker_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.theme = Theme(file=widget.get_file().get_path())
            self.window.stack.set_visible_child_name("themeEditor")
            self.window.theme_editor.set_theme(self.theme)
