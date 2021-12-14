from TableABC import TableABC

class Dummy(TableABC):
    sqlInsert = "insert into Dummy values ({},?,?,?);"
    tableName = 'Dummy'
    tableColumns = 'ID INTEGER PRIMARY KEY, Department VARCHAR(20), BossID int UNSIGNED NOT NULL, NumEmployees int UNSIGNED NOT NULL'
    


    def __init__(self, ID = 0, department = '', bossID = 0, 
            numEmployees = 0):
        self.ID = ID
        self.department = department
        self.bossID = bossID
        self.numEmployees = numEmployees

        self.funcDict = {
            "ID": self.new_id,
            "Department": self.new_department,
            "BossID": self.new_bossID,
            "NumEmployees": self.new_numEmployees,
        }
    
    def createRecord(self):
        self.department = self.new_department()
        self.bossID = self.new_bossID()
        self.numEmployees = self.new_numEmployees()

    def new_id(self):
        return self.integerValidation("the ID")

    def new_department(self):
        return self.stringValidation("the Department name", 20)

    def new_bossID(self):
        return self.integerValidation("the Departments Boss ID")

    def new_numEmployees(self):
        return self.integerValidation("the number of Employees")

    def getData(self, bulkInsert = False):
        if bulkInsert:
            return (self.ID, self.title, self.forename, self.surname, self.email, self.salary)
        else:
            return (self.department, self.bossID, self.numEmployees)

    def getDataStr(self):
        return [self.ID, self.department, self.bossID, self.numEmployees]
