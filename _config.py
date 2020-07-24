import json
import os

class config:
    def __init__(self):
        self.config_dict = {}

        self.path = os.getcwd() + "\\conf.cf"

        init_dict = {
            "tema": "Fusion White",
            "xmlpath": os.getcwd(),
            "databasepath": os.getcwd() + "\\database.db",
            "lasttab": 0,
            "tableWidget_NF": [0,0],
            "tableWidget_duplicata": [0,0],
            "nf_table_columns": ['NFID', 'dhEmi', 'ExNome', 'FxNome', 'FUF', 'nNF'],
            "duplicatas_table_columns": ['FAID', 'dhEmi', 'ExNome', 'nNF', 'FxNome', 'vPag', 'nDup'],
            "detalhes_produto_columns": ['PID'],
            "NFEcolunadate": "dhEmi",
            "dupcolunadate": "dVenc",
            "fornecedores_table_colunas": ["FID"],
            "empresas_table_colunas": ["EID"],
            "transportadoras_table_colunas": ["TID"],
            "produtos_table_colunas": ["PID"],
            "avisos_duplicatas_venc_columns": ["FAID", "dVenc", "FLAGPAGO", "FxNome"],
            "tableWidget_duplicatas_vencidas": [0,0],
            "avisos_duplicata_obs_columns": ["FAID", "dVenc", "FLAGPAGO", "FxNome"],
            "tableWidget_duplicata_com_alerta": [0,0],
            "avisos_nf_venc_columns": ['NFID', 'dhEmi', 'ExNome', 'FxNome', 'FUF', 'nNF'],
            "tableWidget_notas_fiscais_com_vencimento": [0,0],
            "avisos_nf_obs_columns": ['NFID', 'dhEmi', 'ExNome', 'FxNome', 'FUF', 'nNF'],
            "tableWidget_notas_fiscais_com_alertas": [0,0]
        }

        self.translate = {
            "FCNPJCPF" : "Forn. CNPJ",
            "FxNome": "Forn. Razão Social",
            "FxFant": "Forn. Nome Fantasia",
            "FxLgrnroxCpl": "Forn. Endereço",
            "FxBairro": "Forn. Bairro",
            "FCEP": "Forn. CEP",
            "FxMun": "Forn. Municipio",
            "Ffone": "Forn. Telefone",
            "FUF": "Forn. UF",
            "FxPais": "Forn. País",
            "FIE": "Forn. Inscrição Estadual",
            "FIEST": "Forn. IE Substituto",
            "FIM": "Forn. Inscrição Municipal",
            "FcMun": "Forn. Código Municipio",
            "FCNAE": "Forn. CNAE",
            "FCRT": "Forn. Codigo Regime Tributario",

            "ECNPJCPF": "Emp. CNPJ",
            "ExNome": "Emp. Razão Social",
            "ExLgrnroxCpl": "Emp. Endereço",
            "ExBairro": "Emp. Bairro",
            "ECEP": "Emp. CEP",
            "ExMun": "Emp. Municipio",
            "Efone": "Empresa. Telefone",
            "EUF": "Emp. UF",
            "ExPais": "Emp. País",
            "EIE": "Emp. Inscrição Estadual",
            "EISUF": "Emp. EISUF",
            "Eemail": "Emp. Email",
            "EindIEDest": "Emp. Indicador IE",
            "EIM": "Emp. Inscrição Municipal",

            "TCNPJCPF": "Transp. CNPJ",
            "TxNome": "Transp. Razão Social",
            "TIE": "Transp. Inscrição Estadual",
            "TxEnder": "Transp. Endereço",
            "TxMun": "Transp. Municipio",
            "TUF": "Transp. UF",

            "chNFe": "Chave NF",
            "versao": "Versão da NF",
            "mod": "Modelo",
            "serie": "Serie",
            "nNF":	"Numero NF",
            "dhEmi": "Data Emissão",
            "dhSaiEnt": "Data Saída",
            "procEmi": "Processo de Emissão",
            "idDest": "Destino Operação",
            "indFinal": "Consumidor Final",
            "verProc": "Versão Processo",
            "tpEmis": "Tipo Emissão",
            "finNFe": "Finalidade NF",
            "natOp": "Natureza Operação",
            "tpNF": "Tipo NF",
            "indPres": "Indicador de Presença",
            "digVal": "Digest Value",
            "infCpl": "Informações Complementares",
            "modFrete": "Modalidade do Frete",
            "FORNECEDORESCNPJ": "CNPJ do Fornecedor",
            "EMPRESACNPJ": "CNPJ da Empresa",
            "TRANSPORTADORACNPJ": "CNPJ da Transportadora",
            "NUMPRODUTOS": "Número de Produtos",
            "NUMDUPLICATAS": "Número de duplicatas",
            "PRIMEIROVENCIMENTO": "Primeiro Vencimento",
            "PATH": "Caminho",
            "DATAADCI": "Data do Cadastro",
            "DATARECEBIDO": "Data do Recebimento",
            "NFobs": "Observação da NF",
            "NFobsdate": "Data para Obs NF",
            "NFobsflag": "Obs Resolvida?",

            "CNFEchNFe": "C. Chave NFe",
            "nFat": "Número da Fatura",
            "vOrig": "Valor Original",
            "vDesc": "Valor Desconto",
            "vLiq": "Valor Liquido",
            "tPag": "Tipo Pagamento",
            "vPag": "Valor Pagamento",

            "VNFEchNFe": "V. Chave NFe",
            "qVol": "Quantidade Volumes",
            "esp": "Espécie",
            "marca": "Marca",
            "nVol": "Número Volumes",
            "pesoL": "Peso Líquido",
            "pesoB": "Peso Bruto",

            "VNFEchNFe": "V. Chave NFe",
            "nDup": "Número Dup",
            "dVenc": "Vencimento da Dup",
            "vDup": "Valor da Dup",
            "DATAPAGAMENTO": "Data Pagamento",
            "FObs": "Observação da Fatura",
            "Fdatalemb": "Data Lembrete da Fatura",
            "FLAGPAGO": "Duplicata Paga?",
            "FobsFlag": "Obs Resolvida?",

            "PNFEchNFe": "P. Chave NFe",
            "nItem": "Número Item",
            "xProd": "Produto",
            "qCom": "Quantidade Com",
            "uCom": "Unidade Com",
            "vProd": "Valor Produto",
            "cProd": "Codigo Produto",
            "NCM": "NCM",
            "CEST": "CEST",
            "EXTIPI": "EX_TIPI",
            "CFOP": "Codigo Fiscal",
            "vOutro": "Valor Outros",
            "vDesc": "Valor Desconto",
            "vFrete": "Valor Frete",
            "vSeg": "Valor Seguro",
            "cEANTrib": "GTIN",
            "uTrib": "Unidade Tri",
            "qTrib": "Quantidade Tri",
            "vUnCom": "Valor Uni Com",
            "vUnTrib": "Valor Uni Tri",
            "vTotTrib": "Valor Total Tri",
            "infAdProd": "Informação Adicional Produto",

            "TOvBC": "Somatório BC",
            "TOvICMS": "Somatório ICMS",
            "TOvICMSDeson": "Somatório ICMS Desonerado",
            "TOvFCPUFDest": "Somatório ICMS Do FCP",
            "TOvICMSUFDest": "Somatório ICMS Inter. Dest",
            "TOvICMSUFRemet": "Somatório ICMS Inter. Reme",
            "TOvFCP": "Somatório FCP",
            "TOvBCST": "Somatório BC ST",
            "TOvST": "Somatório ICMS ST",
            "TOvFCPST": "Somatório FCP Subs.",
            "TOvFCPSTRet": "Somatório FCP Subs. Retido ",
            "TOvProd": "Somatório Valor Produtos",
            "TOvFrete": "Somatório Valor Frete",
            "TOvSeg": "Somatório Valor Seguro",
            "TOvDesc": "Somatório Valor Desconto",
            "TOvII": "Somatório II",
            "TOvIPI": "Somatório Valor IPI",
            "TOvIPIDevol": "Somatório Valor IPI Devolvido",
            "TOvPIS": "Somatório Valor PIS",
            "TOvCOFINS": "Somatório Valor COFINS",
            "TOvOutro": "Somatório Outros Valores",
            "TOvNF": "Valor Total da NF",
            "TOvTotTrib": "Somatório Valor Total Tributos",

            "orig": "Origem",
            "modBC": "Modalidade BC",
            "vBC": "Valor BC",
            "pICMS": "Alíquota ICMS",
            "vICMS": "Valor ICMS",
            "vBCST": "Valor BC",
            "pICMSST": "Alíquota ICMS ST",
            "vICMSST": "Valor ICMS ST",
            "pMVAST": "Percentual Margem",
            "modBCST": "Modalidade BC ST",
            "cEnq": "Codigo Enquadramento",
            "cSelo": "Codigo Selo",
            "CNPJProd": "CNPJ Produto",
            "qSelo": "Quantidade Selo",
            "CST": "CST",
            "vIPI": "Valor IPI",
            "pIPI": "Alíquota IPI",

            "PISCST": "PIS CST",
            "PISvBC": "PIS Valor BC",
            "pPIS": "PIS Alíquota PIS",
            "vPIS": "PIS Valor PIS",

            "COFINSCST": "COFINS CST",
            "COFINSvBC": "COFINS Valor BC",
            "pCOFINS": "COFINS Alíquota COFINS",
            "vCOFINS": "COFINS Valor COFINS",
        }

        try:
            self.config_dict = json.load(open(self.path, "r", encoding="utf-8"))
            for key, value in init_dict.items():
                if key not in list(self.config_dict.keys()):
                    self.self.config_dict[key] = value
                    json.dump(self.config_dict, open(self.path, "w", encoding="utf-8"), ensure_ascii=False)
        except:
            self.config_dict = init_dict
            json.dump(self.config_dict, open(self.path, "w", encoding="utf-8"), ensure_ascii=False)

    def change_config(self, dict_):
        for key, value in dict_.items():
            if key in list(self.config_dict.keys()):
                self.config_dict[key] = value
        json.dump(self.config_dict, open(self.path, "w", encoding="utf-8"), ensure_ascii=False)

    def get_config(self, column_):
        self.config_dict = json.load(open(self.path, "r", encoding="utf-8"))
        return self.config_dict[column_]

    def translate_column_names(self, columns_, detranslate_=False):
        reversed_translate = {v: k for k, v in self.translate.items()}
        header_names = list(columns_)
        for index, column_name in enumerate(header_names):
            if detranslate_:
                if column_name in list(self.translate.values()):
                    header_names[index] = reversed_translate[column_name]
            else:
                if column_name in list(self.translate.keys()):
                    header_names[index] = self.translate[column_name]
        return header_names

