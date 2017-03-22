import os
import json

from NamespacePathCreator import NamespacePathCreator
from CodeParser import CodeParser

# TODO -> solve, how to call only once for calling from vim  -> save result in vim variable??
class CodeParserBuilder:

    def build():
        actualPath = os.getcwd()

        namespaceCreator = None

        if os.path.isfile(actualPath+'/composer.json'):
            with open('composer.json', 'r', encoding='utf-8') as f:
                composerData = json.load(f)

            if 'autoload' in composerData:
                if 'psr-4' in composerData['autoload']:
                    lineToParse = composerData['autoload']['psr-4']

                    for namespaceStr, pathRepl in lineToParse.items():
                        namespaceCreator = NamespacePathCreator(namespaceStr, pathRepl)

        codeParser = CodeParser(namespaceCreator)

        return codeParser

if __name__ == '__main__':
    print('code parser builder main')
