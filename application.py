import window
from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Adw  # type: ignore


class rMakerApplication(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="io.risi.rtheme.editor", **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = window.MainWindow(application=self)
        self.window.present()


app = rMakerApplication()
app.run(None)
