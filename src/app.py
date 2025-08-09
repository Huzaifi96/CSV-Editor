import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QAction
from dialog import createNewTableDialog

class MainWindow(QMainWindow):
    """
    Main window class for the application.
    """
    def __init__(self):
        super().__init__()
        
        # Set the title and initial size of the window
        self.setWindowTitle("CSV-Editor")
        self.setGeometry(100, 100, 500, 300)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)
        
        # Create Menus
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')

        newAction = QAction('New', self)
        newAction.triggered.connect(self.open_create_new_table_dialog)
        openAction = QAction('Open..',self)

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)

        # Create an instance of QTableWidget
        self.table_widget = QTableWidget()
        
        # Set the horizontal headers (column names)
        # self.table_widget.setHorizontalHeaderLabels(["Column1", "Column2", "Column3"])

        # Add the table to the layout
        layout.addWidget(self.table_widget)
    
    def open_create_new_table_dialog(self):
        # create instance of createNewTableDialog
        self.createTable_window = createNewTableDialog()

        # Connect the dialog's custom signal to slot in the main window
        self.createTable_window.get_dimension.connect(self.create_new_table)

        # Show the dialog as a modal window. This will block execution until it's closed.
        self.createTable_window.exec_()

    def create_new_table(self,rows,columns):

        # This slot will be automatically called when get_dimension signal is emit
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(columns)

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
