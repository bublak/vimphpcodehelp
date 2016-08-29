import unittest

from CodeParser import CodeParser

class TestClassCodeParser(unittest.TestCase):


    def test_getFilenameForOldClass(self):
        cch = CodeParser()

        actualResult = cch.getFilenameForOldClass('IW_User_ClickAndPrint_ClickAndPrintVo')

        self.assertEqual('./portal/user/impl/IW/User/ClickAndPrint/ClickAndPrintVo.php', actualResult)

    def test_getVariable(self):
        cch = CodeParser()

        word = 'modeService'
        lines = self._getLinesForExtendedFolderNamespace()
        lineNumber = 14 # edited against vim: -1
        line = '$newKeys = $modeService->createTags($apime, $propPath, [$text]);'

        actualResult = cch.getVariable(word, lines, lineNumber)

        self.assertEqual('./portal/modeman/impl/IW/ModeMan/Instance/Service.php', actualResult)

    def test_getVariableDefinedInConstructor(self):
        cch = CodeParser()

        word = '_import'
        lines = self._getLinesForVariableDefinedInConstructor()
        lineNumber = 29 # edited against vim: -1
        line = '        $result = $this->_import->importJobs([$jobVoDeveloper, $jobVoTester]);'

        actualResult = cch.getVariable(word, lines, lineNumber)

        self.assertEqual('./portal/module/impl/IX/Module/SubModule/Core/Import.php', actualResult)

    def test_getUseNamespacedWordExtendedFolderNamespace(self):
        cch = CodeParser()

        word = 'Authoron'
        lines = self._getLinesForExtendedFolderNamespace()
        lineNumber = 13
        line = '    $roles    = Model\He\Authoron::getRonce($iniiiice, $model);'

        actualResult = cch.getUseNamespacedWord(word, lines, lineNumber, line);

        self.assertEqual('./portal/cre/impl/IW/Cre/MM/Model/He/Authoron.php', actualResult)
    

    def _getLinesForVariableDefinedInConstructor(self):
        lines = [
            '<?php',
            '',
            'use IX\Module\SubModule\Core\Import;',
            '',
            '/**',
            ' * XXX.',
            ' *',
            ' * @author     XX XX <xx>',
            ' */',
            'class IX_ImportTest extends IX_Core_Test_AbstractTestCase',
            '{',
            '    /**',
            '     * Tested class.',
            '     *',
            '     * @var IX\Module\SubModule\Core\Import',
            '     */',
            '    private $_import = null;',
            '',
            '    /**',
            '     * Tests setup.',
            '     *',
            '     * @return void',
            '     */',
            '    protected function setUp() {',
            '        $this->_import  = new Import($this->_config);',
            '    }',
            '',
            '    public function testCreateJob() {',
            '        $result = $this->_import->importJobs([$jobVoDeveloper, $jobVoTester]);',
            '    }'
        ]

        return lines

    def _getLinesForExtendedFolderNamespace(self):
        lines = [
            '<?php',
            '',
            '// \core\modeman',
            'use IW\ModeMan\Instance\Service;',
            'use IW\Cre\MM\Model;',
            'use IW\Cre\MM\Model\Enum\Feature;',
            'use IW\Cre\MM\ModelManager;',
            'class ABRAKA extends Feature {',
            '',
            '    private function _xxxtes(xxe $ccccccce, Model $model) {',
            '    $acl    = GGGGGGGGGGG::getInstance();',
            '    $he = Model\Authoron\He::getInstance(); //* @var $helper Authoron\He */',
            '    $roles    = Model\He\Authoron::getRonce($iniiiice, $model);',
            '$modeService = Service::getInstance();',
            '$newKeys = $modeService->createTags($apime, $propPath, [$text]);'
        
        ]

        return lines

if __name__ == '__main__':
    unittest.main()
