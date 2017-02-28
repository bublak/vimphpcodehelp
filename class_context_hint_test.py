import unittest

from ClassContextHint import ClassContextHint

class TestClassContextHint(unittest.TestCase):

    def test_loadNamespaceDefinitions(self):
        cch = ClassContextHint('cava')
        lines = self._getLinesForNamespaceDefinitions()

        result = cch.loadNamespaceDefinitions(lines)

        expectedNames = ['Def', 'first', 'second', 'Third', 'UCF']

        self.assertEquals(expectedNames, result)

    def test_checkUnusedNamespaceDefinitionsForLines(self):
        cch = ClassContextHint('cava')
        lines = self._getLinesForNamespaceDefinitions()

        definitions = ['Def', 'first', 'second', 'Third', 'UCF']

        result = cch.checkUnusedNamespaceDefinitionsForLines(lines, definitions)

        expectedResult = ['first', 'second']

        self.assertEquals(expectedResult, result)
    def test_getAncestor(self):
        cch = ClassContextHint('cava')

        lines = self._getLinesForAncestor()
        result = cch.getAncestor(lines)

        self.assertEquals(0, len(cch.hints.functions))
        self.assertEquals(3, cch.hints.parentClass['lineNumber'])
        self.assertEquals('Def', cch.hints.parentClass['name'])

        expectedLines = [
            'namespace afaef\faeggg\affe;',
            '',
            'use tada\ble\Def;'
            '',
            'class Abc extends Def',
            '{',
            ''
        ]

        self.assertEquals(expectedLines, cch.hints.parentClass['lines'])

        self.assertFalse(result)

    def test_getAncestorNoAncestor(self):
        cch = ClassContextHint('cava')

        lines = self._getLinesExample()
        result = cch.getAncestor(lines)

        self.assertFalse(result)

    def test_loadConstants(self):
        cch = ClassContextHint('test/path/')

        lines = self._getLinesForConstants()

        actualResult = cch.loadConstants(lines)

        self.assertEqual(self._expectedResultConstants(), actualResult)

    def test_loadFunctions(self):
        self.maxDiff = None
        cch = ClassContextHint('test/pathB/')

        lines = self._getLinesForFunctions()

        actualResult = cch.loadFunctions(lines)

        #print(actualResult)
        self.assertEqual(self._expectedResultFunctions(), actualResult)

    def test_loadFunctionsFilteredNotFound(self):
        cch = ClassContextHint('bl/bl/')

        lines = self._getLinesForFunctions()

        actualResult = cch.loadFunctions(lines, 'ijk')

        self.assertEqual([], actualResult)

    def test_loadFunctionsFiltered(self):
        cch = ClassContextHint('bl/bl/a')

        lines = self._getLinesForFunctions()

        actualResult = cch.loadFunctions(lines, 'iJk')

        self.assertEqual(['public iJk( $abc, $ddd=null, $d, $e="ble")'], actualResult)

    def test_getContextHints(self):
        cch = ClassContextHint('vvv/ccc')

        lines = self._getLinesForFunctions()

        actualResult = cch.getContextHints(lines)

        expectedResult = []
        expectedResult.extend(self._expectedResultConstants())
        expectedResult.extend('\n')
        expectedResult.extend(self._expectedResultFunctions())

        self.assertEqual(expectedResult, actualResult)

    def test_getContextHintsForFile(self):
        self.maxDiff = None
        cch = ClassContextHint('cava')

        filename = 'testfilebasic.php'

        actualResult = cch.getContextHintsForFile(filename, False)

        result = actualResult.getAllPrintable('', '-block-separator--')
        self.assertEqual(self._expectedResultForFile(), result)

    def test_getMethodHintForFile(self):
        cch = ClassContextHint('vvv')

        filename     = 'testfilebasic.php'
        functionName = '__construct'

        actualResult = cch.getMethodHintForFile(filename, functionName, False)

        # TODO
        #print(actualResult)
        #self.assertEqual(self._expectedResultForFile(), actualResult)


    def _expectedResultForFile(self):
        return [
            "const ABC = 'abc'",
            "const EDF = 'abc'",
            "const EDFG = 'abc_some long text which can break layout or something :) abcdefghijklmnopqr...",
            '-block-separator--',
            'abstract public renderHeaderb(array $preparedHeader)',
            'protected abstract getConfigData()',
            'protected createDOMDocument()',
            'protected setDocumentAttribute(DOMElement $document)',
            'protected static sortFunction($first, $second, $rules)',
            'public __construct($fullPath, $isRoot=false)',
            'public abstract renderHeader(array $preparedHeader)',
            'public addNode(Mputree $node)',
            'public getExecTime()',
            'public getExecTimeRating()',
            'public getFilename()',
            'public getFullPath()',
            'public getNodes()',
            'public save($file)',
            'public setExecTime($time)',
            'public setExecTimeRating($rating)',
            'public setFilename($name)',
            'public setFullPath($path)',
            'public setNodes(array $nodes)',
            'public static getEvaluationBasePath()'
        ]


    def _expectedResultConstants(self):
        return ['const A = "43"', 'const B = "44fads"']

    def _expectedResultFunctions(self):
        return [
            'public aBc()',
            'public eDf($abc, $kva)',
            'public gHch($a, $ccc=null,    $d, $e="ble")',
            'public iJk( $abc, $ddd=null, $d, $e="ble")',
            'public iJkKva( $abc, $ddd=null, $d, $e="ble")'
        ]

    def _getLinesForConstants(self):
        a = ['jedna', 'dve', 'tri', 'const A="43";', 'const B = "44fads";']
        return a

    def _getLinesForFunctions(self):
        a = [
            'jedna',
            'dve',
            'tri',
            'const A="43";',
            'const B = "44fads";',
            '  public function aBc(){',
            'public function eDf($abc, $kva)', '{',
            'public function iJkKva (', ' $abc, $ddd=null,', ' $d, $e="ble") { ', #bug for filter function: iJk
            'public function gHch ($a, $ccc=null,', '    $d, $e="ble") ', ' { ',
            'public function iJk (', ' $abc, $ddd=null,', ' $d, $e="ble") { ',
            'private function _zZz(){',
            'private function xXx($abc, $kva){'
        ]

        return a

    def _getLinesExample(self):
        a = [
            'namespace afaef\faeggg\affe;',
            '',
            'use tada\ble\Def;'
            '',
            'class Abc',
            '{',
            '',
            '',
            '',
            ''
        ]

        return a

    def _getLinesForAncestor(self):
        a = [
            'namespace afaef\faeggg\affe;',
            '',
            'use tada\ble\Def;'
            '',
            'class Abc extends Def',
            '{',
            '',
            'a',
            'b',
            'c'
        ]

        return a

    def _getLinesForNamespaceDefinitions(self):
        a = [
            r'namespace afaef\faeggg\affe;',
            '\n',
            r'use tada\ble\Def;'
            '\n',
            r'use multi\blu\first,'
            '\n',
            r'    multi\blu\second,'
            '\n',
            r'    tmulti\bla\Third;'
            '\n',
            r'use udu\kva\ABC as UCF;'
            '\n',
            '',
            'class Abc extends Def',
            '{',
            'new Third',
            '',
            'function',
            'aUCF'
        ]

        return a

if __name__ == '__main__':
    unittest.main()
