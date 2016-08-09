import re

class ClassContextHint:

    #-> pridat rozlisovani co je co v hints
    hints = []
    
    def __init__(self):
        self.hints = []

    def getContextHintsForFile(self, filename, doPrint):

        with open(filename, 'r') as f:
            read_data = f.readlines()

        if read_data:
            self.getContextHints(read_data)

        if doPrint:
            for line in self.hints:
                if line != None:
                    line += "\n"

                    print line
        else:
            return self.hints

    def getContextHints(self, lines):
        self.loadConstants(lines)
        self.loadFunctions(lines)

        return self.hints

    def loadConstants(self, lines):
        for line in lines:
            newWord = ''
            pattern = 'const (.*)=.*;'

            #printd('pattern: ' + pattern)
            res = re.search(pattern, line)

            if res:
                newWord = res.groups()[0]
                self.hints.append(newWord.strip())

        return self.hints

    def loadAttributes(self, lines):
        for line in lines:
            print line

    def loadFunctions(self, lines):
        #TODO multiline
        #TODO static function

        for line in lines:
            #printd(line)
            newWord = ''
            #pattern = '.*(public|private)\s?function.*(.*\n.*)'
            pattern = '.*(public|protected).*function (.*\(.*\)).*'

            #printd('pattern: ' + pattern)
            res = re.search(pattern, line)

            if res:
                newWord = res.groups()[0] + ' ' + res.groups()[1]

                newWord = newWord.replace('\n', '')
                #print ('pridavam' + newWord);
                self.hints.append(newWord.strip())

        return self.hints


def printd(string, debug=True):
#def printd(string, debug=False):
    if debug == True:
        print(string)

if __name__ == '__main__':
    print 'calling main'
    #vv = ClassContextHint()
    #print vv.basic()
