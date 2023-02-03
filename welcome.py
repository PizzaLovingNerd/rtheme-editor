import new_dialog
from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Gio, Adw  # type: ignore


class Welcome(Gtk.Box):
    def __init__(self, window=Adw.ApplicationWindow):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # Content Box
        self.contentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.contentBox.set_vexpand(True)
        self.contentBox.set_hexpand(True)

        # Add Sidebar
        sidebar = Sidebar()
        self.contentBox.append(sidebar)

        # Add welcome content
        window_handle = Gtk.WindowHandle()
        window_handle.set_vexpand(True)
        window_handle.set_hexpand(True)
        welcome_content = WelcomeContent(window)
        window_handle.set_child(welcome_content)
        self.contentBox.append(window_handle)

        self.append(self.contentBox)


class Sidebar(Gtk.ListBox):
    def __init__(self):
        super().__init__()

        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_hexpand(False)
        self.set_vexpand(True)
        self.set_valign(Gtk.Align.FILL)
        self.set_halign(Gtk.Align.START)
        self.set_size_request(175, -1)

        # Sidebar Icon/Name Grid
        grid = Gtk.Grid()
        grid.set_margin_top(20)
        grid.set_margin_bottom(20)
        grid.set_margin_start(20)
        grid.set_margin_end(20)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_halign(Gtk.Align.CENTER)
        grid_row = Gtk.ListBoxRow(selectable=False, activatable=False)
        grid_row.set_child(grid)
        self.append(grid_row)

        # Sidebar Icon
        # self_logo = Gtk.Image.new_from_file("../icons/rMaker.png")
        # self_logo.set_pixel_size(32)
        # self_logo.set_margin_end(10)
        # grid.attach(self_logo, 0, 0, 1, 2)

        # Sidebar Name
        self_name = Gtk.Label()
        self_name.set_markup("<b>rMaker</b>")
        self_name.set_halign(Gtk.Align.START)
        self_name.set_valign(Gtk.Align.START)
        grid.attach(self_name, 1, 0, 1, 1)

        # Sidebar Version
        self_version = Gtk.Label()
        self_version.set_markup("v0.1.0")
        self_version.set_halign(Gtk.Align.START)
        self_version.set_valign(Gtk.Align.START)
        grid.attach(self_version, 1, 1, 1, 1)

        # Import Recent Projects from Gsettings
        # settings = Gio.Settings.new("io.risi.rmaker")
        # recent_projects_dirs = settings.get_strv("recent-projects")
        # GFe
        # recent_projects = [
        #     project_manager.Project.new_from_dir(p)
        #     for p in recent_projects_dirs
        #     if project_manager.Project.new_from_dir(p) is not None
        # ]

        # Recent Projects Label
        # if len(recent_projects) > 0:
        #     recent_label = Gtk.Label()
        #     recent_label.set_markup("<b>Recent Projects:</b>")
        #     recent_label.set_halign(Gtk.Align.START)
        #     recent_label.set_valign(Gtk.Align.START)
        #     recent_label.set_margin_top(20)
        #     recent_label.set_margin_start(20)
        #     recent_label.set_margin_end(20)
        #     recent_label_row = Gtk.ListBoxRow(selectable=False, activatable=False)
        #     recent_label_row.set_child(recent_label)
        #     self.append(recent_label_row)

        #     # Recent projects
        #     for project in recent_projects:
        #         proj_label = Gtk.Label(label=project.name)
        #         proj_label.set_margin_top(10)
        #         proj_label.set_margin_start(20)
        #         proj_label.set_margin_bottom(10)
        #         proj_label.set_margin_end(20)
        #         proj_label.set_halign(Gtk.Align.START)
        #         self.append(proj_label)


class WelcomeContent(Gtk.Box):
    def __init__(self, window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.window = window
        self.set_vexpand(True)
        self.set_hexpand(True)

        # Add Titlebar
        self.titlebar = Adw.HeaderBar()
        self.titlebar.add_css_class("flat")
        # self.titlebarLabel = Gtk.Label()
        # self.titlebarLabel.set_markup("<b>rMaker</b>")
        # self.titlebar.set_title_widget(self.titlebarLabel)
        self.append(self.titlebar)

        # Text Box
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        text_box.set_vexpand(True)
        text_box.set_hexpand(True)
        text_box.set_valign(Gtk.Align.CENTER)
        text_box.set_halign(Gtk.Align.CENTER)
        self.append(text_box)

        big_welcome = Gtk.Label()
        big_welcome.set_markup("<big><b>Welcome to rMaker</b></big>")
        text_box.append(big_welcome)

        small_welcome = Gtk.Label()
        small_welcome.set_label("Either create or open a project to start.")
        small_welcome.set_margin_bottom(5)
        text_box.append(small_welcome)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        new_button = Gtk.Button(label="New Project")
        new_button.connect("clicked", self.new_project)
        open_button = Gtk.Button(label="Open Project")
        open_button.connect("clicked", self.open_project)
        button_box.append(new_button)
        button_box.append(open_button)
        text_box.append(button_box)

        self.open_dialog = Gtk.FileChooserNative.new(
            parent=window,
            title="Please choose a project.yml file",
            action=Gtk.FileChooserAction.OPEN,
        )
        self.open_dialog.connect("response", self.project_picker_response)

        filefilter = Gtk.FileFilter()
        filefilter.add_pattern("project.yml")
        self.open_dialog.set_filter(filefilter)

    def new_project(self, widget):
        new_window = new_dialog.NewDialog(self.window)
        new_window.present()

    def open_project(self, widget):
        self.open_dialog.show()

    def project_picker_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            # project = project_manager.Project.new_from_dir(widget.get_file().get_parent().get_path())
            # self.window.stack.set_visible_child_name("projectEditor")
            # project.export_yaml()
            # self.window.project_editor.set_project(project)
            pass
