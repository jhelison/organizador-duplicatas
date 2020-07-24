import sqlite3
import os
from datetime import datetime

class new_sql_connection:

    def __init__(self, path_= str(os.getcwd()) + "\\database.db"):
        self.con = sqlite3.connect(path_)
        self.cur = self.con.cursor()
        super().__init__()

    def get_tables_list(self): #WORKING
        sql = ("""
        SELECT
            name
        FROM
            sqlite_master
        WHERE 
            type='table'
        """)
        tables = self.cur.execute(sql).fetchall()
        for index, table in enumerate(tables):
            tables[index] = table[0]
        return tables

    def get_columns_from_table(self, table_name_): #WORKING
        sql = ("""
        PRAGMA table_info(%s)
        """ % table_name_)
        columns = self.cur.execute(sql).fetchall()
        for index, column in enumerate(columns):
            columns[index] = column[1]
        return columns

    def get_data_from_table(self, table_name_, column_="*"): #WORKING
        sql = ("""
        SELECT
            %s
        FROM
            %s
        """ % (column_, table_name_))
        return self.cur.execute(sql).fetchall()

    def get_table_info(self, table_name_): #working
        sql = ("""
        PRAGMA table_info(%s)
        """ % table_name_)
        return self.cur.execute(sql).fetchall()

    def get_column_type_name(self, table_name_, column_): #working
        for index, info in enumerate(self.get_table_info(table_name_)):
            if column_ == info[1]:
                return info[2]
                break
        return None

    def get_key_column_name(self, table_name_): #working
        for index, info in enumerate(self.get_table_info(table_name_)):
            if info[-1] == 1:
                return info[1]
                break

    def get_key_column_index(self, table_name_): #working
        for index, info in enumerate(self.get_table_info(table_name_)):
            if info[-1] == 1:
                return info[0]
                break
        
    def update_single_data(self, table_name_, column_, data_, index_): #need futher testing
        key_column = self.get_key_column_name(table_name_)
        sql = ("""
        UPDATE
            %s
        SET
            %s = \'%s\'
        WHERE
            %s = \'%s\'
        """ % (table_name_, column_, data_, key_column, index_))
        self.cur.execute(sql)

    def update_data_in_bulk_index(self, table_name_, column_, data_, indexes_): #need further testing
        key_column = self.get_key_column_name(table_name_)
        for index in indexes_:
            sql = ("""
            UPDATE
                %s
            SET
                %s = \'%s\'
            WHERE
                %s = \'%s\'
            """ % (table_name_, column_, data_, key_column, index))
            self.cur.execute(sql)

    def get_column_index(self, table_name_, column_): #working
        columns = self.get_columns_from_table(table_name_)
        for index, column in enumerate(columns):
            if column_ == column:
                return index
                break

    def get_data_from_column(self, table_name_, column_): #working
        sql = ("""
        SELECT
            %s
        FROM
            %s
        """ % (column_, table_name_))
        return [item[0] for item in self.cur.execute(sql).fetchall()]


    def update_all_data_in_column(self, table_name_, column_, data_): #working
        sql = ("""
        UPDATE
            %s
        SET
            %s = \'%s\'
        """ % (table_name_, column_, data_))
        self.cur.execute(sql)

    def execute(self, sql_):
        self.cur.execute(sql_)

    def commit_data(self): #working
        self.con.commit()

    def insert_from_dict(self,table_name_, dict_):
        columns_string = "("
        data_string = "("
        for k,v in dict_.items():
            if v == None:
                continue
            columns_string = columns_string + k + ","
            data_string = data_string + "\'" + str(v).replace("\'", "\'\'") + "\'" + ","
        columns_string = columns_string[:-1] + ")"
        data_string = data_string[:-1] + ")"
        sql = ("""
        INSERT INTO
            %s %s
        VALUES
            %s
        """ % (table_name_, columns_string, data_string))
        self.cur.execute(sql)

    def get_data_from_tables_left_join(self, main_table_, table_logic_, filter_columns_ = []):
        text_filter_columns = ""
        if filter_columns_ == []:
            text_filter_columns = "*"
        else:
            for column in filter_columns_:
                text_filter_columns += column + ","
            text_filter_columns = text_filter_columns[:-1]
        pass

        text_table_logic = ""
        for key, value in table_logic_.items():
            text_table_logic += "LEFT JOIN "
            text_table_logic += key + " ON " + value[0] + "=" + value[1] + " "

        sql = ("""
        SELECT
            %s
        FROM
            %s
        %s
        """ % (text_filter_columns, main_table_, text_table_logic))
        return self.cur.execute(sql).fetchall()

    def get_columns_from_multiple_tables(self, tables_):
        columns = []
        for table in tables_:
            columns += self.get_columns_from_table(table)
        return columns

    def get_type_from_multiple_tables(self, tables_, column_):
        for table in tables_:
            if self.get_column_type_name(table, column_) != None:
                return self.get_column_type_name(table, column_)
                break


    

