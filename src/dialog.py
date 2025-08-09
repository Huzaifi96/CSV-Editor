from  PyQt5.QtWidgets import QLabel,QPushButton,QSpinBox,QDialog
from PyQt5.QtCore import Qt, QRect,pyqtSignal
from PyQt5.QtGui import  QFont

class createNewTableDialog(QDialog):

    # Define a custom signal that will emit two integers: rows and columns
    get_dimension = pyqtSignal(int,int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New Table")
        # self.setGeometry(0, 0, 407, 319)
        self.resize(407, 319)
        self.init_ui()
    
    def init_ui(self):
        
        font = QFont()
        font.setPointSize(14)
        self.rowLabel = QLabel("Row(s)",parent=self)
        self.rowLabel.setGeometry(QRect(80, 100, 101, 31))
        self.rowLabel.setFont(font)
        self.rowLabel.setAlignment(Qt.AlignCenter)
        self.columnLabel = QLabel("Column(s)",parent=self)
        self.columnLabel.setGeometry(QRect(90, 140, 101, 31))
        self.columnLabel.setFont(font)
        self.columnLabel.setAlignment(Qt.AlignCenter)

        self.rowSpinBox = QSpinBox(parent=self)
        self.rowSpinBox.setGeometry(QRect(200, 100, 61, 31))
        self.rowSpinBox.setMinimum(1)
        
        self.columnSpinBox = QSpinBox(parent=self)
        self.columnSpinBox.setGeometry(QRect(200, 140, 61, 31))
        self.columnSpinBox.setMinimum(1)
        self.columnSpinBox.setMaximum(100)

        self.createPushButton = QPushButton(text="Create",parent=self)
        self.createPushButton.setGeometry(QRect(40, 230, 319, 28))
        self.createPushButton.clicked.connect(self.create_button_clicked)
    
    def create_button_clicked(self):
        # Get confirmed rows and columns
        rows = self.rowSpinBox.value()
        columns = self.columnSpinBox.value()

        # Emit the signal with the confirmed values
        self.get_dimension.emit(rows,columns)
        # print(f"Rows : {rows} , Columns : {column}")

        # Close the dialog
        self.accept()

class openDialog(QDialog):
    pass
