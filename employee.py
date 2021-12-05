import re

class Employee:
    emailRegex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    titleRegex = "\\b(Mr|Mrs|Ms|Miss|Dr|Sir|They|Them)\\b" #pronouns ik but idk
    sqlInsert = "insert into Employee values (null,?,?,?,?,?);"
    tableName = 'Employee'
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

    def new_id(self):
        value = input("Please input ID: ")
        while(not value.isdigit()):
            value = input("Please Input an Integer: ")
        return int(value)

    def new_title(self):
        value = input("Please input Title: ")
        while(re.search(self.titleRegex, value) is None):
            value = input("Please input a valid title: ")
        return value

    def new_forename(self):
        value = input("Please input Forename: ")
        while(True):
            if value is None:
                value = input("Please input something: ")
            elif len(value) > 20:
                value = input("Please input a surname of 20 characters or less: ")
            else:
                break
        return value

    def new_surname(self):
        value = input("Please input Surname: ")
        while(True):
            if value is None:
                value = input("Please input something: ")
            elif len(value) > 20:
                value = input("Please input a surname of 20 characters or less: ")
            else:
                break
        return value

    def new_email(self):
        value = input("Please input Email: ")
        while(re.search(self.emailRegex, value) is None):
            value = input("Please input a valid Email: ")
        return value
    
    def new_salary(self):
        value = input("Please input Salary: ")
        while(not value.isdigit()):
            value = input("Please Input an Integer: ")
        return int(value)

    def getData(self):
        return (self.title, self.forename, self.surname, self.email, self.salary)

    def getDataStr(self):
        return [self.ID, self.title, self.forename, self.surname,
                self.email, "£{:,.2f}".format(self.salary/100)]

    def getSqlInsert(self):
        return self.sqlInsert
