import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit

import buttons
import password
from ui_main import Ui_MainWindow


class GenPass(QMainWindow):  # главное окно
    def __init__(self):
        super(GenPass, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.slider_spinbox()
        self.set_password()
        self.ui.btn_visibility.clicked.connect(self.change_pass_visible)
        self.ui.btn_copy.clicked.connect(self.copy_pass)

        for btn in buttons.generate_password:
            getattr(self.ui, btn).clicked.connect(self.set_password)



    def slider_spinbox(self):
        self.ui.slider_length.valueChanged.connect(self.ui.spinbox_length.setValue)
        self.ui.spinbox_length.valueChanged.connect(self.ui.slider_length.setValue)
        self.ui.spinbox_length.valueChanged.connect(self.set_password)

    def get_characters(self):
        chars = ""

        for btn in buttons.Characters:
            if getattr(self.ui, btn.name).isChecked():
                chars += btn.value
        return chars

    def set_password(self):
        try:
            self.ui.line_password.setText(
                password.create_new(length=self.ui.spinbox_length.value(), characters=self.get_characters())
            )
        except IndexError:
            self.ui.line_password.clear()

        self.set_entropy()
        self.set_strenght()

    def get_character_numb(self):
        num = 0

        for btn in buttons.character_number.items():
            if getattr(self.ui, btn[0]).isChecked():
                num += btn[1]
        return num

    def set_entropy(self):
        length = len(self.ui.line_password.text())
        char_num = self.get_character_numb()

        self.ui.label_entropy.setText(
            f'Entropy: {password.get_entropy(length, char_num)} bit'
        )

    def set_strenght(self):
        length = len(self.ui.line_password.text())
        char_num = self.get_character_numb()

        for strenght in password.StrengthToEntropy:
            if password.get_entropy(length, char_num) >= strenght.value:
                self.ui.label_strength.setText(f"Strenght: {strenght.name}")

    def change_pass_visible(self):
        if self.ui.btn_visibility.isChecked():
            self.ui.line_password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.line_password.setEchoMode(QLineEdit.Password)

    def copy_pass(self):
        QApplication.clipboard().setText(self.ui.line_password.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GenPass()
    window.show()
    sys.exit(app.exec())
