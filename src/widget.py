from PyQt5.QtWidgets import QTableWidget, QMenu, QAction,QDialog,QMessageBox
from PyQt5.QtCore import Qt
from dialog import sectionHeaderEditorDialog

class BlankTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self._init_table()

    def _init_table(self):
        # Enable a custom context menu
        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(self._show_context_menu_column)
        self.horizontalHeader().sectionDoubleClicked.connect(self._edit_section_header)
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(self._show_context_menu_row)
    
    def _show_context_menu_column(self,pos):
        # Create the column context menu
        menu = QMenu(self)
        
        insert_column_right = QAction("Insert Column Right", self)
        insert_column_left  = QAction("Insert Column Left", self)

        insert_column_right.triggered.connect(self._insert_column_right)
        insert_column_left.triggered.connect(self._insert_column_left)

        menu.addAction(insert_column_right)
        menu.addAction(insert_column_left)
        
        # Determine where to show the menu
        menu.exec_(self.viewport().mapToGlobal(pos))

    def _show_context_menu_row(self,pos):
        # Create the row context menu
        menu = QMenu(self)
        
        insert_row_above = QAction("Insert Row Above", self)
        insert_row_below = QAction("Insert Row Below", self)

        insert_row_above.triggered.connect(self._insert_row_above)
        insert_row_below.triggered.connect(self._insert_row_below)

        menu.addAction(insert_row_above)
        menu.addAction(insert_row_below)

        menu.exec_(self.viewport().mapToGlobal(pos))
    
    def _insert_column_right(self):

        self.insertColumn(self.currentColumn() + 1)

    def _insert_column_left(self):

        if self.currentColumn() == 0:
            self.insertColumn(0)
        else:
            self.insertColumn(self.currentColumn() - 1)

    def _insert_row_above(self):

        if self.currentRow() == 0:
            self.insertRow(0)
        else:
            self.insertRow(self.currentRow() - 1)

    def _insert_row_below(self):

        self.insertRow(self.currentRow() + 1)
    
    def _edit_section_header(self,section_index):
        editorDialog = sectionHeaderEditorDialog(section_index+1)
        result = editorDialog.exec_()

        if result == QDialog.Accepted:
            # QMessageBox.information
            header_name = editorDialog.getSectionHeaderName()
            self.setHorizontalHeaderItem(section_index,header_name)
    
    def _compile_data(self) -> list:
        rows = self.rowCount()
        columns = self.columnCount()
        table_matrix = []
        row_matrix = []
       
        horizontal_headers = self.get_header_list()
        table_matrix.append(horizontal_headers)

        for row_idx in range(0,rows):
            for column_idx in range(0,columns):
                cellItem = self.item(row_idx,column_idx)
                if cellItem is None:
                    row_matrix.append("")
                else:
                    row_matrix.append(cellItem.text())
            
            table_matrix.append(row_matrix)
            row_matrix = []

        return table_matrix

    def get_header_list(self)-> list:
        columns = self.columnCount()
        horizontal_headers = []
        for i in range(0,columns):
            item = self.horizontalHeaderItem(i)
            if item is None:
                horizontal_headers.append("")
            else:
                horizontal_headers.append(item.text())
        return horizontal_headers

    def exportData(self,file_path:str):
        data = self._compile_data()
        rows = self.rowCount() + 1
        columns = self.columnCount()
        row_list = []

        with open(file_path,'w') as file:
            for row_idx in range(0,rows):
                for column_idx in range(0,columns):
                    if column_idx != columns-1:
                        row_list.append(str(data[row_idx][column_idx]) + ",")
                    else:
                        row_list.append(str(data[row_idx][column_idx]) + "\n")
                rowStr = "".join(row_list)
                row_list.clear()
                file.write(rowStr)






