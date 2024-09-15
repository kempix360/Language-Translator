from PyQt5.QtWidgets import QApplication


def apply_styles(app: QApplication):
    # Global styles
    app.setStyleSheet("""
        * {
            font-family: 'Poppins';
            font-weight: bold;
        }
        QLabel {
            font-size: 16px;
        }
        
        QTextEdit {
            font-weight: normal;
            font-size: 14px;
            padding: 10px;
        }
        
        QComboBox {
            font-size: 14px;
            padding: 5px;
        }
        
        QCheckBox {
            font-size: 14px;
            padding: 5px;
        }
        
        QMenuBar {
            background-color: #007bff;
            color: white;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 10px;
        }
        
        QMenuBar::item:selected {
            background-color: #0056b3;
        }
        
        QMenu {
            background-color: #007bff;
            color: white;
            border: 1px solid #0056b3;
        }
        
        QMenu::item:selected {
            background-color: #0056b3;
        }
        
        QMainWindow {
            background-color: #f0f0f0;
        }
    """)
