import unittest

from ClassContextHint import ClassContextHint
from CodeParser import CodeParser
from CodeNavigate import CodeNavigate

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

    def test_navigateToClassFilenameBasic(self):
        self.maxDiff = None

        codeNav = CodeNavigate()

        lines      = self._linesForNavigateToClassFilename()
        searchWord = 'urlHelper'
        lineNumber = 17
        lineNumber = lineNumber - 1 #correction to right line, where is cursor

        filenameResult = codeNav.navigateToClass(searchWord, lines, lineNumber)

        print filenameResult

        self.assertEquals('./portal/cre/views/helpers/CreUrl.php', filenameResult)

    def _linesForNavigateToClassFilename(self):
        lines = [
            '<?php',
            'namespace IW\Cre;',
            'use IW\Cre\Cche\Addp;',
            '',
            '/**',
            '* Some text',
            '* Some text',
            '*',
            '* @author     Some author <author@email.cz>',
            '* @version    SVN: $Id: Bff.php 145409 1951-09-20 11:02:30Z cc.ccc $',
            '* @category   Cre',
            '* @package    Bff',
            '*/',
            'class Bff extends Addp\Mmy',
            '{'
            'protected function kvakva(array $params) {',
            '    $urlHelper = new IW_Cre_Views_Helper_CreUrl();',
            '    $b = $urlHelper->testA();'
        ]

        return lines

if __name__ == '__main__':
    unittest.main()
