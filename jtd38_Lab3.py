import enum
import sqlite3
import re
from employee import Employee 
import sys
import os 

class DBOperations:
    EMAILREGEX = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    TITLEREGEX = "\\b(Mr|Mrs|Ms|Miss|Dr|Sir|They|Them)\\b" #pronouns ik but idk
    DATABASENAME = 'ABCdb.db'
    DEFAULTTABLENAME = 'Employee'
    DEFAULTTABLECOLUMNS = 'ID INTEGER PRIMARY KEY, Title VARCHAR(5), Forename VARCHAR(20), Surname VARCHAR(20), Email VARCHAR(20) NOT NULL, Salary int UNSIGNED NOT NULL'

    sql_createTable = '''create table if not exists
                {}({});'''
    sql_select_all = "select * from {}"

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

    def createRecord(self, table):
        sql_insert = "insert into {} values (".format(table)
        values = []
        try:
            self.openConnection()
            self.cur.execute('PRAGMA TABLE_INFO({})'.format(table))
            results = self.cur.fetchall()

            for _, name, dataType, notNull, _, pk in results:
                if pk==1:
                    sql_insert += "null"
                else:
                    sql_insert += ',?'
                    values.append(self.dataValidation(name, dataType, notNull))
            sql_insert += ')'
            self.cur.execute(sql_insert, values)    
            self.conn.commit()
            print("Inserted data successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def dataValidation(self, name, dataType, notNull):
        value = input("Please input {} ".format(name))

        if dataType=='int UNSIGNED':
            func = self.intCheck
        elif name=='Email':
            func = self.emailCheck
        elif name=='Title':
            func = self.titleCheck
        elif notNull==1:
            func = self.nullCheck
        else:
            return value

        while(func(value)):
            value = input("Please input a valid {}: ".format(name))
        return value
        
    def intCheck(self, x):
        return not x.isdigit()

    def emailCheck(self, x):
        return re.search(self.EMAILREGEX, x) is None

    def titleCheck(self, x):
        return re.search(self.TITLEREGEX, x) is None

    def nullCheck(self, x):
        return x == ''


    def insert_employee_data(self, table):
        #TODO: generalise
        newemp = Employee()
        emp_insert = "insert into Employee values (null,?,?,?,?,?)"

        try:
            self.openConnection()
            self.cur.execute(emp_insert, newemp.getData())
            self.conn.commit()
            print("Inserted data successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def displayAll(self, table): #Dynamic
        try:
            self.openConnection()
            self.cur.execute(self.sql_select_all.format(table))
            results = self.cur.fetchall()
            headers = self.getHeaders(table)

            DisplayNeat(headers, results, "{} Table:".format(table))
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def queryDatabase(self, table): #Dynamic
        command = "select * from {} where ".format(table)
        try:
            self.openConnection()
            headers = self.getHeaders(table)
            queries = getUserQueryStuff(headers)
            command += " and ".join(queries)
            self.cur.execute(command)
            results = self.cur.fetchall()

            cls()
            if len(results)==0:
                print("\nNo Records")
            else: 
                DisplayNeat(headers, results, "Query:")

        except Exception as e:
            print(command)
            print(e)

        finally:
            self.conn.close()

    def updateRecord(self, table):
        command = "update {} SET ".format(table)
        try:
            self.openConnection()
            queries = getUserQueryStuff(self.getHeaders(table), "UPDATE")
            command += ", ".join(queries)
            queries = getUserQueryStuff(self.getHeaders(table))
            command += " where %s;" % (" and ".join(queries))
            self.cur.execute(command)

            if self.conn.total_changes != 0:
                print("\n%d row(s) to be updated" % self.conn.total_changes)
                if confirmAction():
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

    def deleteRecord(self, table): #Dynamic
        command = "delete from {} where ".format(table)
        try:
            self.openConnection()
            queries = getUserQueryStuff(self.getHeaders(table))
            command += " and ".join(queries)
            self.cur.execute(command)
            

            if self.conn.total_changes != 0:
                print("\n%d row(s) to be deleted" % self.conn.total_changes)
                if confirmAction():
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

    def manualQuery(self, table):
        pass

    def dropTable(self, table): #Dynamic
        if confirmAction("DROP {}".format(table), "Type exactly '{}' to confirm! "):
            try:
                self.openConnection()
                self.cur.execute("drop table {};".format(table))
                self.conn.commit()
                print("{} table dropped!".format(table))
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

#COULD BE STATIC FUNCTIONS-----------------------------------------------------

def DisplayNeat(headers, results, title):
    f = ''
    for i in range(len(headers)):
        values = [len(headers[i])] + [len(str(row[i])) for row in results]
        f += '{%d:<%d}' % (i, max(values)+1)
    
    print("\n{}".format(title))
    print(f.format(*headers))
    for row in results:
        print(f.format(*row))

def getUserQueryStuff(headers, reason="WHERE"):
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
        
    queries = []
    for i in heads: 
        head = headers[int(i)-1]
        value = input("Please input the value for {}: ".format(head)) 
        if not value.isdigit(): value = "'{}'".format(value)
        queries.append("{} = {}".format(head, value))

    return queries

def confirmAction(confMsg = "confirm", warning = "Type '{}' to confirm! "):
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
    display = False
    while(True):
        if display:
            db_ops.displayAll(table)

        print ("\n   {} Table Menu:".format(table))
        print ("*" * (len("   {} Table Menu:".format(table))+3))
        print (" 1. Toggle {} table Visbility".format(table)) #TODO: make always show with visibility flag
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
            db_ops.queryDatabase(table)
        elif choice == '3':
            db_ops.createRecord(table)
            input("\nPress enter to continue...")
            cls()
        elif choice == '4':
            db_ops.updateRecord(table)
            cls()
        elif choice == '5':
            db_ops.deleteRecord(table)
            cls()
        elif choice == '6':
            #TODO: THIS V
            db_ops.manualQuery(table)
        elif choice == '7':
            if(db_ops.dropTable(table)):
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