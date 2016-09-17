from CodeParser import CodeParser
from BasicGui import BasicGui
from ClassContextHint import ClassContextHint

from Tkinter import *


#TODO nefacha hledat ValidatorType     -> v modeman neco valida... :)
#if (IW_Core_Validate::isEnumValue($validatorName, 'IW\Core\ModeMan\Data\Enum\ValidatorType')) {

#TODO - dvouradkovy definice

class CodeNavigate:

    def navigateToClass(self, className, lines, lineNumber):
        codeParser = CodeParser()
        actualFilePath = codeParser.startSearching(className, lines, lineNumber)

        return actualFilePath

    def navigateToClassFunction(self, className, lines, lineNumber, functionName):
        # TODO -> napsat
        codeParser = CodeParser()
        actualFilePath = codeParser.startSearching(className, lines, lineNumber)

        return actualFilePath

    def getClassContextData(self, className, lines, lineNumber, actualFilePath=None):

        print "PPPPPPPPPPPP:"
        print className
        print "lines"
        print lines
        print lineNumber
        print actualFilePath

        codeParser = CodeParser()

        result = False

        if className != '':
            result = codeParser.startSearching(className, lines, lineNumber)

        if result != False:
            actualFilePath = result

        allHints = {}

        if actualFilePath:
            cch = ClassContextHint(actualFilePath)

            hints = cch.getContextHintsForFile(actualFilePath)

            allHints[actualFilePath] = hints

            hasParent = False
            if hints.parentClass['lineNumber'] != None:
                hasParent = True

            while hasParent:
                lineNumber = hints.parentClass['lineNumber']

                parentClassPath = codeParser.startSearching(
                    hints.parentClass['name'], hints.parentClass['lines'], lineNumber
                )

                printd(' new parent class: ')
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

    # get function anotation comment
    # if the functionName == className, it is use search in actualFilePath (actual file)
    # else the className is searched
    # TODO implement support for search in private methods
    def getFunctionAnotation(self, functionName, className, lineNumber, lines, actualFilePath=None, jump=False):
        functionName = functionName.strip()

        cch = ClassContextHint("bb") # TODO set path properly

        if functionName != '' and functionName != className:
            codeParser = CodeParser()
            result = codeParser.startSearching(className, lines, lineNumber)

            if result != False:
                actualFilePath = result

        while actualFilePath:
            hints = cch.getMethodHintForFile(actualFilePath, functionName, False)

            # Detection, that the functionName was found
            if len(hints.functions) > 0:
                functionData = hints.functions[functionName]

                if jump == True:
                    lineNumber = functionData.lineNumber + 1 #correction for vim
                    return '+' + lineNumber.__str__() + ' ' + actualFilePath 

                self._displayText(functionName, functionData.comment, actualFilePath)

                return True

            lineNumber = hints.parentClass['lineNumber']

            if lineNumber == None:
                return False
            else:
                # get the parent class
                actualFilePath = codeParser.startSearching(
                    hints.parentClass['name'], hints.parentClass['lines'], lineNumber
                )

                printd(' new parent class: ')
                printd(actualFilePath)

    def _printLines(self, data, separator="\n"):
        for line in data:
            if line != None:
                line += separator

                print line

    def _displayText(self, title, ttext, fileName):
        basicGui = BasicGui(title, ttext, fileName)
        basicGui.start()

#def printd(string, debug=True):
def printd(string, debug=False):
    if debug == True:
        print(string)


