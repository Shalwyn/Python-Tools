import deepl
from PyQt5 import QtWidgets, uic
import sys
import os

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath = os.path.join(bundle_dir, 'testwindow.ui')

        self.ui = uic.loadUi(getpath, self)
        self.ui.pushButton.clicked.connect(self.translation)


    def translation(self):
        translated = self.ui.textEdit.toPlainText()
        language = self.ui.comboBox.currentText()
        translator = deepl.Translator("c0231f19-2b40-97b7-dc2c-31b5835cc3b7:fx")
        try:
            result = translator.translate_text(translated, target_lang=language)
            result = str(result)
            self.ui.textEdit_2.clear()
            self.ui.textEdit_2.insertPlainText(result)
        except:
            print("Error")



