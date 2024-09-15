from PyQt5.QtWidgets import (QMainWindow, QLabel, QTextEdit, QVBoxLayout, QWidget, QComboBox, QAction,
                             QFileDialog, QCheckBox)
from PyQt5.QtCore import QTimer, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
from googletrans import Translator
from translation_worker import TranslationWorker


class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread_pool = QThreadPool()
        self.timer = None
        self.dest_lang = None
        self.src_lang_label = None
        self.input_text = None
        self.output_text = None
        self.src_lang = None
        self.auto_detect_checkbox = None
        self.languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
        self.language_map = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Chinese": "zh-cn",
            "Japanese": "ja"
        }
        self.translator = Translator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Translator")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Input label and text area
        input_label = QLabel("Enter text to translate:", self)
        layout.addWidget(input_label)

        self.input_text = QTextEdit(self)
        layout.addWidget(self.input_text)

        # Output label and text area
        output_label = QLabel("Translated text:", self)
        layout.addWidget(output_label)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        # Source language label and combobox
        self.src_lang_label = QLabel("Source Language:", self)
        layout.addWidget(self.src_lang_label)

        self.src_lang = QComboBox(self)
        self.src_lang.addItems(self.languages)
        self.src_lang.setCurrentText("English")
        layout.addWidget(self.src_lang)

        # Destination language combobox
        self.dest_lang = QComboBox(self)
        self.dest_lang.addItems(self.language_map.keys())
        self.dest_lang.setCurrentText("Spanish")
        layout.addWidget(self.dest_lang)

        # Auto-detect language checkbox
        self.auto_detect_checkbox = QCheckBox("Auto-detect source language", self)
        self.auto_detect_checkbox.setChecked(False)
        self.toggle_auto_detect()
        self.auto_detect_checkbox.stateChanged.connect(self.toggle_auto_detect)
        layout.addWidget(self.auto_detect_checkbox)

        # Set layout to the central widget
        central_widget.setLayout(layout)

        # Menu bar
        self.create_menu()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.perform_translation)
        self.timer.start(1000)

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')

        load_action = QAction('Load', self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_translated_file)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt);;All Files (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.input_text.setText(file.read())

    def save_translated_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Translated File", "",
                                                   "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.output_text.toPlainText())

    def detect_language(self, text):
        try:
            detection = self.translator.detect(text)
            return detection.lang  # Returns the detected language code (e.g., 'en', 'es')
        except Exception as e:
            print(f"Language detection error: {e}")
            return None

    def translate_text(self, text, src_lang, dest_lang):
        try:
            translation = self.translator.translate(text, src=src_lang, dest=dest_lang)
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return "Translation failed."

    def perform_translation(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            self.output_text.setPlainText("")
            return

        # Determine source language
        if self.auto_detect_checkbox.isChecked():
            detected_lang = self.detect_language(text)
            if detected_lang:
                src_lang = detected_lang
            else:
                src_lang = 'en'  # Default to English if detection fails
                print("Language detection failed, defaulting to English.")
        else:
            src_lang = self.src_lang.currentText()

        dest_lang = self.language_map[self.dest_lang.currentText()]  # Get the correct language code

        # Perform translation
        worker = TranslationWorker(text, src_lang, dest_lang, self.translator)
        worker.signals.result.connect(self.display_translation)
        worker.signals.error.connect(self.display_error)

        self.thread_pool.start(worker)

    def toggle_auto_detect(self):
        """Toggle the label of source language based on auto-detect status."""
        if self.auto_detect_checkbox.isChecked():
            self.src_lang_label.setText("Language detected automatically")
            self.src_lang.setEnabled(False)  # Disable manual selection when auto-detect is on
        else:
            self.src_lang_label.setText("Source Language:")
            self.src_lang.setEnabled(True)  # Enable manual selection when auto-detect is off

    def display_translation(self, translated_text):
        self.output_text.setPlainText(translated_text)

    def display_error(self, error_message):
        self.output_text.setPlainText(error_message)