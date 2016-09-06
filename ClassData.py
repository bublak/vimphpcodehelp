from ClassElement import *
from EnumClassData import *

class ClassData:

    space = ' '

    path = None;

    parentClass = {'lineNumber': None, 'name': None, 'lines': None}; 
    constants = {};
    functions = {};

    def __init__(self, path):
        self.path = path
        self.constants = {}
        self.functions = {}

    def addFunction(self, name, value, definition, lineNumber, comment=''):
        elem = ClassElement(EnumClassData.OPERATION, name, value, definition, lineNumber, comment)

        self.functions[name] = elem

    def addCommentToFunction(self, name, comment):
        elem = self.functions[name]

        elem.comment = comment
        self.functions[name] = elem

    def addConstant(self, name, value, definition, lineNumber, comment=''):
        elem = ClassElement(EnumClassData.FIELD_CONSTANT, name, value, definition, lineNumber, comment)

        self.constants[name] = elem

    def getConstantsPrintable(self):
        result = self._basicPrinterTransformer(self.constants)

        return result

    def getFunctionsPrintable(self):
        result = self._basicPrinterTransformer(self.functions, '')

        return result

    def getAllPrintable(self, indentation=''):
        result = self._basicPrinterTransformer(self.constants, indentation)
        result.extend(self._basicPrinterTransformer(self.functions, indentation, ''))

        return result

    def _basicPrinterTransformer(self, data, indentation='', joinSign=' = '):
        #TODO cut the value for some limit length
        space = self.space

        result = []

        for elemKey in data.keys():
            item = data.get(elemKey)
            result.append(indentation + item.definition + space + item.name + joinSign + item.value)

        result.sort()

        return result
