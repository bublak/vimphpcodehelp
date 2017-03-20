class NamespacePathCreator:

    path=''
    namespaceDefinition=''

    def __init__(self, namespaceDefinition, path):
        self.namespaceDefinition = namespaceDefinition
        self.path = path + '\\'

    def create(self, line):
        line = line.replace(self.namespaceDefinition, self.path)

        if line.endswith(';'):
            line = line[0:len(line)-1] # get rid off ';' at the end of line

        if line.startswith('use '):
            line = line[4:len(line)] # get rid off 'use '

        line = line.replace('\\', '/') #change path separators
        line = './' + line + '.php'

        return line
