# from ui.KickStartBuilder import ProjectEditor

from gi import require_version

from editor import Editor
from theme_editor import ThemeEditor


require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Adw  # type: ignore


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="rTheme Editor")
        self.set_default_size(800, 600)

        # Create main stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)
        self.set_content(self.stack)

        # Import editor box
        self.editor = Editor(self)
        self.stack.add_named(self.editor, "welcome")

        # Import project editor
        self.project_editor = ThemeEditor()
        self.stack.add_named(self.project_editor, "themeEditor")
