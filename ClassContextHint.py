import re
from ClassData import *

# The processing expect the well formated php code - basic coding standards :)
class ClassContextHint:

    hints = None
    
    def __init__(self, path):
        self.hints = ClassData(path)

    def getAncestor(self, lines):
        # TODO -> add support for extends other class

        pattern = ' extends(.*)' #TODO do it better
        # TODO more classes
        # TODO Test also for implements

        printd(self.hints.path)

        lineNumber = 0

        for line in lines:
            res = re.search(pattern, line)
            #printd('\nzpracovavam line:')
            #printd(line)
            printd('===============================================')

            if line.find("{") > -1: # end of class definitions
                break

            if res:
                printd('je dedicnost: ')
                newClass = res.groups()[0].strip()

                newClass = newClass.replace('\n', '')

                printd(newClass)

                # TODO only one is supported
                # TODO magic 3
                self.hints.parentClass = {'lineNumber': lineNumber, 'name': newClass, 'lines': lines[:lineNumber+3]}

            lineNumber += 1

        return False

    # TODO ADD tests for private methods
    def getMethodHintForFile(self, filename, functionName, doPrint):
        result = []

        with open(filename, 'r') as f:
            read_data = f.readlines()

        self.getAncestor(read_data)
        self.loadFunctions(read_data, functionName)

        print filename
        # TODO -> check that exists
        if self.hints.functions.has_key(functionName):
            lineNumber = self.hints.functions[functionName].lineNumber + 1
        else:
            return self.hints

        read_data = read_data[:lineNumber+5] # 5 -> show first 5 lines from function

        read_data.reverse()

        comment = []
        for line in read_data:
            if line.find('/**') > -1:
                comment.append(line);
                break
            else:
                comment.append(line);

        comment.reverse()

        if doPrint:
            self._printLines(comment, '')
            return True
        else:
            # TODO connect with ClassData element !!!!!!!!!!!!!!!!!!
            return comment

    def getContextHintsForFile(self, filename, doPrint=False):

        with open(filename, 'r') as f:
            read_data = f.readlines()

        printd('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
        if read_data:
            printd( '=============== hledam dedicnost')
            self.getAncestor(read_data)

            self.getContextHints(read_data)

        if doPrint:
            return self._printLines(self.hints.getAllPrintable())
        else:
            return self.hints

    def getContextHints(self, lines):
        self.loadConstants(lines)
        self.loadFunctions(lines)

        return self.hints.getAllPrintable()

    def loadConstants(self, lines):

        constants = []

        lineNumber = 0;

        for line in lines:
            newWord = ''
            pattern = '(const) (.*)(=)(.*);'

            #printd('pattern: ' + pattern)
            res = re.search(pattern, line)

            if res:
                definition = res.groups()[0].strip()
                name = res.groups()[1].strip()
                value = res.groups()[3].strip()

                self.hints.addConstant(name, value, definition, lineNumber)

            lineNumber += 1

        return self.hints.getConstantsPrintable()

    def loadAttributes(self, lines):
        for line in lines:
            print line

    def loadFunctions(self, lines, functionName=False):

        if functionName == False:
            searchFunctionName = '.*'
            patternWithEnd = '(.*public.*|protected.*) function ('+searchFunctionName+') ?(.*\(.*\).*)[{;]'
            patternNotEnded = '(.*public.*|protected.*) function '+searchFunctionName+'\(.*'
        else:
            searchFunctionName = functionName+'.*'
            patternWithEnd = '(.*public.*|protected.*|private.*) function ('+searchFunctionName+') ?(.*\(.*\).*)[{;]'
            patternNotEnded = '(.*public.*|protected.*|private.*) function '+searchFunctionName+'\(.*'


        lineToProcess = False
        lineNumber = 0

        for line in lines:
            printd('\nzpracovavam line:')

            if line.find("{") > -1 or line.find(";") > -1: # function definitions ends with { or ; for interface methods
                printd('has end ===========')
                hasEnd = True
            else:
                printd('has not end ===========')
                hasEnd = False

            printd(line)
            newWord = ''

            if hasEnd == True:
                if lineToProcess != False:
                    lineToProcess += line
                    lineToProcess = lineToProcess.replace('\n', '')
                    line = lineToProcess
                    lineToProcess = False

                printd('CHECKING LINE WITH END: ')
                printd(line)
                wasAdded = self._addFunctionInList(patternWithEnd, line, lineNumber)

                if wasAdded and functionName != False:
                    return self.hints.getFunctionsPrintable()
            else:
                if lineToProcess != False:
                    lineToProcess += line
                else:
                    printd('XXXbbbbbbb pattern: ' + patternNotEnded)
                    res = re.search(patternNotEnded, line)

                    if res:
                        printd('xxxbbbb pattern found - wait to end')
                        lineToProcess = line


            lineNumber += 1;

        return self.hints.getFunctionsPrintable()

    def _addFunctionInList(self, pattern, line, lineNumber):
        printd('XXX pattern for add in list: ' + pattern)
        res = re.search(pattern, line)

        if res:
            printd('xxx pattern found')

            definition = res.groups()[0].strip()
            name = res.groups()[1].strip()
            value = res.groups()[2].replace('\n', '').strip()
            printd ('xxxxxxXXX pridavam function with name: ' + name);

            self.hints.addFunction(name, value, definition, lineNumber)

            return True

        return False

    def _printLines(self, data, separator="\n"):
        for line in data:
            if line != None:
                line += separator

                print line

#def printd(string, debug=True):
def printd(string, debug=False):
    if debug == True:
        print(string)

if __name__ == '__main__':
    print 'calling main'
    #vv = ClassContextHint()
    #print vv.basic()
