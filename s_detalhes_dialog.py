from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
from datetime import datetime

import Ui_u_detalhes_dialog

import _sqlite_handler
import _config
from _personalizedtableitem import personalizedTableWidgetItem
import s_columns_dialog


class Main(QtWidgets.QDialog, Ui_u_detalhes_dialog.Ui_Dialog):
    def __init__(self, NFE_chave_, data_base_):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.NFE_chave = NFE_chave_
        self.main_database = data_base_

        self.config = _config.config()

        #Setup the top lines
        self.lineEdit_chave_de_acesso.setText(NFE_chave_)
        self.lineEdit_numero.setText(str(self.main_database.cur.execute(sql_nfe_maker("nNF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_versao_xml.setText(str(self.main_database.cur.execute(sql_nfe_maker("versao",self.NFE_chave)).fetchall()[0][0]))

        #Setup NFE
        self.lineEdit_NFE_modelo.setText(str(self.main_database.cur.execute(sql_nfe_maker("mod",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_serie.setText(str(self.main_database.cur.execute(sql_nfe_maker("serie",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_numero.setText(str(self.main_database.cur.execute(sql_nfe_maker("nNF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_data_emissao.setText(str(self.main_database.cur.execute(sql_nfe_maker("dhEmi",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_data_saida.setText(str(self.main_database.cur.execute(sql_nfe_maker("dhSaiEnt",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_valor_total.setText(str(self.main_database.cur.execute(sql_nfe_maker("TOvNF",self.NFE_chave)).fetchall()[0][0]))

        #Setup NFE_emitente
        self.lineEdit_NFE_emitente_cnpj.setText(str(self.main_database.cur.execute(sql_nfe_maker("FCNPJCPF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emitente_nome.setText(str(self.main_database.cur.execute(sql_nfe_maker("FxNome",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emitente_inscricao.setText(str(self.main_database.cur.execute(sql_nfe_maker("FIE",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emitente_UF.setText(str(self.main_database.cur.execute(sql_nfe_maker("FUF",self.NFE_chave)).fetchall()[0][0]))

        #Setup NFE_destinatario
        self.lineEdit_NFE_destinatario_cnpj.setText(str(self.main_database.cur.execute(sql_nfe_maker("ECNPJCPF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_Destinatario_nome.setText(str(self.main_database.cur.execute(sql_nfe_maker("ExNome",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_destinatario_IE.setText(str(self.main_database.cur.execute(sql_nfe_maker("EIE",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_destinatario_UF.setText(str(self.main_database.cur.execute(sql_nfe_maker("EUF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_destinatario_natureza.setText(str(self.main_database.cur.execute(sql_nfe_maker("idDest",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_destinatario_operacao.setText(str(self.main_database.cur.execute(sql_nfe_maker("indFinal",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_destinatario_presenca.setText(str(self.main_database.cur.execute(sql_nfe_maker("indPres",self.NFE_chave)).fetchall()[0][0]))

        #Setup NFE Emissão
        self.lineEdit_NFE_emisso_processo.setText(str(self.main_database.cur.execute(sql_nfe_maker("procEmi",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emisso_versao.setText(str(self.main_database.cur.execute(sql_nfe_maker("verProc",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emisso_tipo.setText(str(self.main_database.cur.execute(sql_nfe_maker("tpEmis",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emisso_finalidade.setText(str(self.main_database.cur.execute(sql_nfe_maker("finNFe",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emisso_natureza.setText(str(self.main_database.cur.execute(sql_nfe_maker("natOp",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emisso_tipo_operacao.setText(str(self.main_database.cur.execute(sql_nfe_maker("tpNF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emisso_forma_pagamento.setText(str(self.main_database.cur.execute(sql_nfe_maker("tPag",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_NFE_emisso_diggest.setText(str(self.main_database.cur.execute(sql_nfe_maker("digVal",self.NFE_chave)).fetchall()[0][0]))

        #Setup dados do emitente
        self.lineEdit_emitente_razao_social.setText(str(self.main_database.cur.execute(sql_nfe_maker("FxNome",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_nome_fantasia.setText(str(self.main_database.cur.execute(sql_nfe_maker("FxFant",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_cnpj.setText(str(self.main_database.cur.execute(sql_nfe_maker("FCNPJCPF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_endereco.setText(str(self.main_database.cur.execute(sql_nfe_maker("FxLgrnroxCpl",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_bairro.setText(str(self.main_database.cur.execute(sql_nfe_maker("FxBairro",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_cep.setText(str(self.main_database.cur.execute(sql_nfe_maker("FCEP",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_municipio.setText(str(self.main_database.cur.execute(sql_nfe_maker("FxMun",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_telefone.setText(str(self.main_database.cur.execute(sql_nfe_maker("Ffone",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_uf.setText(str(self.main_database.cur.execute(sql_nfe_maker("FUF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_pais.setText(str(self.main_database.cur.execute(sql_nfe_maker("FxPais",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_ie.setText(str(self.main_database.cur.execute(sql_nfe_maker("FIE",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_ie_substituto.setText(str(self.main_database.cur.execute(sql_nfe_maker("FIEST",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_insc_municipal.setText(str(self.main_database.cur.execute(sql_nfe_maker("FIM",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_municipio_de_ocorrencia.setText(str(self.main_database.cur.execute(sql_nfe_maker("FcMun",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_CNAE.setText(str(self.main_database.cur.execute(sql_nfe_maker("FCNAE",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_emitente_codig_regime.setText(str(self.main_database.cur.execute(sql_nfe_maker("FCRT",self.NFE_chave)).fetchall()[0][0]))

        #Setup Dados Destinatario
        self.lineEdit_destinatario_nome.setText(str(self.main_database.cur.execute(sql_nfe_maker("ExNome",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_CNPJ.setText(str(self.main_database.cur.execute(sql_nfe_maker("ECNPJCPF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_Endereco.setText(str(self.main_database.cur.execute(sql_nfe_maker("ExLgrnroxCpl",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_bairro.setText(str(self.main_database.cur.execute(sql_nfe_maker("ExBairro",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_CEP.setText(str(self.main_database.cur.execute(sql_nfe_maker("ECEP",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_muninipio.setText(str(self.main_database.cur.execute(sql_nfe_maker("ExMun",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_telefone.setText(str(self.main_database.cur.execute(sql_nfe_maker("Efone",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_uf.setText(str(self.main_database.cur.execute(sql_nfe_maker("EUF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_pais.setText(str(self.main_database.cur.execute(sql_nfe_maker("ExPais",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_indecador_ie.setText(str(self.main_database.cur.execute(sql_nfe_maker("EindIEDest",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_inscricao_estadual.setText(str(self.main_database.cur.execute(sql_nfe_maker("EIE",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_suframa.setText(str(self.main_database.cur.execute(sql_nfe_maker("EISUF",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_IM.setText(str(self.main_database.cur.execute(sql_nfe_maker("EIM",self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_destinatario_email.setText(str(self.main_database.cur.execute(sql_nfe_maker("Eemail",self.NFE_chave)).fetchall()[0][0]))

        #Setup produtos table
        tableWidget_produto_corner = self.tableWidget_produtos.findChild(QtWidgets.QAbstractButton)
        tableWidget_produto_corner.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tableWidget_produto_corner.customContextMenuRequested.connect(lambda: self.corner_button_function(
            ["PRODUTO", "PRODUTOICMS", "PRODUTOPIS", "PRODUTOCOFINS"], "detalhes_produto_columns"))
        self.update_table_produto()

        #Setup Totais
        self.lineEdit_totais_1.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvBC", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_2.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvICMS", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_3.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvICMSDeson", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_4.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvFCP", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_5.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvFCPUFDest", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_6.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvICMSUFDest", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_7.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvICMSUFRemet", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_8.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvBCST", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_9.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvST", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_10.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvFCPST", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_11.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvFCPSTRet", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_12.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvProd", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_13.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvFrete", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_14.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvSeg", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_15.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvDesc", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_16.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvII", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_17.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvIPI", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_18.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvIPIDevol", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_19.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvPIS", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_20.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvCOFINS", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_21.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvOutro", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_22.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvNF", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_totais_23.setText(str(self.main_database.cur.execute(sql_totais_maker("TOvTotTrib", self.NFE_chave)).fetchall()[0][0]))

        #Setup transporte
        self.lineEdit_transporte_modalidade_frete.setText(str(self.main_database.cur.execute(sql_transportadora_maker("modFrete", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_transporte_CNPJ.setText(str(self.main_database.cur.execute(sql_transportadora_maker("TCNPJCPF", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_transporte_nome.setText(str(self.main_database.cur.execute(sql_transportadora_maker("TxNome", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_transporte_ie.setText(str(self.main_database.cur.execute(sql_transportadora_maker("TIE", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_transporte_endereco.setText(str(self.main_database.cur.execute(sql_transportadora_maker("TxEnder", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_transporte_municipio.setText(str(self.main_database.cur.execute(sql_transportadora_maker("TxMun", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_transporte_uf.setText(str(self.main_database.cur.execute(sql_transportadora_maker("TUF", self.NFE_chave)).fetchall()[0][0]))

        volumes_data = self.main_database.cur.execute("""
            SELECT
                %s
            FROM 
                VOLUMES
            WHERE
                VNFEchNFe = \'%s\'
        """ % (",".join(["qVol","esp","marca","nVol","pesoL", "pesoB"]), self.NFE_chave)).fetchall()

        self.universal_table_builder(
            self.tableWidget_transporte_volumes,
            volumes_data,
            ["qVol","esp","marca","nVol","pesoL", "pesoB"],
            ["VOLUMES"]
        )

        #Setup Cobrança
        self.lineEdit_cobranca_numero.setText(str(self.main_database.cur.execute(sql_cobranca_maker("nFat", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_cobranca_valor_orignal.setText(str(self.main_database.cur.execute(sql_cobranca_maker("vOrig", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_cobranca_valor_desconto.setText(str(self.main_database.cur.execute(sql_cobranca_maker("vDesc", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_cobranca_valor_liquido.setText(str(self.main_database.cur.execute(sql_cobranca_maker("vLiq", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_cobranca_forma_pagamento.setText(str(self.main_database.cur.execute(sql_cobranca_maker("tPag", self.NFE_chave)).fetchall()[0][0]))
        self.lineEdit_cobranca_valor_pagamento.setText(str(self.main_database.cur.execute(sql_cobranca_maker("vPag", self.NFE_chave)).fetchall()[0][0]))

        fatura_data = self.main_database.cur.execute("""
            SELECT
                %s
            FROM
                FATURAS
            WHERE
                FNFEchNFe = \'%s\'
        """ % (",".join(["nDup", "dVenc", "vDup", "DATAPAGAMENTO"]), self.NFE_chave)).fetchall()

        self.universal_table_builder(
            self.tableWidget_cobranca,
            fatura_data,
            ["nDup", "dVenc", "vDup", "DATAPAGAMENTO"],
            ["FATURAS"]
        )

        #Setup informações adicionais
        self.textEdit_informacaoes_informacoes_complementares.setText(str(self.main_database.cur.execute("""
            SELECT
                infCpl
            FROM
                NFE
            WHERE
                chNFe = \'%s\'
        """ % self.NFE_chave).fetchall()[0][0]))

    def update_table_produto(self):
        produto_data = self.main_database.cur.execute("""
            SELECT
                %s
            FROM
                PRODUTO
            LEFT JOIN PRODUTOICMS ON PRODUTOICMS.PRODUTOID = PRODUTO.PID
            LEFT JOIN PRODUTOPIS ON PRODUTOPIS.PISPRODUTOID = PRODUTO.PID
            LEFT JOIN PRODUTOCOFINS ON PRODUTOCOFINS.COFINSPRODUTOID = PRODUTO.PID
            WHERE
                PNFEchNFe = \'%s\'
        """ % (",".join(self.config.get_config("detalhes_produto_columns")), self.NFE_chave)).fetchall()

        self.universal_table_builder(
            self.tableWidget_produtos,
            produto_data,
            self.config.get_config("detalhes_produto_columns"),
            ["PRODUTO", "PRODUTOICMS", "PRODUTOPIS", "PRODUTOCOFINS"]
            )

    def corner_button_function(self, columns_, database_name_):
        self.coluns_dialog = s_columns_dialog.Main(
            self.main_database.get_columns_from_multiple_tables(columns_), database_name_)
        self.coluns_dialog.exec_()
        self.update_table_produto()

    def universal_table_builder(self, Qtable_, data_, columns_, table_names_):
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

def sql_nfe_maker(column_, chave_):
    return ("""
    SELECT
        %s
    FROM
        NFE
    LEFT JOIN FORNECEDORES ON FORNECEDORES.FCNPJCPF = NFE.FORNECEDORESCNPJ
    LEFT JOIN EMPRESA ON EMPRESA.ECNPJCPF = NFE.EMPRESACNPJ
    LEFT JOIN COBRANCA ON COBRANCA.CNFEchNFe = NFE.chNFe
    LEFT JOIN TOTAIS ON TOTAIS.TONFEchNFe = NFE.chNFe
    WHERE
        NFE.chNFe = \'%s\'
    """ % (column_, chave_))

def sql_totais_maker(column_, chave_):
    return("""
    SELECT
        %s
    FROM
        TOTAIS
    WHERE
        TONFEchNFe = \'%s\'
    """ % (column_, chave_))

def sql_transportadora_maker(column_, chave_):
    return("""
    SELECT
        %s
    FROM
        NFE
    LEFT JOIN TRANSPORTADORA ON TRANSPORTADORA.TCNPJCPF = NFE.TRANSPORTADORACNPJ
    WHERE
        NFE.chNFe = \'%s\'
    """ % (column_, chave_))

def sql_cobranca_maker(column_, chave_):
    return("""
    SELECT
        %s
    FROM
        COBRANCA
    WHERE
        COBRANCA.CNFEchNFe = \'%s\'
    """ % (column_, chave_))




