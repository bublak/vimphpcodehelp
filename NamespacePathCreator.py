class NamespacePathCreator:

    path=''
    namespaceDefinition=''

    def __init__(self, namespaceDefinition, path):
        self.namespaceDefinition = namespaceDefinition
        self.path = path + '\\'

        printd(namespaceDefinition)
        printd(path)

    def create(self, line):
        printd('analyzuju radku v NamespacePathCreator')
        printd(line)

        line = line.replace(self.namespaceDefinition, self.path)

        if line.endswith(';'):
            line = line[0:len(line)-1] # get rid off ';' at the end of line

        if line.startswith('use '):
            line = line[4:len(line)] # get rid off 'use ' at the beginning of line

        line = line.replace('\\', '/') #change path separators
        line = './' + line + '.php'

        return line

#def printd(string, debug=True):
def printd(string, debug=False):
    if debug == True:
        print(string)


