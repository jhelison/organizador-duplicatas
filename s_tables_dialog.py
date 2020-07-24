from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime

import Ui_u_tabelas_dialog
import _sqlite_handler
import _config
import s_columns_dialog

from _personalizedtableitem import personalizedTableWidgetItem


class Main(QtWidgets.QDialog, Ui_u_tabelas_dialog.Ui_Dialog):
    def __init__(self, main_database, table_name):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.table_name = table_name
        self.main_database = main_database
        self.config = _config.config()
        
        if table_name == "FORNECEDORES":
            self.colunas = "fornecedores_table_colunas"
        elif table_name == "EMPRESA":
            self.colunas = "empresas_table_colunas"
        elif table_name == "TRANSPORTADORA":
            self.colunas = "transportadoras_table_colunas"
        elif table_name == "PRODUTO":
            self.colunas = "produtos_table_colunas"
        
        self.update_table()
    
        tableWidget_corner = self.tableWidget.findChild(QtWidgets.QAbstractButton)
        tableWidget_corner.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tableWidget_corner.customContextMenuRequested.connect(lambda: self.corner_button_function(
            [self.table_name], self.colunas))
        
        self.populate_combobox_filtro(self.comboBox_lista_tabelas, self.colunas)
        
        self.lineEdit_filter_text.textChanged.connect(lambda: self.table_widget_filter(self.tableWidget))
        self.comboBox_lista_tabelas.currentIndexChanged.connect(lambda: self.table_widget_filter(self.tableWidget))
        
        
    def populate_combobox_filtro(self, Qcombobox_, config_name_):
        columns = self.config.get_config(config_name_)

        Qcombobox_.clear()
        Qcombobox_.addItem("Tudo")

        translated_columns = self.config.translate_column_names(columns)
        for column in translated_columns:
            Qcombobox_.addItem(column)
            
    def table_widget_filter(self, Qtable_):

        text_filter_column = self.comboBox_lista_tabelas.currentText()

        for index in range(Qtable_.columnCount()):
            if text_filter_column != "Tudo":
                if Qtable_.horizontalHeaderItem(index).text() == text_filter_column:
                    text_filter_column = index

        filter_text = self.lineEdit_filter_text.text().split(";")

        #SET THE ROW VISIBILITY
        for row in range(Qtable_.rowCount()):
            Qtable_.showRow(row)

            show_row = True

            if show_row:
                if text_filter_column != "":
                    if text_filter_column == "Tudo":
                        show_row = False
                        for column_index in range(Qtable_.columnCount()):
                            for text in filter_text:
                                if text.upper() in Qtable_.item(row, column_index).text().upper():
                                    show_row = True
                                    break
                    else:
                        for text in filter_text:
                            if text.upper() not in Qtable_.item(row, text_filter_column).text().upper():
                                show_row = False
            if not show_row:
                Qtable_.hideRow(row)
        
        
    def corner_button_function(self, columns_, database_name_):
        self.coluns_dialog = s_columns_dialog.Main(
            self.main_database.get_columns_from_multiple_tables(columns_), database_name_)
        self.coluns_dialog.exec_()
        self.update_table()
            
    
    def update_table(self):
        sql = (f"""
               SELECT {",".join(self.config.get_config(self.colunas))}
               FROM {self.table_name}
               """)
        data = self.main_database.cur.execute(sql).fetchall()
        
        self.universal_table_builder(
            self.tableWidget,
            data,
            self.config.get_config(self.colunas),
            [self.table_name]
        )
        

    def universal_table_builder(self, Qtable_, data_, columns_, table_names_):
        def qtable_date_converter(date_):
            return datetime.strptime(date_, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
    
        def date_time_to_int(date_):
            return datetime.strptime(date_, "%Y-%m-%d %H:%M:%S").timestamp()

        #Make it non editable
        Qtable_.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        header_names = self.config.translate_column_names(columns_)
        Qtable_.setColumnCount(len(columns_))
        Qtable_.setHorizontalHeaderLabels(header_names)

        Qtable_.setRowCount(len(data_))

        #Setup colors
        Qtable_.setAlternatingRowColors(True)
        qtable_palette = QtGui.QPalette()
        if self.config.get_config("tema") == "Fusion Dark":
            qtable_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        else:
            qtable_palette.setColor(
                QtGui.QPalette.AlternateBase, QtGui.QColor(229, 230, 235))
        Qtable_.setPalette(qtable_palette)

        Qtable_.setSortingEnabled(False)

        #Fill the data
        if len(data_) != 0:

            for column in range(len(columns_)):

                # column_type = self.main_database.get_column_type_name(table_names_, columns_[column])
                column_type = self.main_database.get_type_from_multiple_tables(
                    table_names_, columns_[column])
                
                for row in range(len(data_)):

                    if column_type == "INTEGER" or column_type == "FLOAT":
                        if data_[row][column] != None:
                            newitem = personalizedTableWidgetItem(
                                str(data_[row][column]), data_[row][column])
                            Qtable_.setItem(row, column, newitem)
                        else:
                            newitem = personalizedTableWidgetItem("", 0)
                            Qtable_.setItem(row, column, newitem)

                    elif column_type == "TIMESTAMP":
                        if data_[row][column] != None:
                            TIMESTAMP = data_[row][column]
                            newitem = personalizedTableWidgetItem(qtable_date_converter(
                                TIMESTAMP), date_time_to_int(TIMESTAMP))
                            Qtable_.setItem(row, column, newitem)
                        else:
                            newitem = personalizedTableWidgetItem("", 0)
                            Qtable_.setItem(row, column, newitem)

                    else:
                        newitem = QtWidgets.QTableWidgetItem((data_[row][column]))
                        Qtable_.setItem(row, column, newitem)

        Qtable_.resizeColumnsToContents()

        Qtable_.setSortingEnabled(True)