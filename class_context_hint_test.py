import unittest

from ClassContextHint import ClassContextHint

class TestClassContextHint(unittest.TestCase):

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

        #print actualResult
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
        expectedResult.extend(self._expectedResultFunctions())

        self.assertEqual(expectedResult, actualResult)

    def test_getContextHintsForFile(self):
        self.maxDiff = None
        cch = ClassContextHint('cava')

        filename = 'testfilebasic.php'

        actualResult = cch.getContextHintsForFile(filename, False)

        self.assertEqual(self._expectedResultForFile(), actualResult)

    def test_getMethodHintForFile(self):
        cch = ClassContextHint('vvv')

        filename     = 'testfilebasic.php'
        functionName = '__construct'

        actualResult = cch.getMethodHintForFile(filename, functionName, False)

        # TODO
        #print actualResult
        #self.assertEqual(self._expectedResultForFile(), actualResult)

    def _expectedResultForFile(self):
        return [
            "const ABC = 'abc'",
            "const EDF = 'abc'",
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
            'public iJk( $abc, $ddd=null, $d, $e="ble")'
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
            'public function gHch ($a, $ccc=null,', '    $d, $e="ble") ', ' { ',
            'public function iJk (', ' $abc, $ddd=null,', ' $d, $e="ble") { ',
            'private function _zZz(){',
            'private function xXx($abc, $kva){'
        ] 

        return a


if __name__ == '__main__':
    unittest.main()
