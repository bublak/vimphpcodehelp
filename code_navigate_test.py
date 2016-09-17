import unittest

from ClassContextHint import ClassContextHint
from CodeParser import CodeParser

class TestCodeNavigate(unittest.TestCase):

    def test_getAncestorFromFile(self):
        self.maxDiff = None
        cch = ClassContextHint('cava')

        filename = 'testfilebasica.php'

        actualResult = cch.getContextHintsForFile(filename, False)

        self.assertEquals('AbstractVisibility', cch.hints.parentClass['name'])

        codeParser = CodeParser()

        lineNumber = 19

        parentClassPath = codeParser.startSearching(
            cch.hints.parentClass['name'], cch.hints.parentClass['lines'], lineNumber
        )

        self.assertEquals('./portal/user/impl/IW/User/Visibility/AbstractVisibility.php', parentClassPath)

if __name__ == '__main__':
    unittest.main()
