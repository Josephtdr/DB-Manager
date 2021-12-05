import sqlite3
from employee import Employee 
from TableOperations import TableOperations

class DBOperations:
    databaseName = 'ABCdb.db'
    SQL_createTable = '''create table if not exists
                {}({});'''

    tableObjDict = {
            "Employee": Employee
    }
    
    def openTable(self, table):
        self.Table = TableOperations(table, 
                        self.tableObjDict[table], 
                        self.databaseName)

    def createTable(self, table):
        tmpObj = self.tableObjDict[table]()
        tableName = tmpObj.tableName
        columns = tmpObj.tableColumns
        try:
            self.openConnection()
            if(self.tableExists(tableName)):
                return False
            else:
                self.cur.execute(self.SQL_createTable.format(tableName, columns))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def openConnection(self):
        self.conn = sqlite3.connect(self.databaseName)
        self.cur = self.conn.cursor()

    def tableExists(self, table):
        SQL_checkTable = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table)
        self.cur.execute(SQL_checkTable)
        return True if len(self.cur.fetchall())!=0 else False

    def getTables(self):
        SQL_getTables = "SELECT name FROM sqlite_master WHERE type='table';"
        try:
            self.openConnection()
            self.cur.execute(SQL_getTables)
            tables = self.cur.fetchall()
            return [i[0] for i in tables]
        except Exception as e:
            print(e)
        finally:
            self.conn.close()