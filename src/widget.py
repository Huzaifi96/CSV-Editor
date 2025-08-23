from PyQt5.QtWidgets import QTableWidget, QMenu, QAction
from PyQt5.QtCore import Qt

class BlankTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self._init_table()

    def _init_table(self):
        # Enable a custom context menu
        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(self._show_context_menu_column)
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





