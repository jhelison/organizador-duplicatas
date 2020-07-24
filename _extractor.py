import xmltodict
import os
import _sqlite_handler
from datetime import datetime, date

# data_base = _sqlite_handler.new_sql_connection()
class extractor():
    def __init__(self, data_base):
        self.data_base = data_base

        if self.data_base.get_tables_list() == []:
            self.data_base.execute("""
            CREATE TABLE FORNECEDORES (
                FID INTEGER PRIMARY KEY AUTOINCREMENT,
                FCNPJCPF TEXT NOT NULL UNIQUE,
                FxNome TEXT,
                FxFant TEXT,
                FxLgrnroxCpl TEXT,
                FxBairro TEXT,
                FCEP INTEGER,
                FxMun TEXT,
                Ffone TEXT,
                FUF TEXT,
                FxPais TEXT,
                FIE TEXT,
                FIEST TEXT,
                FIM TEXT,
                FcMun TEXT,
                FCNAE TEXT,
                FCRT TEXT
            )
            """)
            self.data_base.execute("""
            CREATE TABLE EMPRESA (
                EID INTEGER PRIMARY KEY AUTOINCREMENT,
                ECNPJCPF TEXT NOT NULL UNIQUE,
                ExNome TEXT,
                ExLgrnroxCpl TEXT,
                ExBairro TEXT,
                ECEP INTEGER,
                ExMun TEXT,
                Efone TEXT,
                EUF TEXT,
                ExPais TEXT,
                EIE TEXT,
                EISUF TEXT,
                Eemail TEXT,
                EindIEDest TEXT,
                EIM TEXT
            )
            """)
            self.data_base.execute("""
            CREATE TABLE TRANSPORTADORA (
                TID INTEGER PRIMARY KEY AUTOINCREMENT,
                TCNPJCPF TEXT NOT NULL UNIQUE,
                TxNome TEXT,
                TIE TEXT,
                TxEnder TEXT,
                TxMun TEXT,
                TUF TEXT
            )
            """)
            self.data_base.execute("""
            CREATE TABLE NFE (
                NFID INTEGER PRIMARY KEY AUTOINCREMENT,
                chNFe TEXT NOT NULL UNIQUE,
                versao TEXT,
                mod	INTEGER,
                serie INTEGER,
                nNF	INTEGER,
                dhEmi TIMESTAMP,
                dhSaiEnt TIMESTAMP,
                procEmi	INTEGER,
                idDest INTEGER,
                indFinal INTEGER,
                verProc	TEXT,
                tpEmis INTEGER,
                finNFe INTEGER,
                natOp TEXT,
                tpNF INTEGER,
                indPres TEXT,
                digVal TEXT,
                infCpl TEXT,
                modFrete TEXT,
                FORNECEDORESCNPJ TEXT,
                EMPRESACNPJ TEXT,
                TRANSPORTADORACNPJ TEXT,
                NUMPRODUTOS INTEGER,
                NUMDUPLICATAS INTEGER DEFAULT 0,
                PRIMEIROVENCIMENTO TIMESTAMP,
                PATH TEXT,
                DATAADCI TIMESTAMP,
                FLAGRECEBIDO INTEGER DEFAULT 0,
                DATARECEBIDO TIMESTAMP,
                NFobs TEXT,
                NFobsdate TIMESTAMP,
                NFobsflag INTEGER DEFAULT 0,
                FOREIGN KEY (FORNECEDORESCNPJ)
                    REFERENCES FORNECEDORES (FCNPJCPF),
                FOREIGN KEY (EMPRESACNPJ)
                    REFERENCES EMPRESA (ECNPJCPF),
                FOREIGN KEY (TRANSPORTADORACNPJ)
                    REFERENCES TRANSPORTADORA (TCNPJCPF)
            )
            """)
            self.data_base.execute("""
            CREATE TABLE TOTAIS (
                TOID INTEGER PRIMARY KEY AUTOINCREMENT,
                TONFEchNFe TEXT NOT NULL UNIQUE,
                TOvBC FLOAT,
                TOvICMS FLOAT,
                TOvICMSDeson FLOAT,
                TOvFCPUFDest FLOAT,
                TOvICMSUFDest FLOAT,
                TOvICMSUFRemet FLOAT,
                TOvFCP FLOAT,
                TOvBCST FLOAT,
                TOvST FLOAT,
                TOvFCPST FLOAT,
                TOvFCPSTRet FLOAT,
                TOvProd FLOAT,
                TOvFrete FLOAT,
                TOvSeg FLOAT,
                TOvDesc FLOAT,
                TOvII FLOAT,
                TOvIPI FLOAT,
                TOvIPIDevol FLOAT,
                TOvPIS FLOAT,
                TOvCOFINS FLOAT,
                TOvOutro FLOAT,
                TOvNF FLOAT,
                TOvTotTrib FLOAT
            )
            """)
            self.data_base.execute("""
            CREATE TABLE COBRANCA (
                CID INTEGER PRIMARY KEY AUTOINCREMENT,
                CNFEchNFe TEXT NOT NULL UNIQUE,
                nFat INTEGER,
                vOrig FLOAT,
                vDesc FLOAT,
                vLiq FLOAT,
                tPag TEXT,
                vPag FLOAT,
                FOREIGN KEY (CNFEchNFe)
                    REFERENCES NFE (chNFe)
            )
            """)
            self.data_base.execute("""
            CREATE TABLE VOLUMES (
                VID INTEGER PRIMARY KEY AUTOINCREMENT,
                VNFEchNFe TEXT NOT NULL,
                qVol INTEGER,
                esp TEXT,
                marca TEXT,
                nVol TEXT,
                pesoL FLOAT,
                pesoB FLOAT,
                FOREIGN KEY (VNFEchNFe)
                    REFERENCES NFE (chNFe)
            )
            """)
            self.data_base.execute("""
            CREATE TABLE FATURAS (
                FAID INTEGER PRIMARY KEY AUTOINCREMENT,
                FNFEchNFe TEXT NOT NULL,
                nDup INTEGER,
                dVenc TIMESTAMP,
                vDup FLOAT,
                DATAPAGAMENTO TIMESTAMP,
                FObs TEXT,
                Fdatalemb TIMESTAMP,
                FLAGPAGO INTEGER DEFAULT 0,
                FobsFlag INTEGER DEFAULT 0,
                FOREIGN KEY (FNFEchNFe)
                    REFERENCES NFE (chNFe)
            )
            """)
            self.data_base.execute("""
            CREATE TABLE PRODUTO (
                PID INTEGER PRIMARY KEY AUTOINCREMENT,
                PNFEchNFe TEXT NOT NULL,
                nItem INTEGER,
                xProd TEXT,
                qCom INTEGER,
                uCom TEXT,
                vProd FLOAT,
                cProd INTEGER,
                NCM INTEGER,
                CEST INTEGER,
                EXTIPI INTEGER,
                CFOP INTEGER,
                vOutro FLOAT,
                vDesc FLOAT,
                vFrete FLOAT,
                vSeg FLOAT,
                cEANTrib INTEGER,
                uTrib TEXT,
                qTrib INTEGER,
                vUnCom FLOAT,
                vUnTrib FLOAT,
                vTotTrib FLOAT,
                infAdProd TEXT,
                FOREIGN KEY (PNFEchNFe)
                    REFERENCES NFE (chNFe)
            )
            """)
            self.data_base.execute("""
            CREATE TABLE PRODUTOICMS (
                PRODUTOID INTEGER PRIMARY KEY AUTOINCREMENT,
                orig INTEGER,
                modBC INTEGER,
                vBC FLOAT,
                pICMS FLOAT,
                vICMS FLOAT,
                vBCST FLOAT,
                pICMSST FLOAT,
                vICMSST FLOAT,
                pMVAST FLOAT,
                modBCST INTEGER,
                cEnq INTEGER,
                cSelo FLOAT,
                CNPJProd TEXT,
                qSelo FLOAT,
                CST INTEGER,
                vIPI FLOAT,
                pIPI FLOAT,
                FOREIGN KEY (PRODUTOID)
                    REFERENCES PRODUTO (PID)
            )
            """)
            self.data_base.execute("""
            CREATE TABLE PRODUTOPIS (
                PISPRODUTOID INTEGER PRIMARY KEY AUTOINCREMENT,
                PISCST INTEGER,
                PISvBC FLOAT,
                pPIS FLOAT,
                vPIS FLOAT,
                FOREIGN KEY (PISPRODUTOID)
                    REFERENCES PRODUTO (PID)
            )
            """)
            self.data_base.execute("""
            CREATE TABLE PRODUTOCOFINS (
                COFINSPRODUTOID INTEGER PRIMARY KEY AUTOINCREMENT,
                COFINSCST INTEGER,
                COFINSvBC FLOAT,
                pCOFINS	FLOAT,
                vCOFINS	FLOAT,
                FOREIGN KEY (COFINSPRODUTOID)
                    REFERENCES PRODUTO (PID)
            )
            """)
            self.data_base.commit_data()

    def get_files_list(self, path_):
        filepaths = {}
        keys_on_database = self.data_base.get_data_from_column("NFE", "chNFe")
        for file in os.listdir(path_):
            filepath = path_ + "\\" + file
            if ".xml" in file:
                try:
                    file = xmltodict.parse(open(filepath, encoding="utf-8").read())
                    chave_nfe = str(file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None))
                    if chave_nfe not in keys_on_database:
                        filepaths[chave_nfe] = filepath
                except:
                    continue
            else:
                continue
        return filepaths
    
        
    def process_file_on_database(self, path_):
        file = xmltodict.parse(open(path_, encoding="utf-8").read())
        #CHECK IF THERES ALREADY THE NF IN THE DATABASE
        empresa = {}
        fornecedor = {}
        transportadora = {}

        #FORNECEDORES
        if str(file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CNPJ", 0)) not in self.data_base.get_data_from_column("FORNECEDORES", "FCNPJCPF"):
            if str(file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CPF", 0)) not in self.data_base.get_data_from_column("FORNECEDORES", "FCNPJCPF"):


                if file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CNPJ", None) != None:
                    fornecedor["FCNPJCPF"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CNPJ", None)
                else:
                    fornecedor["FCNPJCPF"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CPF", None)

                fornecedor["FxNome"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("xNome", None)
                fornecedor["FxFant"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("xFant", None)

                fornecedor["FxLgrnroxCpl"] = (str(file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("xLgr", None)) + ", " +
                                            str(file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("nro", None)) + ", " +
                                            str(file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("xCpl", None)))

                fornecedor["FxBairro"] = file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("xBairro", None)
                fornecedor["FCEP"] = file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("CEP", None)
                fornecedor["FxMun"] = file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("xMun", None)
                fornecedor["Ffone"] = file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("fone", None)
                fornecedor["FUF"] = file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("UF", None)
                fornecedor["FxPais"] = file["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"].get("xPais", None)

                fornecedor["FIE"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("IE", None)
                fornecedor["FIEST"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("IEST", None)
                fornecedor["FIM"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("IM", None)
                fornecedor["FcMun"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("cMun", None)
                fornecedor["FCNAE"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CNAE", None)
                fornecedor["FCRT"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CRT", None)

        #EMPRESAS
        if str(file["nfeProc"]["NFe"]["infNFe"]["dest"].get("CNPJ", 0)) not in self.data_base.get_data_from_column("EMPRESA", "ECNPJCPF"):
            if str(file["nfeProc"]["NFe"]["infNFe"]["dest"].get("CPF", 0)) not in self.data_base.get_data_from_column("EMPRESA", "ECNPJCPF"):

                if file["nfeProc"]["NFe"]["infNFe"]["dest"].get("CNPJ", None) != None:
                    empresa["ECNPJCPF"] = file["nfeProc"]["NFe"]["infNFe"]["dest"].get(
                        "CNPJ", None)
                else:
                    empresa["ECNPJCPF"] = file["nfeProc"]["NFe"]["infNFe"]["dest"].get("CPF", None)

                empresa["ExNome"] = file["nfeProc"]["NFe"]["infNFe"]["dest"].get("xNome", None)

                empresa["ExLgrnroxCpl"] = (str(file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("xLgr", None)) + ", " +
                                            str(file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("nro", None)) + ", " +
                                            str(file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("xCpl", None)))

                empresa["ExBairro"] = file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("xBairro", None)
                empresa["ECEP"] = file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("CEP", None)
                empresa["ExMun"] = file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("xMun", None)
                empresa["Efone"] = file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("fone", None)
                empresa["EUF"] = file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("UF", None)
                empresa["ExPais"] = file["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"].get("xPais", None)

                empresa["EIE"] = file["nfeProc"]["NFe"]["infNFe"]["dest"].get("IE", None)
                empresa["EISUF"] = file["nfeProc"]["NFe"]["infNFe"]["dest"].get("ISUF", None)

                empresa["Eemail"] = file["nfeProc"]["NFe"]["infNFe"]["dest"].get("email", None)

        #TRANSPORTADORAS

        if file["nfeProc"]["NFe"]["infNFe"]["transp"].get("transporta", None) != None:
            if file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("CNPJ", None) != None:
                if str(file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("CNPJ", 0)) not in self.data_base.get_data_from_column("TRANSPORTADORA", "TCNPJCPF"):

                    transportadora["TCNPJCPF"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("CNPJ", 0)
                    transportadora["TxNome"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("xNome", None)
                    transportadora["TIE"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("IE", None)
                    transportadora["TxEnder"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("xEnder", None)
                    transportadora["TxMun"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("xMun", None)
                    transportadora["TUF"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("UF", None)

        #GET NF DATA!_____________________________________________
        NFE = {}

        NFE["chNFe"] = str(file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None))
        NFE["versao"] = str(file["nfeProc"]["NFe"]["infNFe"]["@versao"])
        NFE["mod"] = file["nfeProc"]["NFe"]["infNFe"]["ide"].get("mod", None)
        NFE["serie"] = file["nfeProc"]["NFe"]["infNFe"]["ide"].get("serie", None)
        NFE["indFinal"] = file["nfeProc"]["NFe"]["infNFe"]["ide"].get("indFinal", None)
        NFE["idDest"] = file["nfeProc"]["NFe"]["infNFe"]["ide"].get("idDest", None)
        NFE["nNF"] = file["nfeProc"]["NFe"]["infNFe"]["ide"].get("nNF", None)
        NFE["dhEmi"] = parse_date(file["nfeProc"]["NFe"]["infNFe"]["ide"].get("dhEmi", None)) if file["nfeProc"]["NFe"]["infNFe"]["ide"].get("dhEmi", None) != None else None
        NFE["dhSaiEnt"] = parse_date(file["nfeProc"]["NFe"]["infNFe"]["ide"].get("dhSaiEnt", None)) if file["nfeProc"]["NFe"]["infNFe"]["ide"].get("dhSaiEnt", None) != None else None
        NFE["procEmi"]=file["nfeProc"]["NFe"]["infNFe"]["ide"].get("procEmi", None)
        NFE["verProc"]=file["nfeProc"]["NFe"]["infNFe"]["ide"].get("verProc", None)
        NFE["tpEmis"]=file["nfeProc"]["NFe"]["infNFe"]["ide"].get("tpEmis", None)
        NFE["indPres"] = file["nfeProc"]["NFe"]["infNFe"]["ide"].get("indPres", None)
        NFE["finNFe"]=file["nfeProc"]["NFe"]["infNFe"]["ide"].get("finNFe", None)
        NFE["natOp"]=file["nfeProc"]["NFe"]["infNFe"]["ide"].get("natOp", None)
        NFE["tpNF"]=file["nfeProc"]["NFe"]["infNFe"]["ide"].get("tpNF", None)
        NFE["EindIEDest"] = file["nfeProc"]["NFe"]["infNFe"]["ide"].get("EindIEDest", None)
        NFE["EIM"] = file["nfeProc"]["NFe"]["infNFe"]["ide"].get("EIM", None)

        if file["nfeProc"]["NFe"]["infNFe"].get("transp", None) != None:
            NFE["modFrete"] = file["nfeProc"]["NFe"]["infNFe"]["transp"].get("modFrete", None)

        NFE["digVal"]=file["nfeProc"]["protNFe"]["infProt"].get("digVal", None)

        if file["nfeProc"]["NFe"]["infNFe"].get("infAdic", None) != None:
            NFE["infCpl"]=file["nfeProc"]["NFe"]["infNFe"]["infAdic"].get("infCpl", None)

        if file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CNPJ", None) != None: 
            NFE["FORNECEDORESCNPJ"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CNPJ", None)
        else:
            NFE["FORNECEDORESCNPJ"] = file["nfeProc"]["NFe"]["infNFe"]["emit"].get("CPF", None)

        if file["nfeProc"]["NFe"]["infNFe"]["dest"].get("CNPJ", None) != None:
            NFE["EMPRESACNPJ"] = file["nfeProc"]["NFe"]["infNFe"]["dest"].get("CNPJ", None)
        else:
            NFE["EMPRESACNPJ"] = file["nfeProc"]["NFe"]["infNFe"]["dest"].get("CPF", None)


        if file["nfeProc"]["NFe"]["infNFe"]["transp"].get("transporta", None) != None:
            if file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("CNPJ", None) != None:
                NFE["TRANSPORTADORACNPJ"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["transporta"].get("CNPJ", None)
        
        if type(file["nfeProc"]["NFe"]["infNFe"]["det"]) == list:
            NFE["NUMPRODUTOS"] = len(file["nfeProc"]["NFe"]["infNFe"]["det"])
        else:
            NFE["NUMPRODUTOS"] = 1

        if file["nfeProc"]["NFe"]["infNFe"].get("cobr", None) != None:
            if file["nfeProc"]["NFe"]["infNFe"]["cobr"].get("dup", None) != None:
                if type(file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"]) == list:
                    NFE["NUMDUPLICATAS"] = len(file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"])
                    NFE["PRIMEIROVENCIMENTO"] = parse_date(file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][0].get("dVenc", None), True) if file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][0].get("dVenc", None) != None else None
                else:
                    NFE["NUMDUPLICATAS"] = 1
                    NFE["PRIMEIROVENCIMENTO"] = parse_date(file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"].get("dVenc", None), True) if file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"].get("dVenc", None) != None else None
        
        NFE["PATH"] = path_
        NFE["DATAADCI"] = datetime.now()
                

        #COBRANÇA___________________________________
        cobranca = {}
        cobranca["CNFEchNFe"] = file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None)
        if file["nfeProc"]["NFe"]["infNFe"].get("cobr", None) != None:
            cobranca["nFat"] = file["nfeProc"]["NFe"]["infNFe"]["cobr"]["fat"].get("nFat", None)
            cobranca["vOrig"] = file["nfeProc"]["NFe"]["infNFe"]["cobr"]["fat"].get("vOrig", None)
            cobranca["vDesc"] = file["nfeProc"]["NFe"]["infNFe"]["cobr"]["fat"].get("vDesc", None)
            cobranca["vLiq"] = file["nfeProc"]["NFe"]["infNFe"]["cobr"]["fat"].get("vLiq", None)

        if type(file["nfeProc"]["NFe"]["infNFe"]["pag"]["detPag"]) == list:
            cobranca["tPag"] = tipo_pagamento(file["nfeProc"]["NFe"]["infNFe"]["pag"]["detPag"][0].get("tPag", None))
            cobranca["vPag"] = file["nfeProc"]["NFe"]["infNFe"]["pag"]["detPag"][0].get("vPag", None)
        else:
            cobranca["tPag"] = tipo_pagamento(file["nfeProc"]["NFe"]["infNFe"]["pag"]["detPag"].get("tPag", None))
            cobranca["vPag"] = file["nfeProc"]["NFe"]["infNFe"]["pag"]["detPag"].get("vPag", None)


        #TOTAIS________________________________________________________________
        totais = {}
        totais["TONFEchNFe"] = file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None)

        totais["TOvBC"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vBC", None)
        totais["TOvICMS"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vICMS", None)
        totais["TOvICMSDeson"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vICMSDeson", None)
        totais["TOvFCPUFDest"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vFCPUFDest", None)
        totais["TOvICMSUFDest"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vICMSUFDest", None)
        totais["TOvICMSUFRemet"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vICMSUFRemet", None)
        totais["TOvFCP"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vFCP", None)
        totais["TOvBCST"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vBCST", None)
        totais["TOvST"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vST", None)
        totais["TOvFCPST"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vFCPST", None)
        totais["TOvFCPSTRet"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vFCPSTRet", None)
        totais["TOvProd"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vProd", None)
        totais["TOvFrete"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vFrete", None)
        totais["TOvSeg"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vSeg", None)
        totais["TOvDesc"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vDesc", None)
        totais["TOvII"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vII", None)
        totais["TOvIPI"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vIPI", None)
        totais["TOvIPIDevol"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vIPIDevol", None)
        totais["TOvPIS"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vPIS", None)
        totais["TOvCOFINS"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vCOFINS", None)
        totais["TOvOutro"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vOutro", None)
        totais["TOvNF"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vNF", None)
        totais["TOvTotTrib"] = file["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"].get("vTotTrib", None)



        #VOLUMES_______________________________________________________________

        if file["nfeProc"]["NFe"]["infNFe"]["transp"].get("vol", None) != None:
            if type(file["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"]) == list:
                for volume in file["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"]:
                    volumes = {}
                    volumes["VNFEchNFe"] = file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None)
                    volumes["qVol"] = volume.get("qVol", None)
                    volumes["esp"] = volume.get("esp", None)
                    volumes["marca"] = volume.get("marca", None)
                    volumes["nVol"] = volume.get("nVol", None)
                    volumes["pesoL"] = volume.get("pesoL", None)
                    volumes["pesoB"] = volume.get("pesoB", None)
                    self.data_base.insert_from_dict("VOLUMES", volumes)
            else:
                volumes = {}
                volumes["VNFEchNFe"] = file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None)
                volumes["qVol"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"].get("qVol", None)
                volumes["esp"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"].get("esp", None)
                volumes["marca"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"].get("marca", None)
                volumes["nVol"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"].get("nVol", None)
                volumes["pesoL"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"].get("pesoL", None)
                volumes["pesoB"] = file["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"].get("pesoB", None)
                self.data_base.insert_from_dict("VOLUMES", volumes)

        #FAUTRA_____________________________________________________________
        if file["nfeProc"]["NFe"]["infNFe"].get("cobr", None) != None:
            if file["nfeProc"]["NFe"]["infNFe"]["cobr"].get("dup", None) != None:
                if type(file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"]) == list:
                    for index in range(len(file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"])):
                        fatura = {}
                        fatura["FNFEchNFe"] = file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None)
                        fatura["nDup"] = file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][index].get("nDup", None)
                        fatura["dVenc"] = parse_date(file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][index].get("dVenc", None), True) if file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][index].get("dVenc", None) != None else None
                        fatura["vDup"] = file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][index].get("vDup", None)
                        self.data_base.insert_from_dict("FATURAS", fatura)
                else:
                    fatura = {}
                    fatura["FNFEchNFe"] = file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None)
                    fatura["nDup"] = file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"].get("nDup", None)
                    fatura["dVenc"] = parse_date(file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"].get("dVenc", None), True) if file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"].get("dVenc", None) != None else None
                    fatura["vDup"] = file["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"].get("vDup", None)
                    self.data_base.insert_from_dict("FATURAS", fatura)

        #PRODUTOS__________________________________________________________________________________
        if type(file["nfeProc"]["NFe"]["infNFe"]["det"]) == list:
            for index in range(len(file["nfeProc"]["NFe"]["infNFe"]["det"])):
                produto = {}

                produto["PNFEchNFe"] = file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None)

                produto["nItem"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index].get("@nItem", None)

                produto["xProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("xProd", None)
                produto["qCom"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("qCom", None)
                produto["uCom"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("uCom", None)
                produto["vProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("vProd", None)
                produto["cProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("cProd", None)
                produto["NCM"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("NCM", None)
                produto["CEST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("CEST", None)
                produto["EXTIPI"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("EXTIPI", None)
                produto["CFOP"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("CFOP", None)
                produto["vOutro"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("vOutro", None)
                produto["vDesc"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("vDesc", None)
                produto["vFrete"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("vFrete", None)
                produto["vSeg"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("vSeg", None)
                produto["cEANTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("cEANTrib", None)
                produto["uTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("uTrib", None)
                produto["qTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("qTrib", None)
                produto["vUnCom"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("vUnCom", None)
                produto["vUnTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["prod"].get("vUnTrib", None)

                produto["vTotTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"].get("vTotTrib", None)

                produto["infAdProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index].get("infAdProd", None)

                self.data_base.insert_from_dict("PRODUTO", produto)

                produtoicms = {}

                key = list(dict(file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"]).keys())[0]

                produtoicms["orig"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key]["orig"]
                produtoicms["modBC"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("modBC", None)
                produtoicms["vBC"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("vBC", None)
                produtoicms["pICMS"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("pICMS", None)
                produtoicms["vICMS"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("vICMS", None)
                produtoicms["vBCST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("vBCST", None)
                produtoicms["pICMSST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("pICMSST", None)
                produtoicms["vICMSST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("vICMSST", None)
                produtoicms["pMVAST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("pMVAST", None)
                produtoicms["modBCST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["ICMS"][key].get("modBCST", None)

                if file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"].get("IPI", None) != None:
                    produtoicms["cEnq"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"].get("cEnq", None)
                    produtoicms["cSelo"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"].get("cSelo", None)
                    produtoicms["CNPJProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"].get("CNPJProd", None)
                    produtoicms["qSelo"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"].get("qSelo", None)

                    if file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"].get("IPINT", None) != None:
                        produtoicms["CST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"]["IPINT"].get("CST", None)
                    elif file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"].get("IPITrib", None) != None:
                        produtoicms["CST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"]["IPITrib"].get("CST", None)
                        produtoicms["vIPI"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"]["IPITrib"].get("vIPI", None)
                        produtoicms["pIPI"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["IPI"]["IPITrib"].get("pIPI", None)

                self.data_base.insert_from_dict("PRODUTOICMS", produtoicms)
                
                produtopis = {}

                key = list(dict(file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["PIS"]).keys())[0]
                
                produtopis["PISCST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["PIS"][key]["CST"]
                produtopis["PISvBC"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["PIS"][key].get("vBC", None)
                produtopis["pPIS"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["PIS"][key].get("pPIS", None)
                produtopis["vPIS"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["PIS"][key].get("vPIS", None)

                self.data_base.insert_from_dict("PRODUTOPIS", produtopis)

                produtocofins = {}

                key = list(dict(file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["COFINS"]).keys())[0]

                produtocofins["COFINSCST"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["COFINS"][key]["CST"]
                produtopis["COFINSvBC"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["COFINS"][key].get("vBC", None)
                produtopis["pCOFINS"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["COFINS"][key].get("pCOFINS", None)
                produtopis["vCOFINS"] = file["nfeProc"]["NFe"]["infNFe"]["det"][index]["imposto"]["COFINS"][key].get("vCOFINS", None)

                self.data_base.insert_from_dict("PRODUTOCOFINS", produtocofins)
        else:
            produto = {}

            produto["PNFEchNFe"] = file["nfeProc"]["protNFe"]["infProt"].get("chNFe", None)

            produto["nItem"] = file["nfeProc"]["NFe"]["infNFe"]["det"].get("@nItem", None)

            produto["xProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("xProd", None)
            produto["qCom"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("qCom", None)
            produto["uCom"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("uCom", None)
            produto["vProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("vProd", None)
            produto["cProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("cProd", None)
            produto["NCM"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("NCM", None)
            produto["CEST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("CEST", None)
            produto["EXTIPI"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("EXTIPI", None)
            produto["CFOP"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("CFOP", None)
            produto["vOutro"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("vOutro", None)
            produto["vDesc"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("vDesc", None)
            produto["vFrete"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("vFrete", None)
            produto["vSeg"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("vSeg", None)
            produto["cEANTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("cEANTrib", None)
            produto["uTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("uTrib", None)
            produto["qTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("qTrib", None)
            produto["vUnCom"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("vUnCom", None)
            produto["vUnTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["prod"].get("vUnTrib", None)

            produto["vTotTrib"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"].get("vTotTrib", None)

            produto["infAdProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"].get("infAdProd", None)

            self.data_base.insert_from_dict("PRODUTO", produto)

            produtoicms = {}

            key = list(dict(file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"]).keys())[0]

            produtoicms["orig"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key]["orig"]
            produtoicms["modBC"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("modBC", None)
            produtoicms["vBC"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("vBC", None)
            produtoicms["pICMS"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("pICMS", None)
            produtoicms["vICMS"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("vICMS", None)
            produtoicms["vBCST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("vBCST", None)
            produtoicms["pICMSST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("pICMSST", None)
            produtoicms["vICMSST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("vICMSST", None)
            produtoicms["pMVAST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("pMVAST", None)
            produtoicms["modBCST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["ICMS"][key].get("modBCST", None)

            if file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"].get("IPI", None) != None:
                produtoicms["cEnq"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"].get("cEnq", None)
                produtoicms["cSelo"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"].get("cSelo", None)
                produtoicms["CNPJProd"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"].get("CNPJProd", None)
                produtoicms["qSelo"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"].get("qSelo", None)

                if file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"].get("IPINT", None) != None:
                    produtoicms["CST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"]["IPINT"].get("CST", None)
                elif file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"].get("IPITrib", None) != None:
                    produtoicms["CST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"]["IPITrib"].get("CST", None)
                    produtoicms["vIPI"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"]["IPITrib"].get("vIPI", None)
                    produtoicms["pIPI"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["IPI"]["IPITrib"].get("pIPI", None)

            self.data_base.insert_from_dict("PRODUTOICMS", produtoicms)
            
            produtopis = {}

            key = list(dict(file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["PIS"]).keys())[0]
            
            produtopis["PISCST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["PIS"][key]["CST"]
            produtopis["PISvBC"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["PIS"][key].get("vBC", None)
            produtopis["pPIS"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["PIS"][key].get("pPIS", None)
            produtopis["vPIS"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["PIS"][key].get("vPIS", None)

            self.data_base.insert_from_dict("PRODUTOPIS", produtopis)

            produtocofins = {}

            key = list(dict(file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["COFINS"]).keys())[0]

            produtocofins["COFINSCST"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["COFINS"][key]["CST"]
            produtopis["COFINSvBC"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["COFINS"][key].get("vBC", None)
            produtopis["pCOFINS"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["COFINS"][key].get("pCOFINS", None)
            produtopis["vCOFINS"] = file["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]["COFINS"][key].get("vCOFINS", None)

            self.data_base.insert_from_dict("PRODUTOCOFINS", produtocofins)

        if bool(fornecedor):
            self.data_base.insert_from_dict("FORNECEDORES", fornecedor)
        if bool(empresa):
            self.data_base.insert_from_dict("EMPRESA", empresa)
        if bool(transportadora):
            self.data_base.insert_from_dict("TRANSPORTADORA", transportadora)

        self.data_base.insert_from_dict("COBRANCA", cobranca)
        self.data_base.insert_from_dict("TOTAIS", totais)
        self.data_base.insert_from_dict("NFE", NFE) #NOT NEED TO COMMIT UNTILL THE ENDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
        self.data_base.commit_data()


def tipo_pagamento(tpag):
    if int(tpag) == 1:
        return 'Dinheiro'
    elif int(tpag) == 2:
        return 'Cheque'
    elif int(tpag) == 3:
        return 'Cartão de Crédito'
    elif int(tpag) == 4:
        return 'Cartão de Débito'
    elif int(tpag) == 5:
        return 'Crédito Loja'
    elif int(tpag) == 10:
        return 'Vale Alimentação'
    elif int(tpag) == 11:
        return 'Vale Refeição'
    elif int(tpag) == 12:
        return 'Vale Presente'
    elif int(tpag) == 13:
        return 'Vale Combustível'
    elif int(tpag) == 14:
        return "Duplicata Mercantil"
    elif int(tpag) == 15:
        return 'Boleto'
    elif int(tpag) == 90:
        return 'Sem Pagamento'
    elif int(tpag) == 99:
        return 'Outros'
    else:
        return 'ERROR' + str(tpag)

def parse_date(text_, onlyDate_=False):
    if onlyDate_:
        return datetime(
            int(text_[:4]),
            int(text_[5:7]),
            int(text_[8:10])
        )
    else:
        return datetime(
            int(text_[:4]),
            int(text_[5:7]),
            int(text_[8:10]),
            int(text_[11:13]),
            int(text_[14:16]),
            int(text_[17:19])
        )



