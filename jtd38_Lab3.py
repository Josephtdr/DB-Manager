import sqlite3
import re
from employee import Employee 
import sys
import os 

class DBOperations:
    DATABASENAME = 'ABCdb.db'
    DEFAULTTABLENAME = 'Employee'
    DEFAULTTABLECOLUMNS = 'ID INTEGER PRIMARY KEY, Title VARCHAR(5), Forename VARCHAR(20), Surname VARCHAR(20), Email VARCHAR(20) NOT NULL, Salary int UNSIGNED NOT NULL'

    sql_createTable = '''create table if not exists
                {}({});'''
    

    curTable = ''

    def openConnection(self):
        self.conn = sqlite3.connect(self.DATABASENAME)
        self.cur = self.conn.cursor()

    def createTable(self):
        '''
        TODO: the below shit
        using sqlite3.complete_statement(buffer):
        Like the buffer they give, 
        1. enter column name
        2. enter variable type, till valid vairable type
        3. enter not null
        4. enter primary key or reference
        5. loop back to 1 (break on blank enter)
        '''
        tablename=''
        columns=''
        if not tablename: tablename = self.DEFAULTTABLENAME 
        if not columns: columns = self.DEFAULTTABLECOLUMNS 
        try:
            self.openConnection()
            if(self.tableExists(tablename)):
                print("\nThis table is already created")
                input("Press enter to continue...")
            else:
                self.cur.execute(self.sql_createTable.format(tablename, columns))
                self.conn.commit()
                print("\nTable created successfully")
                input("Press enter to continue...")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def createRecord(self):
        newRecord = globals()[self.curTable]()
        newRecord.create_record()
        sqlInsert = newRecord.getSqlInsert()
        data = newRecord.getData()
        try:
            self.openConnection()
            self.cur.execute(sqlInsert, data)
            self.conn.commit()
            print("Inserted data successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def displayAll(self): #Dynamic
        command = "select * from {}".format(self.curTable)
        try:
            self.openConnection()
            self.cur.execute(command)
            results = self.cur.fetchall()
            headers = self.getHeaders(self.curTable)

            self.displayNeat(headers, results, "{} Table:".format(self.curTable))
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def basicQueryDatabase(self): #Dynamic
        command = "select * from {} where ".format(self.curTable)
        try:
            self.openConnection()
            headers = self.getHeaders(self.curTable)
            queries, values = getUserQueryStuff(headers)
            command += " and ".join(queries)
            self.cur.execute(command, values)
            results = self.cur.fetchall()

            cls()
            if len(results)==0:
                print("\nNo Records")
            else: 
                self.displayNeat(headers, results, "Query:")

        except Exception as e:
            print(e)

        finally:
            self.conn.close()

    def updateRecord(self):
        command = "update {} SET ".format(self.curTable)
        try:
            self.openConnection()
            queries, valuesU = getUserQueryStuff(self.getHeaders(self.curTable), "UPDATE", "U")
            command += ", ".join(queries)
            queries, valuesW = getUserQueryStuff(self.getHeaders(self.curTable))
            command += " where %s;" % (" and ".join(queries))
            self.cur.execute(command, valuesU | valuesW)

            if self.conn.total_changes != 0:
                print("\n%d row(s) to be updated" % self.conn.total_changes)
                if not confirmAction():
                    self.conn.commit()
                else:
                    print("Cancelling!")
            else:
                print("\nNo records found")
        except Exception as e:
            print(e)
            print(command)
        finally:
            self.conn.close()

    def deleteRecord(self): #Dynamic
        command = "delete from {} where ".format(self.curTable)
        try:
            self.openConnection()
            queries, values = getUserQueryStuff(self.getHeaders(self.curTable))
            command += " and ".join(queries)
            self.cur.execute(command, values)
            

            if self.conn.total_changes != 0:
                print("\n%d row(s) to be deleted" % self.conn.total_changes)
                if not confirmAction():
                    self.conn.commit()
                else:
                    print("Cancelling!")
            else:
                print("\nNo records found")
        except Exception as e:
            print(e)
            print(command)

        finally:
            self.conn.close()

    def manualQuery(self):
        pass

    def dropTable(self): #Dynamic
        if confirmAction("DROP {}".format(self.curTable), "Type exactly '{}' to confirm! "):
            try:
                self.openConnection()
                self.cur.execute("drop table {};".format(self.curTable))
                self.conn.commit()
                print("{} table dropped!".format(self.curTable))
                return True
            except Exception as e:
                print(e)
            finally:
                self.conn.close()        
        else:
            print("\nCancelling!")
            return False

#USEFUL FUNCTIONS-----------------------------------------------------
    def tableExists(self, table): #Dynamic
        command = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table)
        self.cur.execute(command)
        return True if len(self.cur.fetchall())!=0 else False
    
    def getHeaders(self, table):
        try:
            self.openConnection()
            self.cur.execute("select * from {};".format(table))
            return [i[0] for i in self.cur.description] #list of headers
        except Exception as e:
            print(e)

    def getTables(self):
        try:
            self.openConnection()
            self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cur.fetchall()
            return [i[0] for i in tables]
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def setCurrentTable(self, table):
        self.curTable = table

    def displayNeat(self, headers, results, title):
        #conv results to relavent obj
        results = [globals()[self.curTable](*row) for row in results]
        results = [row.getDataStr() for row in results]
        f = ''
        for i in range(len(headers)):
            values = [len(headers[i])] + [len(str(row[i])) for row in results]
            f += '{%d:<%d}' % (i, max(values)+1)

        print("\n{}".format(title))
        print(f.format(*headers))
        for row in results:
            print(f.format(*row))

