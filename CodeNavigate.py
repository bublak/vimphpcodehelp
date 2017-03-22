from BasicGui import BasicGui
from ClassContextHint import ClassContextHint

# TODO -> inject Renderer class

#TODO nefacha hledat ValidatorType     -> v modeman neco valida... :)
#if (IW_Core_Validate::isEnumValue($validatorName, 'IW\Core\ModeMan\Data\Enum\ValidatorType')) {

#TODO - dvouradkovy definice

class CodeNavigate:

    codeParser = None

    def __init__(self, codeParser=None):
        self.codeParser=codeParser

    def navigateToClass(self, className, lines, lineNumber):
        actualFilePath = self.codeParser.startSearching(className, lines, lineNumber)

        return actualFilePath

    def navigateToClassFunction(self, className, lines, lineNumber, functionName):
        # TODO -> napsat, ted je zneuzita fce getFunctionAnotation s parametrem jump

        return 'not implemented'

    def getClassContextData(self, className, lines, lineNumber, actualFilePath=None):
        if className != '':
            result = self.codeParser.startSearching(className, lines, lineNumber)

            if result != False:
                actualFilePath = result

        actualFilePathOrig = actualFilePath

        allHints = {} # also with parent class data

        while actualFilePath:
            cch   = ClassContextHint(actualFilePath)
            hints = cch.getContextHintsForFile(actualFilePath)

            allHints[actualFilePath] = hints

            lineNumber = hints.parentClass['lineNumber']

            if lineNumber == None:
                actualFilePath = False
            else:
                # get the parent class
                actualFilePath = self.codeParser.startSearching(
                    hints.parentClass['name'], hints.parentClass['lines'], lineNumber
                )

                printd(' new parent class: ')
                printd(actualFilePath)

        text = [] 
        for hh in allHints:
            text.append('\n= = = = = = = = = =\n')
            text.append(hh + ': \n')
            item = allHints.get(hh)
            text.extend(item.getAllPrintable('\n      '))

        self._displayText(actualFilePathOrig, text, actualFilePathOrig, allHints)

    # get function anotation comment
    # if the functionName == className, it is use search in actualFilePath (actual file)
    # else the className is searched
    # TODO implement support for search in private methods
    def getFunctionAnotation(self, functionName, className, lineNumber, lines, actualFilePath=None, jump=False):
        functionName = functionName.strip()

        cch = ClassContextHint("bb") # TODO set path properly

        if functionName != '' and functionName != className:
            result = self.codeParser.startSearching(className, lines, lineNumber)

            if result != False:
                actualFilePath = result

        while actualFilePath:
            hints = cch.getMethodHintForFile(actualFilePath, functionName, False)

            # Detection, that the functionName was found
            if len(hints.functions) > 0:
                functionData = hints.functions[functionName]

                if jump == True:
                    lineNumber = functionData.lineNumber + 1 #correction for vim
                    #vim command to open file on line   :e +50 filename
                    return '+' + lineNumber.__str__() + ' ' + actualFilePath 

                self._displayText(functionName, functionData.comment, actualFilePath)

                return True

            lineNumber = hints.parentClass['lineNumber']

            if lineNumber == None:
                return False
            else:
                # get the parent class
                actualFilePath = self.codeParser.startSearching(
                    hints.parentClass['name'], hints.parentClass['lines'], lineNumber
                )

                printd(' new parent class: ')
                printd(actualFilePath)

    def _displayText(self, title, ttext, fileName, hintsData=None):
        basicGui = BasicGui(title, ttext, fileName, hintsData)
        basicGui.start()

#def printd(string, debug=True):
def printd(string, debug=False):
    if debug == True:
        print(string)


