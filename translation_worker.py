from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class WorkerSignals(QObject):
    result = pyqtSignal(str)  # Signal for successful translation
    error = pyqtSignal(str)  # Signal for translation errors


class TranslationWorker(QRunnable):
    def __init__(self, text, src_lang, dest_lang, translator):
        super().__init__()
        self.text = text
        self.src_lang = src_lang
        self.dest_lang = dest_lang
        self.translator = translator
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            translated_text = self.translator.translate(self.text, src=self.src_lang, dest=self.dest_lang).text
            self.signals.result.emit(translated_text)
        except Exception as e:
            self.signals.error.emit(f"Translation error: {e}")