#STATIC FUNCTIONS-----------------------------------------------------
def getUserQueryStuff(headers, reason="WHERE", append = "W"):
    heads = getUserHeaderSelection(headers, reason)

    queries = []
    values = {}
    for i in heads: 
        head = headers[int(i)-1]
        value = input("Please input the value for {}: ".format(head)) 
        queries.append("{0}=:{0}{1}".format(head, append))
        values["{}{}".format(head, append)] = value
    return queries, values

def getUserHeaderSelection(headers, reason):
    headersNUM = [str(x+1) for x in list(range(len(headers)))]
    selecString = ", ".join(["[{}]{}".format(i+1, headers[i]) for i in range(len(headers))])

    print("\n" + selecString) #prints the numerated options of headers to choose from
    userInput = input("Please input all headers (seperated by space) for {} query: ".format(reason))
    
    heads = list(filter(None, userInput.split(" ")))
    while True:
        try:
            if any(x not in headersNUM for x in heads) or not userInput:
                raise TypeError
            elif any(heads.count(x) > 1 for x in heads):
                raise IndexError
            break
        except TypeError: #kinda just raised random errors ngl
            userInput = input("Please input valid intgers: ")
        except IndexError:
            userInput = input("Please input non duplicate intgers: ")
        finally:
            heads = list(filter(None, userInput.split(" ")))
    return heads

def confirmAction(confMsg = "exit", warning = "Type '{}' to cancel! "):
    value = input(warning.format(confMsg))
    return True if value == confMsg else False

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#---------------------------menus--------------------------------
def menu1():
    db_ops = DBOperations()

    while(True):
        tables = db_ops.getTables()
        tableLen = len(tables)
        print ("\n  Menu:")
        print ("*" * (len("  Menu:")+2))
        print (" 1. Create (new) table Employee")
        for i, table in enumerate(tables):
            print(" {}. Interact with {} table".format(i+2, table))
        print (" {}. Exit".format(2 + tableLen))


        choice = input("Enter your choice: ")
        while(not choice.isdigit() or int(choice) not in list(range(1, 3+tableLen))):
            choice = input("Please enter a valid choice: ")
        else:
            choice = int(choice)
            if choice == 1:
                db_ops.createTable()
            elif choice > 1 and choice < 2+tableLen:
                cls()
                menu2(tables[choice-2], db_ops)
            elif choice == 2+tableLen:
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
        cls()

def menu2(table, db_ops):
    db_ops.setCurrentTable(table)

    display = False
    while(True):
        if display:
            db_ops.displayAll()

        print ("\n   {} Table Menu:".format(table))
        print ("*" * (len("   {} Table Menu:".format(table))+3))
        print (" 1. Toggle {} table Visbility".format(table))
        print (" 2. Query %s for records" % table)
        print (" 3. Create record")
        print (" 4. Update record(s)")
        print (" 5. Delete record(s)")
        print (" 6. Manual SQL Query (WARNING)")
        print (" 7. Drop table (WARNING DATA CANNOT BE RECOVERED)")
        print (" 8. Return to main menu")

        choice = input("Enter your choice: ")
        while(choice not in ['1','2','3','4','5','6','7','8']):
            choice = input("Please enter a valid choice: ")
        if choice == '1':
            cls()
            display = False if display else True
        elif choice == '2':
            db_ops.basicQueryDatabase()
            '''
            TODO: Advanced query with functionality such as
                  >, <, like, count({column}), group by, having
            '''
        elif choice == '3':
            db_ops.createRecord()
            input("\nPress enter to continue...")
            cls()
        elif choice == '4':
            db_ops.updateRecord()
            cls()
        elif choice == '5':
            db_ops.deleteRecord()
            cls()
        elif choice == '6':
            #TODO: THIS V
            db_ops.manualQuery()
        elif choice == '7':
            if(db_ops.dropTable()):
                break
            else:
                input("\nPress enter to continue...")
                cls()
        elif choice == '8':
            break;

if __name__ == '__main__':
    try:
        menu1()
    except KeyboardInterrupt:
        print('\nInterrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)