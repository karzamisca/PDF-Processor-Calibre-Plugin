from calibre.customize import InterfaceActionBase

class TextExtractorPlugin(InterfaceActionBase):
    name = 'Text Extractor Plugin'
    description = 'Extract text from PDF based on keyword'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Hoàng Minh Quân'
    version = (1, 0, 0)
    minimum_calibre_version = (0, 7, 53)

    actual_plugin = 'calibre_plugins.text_extractor.ui:TextExtractorPluginUI'

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.text_extractor.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        config_widget.save_settings()
        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()
