from  PyQt5.QtWidgets import QLabel,QPushButton,QSpinBox,QDialog,QFileDialog,QVBoxLayout,QFormLayout,QLineEdit, QDialogButtonBox
from PyQt5.QtCore import Qt, QRect,pyqtSignal
from PyQt5.QtGui import  QFont

class createNewTableDialog(QDialog):

    # Define a custom signal that will emit two integers: rows and columns
    get_dimension = pyqtSignal(int,int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New Table")
        # self.setGeometry(0, 0, 407, 319)
        self.resize(280, 237)
        self.initUI()
    
    def initUI(self):
        
        font = QFont()
        font.setPointSize(12)

        self.rowLabel = QLabel("Row(s)",parent=self)
        self.rowLabel.setGeometry(QRect(40, 60, 101, 31))
        self.rowLabel.setFont(font)
        self.rowLabel.setAlignment(Qt.AlignCenter)
        self.columnLabel = QLabel("Column(s)",parent=self)
        self.columnLabel.setGeometry(QRect(50, 100, 101, 31))
        self.columnLabel.setFont(font)
        self.columnLabel.setAlignment(Qt.AlignCenter)

        spinBoxfont = QFont()
        spinBoxfont.setPointSize(11)

        self.rowSpinBox = QSpinBox(parent=self)
        self.rowSpinBox.setGeometry(QRect(150, 60, 61, 31))
        self.rowSpinBox.setFont(spinBoxfont)
        self.rowSpinBox.setMinimum(1)
        self.rowSpinBox.setMaximum(100)

        self.columnSpinBox = QSpinBox(parent=self)
        self.columnSpinBox.setGeometry(QRect(150, 100, 61, 31))
        self.columnSpinBox.setFont(spinBoxfont)
        self.columnSpinBox.setMinimum(1)
        self.columnSpinBox.setMaximum(100)

        self.createPushButton = QPushButton(text="Create",parent=self)
        self.createPushButton.setGeometry(QRect(50, 170, 181, 28))
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

class openFileDialog(QFileDialog):

    def __init__(self):
        super().__init__()
    
    def open_file(self):
        filename, _ = self.getOpenFileName(parent=self,
                                           caption='Open File',
                                           directory='',
                                           filter='Text Files (*.txt);;All Files (*)')
        if filename:
            try:
                print(f"The file selected is {filename}")
            except Exception as e:
                print(f"Error opening file: {e}")

class insertHorizontalHeaderDialog(QDialog):

    def __init__(self,num_colums):
        super().__init__()
        self.setWindowTitle("Insert Horizontal Header")
        self.num_colums = num_colums
        self.header_inputs = []
        self.initUI()
    
    def initUI(self):
        dialog_layout = QVBoxLayout(self)

        form_layout = QFormLayout(self)
        form_layout.setContentsMargins(20,20,20,20)

        for i in range(self.num_colums):
            textLabel = QLabel(f" Column {i} Header : ")
            lineEdit = QLineEdit()
            self.header_inputs.append(lineEdit)
            form_layout.addRow(textLabel,lineEdit)

        dialog_layout.addLayout(form_layout)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        dialog_layout.addWidget(self.buttonBox)
        self.setLayout(dialog_layout)
        self.setMinimumWidth(350)

    def getHeaders(self) -> list:

        return [input.text().strip() for input in self.header_inputs]

