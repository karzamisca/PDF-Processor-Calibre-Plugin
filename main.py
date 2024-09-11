import os #Built in for Python 3.12.6
import zipfile #Built in for Python 3.12.6
import io #Built in for Python 3.12.6
import re #Built in for Python 3.12.6
from bs4 import BeautifulSoup #v4.12.3 
from PyQt5 import QtWidgets, QtCore, QtGui #v5.15.11 
from calibre_plugins.text_extractor.PyPDF2 import PdfReader #v3.0.1, abandoned, recommend switchung to pypdf 4.3.1

def split_sentences(text):
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    return sentence_endings.split(text)

def clean_text(text):
    # Remove multiple newlines and excessive whitespace
    cleaned_text = re.sub(r'\n+', '\n', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def extract_text_from_epub(epub_path, keyword, output_folder, num_sentences, direction):
    extracted_text = []
    sentences = []
    sentence_page_map = {}

    with zipfile.ZipFile(epub_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.xhtml') or file_info.filename.endswith('.html'):
                with zip_ref.open(file_info) as f:
                    soup = BeautifulSoup(f, 'lxml')
                    text = soup.get_text()
                    page_sentences = split_sentences(text)
                    sentences.extend(page_sentences)
                    sentence_page_map.update({i: file_info.filename for i, _ in enumerate(page_sentences, start=len(sentences) - len(page_sentences))})

    keyword_indices = [i for i, s in enumerate(sentences) if keyword.lower() in s.lower()]

    for index in keyword_indices:
        if direction == "Forward":
            selected_sentences = sentences[index:index + num_sentences]
        elif direction == "Backward":
            selected_sentences = sentences[max(0, index - num_sentences + 1):index + 1]

        page_number = sentence_page_map.get(index, 1)
        extracted_text.append(f"KEYWORD FOUND IN {page_number}, SENTENCE {index + 1}:\n{' '.join(selected_sentences)}")

    if extracted_text:
        text_filename = os.path.join(output_folder, "extracted_text.txt")
        with open(text_filename, "w", encoding="utf-8") as text_file:
            cleaned_text = clean_text("\n\n".join(extracted_text))
            text_file.write(cleaned_text)

def extract_text_from_pdf(pdf_path, keyword, output_folder, num_sentences, direction):

    pdf_document = PdfReader(pdf_path)
    extracted_text = []
    sentences = []
    sentence_page_map = {}

    for page_number, page in enumerate(pdf_document.pages):
        text = page.extract_text()
        if text:
            page_sentences = split_sentences(text)
            sentences.extend(page_sentences)
            sentence_page_map.update({i: page_number + 1 for i, _ in enumerate(page_sentences, start=len(sentences) - len(page_sentences))})

    keyword_indices = [i for i, s in enumerate(sentences) if keyword.lower() in s.lower()]

    for index in keyword_indices:
        if direction == "Forward":
            selected_sentences = sentences[index:index + num_sentences]
        elif direction == "Backward":
            selected_sentences = sentences[max(0, index - num_sentences + 1):index + 1]

        page_number = sentence_page_map.get(index, 1)
        extracted_text.append(f"KEYWORD FOUND ON PAGE {page_number}, SENTENCE {index + 1}:\n{' '.join(selected_sentences)}")

    if extracted_text:
        text_filename = os.path.join(output_folder, "extracted_text.txt")
        with open(text_filename, "w", encoding="utf-8") as text_file:
            cleaned_text = clean_text("\n\n".join(extracted_text))
            text_file.write(cleaned_text)

def search_keyword_in_pdf(pdf_path, keyword, num_sentences, direction):

    pdf_document = PdfReader(pdf_path)
    results = []
    sentences = []
    sentence_page_map = {}

    for page_number, page in enumerate(pdf_document.pages):
        text = page.extract_text()
        if text:
            page_sentences = split_sentences(text)
            sentences.extend(page_sentences)
            sentence_page_map.update({i: page_number + 1 for i, _ in enumerate(page_sentences, start=len(sentences) - len(page_sentences))})

    keyword_indices = [i for i, s in enumerate(sentences) if keyword.lower() in s.lower()]

    for index in keyword_indices:
        if direction == "Forward":
            selected_sentences = sentences[index:index + num_sentences]
        elif direction == "Backward":
            selected_sentences = sentences[max(0, index - num_sentences + 1):index + 1]

        page_number = sentence_page_map.get(index, 1)
        results.append(f"KEYWORD FOUND ON PAGE {page_number}, SENTENCE {index + 1}:\n{' '.join(selected_sentences)}")
    cleaned_results = clean_text("\n\n".join(results))    
    return cleaned_results

def search_keyword_in_epub(epub_path, keyword, num_sentences, direction):
    extracted_text = []
    sentences = []
    sentence_page_map = {}

    with zipfile.ZipFile(epub_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.xhtml') or file_info.filename.endswith('.html'):
                with zip_ref.open(file_info) as f:
                    soup = BeautifulSoup(f, 'lxml')
                    text = soup.get_text()
                    page_sentences = split_sentences(text)
                    sentences.extend(page_sentences)
                    sentence_page_map.update({i: file_info.filename for i, _ in enumerate(page_sentences, start=len(sentences) - len(page_sentences))})

    keyword_indices = [i for i, s in enumerate(sentences) if keyword.lower() in s.lower()]

    for index in keyword_indices:
        if direction == "Forward":
            selected_sentences = sentences[index:index + num_sentences]
        elif direction == "Backward":
            selected_sentences = sentences[max(0, index - num_sentences + 1):index + 1]

        page_number = sentence_page_map.get(index, 1)
        extracted_text.append(f"KEYWORD FOUND IN {page_number}, SENTENCE {index + 1}:\n{' '.join(selected_sentences)}")

    cleaned_results = clean_text("\n\n".join(extracted_text))
    return cleaned_results

class TextExtractorDialog(QtWidgets.QDialog):
    def __init__(self, gui, icon, do_user_config):
        super().__init__(gui)
        self.gui = gui
        self.do_user_config = do_user_config
        self.db = gui.current_db

        self.l = QtWidgets.QVBoxLayout()
        self.setLayout(self.l)

        self.input_folder_var = QtWidgets.QLineEdit(self)
        self.output_folder_var = QtWidgets.QLineEdit(self)
        self.input_file_var = QtWidgets.QLineEdit(self)
        self.text_var = QtWidgets.QCheckBox("Extract Text", self)
        self.search_keyword_var = QtWidgets.QLineEdit(self)
        self.search_results_var = QtWidgets.QTextEdit(self)
        self.search_results_var.setReadOnly(True)

        self.direction_var = QtWidgets.QComboBox(self)
        self.direction_var.addItems(["Forward", "Backward"])
        self.num_sentences_var = QtWidgets.QSpinBox(self)
        self.num_sentences_var.setMinimum(1)
        self.num_sentences_var.setValue(5)

        input_folder_label = QtWidgets.QLabel("Input Folder:", self)
        output_folder_label = QtWidgets.QLabel("Output Folder:", self)
        input_file_label = QtWidgets.QLabel("Or Input File:", self)
        direction_label = QtWidgets.QLabel("Extract Text Direction:", self)
        num_sentences_label = QtWidgets.QLabel("Number of Sentences:", self)
        search_keyword_label = QtWidgets.QLabel("Search Keyword:", self)

        browse_input_folder_btn = QtWidgets.QPushButton("Browse Folder", self)
        browse_output_folder_btn = QtWidgets.QPushButton("Browse", self)
        browse_input_file_btn = QtWidgets.QPushButton("Browse File", self)
        process_btn = QtWidgets.QPushButton("Process Files", self)
        search_btn = QtWidgets.QPushButton("Search Keyword", self)

        browse_input_folder_btn.clicked.connect(self.browse_input_folder)
        browse_output_folder_btn.clicked.connect(self.browse_output_folder)
        browse_input_file_btn.clicked.connect(self.browse_input_file)
        process_btn.clicked.connect(self.process_files)
        search_btn.clicked.connect(self.search_keyword)

        self.l.addWidget(input_folder_label)
        self.l.addWidget(self.input_folder_var)
        self.l.addWidget(browse_input_folder_btn)
        self.l.addWidget(input_file_label)
        self.l.addWidget(self.input_file_var)
        self.l.addWidget(browse_input_file_btn)
        self.l.addWidget(output_folder_label)
        self.l.addWidget(self.output_folder_var)
        self.l.addWidget(browse_output_folder_btn)
        self.l.addWidget(self.text_var)
        self.l.addWidget(direction_label)
        self.l.addWidget(self.direction_var)
        self.l.addWidget(num_sentences_label)
        self.l.addWidget(self.num_sentences_var)
        self.l.addWidget(search_keyword_label)
        self.l.addWidget(self.search_keyword_var)
        self.l.addWidget(search_btn)
        self.l.addWidget(self.search_results_var)
        self.l.addWidget(process_btn)

        self.setWindowTitle('Text Extractor Plugin')
        self.setWindowIcon(icon)
        self.resize(self.sizeHint())

    def browse_input_folder(self):
        folder_selected = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Input Folder")
        self.input_folder_var.setText(folder_selected)

    def browse_output_folder(self):
        folder_selected = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder")
        self.output_folder_var.setText(folder_selected)

    def browse_input_file(self):
        file_selected = QtWidgets.QFileDialog.getOpenFileName(self, "Select Input File", filter="PDF files (*.pdf);;EPUB files (*.epub)")[0]
        self.input_file_var.setText(file_selected)

    def search_keyword(self):
        input_file = self.input_file_var.text()
        keyword = self.search_keyword_var.text()
        num_sentences = self.num_sentences_var.value()
        direction = self.direction_var.currentText()
        if not input_file or not keyword:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please select an input file and enter a keyword.")
            return
        
        if input_file.lower().endswith(".pdf"):
            results = search_keyword_in_pdf(input_file, keyword, num_sentences, direction)
        elif input_file.lower().endswith(".epub"):
            results = search_keyword_in_epub(input_file, keyword, num_sentences, direction)
        else:
            QtWidgets.QMessageBox.warning(self, "File Type Error", "Unsupported file type.")
            return

        self.search_results_var.setPlainText(results)

    def process_files(self):
        input_folder = self.input_folder_var.text()
        output_folder = self.output_folder_var.text()
        input_file = self.input_file_var.text()
        extract_text = self.text_var.isChecked()

        if not input_folder and not input_file:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please select either an input folder or an input file.")
            return
        if not output_folder:
            QtWidgets.QMessageBox.warning(self, "Output Error", "Please select an output folder.")
            return
        if not extract_text:
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select at least one processing option.")
            return

        keyword = self.search_keyword_var.text()
        num_sentences = self.num_sentences_var.value()
        direction = self.direction_var.currentText()

        if input_file:
            file_paths = [input_file]
        else:
            file_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith((".pdf", ".epub"))]

        for file_path in file_paths:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            file_output_folder = os.path.join(output_folder, file_name)
            os.makedirs(file_output_folder, exist_ok=True)
            if extract_text and keyword:
                if file_path.lower().endswith(".pdf"):
                    extract_text_from_pdf(file_path, keyword, file_output_folder, num_sentences, direction)
                elif file_path.lower().endswith(".epub"):
                    extract_text_from_epub(file_path, keyword, file_output_folder, num_sentences, direction)

        QtWidgets.QMessageBox.information(self, "Processing Complete", "Processing has been completed successfully.")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TextExtractorDialog(None, QtGui.QIcon(), None)
    window.show()
    app.exec_()
