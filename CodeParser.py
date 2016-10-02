import re

#TODO nefacha:
#class Buffer extends Adapter\Memory   -> hledat Memory

#TODO nefacha hledat Singleton:
#namespace IW\Core;
#
#abstract class AbstractService implements InjectableSingleton
#{
#
#    //singleton functionality
#    use Singleton;
#

class CodeParser:

    # NOTE: last char of line is deleted by processing line, so there should be for example ';'
    def _getNamespacedClass(self, line):
        self.printd('vstupuju getnamespaced class with line:');
        self.printd(line);
        #note: if there is not ' as ' -> the -1 value is returned, which caused cutting the ; at the end of line!!!
        line = line[:line.find(' as ')] 

        if line.find('use ') == 0:
            #cut off "use "
            line = line[4:]

        if line.find("_") > -1:
            line = self.getFilenameForOldClass(line)
        else:
            line = line.replace('\\', '/') #change path separators

            module = line[3:len(line)]
            module = module[:module.find('/')]
            module = module.lower()

            line = './portal/' + module + '/impl/' + line + '.php'

        self.printd('namespace line to open:')
        self.printd(line)

        return line

    # method for searching path for known class word
    # first search for old class, if not found, try to get namespaced class
    def getFilenameForClassWord(self, word, lines, lineNumber, line):
        self.printd('Hledam filename for class word: ' + word)
        oldFilename = self.getFilenameForOldClass(word)

        if oldFilename != False:
            return oldFilename
        else:
            return self.getUseNamespacedWord(word, lines, lineNumber, line)

    def startSearching(self, word, lines, lineNumber):

        line = lines[lineNumber]

        result = self.getFilenameForOldClass(word)

        if result != False:
            self.printd('is old class def')
            return result
        else: 
            result = self.getKnownDefinitions(word, lines, lineNumber)

        return result

    # search backwards from lineNumber, until the search word or word 'function' is find, if no definition and function found,
    # search from begin of file
    def getVariable(self, word, lines, lineNumber):

        self.printd('vstupuju do getVariable')

        foundedLine = False 
        result      = False
        hasFunction = False

        i = 0
        for i in range(lineNumber, 0, -1):
            line = lines[i]

            patternWord = word + ' *='
            if re.search(patternWord, line):
                self.printd('slovo nalezeno, radka: ' + line)
                foundedLine = line
                break

            patternFunction = ' *function ';  # handle constructor (skip it)

            if re.search(patternFunction, line):
                hasFunction = True
                break;

        if hasFunction == True:
            self.printd('byla funkce, hledam od zacatku')
            i = 0
            for i in range(0, lineNumber):
                line = lines[i]

                patternWord = word + ' *='
                if re.search(patternWord, line):
                    foundedLine = line

                    self.printd('nalezena variable na radce: ' + i.__str__())
                    self.printd(' radka: ' + line)
                    result = self.processLineForClassDefinition(word, lines, line, i)

                    if result != False:
                        return result
                    else:
                        foundedLine = False

        if foundedLine != False:
            self.printd('nalezena variable na radce: ' + i.__str__())
            self.printd(' radka: ' + line)
            result = self.processLineForClassDefinition(word, lines, line, i)

        return result

    def processLineForClassDefinition(self, word, lines, line, lineNumber):
        self.printd(' && process line for class definition &&')
            
        restOfLine = line.split('=', 1)[1].strip()

        self.printd(restOfLine)

        pattern = '(.*)::getInstance\(\)'

        self.printd('pattern: ' + pattern)
        res = re.search(pattern, restOfLine)
        if res:
            newWord = res.groups()[0]
            self.printd('hledane nove slovo: ' + newWord)
            return self.getUseNamespacedWord(newWord, lines, lineNumber, line)

        quotes = '[\'|"]'
        pattern = 'IW_Core_BeanFactory::singleton\(' + quotes + '(.*)' + quotes + '\)';
        self.printd('pattern: ' + pattern)
        res = re.search(pattern, restOfLine)
        if res:
            newWord = res.groups()[0]
            self.printd('hledane nove slovo: ' + newWord)
            oldFilename = self.getFilenameForOldClass(newWord)

            if oldFilename != False:
                return oldFilename

        pattern = 'IW_Core_BeanFactory::singleton\(' + '(.*)::class' + '\)';
        self.printd('pattern: ' + pattern)
        res = re.search(pattern, restOfLine)
        if res:
            newWord = res.groups()[0]
            self.printd('hledane nove slovo: ' + newWord)

            return self.getFilenameForClassWord(newWord, lines, lineNumber, line)

        pattern = 'new (.*?)\('; # the ? cause not greedy behaviour

        self.printd('pattern: ' + pattern)
        res = re.search(pattern, restOfLine)
        if res:
            newWord = res.groups()[0]
            self.printd('hledane nove slovo: ' + newWord)
            return self.getUseNamespacedWord(newWord, lines, lineNumber, line)
            
        pattern = '(.*?)::create'; # the ? cause not greedy behaviour

        self.printd('pattern: ' + pattern)
        res = re.search(pattern, restOfLine)
        if res:
            newWord = res.groups()[0]
            self.printd('hledane nove slovo: ' + newWord)
            return self.getUseNamespacedWord(newWord, lines, lineNumber, line)

        #TODO implement all other types :)
        # x) tohle nejde: (protoze otevre ba, misto hledanyho aaa: $aaa  = $ba->getAAAById($aaId);
        # x) tohle nevim jestli ma cenu: function definition, like:   $neco = $this->getDef();
        return False
        

    def getKnownDefinitions(self, word, lines, lineNumber):
        self.printd('vstupuju getKnownDefinitions')

        line = lines[lineNumber]
        self.printd('hledane slovo: ' + word + '; A radka: ')
        self.printd(line)

        quotes = '[\'|"]'

        pattern = '\$' + word;

        self.printd(pattern);
        if re.search(pattern, line):
            self.printd('found variable A')
            return self.getVariable(word, lines, lineNumber)

        pattern = '->' + word;

        self.printd(pattern);
        if re.search(pattern, line):
            self.printd('found variable B')
            return self.getVariable(word, lines, lineNumber)

        #$orgService = IW_Core_BeanFactory::singleton('IW_OrgStr_User_Service')
        pattern = 'IW_Core_BeanFactory::singleton\(' + quotes + word + quotes + '\)';

        self.printd(pattern);
        if re.search(pattern, line):
            self.printd('found beanfactory singleton')

            oldFilename = self.getFilenameForOldClass(word)

            if oldFilename != False:
                return oldFilename

        #new Word()
        # ->valid(new VoValidator(), $listViewVo, 'listViewVo')
        #throw new IW_Core_Authorization_Exception(
        pattern = 'new ' + word + '\('; #pridat bily znaky pred zavorku, a aby nebyl zravej

        self.printd(pattern);
        if re.search(pattern, line):
            self.printd('found new word')
            return self.getUseNamespacedWord(word, lines, lineNumber, line)

        # NOT this -> IW_Core_Validate::getInstance() -> this is catched before with  getFilenameForOldClass(word)
        # but this-> Service::getInstance()
        pattern = word + '::getInstance\('; #pridat bily znaky pred zavorku, a aby nebyl zravej

        self.printd(pattern);
        self.printd(re.search(pattern, line));
        if re.search(pattern, line):
            self.printd('found word::getinstance')
            return self.getUseNamespacedWord(word, lines, lineNumber, line)

        pattern = word + '::class';

        self.printd(pattern);
        self.printd(re.search(pattern, line));
        if re.search(pattern, line):
            self.printd('found word::class')
            return self.getUseNamespacedWord(word, lines, lineNumber, line)

        pattern = word + '::';

        self.printd(pattern);
        self.printd(re.search(pattern, line));
        if re.search(pattern, line):
            self.printd('found word::')
            return self.getUseNamespacedWord(word, lines, lineNumber, line)

        #use \Brum\Vrum\Rum as Word;
        pattern = 'use .*as ' + word; #pridat zacatek radku

        self.printd(pattern);
        if re.search(pattern, line):
            self.printd('found use as word')
            return self.getUseNamespacedWordFromLine(word, lines, lineNumber)
        
        #use \Brum\Vrum\Word;
        #use \Brum\Vrum\Word as Rum;
        pattern = 'use .*' + word + '(;| )';  #pridat zacatek radku

        self.printd(pattern);
        if re.search(pattern, line):
            self.printd('found use word')
            return self.getUseNamespacedWordFromLine(word, lines, lineNumber)


        # try fallback (for expample for:  class A extends B) -> searching B
        self.printd('try fallback namespace')
        return self.getUseNamespacedWord(word, lines, lineNumber, line)
        #self.printd('koncim, nic jsem nenasel')
        #return False

    def getFilenameForOldClass(self, word):
        pattern = 'IW_\w+'

        if re.search(pattern, word) == None:
            return False;

        module = word[3:len(word)]
        rest = module[module.find('_')+1:]
        rest = rest + '.php'
        rest = rest.replace('_', '/')

        module = module[:module.find('_')]

        return './portal/' + module.lower() + '/impl/IW/' + module + '/' + rest

    def getUseNamespacedWordFromLine(self, word, lines, lineNumber):
        line = lines[lineNumber]

        return self._getNamespacedClass(line)

    def getUseNamespacedWord(self, word, lines, lineNumber, line):
        self.printd('hledam v namespace')

        result = self.getFilenameForOldClass(word)

        if result != False:
            self.printd('is old class def')
            return result

        # try first find the extended namespace use:  ABCD\EFG\word
        hasExtendedNamespace = False
        pattern = '([\w\\\\]*\\\\'+ word +')';

        self.printd('hledam pattern: ' + pattern);
        self.printd('na radce: ' + line);
        self.printd(re.search(pattern, line));
        res = re.search(pattern, line)
        if res:
            hasExtendedNamespace = True

            self.printd('found extended FFFF namespace ' + word)
            word = res.groups()[0]
            self.printd('found extended namespace ' + word)
            
        result = False
        i = 0
        namespaceDefLine = False
        namespaceDefPattern = 'namespace '

        cycleLineNumber = lineNumber;

        # i want another 3 lines, if are posible ( to support case: 
        # search for word Job, so the line number is less then the: namespace definitions ends with class {
        # class JobBB extends Job
        # {

        count = 0

        while len(lines) > cycleLineNumber and count < 3:
            cycleLineNumber += 1
            count += 1

        self.printd('cycle line number: ')
        self.printd(cycleLineNumber)
        for i in range(0, cycleLineNumber):
            self.printd('radek: ' + lines[i])
            self.printd('slovo: ' + word)
            self.printd('bylo nalezeno?: ' + lines[i].find(word).__str__())
            self.printd(' ');

            line = lines[i]

            if namespaceDefLine == False:
                namespaceDefPosition = lines[i].find(namespaceDefPattern)

                if namespaceDefPosition > -1:
                    namespaceDefLine = lines[i][namespaceDefPosition+len(namespaceDefPattern):]

                    namespaceDefLine = namespaceDefLine.replace('\n', '')
                    namespaceDefLine = namespaceDefLine.replace(';', '\\'+word)
                    namespaceDefLine += ';'

                    self.printd('namespace current directory:')
                    self.printd(namespaceDefLine)

                    if hasExtendedNamespace == True:
                        self.printd('lezu do namespaced class pro extended namespace')
                        result = self._getNamespacedClass(namespaceDefLine);
                        break;

            if line.find("{") > -1: # namespace definitions ends with class {
                self.printd(''),
                self.printd('konec namespace definitions, try current directory:');

                if namespaceDefLine == False:
                    #maybe the part of folder, cut the end, and try find again
                    beforePart = word[word.find('\\'):]
                    part = word[:word.find('\\')]

                    if len(part) == len(word):
                        # nic se nezkratilo ==> nenalezeno
                        return False

                    resultPart = self.getUseNamespacedWord(part, lines, i, '')

                    beforePart = beforePart.replace('\\', '/') #change path separators
                    newResult = resultPart[:resultPart.find('.php')]
                    newResult = newResult + beforePart + '.php'

                    return newResult
                else:
                    #open in current directory
                    result = self._getNamespacedClass(namespaceDefLine)
                break
            elif hasExtendedNamespace == False:

                if re.search(r"\b"+word+r"\b"+';', lines[i]) > -1:
                    if line.find(" as ") > -1:
                        #This if is for lines like:
                        # use IW\Core\ListView\Service;
                        # use IW\Core\ListView\Category\Service as CategoryService;
                        # -- and we search Service   So the code is prevent for opening wrong Category/Service
                        part = line[line.find(' as ')+4:-1]
                        if part == word:
                            result = self._getNamespacedClass(line)
                        else:
                            continue
                    else:
                        result = self._getNamespacedClass(line)

                    break

        self.printd('nasel jsem: ' + result)
        return result

    #def printd(self, string, debug=True):
    def printd(self, string, debug=False):
        if debug == True:
            print(string)

if __name__ == '__main__':
    print 'code navigate main'
