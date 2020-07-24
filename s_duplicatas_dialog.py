from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import calendar

import _sqlite_handler
from _personalizedtableitem import personalizedTableWidgetItem
import _config

import Ui_u_duplicatas_dialog


class Main(QtWidgets.QDialog, Ui_u_duplicatas_dialog.Ui_Dialog):
    def __init__(self, nf_chave, main_database):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.nf_chave = nf_chave
        self.main_database = main_database
        self.config = _config.config()
        
        self.update_table()
        
        self.tableWidget_duplicatas.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_duplicatas.customContextMenuRequested.connect(self.tablewidget_context_menu)
                
        self.pushButton_cancelar.clicked.connect(lambda: self.close())
        self.pushButton_ok.clicked.connect(self.button_ok_clicked)
        
    def button_ok_clicked(self):
        sql = (f"""
                SELECT FAID
                FROM FATURAS
                WHERE FNFEchNFe = \'{self.nf_chave}\'
                """)
        ids = self.main_database.cur.execute(sql).fetchall()
        ids = [x[0] for x in ids]
        
        if self.tableWidget_duplicatas.rowCount() > 0:

            
            data = {}
            for row in range(self.tableWidget_duplicatas.rowCount()):
                id = int(self.tableWidget_duplicatas.item(row, 0).text())
                data[id] = []
                
                data[id].append(self.tableWidget_duplicatas.item(row, 1).text())
                
                try:
                    data[id].append(datetime.strptime(self.tableWidget_duplicatas.cellWidget(row, 2).text(), "%d-%m-%Y"))
                except:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText(f"Data de pagamento da coluna {row + 1} em branco")
                    msg.exec_()
                    return
                
                try:
                    data[id].append(float(self.tableWidget_duplicatas.cellWidget(row, 3).text()))
                except:
                    data[id].append("NULL")
                    
                data[id].append(self.tableWidget_duplicatas.cellWidget(row, 4).text())
                
                widget = self.tableWidget_duplicatas.cellWidget(row, 5)
                if widget.findChild(QtWidgets.QCheckBox).isChecked():
                    data[id].append(1)
                else:
                    data[id].append(0)
                
                data_obs = self.tableWidget_duplicatas.cellWidget(row, 6).text()
                if len(data_obs) > 8:
                    data[id].append(datetime.strptime(data_obs, "%d-%m-%Y"))
                else:
                    data[id].append("NULL")
            
            for id, row_data in data.items():
                if id in ids:
                    sql = (f"""
                           UPDATE FATURAS
                           SET nDup =  \'{row_data[0]}\', dVenc = \'{row_data[1]}\', vDup = \'{row_data[2]}\', FObs = \'{row_data[3]}\', FobsFlag = \'{row_data[4]}\', Fdatalemb = \'{row_data[5]}\'
                           WHERE FAID = \'{id}\'
                           """)
                    self.main_database.cur.execute(sql)
                else:
                    sql = (f"""
                           INSERT INTO FATURAS (nDup, dVenc, vDup, FObs, FobsFlag, Fdatalemb, FNFEchNFe)
                           VALUES (\'{row_data[0]}\', \'{row_data[1]}\', \'{row_data[2]}\', \'{row_data[3]}\', \'{row_data[4]}\',  \'{row_data[5]}\', \'{self.nf_chave}\')
                           """)
                    self.main_database.cur.execute(sql)
                    
            for id in ids:
                if id not in data.keys():
                    sql = (f"""
                           DELETE FROM FATURAS
                           WHERE FAID = \'{id}\'
                           """)
                    self.main_database.cur.execute(sql)
                    
        else:
            for id in ids:
                sql = (f"""
                    DELETE FROM FATURAS
                    WHERE FAID = \'{id}\'
                    """)
                self.main_database.cur.execute(sql)
                
        self.main_database.con.commit()
        self.close()
            
            
                
            
    def tablewidget_context_menu(self):
        
        context_menu = QtWidgets.QMenu()
        
        context_menu.addAction("Adicionar Duplicata")
        context_menu.addAction("Remover Ultima Duplicata")
        
        action = context_menu.exec(QtGui.QCursor.pos())
        
        if action != None:
            if action.text() == "Adicionar Duplicata":
                self.adicionar_duplicata()
            if action.text() == "Remover Ultima Duplicata":
                self.remover_duplicata()
            
    def adicionar_duplicata(self):
        sql = (f"""
               SELECT FAID
               FROM FATURAS
               ORDER BY FAID DESC
               LIMIT 1
               """)
        last_id = self.main_database.cur.execute(sql).fetchall()[0][0]
        num_rows = self.tableWidget_duplicatas.rowCount()
        
        self.tableWidget_duplicatas.setSortingEnabled(False)
        self.tableWidget_duplicatas.insertRow(num_rows)
        #ROW 0
        if num_rows > 0:
            last_table_id = int(self.tableWidget_duplicatas.item(num_rows - 1, 0).text())
            if last_table_id >= last_id:
                last_id = last_table_id + 1
        fat_id_item = personalizedTableWidgetItem(str(last_id), last_id)
        fat_id_item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget_duplicatas.setItem(num_rows, 0, fat_id_item)
        #ROW 1
        if num_rows > 0:
            num_fat = int(self.tableWidget_duplicatas.item(num_rows - 1, 1).text()) + 1
        else:
            num_fat = 1
        num_fat_item = personalizedTableWidgetItem(str(num_fat), num_fat)
        num_fat_item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget_duplicatas.setItem(num_rows, 1, num_fat_item)
        #ROW 2
        data_pag_edit = QtWidgets.QLineEdit(self.tableWidget_duplicatas)
        data_pag_edit.setInputMask("00-00-0000")
        data_pag_edit.editingFinished.connect(lambda: self.on_date_changed(data_pag_edit))
        self.tableWidget_duplicatas.setCellWidget(num_rows, 2, data_pag_edit)
        #ROW 3
        valor_edit = QtWidgets.QLineEdit(self.tableWidget_duplicatas)
        valor_edit.textChanged.connect(self.on_value_changed)
        self.tableWidget_duplicatas.setCellWidget(num_rows, 3, valor_edit)
        #ROW 4
        obs_edit = QtWidgets.QLineEdit(self.tableWidget_duplicatas)
        obs_edit.textChanged.connect(self.on_obs_change)
        self.tableWidget_duplicatas.setCellWidget(num_rows, 4, obs_edit)
        #ROW 5
        checkbox_widget = QtWidgets.QWidget()
        checkbox = QtWidgets.QCheckBox()
        aligment_box = QtWidgets.QHBoxLayout(checkbox_widget)
        aligment_box.addWidget(checkbox)
        aligment_box.setAlignment(QtCore.Qt.AlignCenter)
        aligment_box.setContentsMargins(0,0,0,0)
        self.tableWidget_duplicatas.setCellWidget(num_rows, 5, checkbox_widget)
        #ROW 6
        data_obs_edit = QtWidgets.QLineEdit(self.tableWidget_duplicatas)
        data_obs_edit.setInputMask("00-00-0000")
        data_obs_edit.editingFinished.connect(lambda: self.on_date_changed(data_obs_edit))
        self.tableWidget_duplicatas.setCellWidget(num_rows, 6, data_obs_edit)
        
        self.tableWidget_duplicatas.scrollToBottom()
        
    def remover_duplicata(self):
        num_rows = self.tableWidget_duplicatas.rowCount()
        
        self.tableWidget_duplicatas.removeRow(num_rows - 1)
        self.tableWidget_duplicatas.scrollToBottom()
        
    def on_obs_change(self):
        pass
            
    
    def on_value_changed(self):
        row = self.tableWidget_duplicatas.currentRow()
        column = self.tableWidget_duplicatas.currentColumn()
        
        value = self.tableWidget_duplicatas.cellWidget(row, column).text()
        
        if value != "":
            if value[-1] == "," or value[-1] == ".":
                if "." in list(value[:-1]):
                    value = value[:-1]
                else:
                    value = value[:-1] + "."
            else: 
                if not value[-1].isnumeric():
                    value = value[:-1]
                
        self.tableWidget_duplicatas.cellWidget(row, column).setText(value)
                
    def on_date_changed(self, timeedit):
        
        def change_char_at_indexes(text, index_char):
            if bool(text):
                chars = list(text)
                for index, char in index_char.items():
                    chars[index] = char
                return "".join(chars)
        
        row = self.tableWidget_duplicatas.currentRow()
        column = self.tableWidget_duplicatas.currentColumn()
        text = self.tableWidget_duplicatas.cellWidget(row, column).text()
        
        if len(text) in [8,10]:
            #change the month
            if int(text[3:5]) > 12:
                if int(text[3:5]) == 0:
                    text = change_char_at_indexes(text, {3:"0", 4:"1"})
                else:
                    text = change_char_at_indexes(text, {3:"1", 4:"2"})
            #Get the year and days in month
            if len(text) == 8:
                year = int(datetime.strptime(text[6:8], "%y").strftime("%Y"))
                day_in_month = calendar.monthrange(year, int(text[3:5]))[1]
                text = text[:6] + str(year)
            elif len(text) == 10:
                year = int(text[6:10])
                day_in_month = calendar.monthrange(year, int(text[3:5]))[1]
                text = text[:6] + str(year)
            #if days bigger than day in month
            if int(text[0:2]) == 0:
                text = change_char_at_indexes(text, {0: "0", 1: "1"})
            if int(text[0:2]) > day_in_month:
                days_in_month = [int(x) for x in str(day_in_month)]
                text = change_char_at_indexes(text, {0: str(days_in_month[0]), 1: str(days_in_month[1])})
            
            self.tableWidget_duplicatas.cellWidget(row, column).setText(text)
        else:
            text = ""
            self.tableWidget_duplicatas.cellWidget(row, column).setText(text)
            
    def update_table(self):
        self.universal_table_builder(self.tableWidget_duplicatas,
                                self.get_duplicatas_data(),
                                ["FAID", "nDup", "dVenc", "vDup", "FObs", "FobsFlag", "Fdatalemb"],
                                ["FATURAS"])

    def get_duplicatas_data(self):
        tables_to_select = ["FAID", "nDup", "dVenc", "vDup", "FObs", "FobsFlag", "Fdatalemb"]
        sql = (f"""
                SELECT {",".join(tables_to_select)}
                FROM FATURAS
                WHERE FNFEchNFe = \'{self.nf_chave}\'
                """)
        return self.main_database.cur.execute(sql).fetchall()
        
        
    def universal_table_builder(self, Qtable_, data_, columns_, table_names_):
        def qtable_date_converter(date_):
            return datetime.strptime(date_, "%Y-%m-%d %H:%M:%S")

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
                        if column == 3:
                            value_line_edit = QtWidgets.QLineEdit(Qtable_)
                            value_line_edit.setText(str(data_[row][column]))
                            Qtable_.setCellWidget(row, column, value_line_edit)
                            Qtable_.cellWidget(row, column).textChanged.connect(self.on_value_changed)
                            
                        elif column == 5:
                            checkbox_widget = QtWidgets.QWidget()
                            checkbox = QtWidgets.QCheckBox()
                            if data_[row][column] == 1:
                                checkbox.setChecked(True)
                            aligment_box = QtWidgets.QHBoxLayout(checkbox_widget)
                            aligment_box.addWidget(checkbox)
                            aligment_box.setAlignment(QtCore.Qt.AlignCenter)
                            aligment_box.setContentsMargins(0,0,0,0)
                            Qtable_.setCellWidget(row, column, checkbox_widget)
                            
                            
                                                        
                        else:
                            newitem = personalizedTableWidgetItem(
                                str(data_[row][column]), data_[row][column])
                            if column in [0, 1]:
                                newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                            Qtable_.setItem(row, column, newitem)

                    elif column_type == "TIMESTAMP":
                        try:
                            timeStamp = qtable_date_converter(data_[row][column]).strftime("%d-%m-%Y")
                        except:
                            timeStamp = ""
                                                        
                        timeedit = QtWidgets.QLineEdit(Qtable_)
                        
                        # if column == 6:
                        #     timeedit.setEnabled(True)
                        timeedit.setInputMask("00-00-0000")
                        timeedit.setText(timeStamp)
                        Qtable_.setCellWidget(row, column, timeedit)
                        Qtable_.cellWidget(row, column).editingFinished.connect(lambda: self.on_date_changed(timeedit))

                    else:
                        if column == 4:
                            newitem = QtWidgets.QLineEdit(Qtable_)
                            newitem.setText(data_[row][column])
                            Qtable_.setCellWidget(row, column, newitem)
                            Qtable_.cellWidget(row, column).textChanged.connect(self.on_obs_change)
                        else:
                            newitem = QtWidgets.QTableWidgetItem((data_[row][column]))
                            Qtable_.setItem(row, column, newitem)
                            

        Qtable_.resizeColumnsToContents()
        
        #paint the table
        sql = (f"""
               SELECT FAID, FLAGPAGO
               FROM FATURAS
               WHERE FNFEchNFe = \'{self.nf_chave}\'
               """)
        id_flag = self.main_database.cur.execute(sql).fetchall()
        ids = [x[0] for x in id_flag if x[1] == 1]
        for row in range(self.tableWidget_duplicatas.rowCount()):
            if int(self.tableWidget_duplicatas.item(row, 0).text()) in ids:
                for column in range(self.tableWidget_duplicatas.columnCount()):
                    if self.tableWidget_duplicatas.item(row, column) != None:
                        self.tableWidget_duplicatas.item(row, column).setBackground(QtGui.QColor(82,191,144))