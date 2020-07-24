from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
from datetime import datetime

import _extractor
import _sqlite_handler
import _config
from _personalizedtableitem import personalizedTableWidgetItem
import s_columns_dialog

import Ui_u_avisos_dialog

class Main(QtWidgets.QDialog,  Ui_u_avisos_dialog.Ui_Dialog):
    def __init__(self, data_base):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.main_database = data_base
        self.config = _config.config()
        
        self.build_duplicatas_vencidas_table()
        self.build_duplicatas_avisos_table()
        
        self.build_nf_venc_proximo()
        self.build_nf_obs_proximo()
        
        duplicatas_vencidas_corner = self.tableWidget_duplicatas_vencidas.findChild(QtWidgets.QAbstractButton)
        duplicatas_vencidas_corner.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        duplicatas_vencidas_corner.customContextMenuRequested.connect(lambda: self.corner_button_function(
            ["FATURAS", "NFE", "FORNECEDORES", "EMPRESA"], "avisos_duplicatas_venc_columns"))
        
        duplicatas_com_alerta_corner = self.tableWidget_duplicata_com_alerta.findChild(QtWidgets.QAbstractButton)
        duplicatas_com_alerta_corner.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        duplicatas_com_alerta_corner.customContextMenuRequested.connect(lambda: self.corner_button_function(
            ["FATURAS", "NFE", "FORNECEDORES", "EMPRESA"], "avisos_duplicata_obs_columns"))
        
        notas_fiscais_com_vencimento_corner = self.tableWidget_notas_fiscais_com_vencimento.findChild(QtWidgets.QAbstractButton)
        notas_fiscais_com_vencimento_corner.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        notas_fiscais_com_vencimento_corner.customContextMenuRequested.connect(lambda: self.corner_button_function(
            ["NFE", "FORNECEDORES", "EMPRESA"], "avisos_nf_venc_columns"))
        
        notas_fiscais_com_alertas_corner = self.tableWidget_notas_fiscais_com_alertas.findChild(QtWidgets.QAbstractButton)
        notas_fiscais_com_alertas_corner.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        notas_fiscais_com_alertas_corner.customContextMenuRequested.connect(lambda: self.corner_button_function(
            ["NFE", "FORNECEDORES", "EMPRESA"], "avisos_nf_obs_columns"))

    def corner_button_function(self, columns_, database_name_):
        self.coluns_dialog = s_columns_dialog.Main(
            self.main_database.get_columns_from_multiple_tables(columns_), database_name_)
        self.coluns_dialog.exec_()
        
        self.build_duplicatas_vencidas_table()
        self.build_duplicatas_avisos_table()
        
        self.build_nf_venc_proximo()
        self.build_nf_obs_proximo()

        
    def build_duplicatas_vencidas_table(self):
        sql = (f"""
               SELECT {",".join(self.config.get_config("avisos_duplicatas_venc_columns"))}
               FROM FATURAS
               LEFT JOIN NFE ON NFE.chNFe = FATURAS.FNFEchNFe
               LEFT JOIN FORNECEDORES ON FORNECEDORES.FCNPJCPF = NFE.FORNECEDORESCNPJ
               LEFT JOIN EMPRESA ON EMPRESA.ECNPJCPF = NFE.EMPRESACNPJ
               WHERE dVenc < date('now')
                AND FLAGPAGO == 0
               """)
        
        faturas_vencidas = self.main_database.cur.execute(sql).fetchall()
        
        self.universal_table_builder(
            self.tableWidget_duplicatas_vencidas,
            faturas_vencidas,
            self.config.get_config("avisos_duplicatas_venc_columns"),
            ["FATURAS", "NFE", "FORNECEDORES", "EMPRESA"]
        )
        
    def build_duplicatas_avisos_table(self):
        sql = (f"""
               SELECT {",".join(self.config.get_config("avisos_duplicata_obs_columns"))}
               FROM FATURAS
               LEFT JOIN NFE ON NFE.chNFe = FATURAS.FNFEchNFe
               LEFT JOIN FORNECEDORES ON FORNECEDORES.FCNPJCPF = NFE.FORNECEDORESCNPJ
               LEFT JOIN EMPRESA ON EMPRESA.ECNPJCPF = NFE.EMPRESACNPJ
               WHERE length(FObs) > 0
               AND dVenc > date('now')
               AND FobsFlag == 0
               AND FLAGPAGO == 0
               """)
        
        faturas_obs = self.main_database.cur.execute(sql).fetchall()
        
        self.universal_table_builder(
            self.tableWidget_duplicata_com_alerta,
            faturas_obs,
            self.config.get_config("avisos_duplicata_obs_columns"),
            ["FATURAS", "NFE", "FORNECEDORES", "EMPRESA"]
        )
        
    def build_nf_venc_proximo(self):
        sql = (f"""
               SELECT {",".join(self.config.get_config("avisos_nf_venc_columns"))}
               FROM NFE
               LEFT JOIN FORNECEDORES ON FORNECEDORES.FCNPJCPF = NFE.FORNECEDORESCNPJ
               LEFT JOIN EMPRESA ON EMPRESA.ECNPJCPF = NFE.EMPRESACNPJ
               WHERE PRIMEIROVENCIMENTO IS NOT NULL
               AND PRIMEIROVENCIMENTO < date('now', '+7 day')
               AND FLAGRECEBIDO == 0
               """)
        
        nf_venc = self.main_database.cur.execute(sql).fetchall()
        
        self.universal_table_builder(
            self.tableWidget_notas_fiscais_com_vencimento,
            nf_venc,
            self.config.get_config("avisos_nf_venc_columns"),
            ["NFE", "FORNECEDORES", "EMPRESA"]
        )
        
    def build_nf_obs_proximo(self):
        sql = (f"""
               SELECT {",".join(self.config.get_config("avisos_nf_obs_columns"))}
               FROM NFE
               LEFT JOIN FORNECEDORES ON FORNECEDORES.FCNPJCPF = NFE.FORNECEDORESCNPJ
               LEFT JOIN EMPRESA ON EMPRESA.ECNPJCPF = NFE.EMPRESACNPJ
               WHERE length(NFobs) > 0
               AND NFobsdate < date('now', '+7 day')
               AND NFobsflag == 0
               """)
        
        nf_obs = self.main_database.cur.execute(sql).fetchall()
        
        self.universal_table_builder(
            self.tableWidget_notas_fiscais_com_alertas,
            nf_obs,
            self.config.get_config("avisos_nf_obs_columns"),
            ["NFE", "FORNECEDORES", "EMPRESA"]
        )
        

    def universal_table_builder(self, Qtable_, data_, columns_, table_names_):
        def save_table_sort(logical_index_):
            self.config.change_config({Qtable_.objectName(): [logical_index_, Qtable_.horizontalHeader().sortIndicatorOrder()]})
            
        def qtable_date_converter(date_):
            date = date_.split(".")[0]
            return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
    
        def date_time_to_int(date_):
            date = date_.split(".")[0]
            return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp()

        #Make it non editable
        Qtable_.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        header_names = self.config.translate_column_names(columns_)
        Qtable_.setColumnCount(len(columns_))
        Qtable_.setHorizontalHeaderLabels(header_names)

        Qtable_.setRowCount(len(data_))
        
        headers = Qtable_.horizontalHeader()
        headers.sectionClicked.connect(save_table_sort)

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
                        newitem = personalizedTableWidgetItem(
                            str(data_[row][column]), data_[row][column])
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
        
        sorting_config = self.config.get_config(Qtable_.objectName())
        if sorting_config[1] == 0:
            Qtable_.sortByColumn(sorting_config[0], QtCore.Qt.AscendingOrder)
        else:
            Qtable_.sortByColumn(sorting_config[0], QtCore.Qt.DescendingOrder)
        Qtable_.setSortingEnabled(True)