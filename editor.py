from common import APP_NAME, Content, file_picker
from theme import Theme
from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Adw  # type: ignore


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


class WelcomeContent(Content):
    def __init__(self, window):
        super().__init__()
        self.window = window

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

        self.open_dialog = file_picker(
            window,
            self.theme_picker_response,
            Gtk.FileChooserAction.OPEN,
            "Please choose a *.rtheme file to edit",
        )

    def new_theme(self, widget):
        pass

    def open_theme(self, widget):
        self.open_dialog.show()

    def theme_picker_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.theme = Theme(file=widget.get_file().get_path())
            self.window.stack.set_visible_child_name("themeEditor")
            self.window.theme_editor.theme = self.theme
