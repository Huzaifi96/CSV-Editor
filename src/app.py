import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction,QMenu, QDialog,QMessageBox
from dialog import createNewTableDialog, openFileDialog,insertHorizontalHeaderDialog
from widget import BlankTableWidget

class MainWindow(QMainWindow):
    """
    Main window class for the application.
    """
    def __init__(self):
        super().__init__()
        
        # Set the title and initial size of the window
        self.setWindowTitle("CSV-Editor")
        self.setGeometry(100, 100, 1000, 800)

        # initialize variable
        self.table_row = 0
        self.table_column = 0
        self._table_exists = False
        # initialize UI
        self.initUI()

    def initUI(self):
        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)
        
        menuBar = self.menuBar()

        # Create File Menus
        fileMenu = menuBar.addMenu('File')

        newAction = QAction('New', self)
        newAction.triggered.connect(self.open_create_new_table_dialog)

        openAction = QAction('Open..',self)
        openAction.triggered.connect(self.open_file_dialog)

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)

        # Create Edit Menus
        self.editMenu = menuBar.addMenu('Edit')
        self.insertSubMenu = QMenu('Insert',self)
        self.horizontalHeader = QAction('Insert Horizontal Header',self)
        self.horizontalHeader.setEnabled(self._table_exists)
        self.horizontalHeader.triggered.connect(self.insert_horizontal_header_dialog)

        self.insertSubMenu.addAction(self.horizontalHeader)
        self.editMenu.addMenu(self.insertSubMenu)

        # Create an instance of QTableWidget
        self.table = BlankTableWidget()
        # self.table.setColumnCount
        # Set the horizontal headers (column names)
        # self.table_widget.setHorizontalHeaderLabels(["Column1", "Column2", "Column3"])

        layout.addWidget(self.table)
    
    def _enable_action(self,enable_flag):
        
        self.horizontalHeader.setEnabled(enable_flag)

    def open_create_new_table_dialog(self):
        # create instance of createNewTableDialog
        self.createTable_window = createNewTableDialog()

        # Connect the dialog's custom signal to slot in the main window
        self.createTable_window.get_dimension.connect(self.create_new_table)

        # Show the dialog as a modal window. This will block execution until it's closed.
        self.createTable_window.exec_()

        # enable table exist flags and action menus
        self._table_exists = True
        self._enable_action(self._table_exists)

    def create_new_table(self,rows,columns):

        # This slot will be automatically called when get_dimension signal is emit
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        # update current number of rows and column in the main windows
        self.table_row = rows
        self.table_column = columns
    
    def open_file_dialog(self):

        openFile = openFileDialog()
        openFile.open_file()

    def insert_horizontal_header_dialog(self):
        dialog = insertHorizontalHeaderDialog(self.table_column)

        result = dialog.exec_()

        if result == QDialog.Accepted:
            headers = dialog.getHeaders()
            self.table.setHorizontalHeaderLabels(headers)
            QMessageBox.information(self,"Headers Entered","Successfully set headers")
        else:
            QMessageBox.information(self, "Cancelled","Header input cancelled")

# The application entry point
if __name__ == '__main__':
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    
    # Create an instance of our main window
    main_window = MainWindow()
    
    # Show the window
    main_window.show()
    
    # Start the event loop
    sys.exit(app.exec_())
