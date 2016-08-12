import unittest

from CodeNavigate import CodeNavigate

class TestClassContextHint(unittest.TestCase):

    #TODO controler class User_UserController extends IW_User_Core_Controller

    def test_getFilenameForOldClass(self):
        cch = CodeNavigate()

        actualResult = cch.getFilenameForOldClass('IW_User_ClickAndPrint_ClickAndPrintVo')

        self.assertEqual('./portal/user/impl/IW/User/ClickAndPrint/ClickAndPrintVo.php', actualResult)

    
    def test_getUseNamespacedWordExtendedFolderNamespace(self):
        cch = CodeNavigate()

        word = 'Authoron'
        lines = self._getLinesForExtendedFolderNamespace()
        lineNumber = 12
        line = '    $roles    = Model\He\Authoron::getRonce($iniiiice, $model);'

        actualResult = cch.getUseNamespacedWord(word, lines, lineNumber, line);

        self.assertEqual('./portal/cre/impl/IW/Cre/MM/Model/He/Authoron.php', actualResult)

    def _getLinesForExtendedFolderNamespace(self):
        lines = [
            '<?php',
            '',
            '// \core\modeman',
            'use IW\Cre\MM\Model;',
            'use IW\Cre\MM\Model\Enum\Feature;',
            'use IW\Cre\MM\ModelManager;',
            'class ABRAKA {'
            '',
            '    private function _xxxtes(xxe $ccccccce, Model $model) {',
            '    $acl    = GGGGGGGGGGG::getInstance();',
            '    $he = Model\Authoron\He::getInstance(); //* @var $helper Authoron\He */',
            '    $roles    = Model\He\Authoron::getRonce($iniiiice, $model);'
        ]

        return lines

if __name__ == '__main__':
    unittest.main()
