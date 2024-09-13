from PyQt5.QtWidgets import QMainWindow, QLabel, QTextEdit, QVBoxLayout, QWidget, QComboBox, QAction, QFileDialog
from PyQt5.QtCore import QTimer
from googletrans import Translator


class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translate_button = None
        self.dest_lang = None
        self.src_lang = None
        self.output_text = None
        self.input_text = None
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

        # Language selection
        self.src_lang = QComboBox(self)
        self.src_lang.addItems(["English", "Spanish", "French", "German", "Chinese", "Japanese"])
        self.src_lang.setCurrentText("English")
        layout.addWidget(self.src_lang)

        self.dest_lang = QComboBox(self)
        self.dest_lang.addItems(["English", "Spanish", "French", "German", "Chinese", "Japanese"])
        self.dest_lang.setCurrentText("Spanish")
        layout.addWidget(self.dest_lang)

        # # Translate button
        # self.translate_button = QPushButton("Translate", self)
        # self.translate_button.clicked.connect(self.perform_translation)
        # layout.addWidget(self.translate_button)

        # Set layout to the central widget
        central_widget.setLayout(layout)

        # Menu bar
        self.create_menu()

        # Timer for automatic translation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.perform_translation)
        self.timer.start(1000)  # 1 second interval

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

    def translate_text(self, text, src_lang, dest_lang):
        translation = self.translator.translate(text, src=src_lang, dest=dest_lang)
        return translation.text

    def perform_translation(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            self.output_text.setPlainText("")
            return
        src = self.src_lang.currentText()
        dest = self.dest_lang.currentText()
        translated_text = self.translate_text(text, src, dest)
        self.output_text.setPlainText(translated_text)