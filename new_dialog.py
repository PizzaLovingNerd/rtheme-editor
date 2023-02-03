import os.path
from gi import require_version


require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Gio, Adw  # type: ignore

_HOME = os.path.expanduser("~")


class NewDialog(Adw.ApplicationWindow):
    def __init__(self, window=Adw.ApplicationWindow):
        super().__init__()
        self.window = window
        self.set_default_size(700, 500)
        self.set_modal(True)
        self.set_transient_for(window)

        # Window buttons overlay
        self.window_buttons_overlay = Gtk.Overlay()
        window_controls = Gtk.WindowControls(side=Gtk.PackType.END)
        window_controls.set_decoration_layout(":close")
        window_controls.set_valign(Gtk.Align.START)
        window_controls.set_halign(Gtk.Align.END)
        window_controls.set_margin_top(5)
        window_controls.set_margin_end(5)
        self.window_buttons_overlay.add_overlay(window_controls)
        self.set_content(self.window_buttons_overlay)

        # Create box
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.set_vexpand(True)
        self.box.set_hexpand(True)
        self.window_buttons_overlay.set_child(self.box)

        # Create sidebar
        # self.sidebar = distros.DistroSidebar()
        # self.sidebar.connect("row-selected", self.sidebar_row_activated)
        # self.base = self.sidebar.get_selected_base()
        # self.box.append(self.sidebar)

        # Create content
        self.content_handle = Gtk.WindowHandle(vexpand=True, hexpand=True)
        self.content_scroll = Gtk.ScrolledWindow()
        self.content_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_box.set_vexpand(True)
        self.content_box.set_hexpand(True)
        self.content_box.set_valign(Gtk.Align.FILL)
        self.content_box.set_halign(Gtk.Align.FILL)
        self.settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.settings_box.set_vexpand(True)
        self.settings_box.set_valign(Gtk.Align.FILL)
        self.content_scroll.set_child(self.settings_box)
        self.content_box.append(self.content_scroll)
        self.content_handle.set_child(self.content_box)
        self.box.append(self.content_handle)

        # Project Settings
        project_settings = Adw.PreferencesGroup(title="Project Settings")
        project_settings.set_margin_top(20)
        project_settings.set_margin_bottom(20)
        project_settings.set_margin_start(20)
        project_settings.set_margin_end(20)
        project_settings.set_vexpand(False)
        project_settings.set_hexpand(True)
        project_settings.set_valign(Gtk.Align.START)
        project_settings.set_halign(Gtk.Align.FILL)
        self.settings_box.append(project_settings)

        # Project Name
        self.project_name = Adw.EntryRow(title="Project Name")
        self.project_name.set_text("rMakerProject OS")
        self.project_name.connect("changed", self.check_valid)
        project_settings.add(self.project_name)

        # Project Location
        self.project_location = Adw.EntryRow(title="Project Location")
        self.project_location.connect("changed", self.check_valid)
        self.project_location.set_text(f"{_HOME}/Documents/rMakerProjects")
        self.project_location_button = Gtk.Button(icon_name="folder-open-symbolic")
        self.project_location_button.add_css_class("flat")
        self.project_location_button.add_css_class("circular")
        self.project_location_button.set_valign(Gtk.Align.CENTER)
        self.project_location_button.connect("clicked", self.folder_picker_button)
        self.project_location.add_suffix(self.project_location_button)

        self.dialog = Gtk.FileChooserNative.new(
            title="Please choose a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        self.dialog.connect("response", self.folder_picker_response)

        # Project Subdirectory Label
        project_subdirectory_label = Gtk.Label(xalign=0)
        project_subdirectory_label.set_markup(
            "<small>Project will be created in a subdirectory of the selected location</small>"
        )
        project_subdirectory_label.set_valign(Gtk.Align.START)
        project_subdirectory_label.set_margin_start(10)
        project_subdirectory_label.set_margin_top(10)
        project_subdirectory_label.add_css_class("dim-label")

        project_settings.add(self.project_location)
        project_settings.add(project_subdirectory_label)

        # Base Distro Settings
        base_distro_settings = Adw.PreferencesGroup(title="Base Distro Settings")
        base_distro_settings.set_margin_top(20)
        base_distro_settings.set_margin_bottom(20)
        base_distro_settings.set_margin_start(20)
        base_distro_settings.set_margin_end(20)
        base_distro_settings.set_vexpand(True)
        base_distro_settings.set_hexpand(True)
        base_distro_settings.set_valign(Gtk.Align.FILL)
        base_distro_settings.set_halign(Gtk.Align.FILL)
        self.settings_box.append(base_distro_settings)

        # Base Distro Variants
        self.variant_selector = VariantSelector(self.base.variants)
        base_distro_settings.add(self.variant_selector)

        # Base Distro Version
        base_distro_version = Adw.ActionRow(title="Base Distro Version")
        base_distro_version_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        base_distro_version_box.set_margin_top(10)
        base_distro_version_box.set_margin_bottom(10)
        base_distro_version_box.set_margin_start(10)
        base_distro_version_box.set_margin_end(10)
        base_distro_version_box.set_hexpand(True)
        base_distro_version.set_child(base_distro_version_box)

        base_distro_version_label = Gtk.Label(label="Base Distro Version")
        base_distro_version_label.set_halign(Gtk.Align.START)
        base_distro_version_label.set_hexpand(True)
        base_distro_version_box.append(base_distro_version_label)

        self.base_distro_version_combo = Gtk.ComboBoxText()
        self.base_distro_version_combo.set_halign(Gtk.Align.END)
        base_distro_version_box.append(self.base_distro_version_combo)
        base_distro_settings.add(base_distro_version)

        # Create and Cancel Buttons
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.button_box.set_halign(Gtk.Align.END)
        self.button_box.set_hexpand(True)
        self.button_box.set_valign(Gtk.Align.END)
        self.button_box.set_vexpand(False)
        self.button_box.set_margin_top(10)
        self.button_box.set_margin_bottom(10)
        self.button_box.set_margin_start(10)
        self.button_box.set_margin_end(10)

        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.set_halign(Gtk.Align.END)
        self.cancel_button.set_valign(Gtk.Align.END)
        self.cancel_button.set_hexpand(False)
        self.cancel_button.set_vexpand(False)
        self.cancel_button.connect("clicked", lambda button: self.destroy())
        self.button_box.append(self.cancel_button)

        self.create_button = Gtk.Button(label="Create")
        self.create_button.set_halign(Gtk.Align.END)
        self.create_button.set_valign(Gtk.Align.END)
        self.create_button.set_hexpand(False)
        self.create_button.set_vexpand(False)
        self.create_button.connect("clicked", self.create_button_clicked)
        self.button_box.append(self.create_button)

        self.content_box.append(self.button_box)

        self.refresh_base_distro()

    def variant_revealer_button_clicked(self, widget):
        if self.variant_revealer.get_reveal_child():
            self.variant_revealer.set_reveal_child(False)
            self.variant_revealer_button.set_icon_name("go-down-symbolic")
        else:
            self.variant_revealer.set_reveal_child(True)
            self.variant_revealer_button.set_icon_name("go-up-symbolic")

    def refresh_base_distro(self):
        self.variant_selector.remove_all()
        self.variant_selector.add_variants(self.base.variants)
        self.variant_selector.set_subtitle(self.base.variants[0].name)

        show_variants = not len(self.base.variants) == 1
        self.variant_selector.set_enable_expansion(show_variants)
        self.variant_selector.set_expanded(False)

        self.base_distro_version_combo.remove_all()
        for version in self.sidebar.get_selected_base().versions:
            self.base_distro_version_combo.append_text(version)
        self.base_distro_version_combo.set_active(0)

    def sidebar_row_activated(self, widget, row):
        self.base = self.sidebar.get_selected_base()
        self.refresh_base_distro()

    def create_button_clicked(self, widget):
        if os.path.exists(
            os.path.realpath(self.project_location.get_text())
            + f"/{self.project_name.get_text()}"
        ):
            dialog = Adw.MessageDialog(transient_for=self)
            dialog.set_heading("Project directory already exists")
            dialog.set_body(
                f"A project with the name\n{self.project_name.get_text()}"
                f" already exists in:\n{self.project_location.get_text()}."
                f"\n\nPlease change the project name or location."
            )
            dialog.set_size_request(400, 200)
            dialog.add_response("ok", "OK")
            dialog.show()
        else:
            self.window.stack.set_visible_child_name("projectEditor")
            # project = project_manager.Project.create_project(
            #     self.project_name.get_text(),
            #     self.project_location.get_text(),
            #     self.base.name,
            #     self.base_distro_version_combo.get_active_text(),
            #     self.variant_selector.get_variant().template,
            #     self.base.git_repo,
            #     self.base_distro_version_combo.get_active_text(),
            #     self.base.get_formatted_mock_chroot(
            #         self.base_distro_version_combo.get_active_text()
            #     ),
            # )
            # project.export_yaml()
            # self.window.project_editor.set_project(project)
            self.destroy()

    def folder_picker_button(self, widget):
        self.dialog.show()

    def folder_picker_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.project_location.set_text(widget.get_file().get_path())

    def check_valid(self, widget) -> bool:
        name = self.project_name.get_text()
        location = self.project_location.get_text()
        valid = True

        # Check if name is blank
        if len(name) == 0:
            valid = False
            self.project_name.add_css_class("error")
        else:
            self.project_name.remove_css_class("error")

        if len(location) == 0 or not os.access(
            os.path.abspath(os.path.join(location, os.pardir)), os.W_OK
        ):
            valid = False
            self.project_location.add_css_class("error")
        else:
            self.project_location.remove_css_class("error")

        # Checks for attribute first because this code is sometimes called before the create button is created
        if hasattr(self, "create_button"):
            self.create_button.set_sensitive(valid)
        return valid


class VariantSelector(Adw.ExpanderRow):
    def __init__(self, variants):
        super().__init__(title="Base Distro Variant")
        self.set_vexpand(True)
        self.set_valign(Gtk.Align.FILL)
        self.widgets = []
        self.variants = variants

    def add(self, *args, **kwargs):
        super().add_row(*args, **kwargs)
        self.widgets.append(args[0])

    def remove_all(self):
        for widget in self.widgets:
            self.remove(widget)
        self.widgets = []

    def add_variants(self, variants):
        last_variant_widget = None
        for variant in variants:
            variant_widget = VariantSelectorItem(variant, last_variant_widget)
            self.add(variant_widget)
            last_variant_widget = variant_widget

    def get_variant(self):
        for child in self.widgets:
            if child.radio.get_active():
                return child.get_variant()


class VariantSelectorItem(Adw.ActionRow):
    def __init__(self, variant, last_widget: Gtk.CheckButton = None):
        super().__init__()

        self.set_activatable(True)

        label = Gtk.Label(label=variant.name)
        label.set_vexpand(True)
        label.set_halign(Gtk.Align.START)

        self.radio = Gtk.CheckButton()
        self.radio.set_halign(Gtk.Align.END)
        if last_widget is None:
            self.radio.set_active(True)
        else:
            self.radio.set_group(last_widget.radio)

        self.add_prefix(label)
        self.add_suffix(self.radio)
        self.variant = variant

        self.connect("activated", self.on_clicked)

    def on_clicked(self, widget):
        self.radio.set_active(True)
        self.get_root().variant_selector.set_subtitle(self.variant.name)

    def get_variant(self):
        return self.variant
