import sqlite3

class TableOperations:
    storedQuery = ''

    def __init__(self, tableName, obj, dbname):
        self.tableName = tableName 
        self.obj = obj #Object representing said table 
        self.DATABASENAME = dbname
        self.initSQL()
        self.initHeaders()

    def initSQL(self):
        self.SQL_selecALL = "select * from {} ".format(self.tableName)
        self.SQL_update = " update {} set ".format(self.tableName)
        self.SQL_delete = "delete from {} ".format(self.tableName)
        self.SQL_drop = "drop table {};".format(self.tableName)
        
    def initHeaders(self):
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
        tableObj.create_record()
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

    def basicQueryDatabase(self, storeQuery):
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

    def advancedQueryDatabase(self, storeQuery):
        pass

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