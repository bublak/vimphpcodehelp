from CodeParser import CodeParser
from ClassContextHint import ClassContextHint

class CodeNavigate:

    def navigateToClass(self, className, lines, lineNumber):
        codeParser = CodeParser()
        actualFilePath = codeParser.startSearching(className, lines, lineNumber)

        return actualFilePath

    def getClassContextData(self, className, lines, lineNumber, actualFilePath=None):

        codeParser = CodeParser()

        if className != '':
            result = codeParser.startSearching(className, lines, lineNumber)

            if result != False:
                actualFilePath = result
            else:
                actualFilePath = result

        allHints = {}

        if actualFilePath:
            cch = ClassContextHint(actualFilePath)

            hints = cch.getContextHintsForFile(actualFilePath)

            allHints[actualFilePath] = hints

            #TODO -> how do  do - while 
            hasParent = False
            if hints.parentClass['lineNumber'] != None:
                hasParent = True

            while hasParent:
                lineNumber = hints.parentClass['lineNumber']

                parentClassPath = codeParser.startSearching(
                    hints.parentClass['name'], hints.parentClass['lines'], lineNumber
                )

                printd(' new parent class: ')

                # TODO proc se musi delat nahrazeni tady? -> nemelo by to vratit v poradku?
                parentClassPath = parentClassPath.replace('\n', '')
                parentClassPath = parentClassPath.replace(';', '')
                printd(parentClassPath)

                cchParent = ClassContextHint(parentClassPath)
                # todo -> tohle tu nemuze byt, protoze se to bude volat z ruznych method, tohle je omezeni na jednu
                hints = cchParent.getContextHintsForFile(parentClassPath)

                allHints[hints.path] = hints

                hasParent = False
                if hints.parentClass['lineNumber'] != None:
                    hasParent = True

        for hh in allHints:
            print hh + ': '
            item = allHints.get(hh)
            self._printLines(item.getAllPrintable('     '))
            print '= '

    def getFunctionAnotation(self, functionName, className, lineNumber, lines, actualFilePath=None):
        functionName = functionName.strip()

        cch = ClassContextHint("bb") # TODO set path properly

        if functionName != '':
            codeParser = CodeParser()
            result = codeParser.startSearching(className, lines, lineNumber)

            if result != False:
                actualFilePath = result

        if actualFilePath:
            # TODO -> jak poznat ze naslo? -> vrati True??
            hints = cch.getMethodHintForFile(actualFilePath, functionName, True)

            if hints == True:
                return True #TODO

            hasParent = False
            if hints.parentClass['lineNumber'] != None:
                hasParent = True

            # TODO TOHLE JE stejny jak v jiny metode
            while hasParent:
                lineNumber = hints.parentClass['lineNumber']

                parentClassPath = codeParser.startSearching(
                    hints.parentClass['name'], hints.parentClass['lines'], lineNumber
                )

                printd(' new parent class: ')

                # TODO proc se musi delat nahrazeni tady? -> nemelo by to vratit v poradku?
                parentClassPath = parentClassPath.replace('\n', '')
                parentClassPath = parentClassPath.replace(';', '')
                printd(parentClassPath)

                cchParent = ClassContextHint(parentClassPath)
                hints = cchParent.getMethodHintForFile(parentClassPath, functionName, True)
                # todo -> tohle tu nemuze byt, protoze se to bude volat z ruznych method, tohle je omezeni na jednu
                if hints == True:
                    return True

                hasParent = False
                if hints.parentClass['lineNumber'] != None:
                    hasParent = True



    def _printLines(self, data, separator="\n"):
        for line in data:
            if line != None:
                line += separator

                print line

#def printd(string, debug=True):
def printd(string, debug=False):
    if debug == True:
        print(string)
