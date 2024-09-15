import sys

from PyQt5.QtWidgets import QApplication
from styles import apply_styles
from translator import TranslatorApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_styles(app)
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
