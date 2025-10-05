import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction,QMenu, QDialog,QMessageBox,QTableWidgetItem,QFileDialog,QToolBar
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from dialog import createNewTableDialog,insertHorizontalHeaderDialog,MessageBoxDialog
from widget import BlankTableWidget
from helper import getImgSource

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

        self.newAction = QAction('New', self)
        self.newAction.triggered.connect(self.open_create_new_table_dialog)
        
        self.openAction = QAction('Open..',self)
        self.openAction.triggered.connect(self.open_file_dialog)

        self.exportAction = QAction('Export',self)
        self.exportAction.setEnabled(self._table_exists)
        self.exportAction.triggered.connect(self.export_file_dialog)

        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.exportAction)

        # Create Edit Menus
        self.editMenu = menuBar.addMenu('Edit')
        self.insertSubMenu = QMenu('Insert',self)
        self.horizontalHeader = QAction('Insert Horizontal Header',self)
        self.horizontalHeader.setEnabled(self._table_exists)
        self.horizontalHeader.triggered.connect(self.insert_horizontal_header_dialog)

        self.insertSubMenu.addAction(self.horizontalHeader)
        self.editMenu.addMenu(self.insertSubMenu)

        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.setIconSize(QSize(50, 50))

        self.import_toolbar = QAction(QIcon(getImgSource("import.png")), "Import File", self)
        self.import_toolbar.triggered.connect(self.open_file_dialog)

        self.export_toolbar = QAction(QIcon(getImgSource("export.png")), "Export File", self)
        self.export_toolbar.setEnabled(self._table_exists)
        self.export_toolbar.triggered.connect(self.export_file_dialog)

        self.create_toolbar = QAction(QIcon(getImgSource("add-table.png")), "Create new table", self)
        self.create_toolbar.triggered.connect(self.open_create_new_table_dialog)

        self.delete_toolbar = QAction(QIcon(getImgSource("delete-table.png")), "Delete table", self)
        self.delete_toolbar.setEnabled(self._table_exists)

        self.save_toolbar = QAction(QIcon(getImgSource("save_icon.png")), "Save", self)
        self.save_toolbar.setEnabled(self._table_exists)

        toolbar.addAction(self.create_toolbar)
        toolbar.addAction(self.delete_toolbar)
        toolbar.addAction(self.save_toolbar)
        toolbar.addAction(self.import_toolbar)
        toolbar.addAction(self.export_toolbar)
        toolbar.addSeparator()
        # Create an instance of QTableWidget
        self.table = BlankTableWidget()

        layout.addWidget(self.table)
    
    def enable_action(self,enable_flag):
        
        self.horizontalHeader.setEnabled(enable_flag)
        self.exportAction.setEnabled(enable_flag)
        self.export_toolbar.setEnabled(enable_flag)
        self.delete_toolbar.setEnabled(enable_flag)
        self.save_toolbar.setEnabled(enable_flag)

    def open_create_new_table_dialog(self):
        # create instance of createNewTableDialog
        self.createTable_window = createNewTableDialog()

        # Connect the dialog's custom signal to slot in the main window
        self.createTable_window.get_dimension.connect(self.create_new_table)

        # Show the dialog as a modal window. This will block execution until it's closed.
        response = self.createTable_window.exec_()

        if response == QDialog.Accepted:
        # enable table exist flags and action menus
            self._table_exists = True
            self.enable_action(self._table_exists)

    def create_new_table(self,rows,columns):

        # This slot will be automatically called when get_dimension signal is emit
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        # update current number of rows and column in the main windows
        self.table_row = rows
        self.table_column = columns
    
    def open_file_dialog(self):

        # filename = openFileDialog.open_file()
        filename, _ = QFileDialog.getOpenFileName(
                                                  caption='Open File',
                                                  directory='',
                                                  filter='CSV Files (*.csv);;All Files (*)'
                                                 )
        if ".csv" in filename:
            self.populate_table(filename)
        elif filename == '':
            pass
        else:
            MessageBoxDialog.show_error("Error: Incorrect File Type","The file you selected is not a .csv file !")
    
    def export_file_dialog(self):
        file_path, _ = QFileDialog.getSaveFileName(
                                                    self,
                                                    caption="Export Data",
                                                    directory="Untitled.csv",  # Default filename
                                                    filter="CSV Files (*.csv);;All Files (*)"  # File filter
                                                  )
        if file_path != '':
            self.export_data(file_path)

    def insert_horizontal_header_dialog(self):
        dialog = insertHorizontalHeaderDialog(self.table_column)

        result = dialog.exec_()

        if result == QDialog.Accepted:
            headers = dialog.getHeaders()
            self.table.setHorizontalHeaderLabels(headers)
            QMessageBox.information(self,"Headers Entered","Successfully set headers")
        else:
            QMessageBox.information(self, "Cancelled","Header input cancelled")
    
    def populate_table(self,filename):

        try:
            data = pd.read_csv(filename)
        except pd.errors.EmptyDataError:
            MessageBoxDialog.show_error("Error: Empty Data","The file is empty or invalid !")
            return
            
        rows,columns = data.shape

        if rows == 0:
            table_headings = list(data.columns)
            self.set_row_column_table(rows+1,columns)
            self.table.setHorizontalHeaderLabels(table_headings)
        else:
            table_headings = list(data.columns)
            self.set_row_column_table(rows,columns)
            self.table.setHorizontalHeaderLabels(table_headings)

            for row_idx in range (0,rows):
                for column_idx in range(0,columns):
                    value = data.iat[row_idx,column_idx]
                    if pd.isna(value):
                        # handle NaN value
                        display_value  = " "
                    else:
                        display_value  = str(value)

                    item = QTableWidgetItem(display_value)
                    self.table.setItem(row_idx,column_idx,item)

    def set_row_column_table(self,row_count=0,column_count=0):
        if row_count != 0:
            self.table.setRowCount(row_count)
            self.table_row = row_count
        if row_count != 0:
            self.table.setColumnCount(column_count)
            self.table_column = column_count
    
    def export_data(self,filepath:str):
        self.table.exportData(filepath)

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
