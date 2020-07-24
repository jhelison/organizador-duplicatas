import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

import os
import sys
from datetime import datetime, date, timedelta
import calendar
import pyperclip

import _sqlite_handler
import _config
from _personalizedtableitem import personalizedTableWidgetItem

import Ui_u_MainWindowUI
import s_carregamento
import s_columns_dialog
import s_detalhes_dialog
import s_duplicatas_dialog
import s_tables_dialog
import s_avisos_dialog


class Main(QtWidgets.QMainWindow, Ui_u_MainWindowUI.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        #Get config database
        self.config = _config.config()
        
        #Set the SQL database
        self.main_database = _sqlite_handler.new_sql_connection(self.config.get_config("databasepath"))

        #Get the tables
        self.update_tables_NFE()
        self.update_tables_duplicatas()
  
        #Implement dialog system
        self.actionSelecionar_pasta_com_XML.triggered.connect(self.action_selecionar_pasta_xml)
        self.actionAtualizar_banco_de_dados.triggered.connect(self.action_actionAtualizar_banco_de_dados)
        self.actionEscolher_arquivo_do_banco_de_dados.triggered.connect(self.action_escolher_pasta_do_banco_dados)
        self.actionAtualizar_Tabelas.triggered.connect(self.action_atualizar_tabelas)
        
        #Implement the themes on actions
        self.actionFusion_Dark.triggered.connect(self.action_theme_fusion_dark)
        self.actionFusion_White.triggered.connect(self.action_theme_fusion_white)
        
        #TABLES ACTIONS
        self.actionFornecedores.triggered.connect(self.action_tabelas_fornecedores)
        self.actionEmpresas.triggered.connect(self.action_tabelas_empresas)
        self.actionTransportadoras.triggered.connect(self.action_tabelas_transportadoras)
        self.actionProdutos.triggered.connect(self.action_tabelas_produtos)
        
        self.actionAvisos.triggered.connect(self.action_avisos)
        
        #Theme from config
        if self.config.get_config("tema") == "Fusion Dark":
            self.action_theme_fusion_dark()
        else:
            self.action_theme_fusion_white()

        #Setup last tab
        self.tabWidget.setCurrentIndex(self.config.get_config("lasttab"))
        self.tabWidget.currentChanged.connect(self.on_tab_change)

        #Setup the first filter
        self.lineEdit_nf_filtro_text.textChanged.connect(lambda: self.table_widget_filter(self.tableWidget_NF))
        self.dateEdit_NF_inicial.dateChanged.connect(lambda: self.date_edit_on_predate_change(self.tableWidget_NF))
        self.dateEdit_NF_final.dateChanged.connect(lambda: self.date_edit_on_predate_change(self.tableWidget_NF))

        self.lineEdit_duplicatas_filtro_text.textChanged.connect(lambda: self.table_widget_filter(self.tableWidget_duplicata))
        self.dateEdit_duplicata_inicial.dateChanged.connect(lambda: self.date_edit_on_predate_change(self.tableWidget_duplicata))
        self.dateEdit_duplicata_final.dateChanged.connect(lambda: self.date_edit_on_predate_change(self.tableWidget_duplicata))

        #Setup corner Buttons
        tableWidget_NF_corner = self.tableWidget_NF.findChild(QtWidgets.QAbstractButton)
        tableWidget_NF_corner.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tableWidget_NF_corner.customContextMenuRequested.connect(lambda: self.corner_button_function(
            ["NFE", "FORNECEDORES", "EMPRESA", "TRANSPORTADORA", "TOTAIS"], "nf_table_columns"))
        tableWidget_tableWidget_duplicata_corner = self.tableWidget_duplicata.findChild(QtWidgets.QAbstractButton)
        tableWidget_tableWidget_duplicata_corner.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tableWidget_tableWidget_duplicata_corner.customContextMenuRequested.connect(lambda: self.corner_button_function(
            ["FATURAS", "NFE", "COBRANCA", "FORNECEDORES", "EMPRESA"], "duplicatas_table_columns"))

        #Sava date combobox changes:
        self.comboBox_nfe_data_coluna.currentIndexChanged.connect(lambda: self.combobox_column_date_change(self.comboBox_nfe_data_coluna, "NFEcolunadate"))
        self.comboBox_duplicata_data_coluna.currentIndexChanged.connect(lambda: self.combobox_column_date_change(self.comboBox_duplicata_data_coluna, "dupcolunadate"))

        #Setup the clean filters
        self.pushButton_nf_limpar_filtro.clicked.connect(lambda: self.button_limpar_filtro(self.tableWidget_NF))
        self.pushButton_duplicata_limpar_filtro.clicked.connect(lambda: self.button_limpar_filtro(self.tableWidget_duplicata))

        self.combobox_populate_pre_date()
        self.comboBox_nfe_pre_dates.currentTextChanged.connect(lambda: self.combobox_predate_updater(self.tableWidget_NF))
        self.comboBox_duplicatas_pre_dates.currentTextChanged.connect(lambda: self.combobox_predate_updater(self.tableWidget_duplicata))

        #setup the context menu police
        self.tableWidget_NF.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_NF.customContextMenuRequested.connect(lambda: self.tablewidget_context_menu(self.tableWidget_NF))
        self.tableWidget_duplicata.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_duplicata.customContextMenuRequested.connect(lambda: self.tablewidget_context_menu(self.tableWidget_duplicata))

        #Setup Qtable double click
        self.tableWidget_NF.doubleClicked.connect(lambda: self.double_click_table_detalhes(self.tableWidget_NF))
        self.tableWidget_duplicata.doubleClicked.connect(lambda: self.double_click_table_detalhes(self.tableWidget_duplicata))
        
        #Make backup of the database
        self.make_backup()
        
        #Add shortcut for table update
        self.f5_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("F5"), self)
        self.f5_shortcut.activated.connect(self.action_atualizar_tabelas)
        
        #Open Main Window
        self.show()
        
        #Open Avisos Dialog
        QtWidgets.QApplication.processEvents()
        
        self.avisos_dialog_open()

                

    def avisos_dialog_open(self):
        if self.main_database.get_tables_list():
            self.avisos_dialog = s_avisos_dialog.Main(self.main_database)
            self.avisos_dialog.show()
    
    #Reset dates:
    def date_input_reset(self, Qtable_):
        if Qtable_.objectName() == "tableWidget_NF":
            selected_column = self.comboBox_nfe_data_coluna.currentText()

            qwidget_data_inicial = self.dateEdit_NF_inicial
            qwidget_data_final = self.dateEdit_NF_final
        else:
            selected_column = self.comboBox_duplicata_data_coluna.currentText()

            qwidget_data_inicial = self.dateEdit_duplicata_inicial
            qwidget_data_final = self.dateEdit_duplicata_final

        if selected_column != "":
            for index in range(Qtable_.columnCount()):
                if Qtable_.horizontalHeaderItem(index).text() == selected_column:
                    selected_column = index
                    break
            min_date = date.max
            max_date = date.min
            for row in range(Qtable_.rowCount()):
                row_date = Qtable_.item(row, selected_column).text()
                if row_date != "":
                    row_date = datetime.strptime(row_date, "%d-%m-%Y").date()
                    if min_date > row_date:
                        min_date = row_date
                    if max_date < row_date:
                        max_date = row_date
                else:
                    min_date = date.min
            qwidget_data_inicial.setDate(min_date)
            qwidget_data_final.setDate(max_date)
            
    def make_backup(self):
        #Make the backup folder
        backup_path = os.getcwd() + "\\backup\\"
        
        if "backup" not in os.listdir():
            os.mkdir("backup")
            
        # files = []
        # for file in os.listdir(backup_path):
        #     if file.endswith(".db"):
        #         try:
        #             files.append(datetime.strptime(file[:-3], "%d-%m-%Y"))
        #         except:
        #             pass
        # if len(files) >= 6:
            
                    
        if "database.db" in os.listdir():
            today = datetime.strftime(datetime.today(), "%d-%m-%Y")
            path = backup_path + today + ".db"
            os.system(f'copy "database.db" \"{path}\" /Y')
        
            
    #Abrir detalhes
    def double_click_table_detalhes(self, Qtable_):
        def get_chave():
            if Qtable_.objectName() == "tableWidget_NF":
                column_chave = "chNFe"
                table_name = "NFE"
                id_column = "NFID"
            else:
                column_chave = "FNFEchNFe"
                table_name = "FATURAS"
                id_column = "FAID"
                
            return self.main_database.cur.execute(f"""
                                                  SELECT
                                                      {column_chave}
                                                  FROM
                                                      {table_name}
                                                  WHERE
                                                      {id_column} = {Qtable_.selectedItems()[0].text()}
                                                  """).fetchall()[0][0]
            
        self.detalhes_dialog = s_detalhes_dialog.Main(get_chave(), self.main_database)
        self.detalhes_dialog.exec_()

    #Setup the today button
    def combobox_populate_pre_date(self):
        combobox_widgets = [self.comboBox_nfe_pre_dates, self.comboBox_duplicatas_pre_dates]

        for widget in combobox_widgets:
            widget.addItem("Tudo")

            widget.insertSeparator(1)
            widget.addItem("Amanhã") 
            widget.addItem("Hoje")
            widget.addItem("Ontem")

            widget.insertSeparator(5)
            widget.addItem("Próxima Semana")
            widget.addItem("Esta Semana")
            widget.addItem("Semana Passada")
            
            widget.insertSeparator(10)
            widget.addItem("Próximo Més") 
            widget.addItem("Este Més") 
            widget.addItem("Més Passado")

            widget.insertSeparator(14)
            widget.addItem("Próximo Trimestre")
            widget.addItem("Este Trimestre")
            widget.addItem("Trimestre Passado")

            widget.insertSeparator(18)
            widget.addItem("Próximo Ano")
            widget.addItem("Este Ano")
            widget.addItem("Ano Passado")

            widget.insertSeparator(22)
            widget.addItem("Personalizado")
            
    #Combobox predate
    def combobox_predate_updater(self, Qtable_):
        today = datetime.now().date()
        if Qtable_.objectName() == "tableWidget_NF":
            combobox = self.comboBox_nfe_pre_dates
            date_initial = self.dateEdit_NF_inicial
            date_final = self.dateEdit_NF_final
        else:
            combobox = self.comboBox_duplicatas_pre_dates
            date_initial = self.dateEdit_duplicata_inicial
            date_final = self.dateEdit_duplicata_final

        if combobox.currentText() == "Tudo":
            self.date_input_reset(Qtable_)

        elif combobox.currentText() == "Amanhã":
            date_initial.setDate(today + timedelta(days=1))
            date_final.setDate(today + timedelta(days=1))

        elif combobox.currentText() == "Hoje":
            date_initial.setDate(today)
            date_final.setDate(today)

        elif combobox.currentText() == "Ontem":
            date_initial.setDate(today + timedelta(days=-1))
            date_final.setDate(today + timedelta(days=-1))

        elif combobox.currentText() == "Próxima Semana":
            week = today.strftime("%Y") + "-" + str(int(today.strftime("%U")) + 1)
            date_initial.setDate(datetime.strptime(week + "-0", "%Y-%U-%w").date())
            date_final.setDate(datetime.strptime(week + "-6", "%Y-%U-%w").date())

        elif combobox.currentText() == "Esta Semana":
            week = today.strftime("%Y") + "-" + str(int(today.strftime("%U")) + 0)
            date_initial.setDate(datetime.strptime(week + "-0", "%Y-%U-%w").date())
            date_final.setDate(datetime.strptime(week + "-6", "%Y-%U-%w").date())

        elif combobox.currentText() == "Semana Passada":
            week = today.strftime("%Y") + "-" + str(int(today.strftime("%U")) - 1)
            date_initial.setDate(datetime.strptime(week + "-0", "%Y-%U-%w").date())
            date_final.setDate(datetime.strptime(week + "-6", "%Y-%U-%w").date())

        elif combobox.currentText() == "Próximo Més":
            if int(today.strftime("%m")) + 1 != 13:
                days = calendar.monthrange(int(today.strftime("%Y")), int(today.strftime("%m")) + 1)
                month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) + 1)
            else:
                days = calendar.monthrange(int(today.strftime("%Y")) + 1, 1)
                month = str(int(today.strftime("%Y")) + 1) + "-" + str(1)
            
            date_initial.setDate(datetime.strptime(month + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(month + "-%s" % days[1], "%Y-%m-%d").date())
        elif combobox.currentText() == "Este Més":
            month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) + 0)
            days = calendar.monthrange(int(today.strftime("%Y")), int(today.strftime("%m")) + 0)
            date_initial.setDate(datetime.strptime(month + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(month + "-%s" % days[1], "%Y-%m-%d").date())

        elif combobox.currentText() == "Més Passado":
            if int(today.strftime("%m")) - 1 != 0:
                days = calendar.monthrange(int(today.strftime("%Y")), int(today.strftime("%m")) - 1)
                month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) - 1)
            else:
                days = calendar.monthrange(int(today.strftime("%Y")) - 1, 12)
                month = str(int(today.strftime("%Y")) - 1) + "-" + str(12)
            
            date_initial.setDate(datetime.strptime(month + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(month + "-%s" % days[1], "%Y-%m-%d").date())

        elif combobox.currentText() == "Próximo Trimestre":
            if int(today.strftime("%m")) + 1 > 12:
                i_month = str(int(today.strftime("%Y")) + 1) + "-" + str(int(today.strftime("%m")) - 11)
            else:
                i_month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) + 1)

            if int(today.strftime("%m")) + 3 > 12:
                f_month = str(int(today.strftime("%Y")) + 1) + "-" + str(int(today.strftime("%m")) - 9)
                f_days = calendar.monthrange(int(today.strftime("%Y")) + 1, int(today.strftime("%m")) - 9)
            else:
                f_month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) + 3)
                f_days = calendar.monthrange(int(today.strftime("%Y")), int(today.strftime("%m")) + 3)
            
            date_initial.setDate(datetime.strptime(i_month + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(f_month + "-%s" % f_days[1], "%Y-%m-%d").date())

        elif combobox.currentText() == "Este Trimestre":
            if int(today.strftime("%m")) - 1 < 1:
                i_month = str(int(today.strftime("%Y")) - 1) + "-" + str(int(today.strftime("%m")) + 11)
            else:
                i_month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) - 1)

            if int(today.strftime("%m")) + 1 > 12:
                f_month = str(int(today.strftime("%Y")) + 1) + "-" + str(int(today.strftime("%m")) - 12)
                f_days = calendar.monthrange(int(today.strftime("%Y")) + 1, int(today.strftime("%m")) - 12)
            else:
                f_month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) + 1)
                f_days = calendar.monthrange(int(today.strftime("%Y")), int(today.strftime("%m")) + 1)
            
            date_initial.setDate(datetime.strptime(i_month + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(f_month + "-%s" % f_days[1], "%Y-%m-%d").date())
            
        elif combobox.currentText() == "Trimestre Passado":
            if int(today.strftime("%m")) - 3 < 1:
                i_month = str(int(today.strftime("%Y")) - 1) + "-" + str(int(today.strftime("%m")) + 9)
            else:
                i_month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) + 1)

            if int(today.strftime("%m")) - 1 < 12:
                f_month = str(int(today.strftime("%Y")) - 1) + "-" + str(int(today.strftime("%m")) + 11)
                f_days = calendar.monthrange(int(today.strftime("%Y")) - 1, int(today.strftime("%m")) + 11)
            else:
                f_month = today.strftime("%Y") + "-" + str(int(today.strftime("%m")) - 1)
                f_days = calendar.monthrange(int(today.strftime("%Y")), int(today.strftime("%m")) - 1)
            
            date_initial.setDate(datetime.strptime(i_month + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(f_month + "-%s" % f_days[1], "%Y-%m-%d").date())

        elif combobox.currentText() == "Próximo Ano":
            years = str(int(today.strftime("%Y")) + 1)
            days = calendar.monthrange(int(today.strftime("%Y")) + 1, 12)
            date_initial.setDate(datetime.strptime(years + "-" + str(1) + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(years + "-" + str(12) + "-%s" % days[1], "%Y-%m-%d").date())

        elif combobox.currentText() == "Este Ano":
            years = str(int(today.strftime("%Y")))
            days = calendar.monthrange(int(today.strftime("%Y")), 12)
            date_initial.setDate(datetime.strptime(years + "-" + str(1) + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(years + "-" + str(12) + "-%s" % days[1], "%Y-%m-%d").date())

        elif combobox.currentText() == "Ano Passado":
            years = str(int(today.strftime("%Y")) - 1)
            days = calendar.monthrange(int(today.strftime("%Y")) - 1, 12)
            date_initial.setDate(datetime.strptime(years + "-" + str(1) + "-01", "%Y-%m-%d").date())
            date_final.setDate(datetime.strptime(years + "-" + str(12) + "-%s" % days[1], "%Y-%m-%d").date())

    #On combobox date change
    def date_edit_on_predate_change(self, Qtable_):
        if Qtable_.objectName() == "tableWidget_NF":
            self.comboBox_nfe_pre_dates.setCurrentIndex(22)
            self.table_widget_filter(self.tableWidget_NF)
        else:
            self.comboBox_duplicatas_pre_dates.setCurrentIndex(22)
            self.table_widget_filter(self.tableWidget_duplicata)

    #Button limpar filtros
    def button_limpar_filtro(self, Qtable_):
        if Qtable_.objectName() == "tableWidget_NF":
            self.comboBox_nf_filtro_colunas.setCurrentIndex(0)
            self.lineEdit_nf_filtro_text.setText("")
            self.date_input_reset(Qtable_)
            self.comboBox_nfe_pre_dates.setCurrentIndex(0)
        else:
            self.comboBox_duplicata_colunas.setCurrentIndex(0)
            self.lineEdit_duplicatas_filtro_text.setText("")
            self.date_input_reset(Qtable_)
            self.comboBox_duplicatas_pre_dates.setCurrentIndex(0)
        for row in range(Qtable_.rowCount()):
            Qtable_.showRow(row)

    #Save date combobox change
    def combobox_column_date_change(self, Qcombobox_, config_name_):
        retranslated_name = self.config.translate_column_names([Qcombobox_.currentText()], True)[0]
        self.config.change_config({config_name_: retranslated_name})

        if config_name_ == "NFEcolunadate":
            self.date_input_reset(self.tableWidget_NF)
        else:
            self.date_input_reset(self.tableWidget_duplicata)

    #Lists Functions
    def build_table(self, Qtable_, data_, columns_, table_names_):
        def save_table_sort(logical_index_):
            self.config.change_config({Qtable_.objectName(): [logical_index_, Qtable_.horizontalHeader().sortIndicatorOrder()]})

        #Make it non editable
        Qtable_.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        header_names = self.config.translate_column_names(columns_)
        Qtable_.setColumnCount(len(columns_))
        Qtable_.setHorizontalHeaderLabels(header_names)

        #Context menu and funciton on the Horizontal header
        headers = Qtable_.horizontalHeader()
        headers.sectionClicked.connect(save_table_sort)

        Qtable_.setRowCount(len(data_))

        #Setup colors
        Qtable_.setAlternatingRowColors(True)
        self.qtable_palette = QtGui.QPalette()
        if self.config.get_config("tema") == "Fusion Dark":
            self.qtable_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        else:
            self.qtable_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(229, 230, 235))
        Qtable_.setPalette(self.qtable_palette)
        
        Qtable_.setSortingEnabled(False)
        
        #Fill the data
        if len(data_) != 0:

            for column in range(len(columns_)):

                # column_type = self.main_database.get_column_type_name(table_names_, columns_[column])
                column_type = self.main_database.get_type_from_multiple_tables(table_names_, columns_[column])

                for row in range(len(data_)):

                    if column_type == "INTEGER" or column_type == "FLOAT":
                        if data_[row][column] != None:
                            newitem = personalizedTableWidgetItem(str(data_[row][column]), data_[row][column])
                            Qtable_.setItem(row, column, newitem)
                        else:
                            newitem = personalizedTableWidgetItem("", 0)
                            Qtable_.setItem(row, column, newitem)

                    elif column_type == "TIMESTAMP":
                        try:
                            TIMESTAMP = data_[row][column]
                            newitem = personalizedTableWidgetItem(self.qtable_date_converter(TIMESTAMP), self.date_time_to_int(TIMESTAMP))
                            Qtable_.setItem(row, column, newitem)
                        except:
                            newitem = personalizedTableWidgetItem("", 0)
                            Qtable_.setItem(row, column, newitem)

                    else:
                        newitem = QtWidgets.QTableWidgetItem((data_[row][column]))
                        Qtable_.setItem(row, column, newitem)

        Qtable_.resizeColumnsToContents()

        #Setuping sort
        sorting_config = self.config.get_config(Qtable_.objectName())
        if sorting_config[1] == 0:
            Qtable_.sortByColumn(sorting_config[0], QtCore.Qt.AscendingOrder)
        else:
            Qtable_.sortByColumn(sorting_config[0], QtCore.Qt.DescendingOrder)
        Qtable_.setSortingEnabled(True)

        #Populate comboxbox
        self.populate_combobox_filtro(self.comboBox_nf_filtro_colunas, "nf_table_columns")
        self.populate_combobox_filtro(self.comboBox_duplicata_colunas, "duplicatas_table_columns")
        combox_date_columns = []
        if len(columns_) > 0:
            for index, column in enumerate(columns_):
                column_type = self.main_database.get_type_from_multiple_tables(table_names_, columns_[index])
                if column_type == "TIMESTAMP":
                    combox_date_columns.append(column)

        #Setup the dates
        self.date_input_reset(Qtable_)

        #Paint the table
        if Qtable_.objectName() == "tableWidget_NF":
            self.date_combobox_set(self.comboBox_nfe_data_coluna, combox_date_columns, "NFEcolunadate")
            self.comboBox_nfe_pre_dates.setCurrentIndex(0)
            flaglistData = self.main_database.cur.execute("""
            SELECT
                NFID, FLAGRECEBIDO
            FROM
                NFE
            """).fetchall()
            ids = [i[0] for i in flaglistData if i[1] == 1]
            for row in range(Qtable_.rowCount()):
                if int(Qtable_.item(row, 0).text()) in ids:
                    for column in range(Qtable_.columnCount()):
                        Qtable_.item(row, column).setBackground(QtGui.QColor(82,191,144))
        else:
            self.date_combobox_set(self.comboBox_duplicata_data_coluna, combox_date_columns, "dupcolunadate")
            self.comboBox_duplicatas_pre_dates.setCurrentIndex(0)
            
            #IDS THAT HAVE BEEN PAYD
            flaglistData = self.main_database.cur.execute("""
            SELECT
                FAID, FLAGPAGO
            FROM
                FATURAS
            """).fetchall()
            payd_ids = [i[0] for i in flaglistData if i[1] == 1]
            
            #IDS THAT HAVE OBS and aren't vencidas
            ids_with_obs = self.main_database.cur.execute("""
                                                          SELECT FAID
                                                          FROM FATURAS
                                                          WHERE length(FObs) > 0
                                                          AND dVenc > date('now')
                                                          AND FobsFlag == 0
                                                          AND FLAGPAGO == 0
            """).fetchall()
            ids_with_obs = [i[0] for i in ids_with_obs]
            
            #IDS THAT ARE LATE
            late_data = self.main_database.cur.execute("""
                                                      SELECT FAID, FLAGPAGO, dVenc
                                                      FROM FATURAS
                                                      """).fetchall()
            late_ids = [i[0] for i in late_data if datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S").date() < datetime.today().date() and i[1] != 1]
            
            for row in range(Qtable_.rowCount()):
                if int(Qtable_.item(row, 0).text()) in payd_ids:
                    for column in range(Qtable_.columnCount()):
                        Qtable_.item(row, column).setBackground(QtGui.QColor(82,191,144))
                        
                if int(Qtable_.item(row, 0).text()) in late_ids:
                    for column in range(Qtable_.columnCount()):
                        Qtable_.item(row, column).setBackground(QtGui.QColor(244,78,78))
                        
                if int(Qtable_.item(row, 0).text()) in ids_with_obs:
                    for column in range(Qtable_.columnCount()):
                        Qtable_.item(row, column).setBackground(QtGui.QColor(255,226,138))

    def tablewidget_flag_changer(self, Qtable_):
        hoje = datetime.today()
        if Qtable_.objectName() == "tableWidget_NF":
            flag_column = "FLAGRECEBIDO"
            table_name = "NFE"
            date_column = "DATARECEBIDO"
            id_column = "NFID"
            name_data_column = "Data do Recebimento"
        else:
            flag_column = "FLAGPAGO"
            table_name = "FATURAS"
            date_column = "DATAPAGAMENTO"
            id_column = "FAID"
            name_data_column = "Data Pagamento"
            sql = (f"""
                   SELECT dVenc
                   FROM FATURAS
                   WHERE FAID = \'{Qtable_.selectedItems()[0].text()}\'
                   """)
            dup_venc_date = self.main_database.cur.execute(sql).fetchall()[0][0]

        
        #Get 
        date_header = -1
        for column_index in range(Qtable_.columnCount()):
            if Qtable_.horizontalHeaderItem(column_index).text() == name_data_column:
                date_header = column_index

        #Get the flag for the selected column
        flag = self.main_database.cur.execute(f"""
        SELECT
            {flag_column}
        FROM
            {table_name}
        WHERE
            {id_column} = \'{Qtable_.selectedItems()[0].text()}\'
        """).fetchall()[0][0]

        selected_row = Qtable_.selectedIndexes()[0].row()

        if flag == 0:
            for index, item in enumerate(Qtable_.selectedItems()):
                if index == date_header:
                    item = personalizedTableWidgetItem(hoje.strftime("%d-%m-%Y"), hoje.timestamp())
                    item.setBackground(QtGui.QColor(82,191,144))
                    Qtable_.setItem(selected_row, index, item)
                else:
                    item.setBackground(QtGui.QColor(82,191,144))

            self.main_database.cur.execute(f"""
            UPDATE
                {table_name}
            SET
                {flag_column} = "1", {date_column} = \'{hoje}\'
            WHERE
                {id_column} = \'{Qtable_.selectedItems()[0].text()}\'
            """)
            self.main_database.con.commit()
            Qtable_.clearSelection()

        else:
            #Make it to the base color again
            if Qtable_.objectName() != "tableWidget_NF":
                if datetime.strptime(dup_venc_date, "%Y-%m-%d %H:%M:%S").date() < datetime.today().date():
                    for column, item in enumerate(Qtable_.selectedItems()):
                        if column == date_header:
                            Qtable_.setSortingEnabled(False)
                            item = personalizedTableWidgetItem("",0)
                            item.setBackground(QtGui.QColor(244,78,78))
                            Qtable_.setItem(selected_row, column, item)
                            Qtable_.setSortingEnabled(True)
                        else:
                            item.setBackground(QtGui.QColor(244,78,78))
                            
                    self.main_database.cur.execute(f"""
                                                    UPDATE
                                                        {table_name}
                                                    SET
                                                        {flag_column} = "0", {date_column} = NULL
                                                    WHERE
                                                        {id_column} = \'{Qtable_.selectedItems()[0].text()}\'
                                                    """)
                    self.main_database.con.commit()
                    Qtable_.clearSelection()
                    return
                        
            Qtable_.setSortingEnabled(False)
            for column,item in enumerate(Qtable_.selectedItems()):
                if type(item) == QtWidgets.QTableWidgetItem:
                    item = QtWidgets.QTableWidgetItem(item.text())
                    Qtable_.setItem(selected_row, column, item)
                else:
                    if column == date_header:
                        item = personalizedTableWidgetItem("",0)
                        Qtable_.setItem(selected_row, column, item)
                    else:
                        item = personalizedTableWidgetItem(item.text(), item.sortKey)
                        Qtable_.setItem(selected_row, column, item)
            Qtable_.setSortingEnabled(True)

            self.main_database.cur.execute(f"""
            UPDATE
                {table_name}
            SET
                {flag_column} = "0", {date_column} = NULL
            WHERE
                {id_column} = \'{Qtable_.selectedItems()[0].text()}\'
            """)
            self.main_database.con.commit()
            Qtable_.clearSelection()

    def tablewidget_context_menu(self, Qtable_):
        mouse_pos = QtGui.QCursor.pos()
        mapped = Qtable_.mapFromGlobal(mouse_pos)
        mapped.setX(mapped.x() - Qtable_.verticalHeader().width())
        mapped.setY(mapped.y() - Qtable_.horizontalHeader().height())
        try:
            selected_item_text = Qtable_.itemAt(mapped).text()
        except:
            selected_item_text = None
        
        def get_chave():
            if Qtable_.objectName() == "tableWidget_NF":
                column_chave = "chNFe"
                table_name = "NFE"
                id_column = "NFID"
            else:
                column_chave = "FNFEchNFe"
                table_name = "FATURAS"
                id_column = "FAID"
                
            return self.main_database.cur.execute(f"""
                                                  SELECT
                                                      {column_chave}
                                                  FROM
                                                      {table_name}
                                                  WHERE
                                                      {id_column} = {Qtable_.selectedItems()[0].text()}
                                                  """).fetchall()[0][0]
        
        if Qtable_.selectedItems() != []:

            context_menu = QtWidgets.QMenu()
            
            if Qtable_.objectName() == "tableWidget_NF":
                context_menu.addAction("Marcar como recebido")
                context_menu.addSeparator()
            else:
                context_menu.addAction("Marcar como pago")
                context_menu.addSeparator()

            context_menu.addAction("Copiar texto da célula")
            context_menu.addAction("Copiar Chave de Acesso")
            context_menu.addSeparator()

            if Qtable_.objectName() != "tableWidget_NF":
                context_menu.addAction("Ir para Nota Fiscal")
                context_menu.addSeparator()

            context_menu.addAction("Abrir Detalhes")
            
            if Qtable_.objectName() == "tableWidget_NF":
                context_menu.addAction("Gerenciar Duplicatas") 

            action = context_menu.exec(QtGui.QCursor.pos())

            if action != None:
                if action.text() == "Copiar texto da célula":
                    if selected_item_text != None:
                        pyperclip.copy(selected_item_text)

                if action.text() == "Copiar Chave de Acesso":
                    pyperclip.copy(get_chave())
                
                if action.text() == "Ir para Nota Fiscal":
                    NFID = self.main_database.cur.execute("""
                    SELECT
                        NFE.NFID
                    FROM
                        FATURAS
                    LEFT JOIN NFE ON NFE.chNFe = FATURAS.FNFEchNFe
                    WHERE
                        FATURAS.FAID = %s
                    """ % (Qtable_.selectedItems()[0].text())).fetchall()[0][0]
                    for row in range(self.tableWidget_NF.rowCount()):
                        if self.tableWidget_NF.item(row, 0).text() == str(NFID):
                            self.tableWidget_NF.showRow(row)
                        else:
                            self.tableWidget_NF.hideRow(row)
                    self.tabWidget.setCurrentIndex(0)
                    self.tableWidget_NF.selectRow(0)
                    
                if action.text() in ["Marcar como pago", "Marcar como recebido"]:
                    self.tablewidget_flag_changer(Qtable_)

                if action.text() == "Abrir Detalhes":
                    self.detalhes_dialog = s_detalhes_dialog.Main(get_chave(), self.main_database)
                    self.detalhes_dialog.exec_()

                if action.text() == "Gerenciar Duplicatas":
                    key = get_chave()
                    self.duplicatas_dialog = s_duplicatas_dialog.Main(get_chave(), self.main_database)
                    self.duplicatas_dialog.exec_()
                    #Update the num of dup and last venc
                    num_duplicatas = self.main_database.cur.execute(f"""
                                                                    SELECT nDup
                                                                    FROM FATURAS
                                                                    WHERE FNFEchNFe = \'{key}\'
                                                                    ORDER BY nDup DESC
                                                                    LIMIT 1
                                                                    """).fetchall()
                    first_venc = self.main_database.cur.execute(f"""
                                                                 SELECT dVenc
                                                                 FROM FATURAS
                                                                 WHERE FNFEchNFe = \'{key}\'
                                                                 ORDER BY dVenc ASC
                                                                 LIMIT 1
                                                                """).fetchall()
                    if bool(num_duplicatas):
                        num_duplicatas = num_duplicatas[0][0]
                        first_venc = f", PRIMEIROVENCIMENTO = \'{first_venc[0][0]}\'"
                    else:
                        num_duplicatas = 0
                        first_venc = f", PRIMEIROVENCIMENTO = NULL"
                    self.main_database.cur.execute(f"""
                                                   UPDATE NFE
                                                   SET NUMDUPLICATAS = {num_duplicatas}{first_venc}
                                                   WHERE chNFe = \'{key}\'
                                                   """)
                    self.main_database.con.commit()
                    self.update_tables_duplicatas()
                    
                            
    def update_tables_NFE(self):
        #Setup NFE table
        if self.main_database.get_tables_list() != []:
            
            NFE_data = self.main_database.get_data_from_tables_left_join(
                "NFE",
                {"FORNECEDORES": ["FORNECEDORES.FCNPJCPF", "NFE.FORNECEDORESCNPJ"],
                 "EMPRESA": ["EMPRESA.ECNPJCPF", "NFE.EMPRESACNPJ"],
                 "TRANSPORTADORA": ["TRANSPORTADORA.TCNPJCPF", "NFE.TRANSPORTADORACNPJ"],
                 "TOTAIS": ["TOTAIS.TONFEchNFe", "NFE.chNFe"]},
                self.config.get_config("nf_table_columns"))

            self.build_table(
                self.tableWidget_NF,
                NFE_data,
                self.config.get_config("nf_table_columns"),
                ["NFE", "FORNECEDORES", "EMPRESA", "TRANSPORTADORA", "TOTAIS"]
            )
            
    def update_tables_duplicatas(self):
        
        if self.main_database.get_tables_list() != []:

            Fatura_data = self.main_database.get_data_from_tables_left_join(
                "FATURAS",
                {"NFE": ["NFE.chNFe", "FATURAS.FNFEchNFe"],
                 "COBRANCA": ["COBRANCA.CNFEchNFe", "NFE.chNFe"],
                 "FORNECEDORES": ["FORNECEDORES.FCNPJCPF", "NFE.FORNECEDORESCNPJ"],
                 "EMPRESA": ["EMPRESA.ECNPJCPF", "NFE.EMPRESACNPJ"]},
                self.config.get_config("duplicatas_table_columns"))
            

            self.build_table(
                self.tableWidget_duplicata,
                Fatura_data,
                self.config.get_config("duplicatas_table_columns"),
                ["FATURAS", "NFE", "COBRANCA", "FORNECEDORES", "EMPRESA"]
            )

    def populate_combobox_filtro(self, Qcombobox_, config_name_):
        columns_NF = self.config.get_config(config_name_)

        Qcombobox_.clear()
        Qcombobox_.addItem("Tudo")

        translated_columns_nf = self.config.translate_column_names(columns_NF)
        for column in translated_columns_nf:
            Qcombobox_.addItem(column)
        

    def corner_button_function(self, columns_, database_name_):
        self.coluns_dialog = s_columns_dialog.Main(
            self.main_database.get_columns_from_multiple_tables(columns_), database_name_)
        self.coluns_dialog.exec_()
        self.update_tables_NFE()
        self.update_tables_duplicatas()

    #Filter 
    def table_widget_filter(self, Qtable_):
        if Qtable_.objectName() == "tableWidget_NF":

            text_filter_column = self.comboBox_nf_filtro_colunas.currentText()
            date_selected_column = self.comboBox_nfe_data_coluna.currentText()


            for index in range(Qtable_.columnCount()):
                if text_filter_column != "Tudo":
                    if Qtable_.horizontalHeaderItem(index).text() == text_filter_column:
                        text_filter_column = index
                
                if Qtable_.horizontalHeaderItem(index).text() == date_selected_column:
                    date_selected_column = index

            filter_text = self.lineEdit_nf_filtro_text.text().split(";")

            date_initial = self.dateEdit_NF_inicial.date().toPyDate()
            date_final = self.dateEdit_NF_final.date().toPyDate()

        else:

            text_filter_column = self.comboBox_duplicata_colunas.currentText()
            date_selected_column = self.comboBox_duplicata_data_coluna.currentText()

            for index in range(Qtable_.columnCount()):
                if text_filter_column != "Tudo":
                    if Qtable_.horizontalHeaderItem(index).text() == text_filter_column:
                        text_filter_column = index

                if Qtable_.horizontalHeaderItem(index).text() == date_selected_column:
                    date_selected_column = index

            filter_text = self.lineEdit_duplicatas_filtro_text.text().split(";")

            date_initial = self.dateEdit_duplicata_inicial.date().toPyDate()
            date_final = self.dateEdit_duplicata_final.date().toPyDate()

        #SET THE ROW VISIBILITY
        for row in range(Qtable_.rowCount()):
            Qtable_.showRow(row)

            show_row = True

            if date_selected_column != "":
                item_date = Qtable_.item(row, date_selected_column).text()
                if item_date == "":
                    item_date = datetime.strptime("14-09-1752", "%d-%m-%Y").date() #Min date of the widget
                else:
                    item_date = datetime.strptime(item_date, "%d-%m-%Y").date()

                if not (item_date >= date_initial and item_date <= date_final):
                    show_row = False

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

    
    #Coluna combobox set
    def date_combobox_set(self, comboBox_, columns_, config_name_):
        comboBox_.clear()
        if columns_ != []:
            for index, column in enumerate(columns_):
                comboBox_.addItem(self.config.translate_column_names([column])[0])
                if self.config.get_config(config_name_) == column:
                    comboBox_.setCurrentIndex(index)

    #Dialogs actions functions
    def action_selecionar_pasta_xml(self):
        xml_path = self.config.get_config("xmlpath")
        self.config.change_config({"xmlpath":QtWidgets.QFileDialog.getExistingDirectory(self, "Selecionar pasta", xml_path)})
        
    def action_escolher_pasta_do_banco_dados(self):
        database_path = self.config.get_config("databasepath")
        database_path = QtWidgets.QFileDialog.getOpenFileName(self, "Selecionar Data Base", database_path, "Banco de Dados (*.db)")[0]
        if database_path != "":
            self.config.change_config({"databasepath": database_path})
            self.main_database = _sqlite_handler.new_sql_connection(self.config.get_config("databasepath"))
            self.update_tables_NFE()
            self.update_tables_duplicatas()
            
    def action_atualizar_tabelas(self):
        self.update_tables_NFE()
        self.update_tables_duplicatas()

    def action_actionAtualizar_banco_de_dados(self):
        self.carregamento_window = s_carregamento.Main(self.config.get_config("xmlpath"), self.main_database)
        self.carregamento_window.show()
        self.carregamento_window.update()
        self.update_tables_NFE()
        self.update_tables_duplicatas()
        
    def action_tabelas_fornecedores(self):
        self.tabelas_windows = s_tables_dialog.Main(self.main_database, "FORNECEDORES")
        self.tabelas_windows.show()
        
    def action_tabelas_empresas(self):
        self.tabelas_windows = s_tables_dialog.Main(self.main_database, "EMPRESA")
        self.tabelas_windows.show()
        
    def action_tabelas_transportadoras(self):
        self.tabelas_windows = s_tables_dialog.Main(self.main_database, "TRANSPORTADORA")
        self.tabelas_windows.show()
        
    def action_tabelas_produtos(self):
        self.tabelas_windows = s_tables_dialog.Main(self.main_database, "PRODUTO")
        self.tabelas_windows.show()

    def action_avisos(self):
        self.avisos_dialog_open()

    #Themes Function
    def action_theme_fusion_dark(self):
        app.setStyle("Fusion")
        app.setPalette(self.dark_palette())
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        self.config.change_config({"tema":"Fusion Dark"})
        self.update_tables_NFE()
        self.update_tables_duplicatas()
        
    def action_theme_fusion_white(self):
        app.setStyle("Fusion")
        app.setPalette(QtGui.QPalette(QtCore.Qt.white))
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        self.config.change_config({"tema":"Fusion White"})
        self.update_tables_NFE()
        self.update_tables_duplicatas()

    def dark_palette(self):
        dark_palette = QtGui.QPalette()
        dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Window, QtGui.QColor(25,25,25))
        dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtGui.QColor(25,25,25))
        dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        return dark_palette

    #On tab change
    def on_tab_change(self):
        self.config.change_config({"lasttab": self.tabWidget.currentIndex()})

    #Utilities functon
    def qtable_date_converter(self, date_):
        date = date_.split(".")[0]
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
    
    def date_time_to_int(self, date_):
        date = date_.split(".")[0]
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.setWindowIcon(QtGui.QIcon("conta.png"))
    # window.show()
    sys.exit(app.exec_())
