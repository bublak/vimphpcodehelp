import unittest

from ClassContextHint import ClassContextHint

class TestClassContextHint(unittest.TestCase):

    def test_loadConstants(self):
        cch = ClassContextHint()

        lines = self._getLinesForConstants()

        actualResult = cch.loadConstants(lines)

        self.assertEqual(self._expectedResultConstants(), actualResult)

    def test_loadFunctions(self):
        cch = ClassContextHint()

        lines = self._getLinesForFunctions()

        actualResult = cch.loadFunctions(lines)

        #print actualResult
        self.assertEqual(self._expectedResultFunctions(), actualResult)

    
    def test_getContextHints(self):
        cch = ClassContextHint()

        lines = self._getLinesForFunctions()

        actualResult = cch.getContextHints(lines)

        expectedResult = []
        expectedResult.extend(self._expectedResultConstants())
        expectedResult.extend(self._expectedResultFunctions())

        self.assertEqual(expectedResult, actualResult)

    def test_getContextHintsForFile(self):
        cch = ClassContextHint()

        filename = 'testfilebasic.php'

        actualResult = cch.getContextHintsForFile(filename, False)

        self.assertEqual(self._expectedResultForFile(), actualResult)


    def _expectedResultForFile(self):
        return [
            "const ABC = 'abc'",
            "const EDF = 'abc'",
            'protected sortFunction($first, $second, $rules)',
            'public getEvaluationBasePath()',
            'protected createDOMDocument()',
            'public __construct($fullPath, $isRoot=false)',
            'public setFullPath($path)',
            'public setFilename($name)',
            'public setNodes(array $nodes)',
            'public setExecTimeRating($rating)',
            'public setExecTime($time)',
            'public addNode(Mputree $node)',
            'public getExecTimeRating()',
            'public getExecTime()',
            'public getNodes()',
            'public getFullPath()',
            'public getFilename()',
            'public save($file)'
        ]


    def _expectedResultConstants(self):
        return ['const A="43"', 'const B = "44fads"']

    def _expectedResultFunctions(self):
        return [
            'public aBc()',
            'public eDf($abc, $kva)',
            'public gHch ($a, $ccc=null,    $d, $e="ble")',
            'public iJk ( $abc, $ddd=null, $d, $e="ble")'
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
