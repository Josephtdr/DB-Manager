import re

class Employee:
    emailRegex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    titleRegex = "\\b(Mr|Mrs|Ms|Miss|Dr|Sir|They|Them)\\b" #pronouns ik but idk
    sqlInsert = "insert into Employee values (null,?,?,?,?,?);"

    def __init__(self, ID = 0, title = '', forename = '', 
            surname = '', email = '', salary = 0):
        self.ID = ID
        self.title = title
        self.forename = forename
        self.surname = surname
        self.email = email
        self.salary = salary


    def create_record(self):
            self.new_employee_title()
            self.new_forename()
            self.new_surname()
            self.new_email()
            self.new_salary()

    def new_employee_title(self):
        value = input("Please input title: ")
        while(re.search(self.titleRegex, value) is None):
            value = input("Please input a valid title: ")
        self.title = value

    def new_forename(self):
        value = input("Please input forename: ")
        while(value is None):
            value = input("Please input something: ")
        self.forename = value
    
    def new_surname(self):
        value = input("Please input Surname: ")
        while(value is None):
            value = input("Please input something: ")
        self.surname = value

    def new_email(self):
        value = input("Please input email: ")
        while(re.search(self.emailRegex, value) is None):
            value = input("Please input a valid email: ")
        self.email = value
    
    def new_salary(self):
        value = input("Please input salary: ")
        while(not value.isdigit()):
            value = input("Please Input an Integer: ")
        self.salary = int(value)

    def set_employee_id(self, employeeID):
        self.ID = employeeID

    def set_employee_title(self, empTitle):
        self.title = empTitle

    def set_forename(self,forename):
        self.forename = forename
    
    def set_surname(self,surname):
        self.surname = surname

    def set_email(self,email):
        self.email = email
    
    def set_salary(self,salary):
        self.salary = salary

    def get_employee_id(self):
        return self.ID

    def getData(self):
        return (self.title, self.forename, self.surname, self.email, self.salary)

    def getDataStr(self):
        return [self.ID, self.title, self.forename, self.surname,
                self.email, "£{:.2f}".format(self.salary/100)]

    def getSqlInsert(self):
        return self.sqlInsert
