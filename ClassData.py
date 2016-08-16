from ClassElement import *
from EnumClassData import *

class ClassData:

    space = ' '

    path = None;

    constants = {};
    functions = {};

    def __init__(self, path):
        self.path = path
        self.constants = {}
        self.functions = {}

    def addFunction(self, name, value, definition, lineNumber, comment=''):
        elem = ClassElement(EnumClassData.OPERATION, name, value, definition, lineNumber, comment)

        self.functions[name] = elem

    def addConstant(self, name, value, definition, lineNumber, comment=''):
        elem = ClassElement(EnumClassData.FIELD_CONSTANT, name, value, definition, lineNumber, comment)

        self.constants[name] = elem

    def getConstantsPrintable(self):
        result = self._basicPrinter(self.constants)

        return result

    def getFunctionsPrintable(self):
        result = self._basicPrinter(self.functions, '')

        return result

    def getAllPrintable(self):
        result = self._basicPrinter(self.constants)
        result.extend(self._basicPrinter(self.functions, ''))

        return result

    def _basicPrinter(self, data, joinSign=' = '):
        #TODO cut the value for some limit length
        space = self.space

        result = []

        for elemKey in data.keys():
            item = data.get(elemKey)
            result.append(item.definition + space + item.name + joinSign + item.value)

        result.sort()

        return result
