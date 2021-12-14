import os
import sqlite3

'''
Class for operations dealing with a given passed table when initialised
'''
class TableOperations:
    storedQuery = ''

    def __init__(self, tableName, obj, dbname):
        self.tableName = tableName 
        self.obj = obj #Object representing said table and containing the representation rules
        self.DATABASENAME = dbname
        self.initialiseSQL()
        self.initialiseHeaders()

    def initialiseSQL(self):
        self.SQL_selecALL = "select * from {} ".format(self.tableName)
        self.SQL_update = " update {} set ".format(self.tableName)
        self.SQL_delete = "delete from {} ".format(self.tableName)
        self.SQL_drop = "drop table {};".format(self.tableName)
        
    def initialiseHeaders(self):
        try:
            self.openConnection()
            self.cur.execute(self.SQL_selecALL)
            self.headers = [i[0] for i in self.cur.description]
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def openConnection(self):
        self.conn = sqlite3.connect(self.DATABASENAME)
        self.cur = self.conn.cursor()

    def queryAll(self):
        try:
            self.openConnection()
            self.cur.execute(self.SQL_selecALL)
            results = self.cur.fetchall()
            return self.headers, results
        except Exception as e:
            print(e)
        finally:
            self.conn.close()
    
    def createRecord(self):
        tableObj = self.obj()
        tableObj.createRecord()
        sqlInsert = tableObj.getSqlInsert()
        data = tableObj.getData()
        try:
            self.openConnection()
            self.cur.execute(sqlInsert, data)
            self.conn.commit()
            print("Inserted data successfully")
            input("\nPress enter to continue...")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def bulkInsertRecords(self):
        tableObj = self.obj()
        sqlInsert = tableObj.getSqlInsert(bulkInsert = True)

        fileName = input("Please enter the .txt file to import data from: ")
        while(fileName[-4:] != ".txt"):
            fileName = input("Please enter a .txt file: ")

        try:
            with open(fileName, 'r') as reader:
                rawdata = reader.readlines()
        
            formattedRecords = []
            for line in rawdata:
                print("yes " + line[-1:])
                if line[-1:] == '\n':
                    line = line[:-1]
                record = tuple(line.split(","))
                formattedRecord = self.obj(*record).getData(bulkInsert = True)
                formattedRecords.append(formattedRecord)
            
        except FileNotFoundError:
            input("\n{} not found, make sure it is in the same directory...".format(fileName))
            return False
        except TypeError:
            print("\nIncorrect number of args supplied for a record.")
            input("make sure data is tab seperated...")
            return False
        
        try:
            self.openConnection()
            self.cur.executemany(sqlInsert, formattedRecords)
            self.conn.commit()
            print("Inserted data successfully")
            input("\nPress enter to continue...")
        except Exception as e:
            input("\n" + str(e) + "..")
        finally:
            self.conn.close()

    def exportToTxt(self):
        fileName = input("Please enter the .txt file to export data to: ")
        while(fileName[-4:] != ".txt"):
            fileName = input("Please enter a .txt file: ")

        if os.path.isfile(fileName):
            print("\nWarning, {} already exists, overwriting file!".format(fileName))
            if confirmAction():
                input("\nCancelling!")
                return False

        _, data = self.queryAll()
        dataStr = [(",".join([str(x) for x in line])+'\n') for line in data]

        with open(fileName, 'w') as writer:
            writer.writelines(dataStr)

        print("\nExported data successfully")
        input("Press enter to continue...")

    def basicQueryForRecord(self, storeQuery):
        command = self.SQL_selecALL + "where "
        try:
            self.openConnection()
            queries, values = getUserQuery(self.obj, self.headers)
            command += " and ".join(queries)
            self.cur.execute(command, values)
            results = self.cur.fetchall()

            if storeQuery:
                self.storedQuery = ( " and ".join(queries), values )

            if len(results)==0:
                print("\nNo Records")
                return ''
            else:
                #(The list of column headers, the results of the query)
                return ([i[0] for i in self.cur.description], results)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def updateRecord(self, storeQuery):
        command = self.SQL_update
        try:
            self.openConnection()
            queries, valuesU = getUserQuery(self.obj, self.headers, "UPDATE", "U")
            command += ", ".join(queries)
            if storeQuery and self.storedQuery:
                queries, valuesW = self.storedQuery
                command += " where {}".format(queries)
            else:
                queries, valuesW = getUserQuery(self.obj, self.headers)
                command += " where {}".format(" and ".join(queries))

            self.cur.execute(command, valuesU | valuesW)

            if self.conn.total_changes != 0:
                print("\n%d row(s) to be updated" % self.conn.total_changes)
                if not confirmAction():
                    self.conn.commit()
                    self.storedQuery = ''
                else:
                    print("Cancelling!")
            else:
                print("\nNo records found")
                input("\nPress enter to continue...")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def deleteRecord(self, storeQuery):
        command = self.SQL_delete
        try:
            self.openConnection()
            if storeQuery and self.storedQuery:
                queries, values = self.storedQuery
                command += " where {}".format(queries)
            else:
                queries, values = getUserQuery(self.obj, self.headers)
                command += " where {}".format(" and ".join(queries))

            self.cur.execute(command, values)
            if self.conn.total_changes != 0:
                print("\n%d row(s) to be deleted" % self.conn.total_changes)
                if not confirmAction():
                    self.conn.commit()
                    self.storedQuery = ''
                else:
                    print("Cancelling!")
            else:
                print("\nNo records found")
        except Exception as e:
            print(e) 
        finally:
            self.conn.close()

    def manualQuery(self):
        pass

    def dropTable(self):
        if confirmAction("DROP {}".format(self.tableName), "Type exactly '{}' to confirm! "):
            try:
                self.openConnection()
                self.cur.execute(self.SQL_drop)
                self.conn.commit()
                print("{} table dropped!".format(self.tableName))
                return True
            except Exception as e:
                print(e)
            finally:
                self.conn.close()        
        else:
            print("\nCancelling!")
            return False

def getUserQuery(obj, headers, reason="WHERE", append = "W"):
        heads = getUserSelection(headers, reason)
        tmpObj = obj()
        queries = []
        values = {}
        for i in heads: 
            head = headers[int(i)-1]
            value = tmpObj.getVariableValidation(head)
            queries.append("{0}=:{0}{1}".format(head, append))
            values["{}{}".format(head, append)] = value
        return queries, values

def getUserSelection(headers, reason):
    selecNUMs = [str(x+1) for x in list(range(len(headers)))]
    selecOptionsStr = ", ".join(["[{}]{}".format(i+1, headers[i]) for i in range(len(headers))])

    print("\n" + selecOptionsStr) #prints the numerated options of 'headers' to choose from
    userInput = input("Please input all headers (seperated by space) for {} query: ".format(reason))
    
    heads = list(filter(None, userInput.split(" ")))
    while True:
        try:
            if any(x not in selecNUMs for x in heads) or not userInput:
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