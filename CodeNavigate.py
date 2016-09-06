from CodeParser import CodeParser
from BasicGui import BasicGui
from ClassContextHint import ClassContextHint

from Tkinter import *

#TODO nefacha hledat ValidatorType
#if (IW_Core_Validate::isEnumValue($validatorName, 'IW\Core\ModeMan\Data\Enum\ValidatorType')) {

#TODO - dvouradkovy definice


# TODO nefacha komentar:
#
#v use search search authorization 48
#$oeAdmin = IW_Core_Utils_CurrentUser::getOrganisationalUnitsAdmin();

# TODO TODO TODO podporu pro private kdyz se hleda ve stejnym souboru -> To uz mi fakt sere

class CodeNavigate:

    def navigateToClass(self, className, lines, lineNumber):
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
        showPrivate = False

        if className != '':
            result = codeParser.startSearching(className, lines, lineNumber)

        if result != False:
            actualFilePath = result
            showPrivate = True

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
            hints = cch.getMethodHintForFile(actualFilePath, functionName, False)

            # Detection, that the functionName was found
            if len(hints.functions) > 0:
                functionData = hints.functions[functionName]

                self._displayText(functionName, functionData.comment, actualFilePath)

                return True

            hasParent = False
            if hints.parentClass['lineNumber'] != None:
                hasParent = True

            # TODO TOHLE JE stejny jak v jiny metode
            while hasParent:
                lineNumber = hints.parentClass['lineNumber']

                parentClassPath = codeParser.startSearching(
                    hints.parentClass['name'], hints.parentClass['lines'], lineNumber
                )

                printd(' new parent class: ', False)

                # TODO proc se musi delat nahrazeni tady? -> nemelo by to vratit v poradku?
                parentClassPath = parentClassPath.replace('\n', '')
                parentClassPath = parentClassPath.replace(';', '')
                printd(parentClassPath, False)

                cchParent = ClassContextHint(parentClassPath)
                hints = cchParent.getMethodHintForFile(parentClassPath, functionName, False)

                # Detection, that the functionName was found
                if len(hints.functions) > 0:
                    functionData = hints.functions[functionName]

                    self._displayText(functionName, functionData.comment, parentClassPath)
                    return True

                hasParent = False
                if hints.parentClass['lineNumber'] != None:
                    hasParent = True

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


