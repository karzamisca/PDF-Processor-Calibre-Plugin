from calibre.gui2.actions import InterfaceAction
from calibre_plugins.text_extractor.main import TextExtractorDialog

class TextExtractorPluginUI(InterfaceAction):

    name = 'Text Extractor Plugin'

    action_spec = ('Text Extractor Plugin', None,
                   'Run the Text Extractor Plugin', 'Ctrl+Shift+F1')

    def genesis(self):
        icon = get_icons('images/icon.png', 'Text Extractor Plugin')
        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)

    def show_dialog(self):
        base_plugin_object = self.interface_action_base_plugin
        do_user_config = base_plugin_object.do_user_config
        d = TextExtractorDialog(self.gui, self.qaction.icon(), do_user_config)
        d.show()

    def apply_settings(self):
        from calibre_plugins.text_extractor.config import prefs
        prefs
