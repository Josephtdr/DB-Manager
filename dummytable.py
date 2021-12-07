class Dummy:
    sqlInsert = "insert into Dummy values (null,?,?,?,?,?);"
    tableName = 'Dummy'
    tableColumns = 'ID INTEGER PRIMARY KEY, Title VARCHAR(5), Forename VARCHAR(20), Surname VARCHAR(20), Email VARCHAR(20) NOT NULL, Salary int UNSIGNED NOT NULL'

    def __init__(self, ID = 0, title = '', forename = '', 
            surname = '', email = '', salary = 0):
        self.ID = ID
        self.title = title
        self.forename = forename
        self.surname = surname
        self.email = email
        self.salary = salary
    
    def create_record(self):
        self.title = self.new_title()
        self.forename = self.new_forename()
        self.surname = self.new_surname()
        self.email = self.new_email()
        self.salary = self.new_salary()

    def getVariableValidation(self, header):
        funcDict = {
            "ID": self.new_id,
            "Title": self.new_title,
            "Forename": self.new_forename,
            "Surname": self.new_surname,
            "Email": self.new_email,
            "Salary": self.new_salary
        }
        validationFunc = funcDict[header]
        return validationFunc()


    def getData(self):
        return (self.title, self.forename, self.surname, self.email, self.salary)

    def getDataStr(self):
        return [self.ID, self.title, self.forename, self.surname,
                self.email, "£{:,.2f}".format(self.salary/100)]

    def getSqlInsert(self):
        return self.sqlInsert