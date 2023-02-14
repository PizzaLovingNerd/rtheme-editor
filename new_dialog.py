from gi import require_version


require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Gio, Adw  # type: ignore


class NewDialog(Adw.ApplicationWindow):
    pass
