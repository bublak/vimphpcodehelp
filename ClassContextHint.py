import re

# The processing expect the well formated php code - basic coding standards :)
class ClassContextHint:

    #-> pridat rozlisovani co je co v hints -> aby se to dalo radit
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
        #TODO cut the value for some limit length

        for line in lines:
            newWord = ''
            pattern = '(const .*=.*);'

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
        # TODO bf, abstract functions -> or functions from interface -> dont have curl at the end: {

        lineToProcess = False

        for line in lines:

            if line.find("{") > -1: # function definitions ends with {
                hasEnd = True
            else:
                hasEnd = False

            printd('\nzpracovavam line:')
            printd(line)
            newWord = ''

            if lineToProcess == False:
                if hasEnd == True:
                    pattern = '.*(public|protected).*function (.*\(.*\).*){'

                    res = re.search(pattern, line)
                    printd('XXX pattern: ' + pattern)

                    if res:
                        printd('xxx pattern found')
                        newWord = res.groups()[0] + ' ' + res.groups()[1]

                        newWord = newWord.replace('\n', '')
                        printd ('xxxxxxXXX   pridavam ' + newWord);
                        self.hints.append(newWord.strip())

                else:
                    pattern = '.*(public|protected).*function .*\('

                    printd('XXXbbbbbbb pattern: ' + pattern)
                    res = re.search(pattern, line)

                    if res:
                        printd('xxxbbbb pattern found - wait to end')
                        lineToProcess = line
            else:
                lineToProcess += line

                if hasEnd == True:
                    pattern = '.*(public|protected).*function (.*\(.*\).*){'

                    lineToProcess = lineToProcess.replace('\n', '')
                    printd(lineToProcess)
                    printd('XXX pattern: ' + pattern)
                    res = re.search(pattern, lineToProcess)

                    if res:
                        printd('xxx pattern found - wait to end')
                        newWord = res.groups()[0] + ' ' + res.groups()[1]

                        newWord = newWord.replace('\n', '')
                        printd ('xxxxxxXXX pridavam ' + newWord);
                        self.hints.append(newWord.strip())

                    lineToProcess = False

        return self.hints


#def printd(string, debug=True):
def printd(string, debug=False):
    if debug == True:
        print(string)

if __name__ == '__main__':
    print 'calling main'
    #vv = ClassContextHint()
    #print vv.basic()
