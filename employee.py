from TableABC import TableABC 

class Employee(TableABC):
    emailRegex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    sqlInsert = "insert into Employee values ({},?,?,?,?,?);"
    tableName = 'Employee'
    tableColumns = 'ID INTEGER PRIMARY KEY, Title VARCHAR(5), Forename VARCHAR(20), Surname VARCHAR(20), Email VARCHAR(20) NOT NULL, Salary int UNSIGNED NOT NULL'


    def __init__(self, ID = 0, title = '', forename = '', 
            surname = '', email = '', salary = 0):
        self.ID = int(ID)
        self.title = title
        self.forename = forename
        self.surname = surname
        self.email = email
        self.salary = int(salary)

        self.funcDict = {
            "ID": self.newID,
            "Title": self.newTitle,
            "Forename": self.newForename,
            "Surname": self.newSurname,
            "Email": self.newEmail,
            "Salary": self.newSalary
        }

    def createRecord(self):
            self.title = self.newTitle()
            self.forename = self.newForename()
            self.surname = self.newSurname()
            self.email = self.newEmail()
            self.salary = self.newSalary()

    def newID(self):
        return self.integerValidation("the ID")

    def newTitle(self):
        return self.stringValidation("Title", 20)

    def newForename(self):
        return self.stringValidation("Forename", 20)

    def newSurname(self):
        return self.stringValidation("Surname", 20)

    def newEmail(self):
        return self.regexValidation("Email", self.emailRegex)
    
    def newSalary(self):
        return self.integerValidation("Salary")

    def getData(self, bulkInsert = False):
        if bulkInsert:
            return (self.ID, self.title, self.forename, self.surname, self.email, self.salary)
        else:
            return (self.title, self.forename, self.surname, self.email, self.salary)

    def getDataStr(self):
        return [self.ID, self.title, self.forename, self.surname,
                self.email, "£{:,.2f}".format(self.salary/100)]

