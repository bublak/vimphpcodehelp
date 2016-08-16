class ClassElement:
    elementType = None
    name        = None
    value       = None
    definition  = None
    comment     = None
    lineNumber  = None

    def __init__(self, elementType, name, value, definition, lineNumber, comment=''):
        self.elementType = elementType

        self.name = name
        self.value = value
        self.definition = definition
        self.lineNumber = lineNumber
        self.comment = comment
