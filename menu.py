import sys
import os
from DBOperations import *

def menu1():
    db = DBOperations()

    while(True):
        tables = db.getTables()
        possibleTables = list(db.tableObjDict.keys())
        tblLen, postblLen = len(tables), len(possibleTables)
        print ("\n  Menu:")
        print ("*" * (len("  Menu:")+2))

        for i, table in enumerate(possibleTables):
            print (" {}. Create {} Table".format(i+1, table))

        for i, table in enumerate(tables):
            print(" {}. Interact with {} Table".format(i+1+postblLen, table))
        print (" {}. Exit".format(1 + tblLen + postblLen))

        choice = input("Enter command: ")
        while(not choice.isdigit() or int(choice) not in list(range(1, 2+tblLen+postblLen))):
            choice = input("Please enter a valid command: ")
        choice = int(choice)

        if 1 <= choice and choice < postblLen+1:
            if db.createTable(possibleTables[choice-1]):
                print("\nTable created successfully")
            else:
                print("\nThis table is already created")
            input("Press enter to continue...")
        elif postblLen+1 <= choice and choice < postblLen+tblLen+1:
            menu2(db, tables[choice-1-postblLen])
        elif choice == 1 + postblLen + tblLen:
            exit()
        cls()

def menu2(db, table):
    db.openTable(table)
    
    dbVisible = False
    storeQuery = False
    resultsToDisplay = ''

    while(True):
        cls()
        
        if not storeQuery:
            db.Table.storedQuery = ''
            
        if dbVisible:
            aheaders, aresults = db.Table.queryAll()
            displayNeat(aheaders, aresults, db.Table.obj, "{} Table:".format(table))

        if resultsToDisplay:
            displayNeat(resultsToDisplay[0], resultsToDisplay[1], db.Table.obj, "Query: ")
            resultsToDisplay = ''

        print("\n   {} Table Menu:".format(table))
        print("*" * (len("   {} Table Menu:".format(table))+3))

        str1 = 'Disable' if dbVisible else 'Enable'
        str2 = 'Disable' if storeQuery else 'Enable'
        tmpstr = "|| V. {} Table Visbility || M. {} Query Memory ||".format(str1, str2)
        print(tmpstr)
        print("-" * len(tmpstr))

        print(" 1. Query %s for records" % table)
        print(" 2. Create record")
        print(" 3. Update record(s)")
        print(" 4. Delete record(s)")
        print(" 5. Manual SQL Query (WARNING)")
        print(" 6. Drop table (WARNING DATA CANNOT BE RECOVERED)")
        print(" 7. Return to main menu")

        choice = input("Enter command: ")
        while(choice not in ['v', 'm', 'V','M','1','2','3','4','5','6','7']):
            choice = input("Please enter a valid command: ")
        
        if choice.lower() == 'v':
            dbVisible = not dbVisible
        elif choice.lower() == 'm':
            if not storeQuery:
                input("\nUpdate and Delete actions will be performed on your previous query... ")
            storeQuery = not storeQuery

        elif choice == '1':
            resultsToDisplay = db.Table.basicQueryDatabase(storeQuery)
            '''
            TODO: Advanced query with functionality such as
                  >, <, like, count({column}), group by, having
            '''
        elif choice == '2':
            db.Table.createRecord()
        elif choice == '3':
            db.Table.updateRecord(storeQuery)
        elif choice == '4':
            db.Table.deleteRecord(storeQuery)
        elif choice == '5':
            #TODO: THIS V
            resultsToDisplay = db.Table.manualQuery()
        elif choice == '6':
            if(db.Table.dropTable()):
                break
            else:
                input("Press enter to continue...")
        elif choice == '7':
            break;

def displayNeat(headers, results, obj, title):
        resultsObjects = [obj(*row) for row in results]
        formattedResults = [row.getDataStr() for row in resultsObjects]
        f = ''
        for i in range(len(headers)):
            lenOfStrings = [len(headers[i])] + [len(str(row[i])) for row in formattedResults]
            f += '{%d:<%d}' % (i, max(lenOfStrings)+1)

        print("\n{}".format(title))
        print(f.format(*headers))
        for row in formattedResults:
            print(f.format(*row))

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
def exit():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == '__main__':
    try:
        menu1()
    except KeyboardInterrupt:
        print('\nInterrupted')
        exit()