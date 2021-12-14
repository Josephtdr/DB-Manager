import re
from abc import ABC, abstractmethod

'''
Abstract base class from which individual tables will inherit from,
limits duplicate code within the program
'''
class TableABC(ABC):
    sqlInsert = ""
    funcDict = {}

    @abstractmethod
    def createRecord(self):
        pass

    @abstractmethod
    def getData(Self):
        pass

    @abstractmethod
    def getDataStr(Self):
        pass
        
    def getVariableValidation(self, header):
        validationFunc = self.funcDict[header]
        return validationFunc()

    def stringValidation(self, header, stringLen):
        value = input("Please input {}: ".format(header))
        while(True):
            if value is None:
                value = input("Please input something: ")
            elif len(value) > stringLen:
                value = input("Please input a surname of {} characters or less: ".format(stringLen))
            else:
                break
        return value

    def integerValidation(self, header):
        value = input("Please input {}: ".format(header))
        while(not value.isdigit()):
            value = input("Please Input an Integer: ")
        return int(value)

    def regexValidation(self, header, regex):
        value = input("Please input {}: ".format(header))
        while(re.search(regex, value) is None):
            value = input("Please input a valid {}: ".format(header))
        return value

    def getSqlInsert(self, bulkInsert = False):
        return self.sqlInsert.format("?" if bulkInsert else "null")