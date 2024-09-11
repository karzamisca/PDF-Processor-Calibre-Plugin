### PDF Processor Calibre Plugin

### `__init__.py`

- **`TextExtractorPlugin`**:
  - **Purpose**: Defines the main plugin class for integrating with Calibre. This class provides metadata about the plugin and handles configuration.
  - **Methods**:
    - `is_customizable()`: Returns whether the plugin can be customized.
    - `config_widget()`: Returns the configuration widget for the plugin.
    - `save_settings(config_widget)`: Saves settings from the configuration widget.

### `main.py`

- **`split_sentences(text)`**:
  - **Purpose**: Splits a given text into sentences using regular expressions.

- **`clean_text(text)`**:
  - **Purpose**: Cleans the text by removing excessive newlines and whitespace.

- **`extract_text_from_epub(epub_path, keyword, output_folder, num_sentences, direction)`**:
  - **Purpose**: Extracts text from EPUB files based on a keyword and saves it to a specified output folder. Supports both forward and backward extraction of sentences.

- **`extract_text_from_pdf(pdf_path, keyword, output_folder, num_sentences, direction)`**:
  - **Purpose**: Extracts text from PDF files based on a keyword and saves it to a specified output folder. Supports both forward and backward extraction of sentences.

- **`search_keyword_in_pdf(pdf_path, keyword, num_sentences, direction)`**:
  - **Purpose**: Searches for a keyword in a PDF file and returns the results as a cleaned string. Supports both forward and backward extraction of sentences.

- **`search_keyword_in_epub(epub_path, keyword, num_sentences, direction)`**:
  - **Purpose**: Searches for a keyword in an EPUB file and returns the results as a cleaned string. Supports both forward and backward extraction of sentences.

- **`TextExtractorDialog`**:
  - **Purpose**: Defines the main dialog for the plugin, providing a user interface for selecting files, folders, keywords, and options for extraction or search.
  - **Methods**:
    - `__init__(self, gui, icon, do_user_config)`: Initializes the dialog with GUI, icon, and configuration options.
    - `browse_input_folder(self)`: Opens a dialog to select the input folder.
    - `browse_output_folder(self)`: Opens a dialog to select the output folder.
    - `browse_input_file(self)`: Opens a dialog to select an input file.
    - `search_keyword(self)`: Searches for the keyword in the selected file and displays results.
    - `process_files(self)`: Processes files in the selected folder or a single file based on user options.

### `ui.py`

- **`TextExtractorPluginUI`**:
  - **Purpose**: Integrates the plugin into Calibre's interface as an action, allowing the user to open the plugin's dialog.
  - **Methods**:
    - `genesis(self)`: Initializes the action, setting up the icon and connecting it to the dialog display.
    - `show_dialog(self)`: Displays the `TextExtractorDialog` when the action is triggered.
    - `apply_settings(self)`: Applies settings from the configuration. (Incomplete in the provided code)

