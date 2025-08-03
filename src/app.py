import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QAction


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
        openAction = QAction('Open..',self)

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)

        # Create an instance of QTableWidget
        self.table_widget = QTableWidget()

        # Set the number of rows and columns based on the data
        self.table_widget.setRowCount(4)
        self.table_widget.setColumnCount(3)
        
        # Set the horizontal headers (column names)
        self.table_widget.setHorizontalHeaderLabels(["Column1", "Column2", "Column3"])

        # Add the table to the layout
        layout.addWidget(self.table_widget)


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
