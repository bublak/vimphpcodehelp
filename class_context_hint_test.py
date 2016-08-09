import unittest

from ClassContextHint import ClassContextHint

class TestClassContextHint(unittest.TestCase):

    def test_loadConstants(self):
        cch = ClassContextHint()

        lines = self._getLinesForConstants()

        actualResult = cch.loadConstants(lines)

        self.assertEqual(['A', 'B'], actualResult)

    def test_loadFunctions(self):
        cch = ClassContextHint()

        lines = self._getLinesForFunctions()

        actualResult = cch.loadFunctions(lines)

        #print actualResult
        #self.assertEqual('context hint abc', actualResult)

    def test_getContextHints(self):
        cch = ClassContextHint()

        lines = self._getLinesForFunctions()

        actualResult = cch.getContextHints(lines)

        #print actualResult
        #self.assertEqual('context hint abc', actualResult)

    def test_getContextHintsForFile(self):
        cch = ClassContextHint()

        filename = 'testfilebasic.php'

        actualResult = cch.getContextHintsForFile(filename, False)

        print actualResult
        #self.assertEqual('context hint abc', actualResult)


    def _getLinesForConstants(self):
        a = ['jedna', 'dve', 'tri', 'const A="43";', 'const B = "44fads";'] 
        return a

    def _getLinesForFunctions(self):
        a = [
            'jedna', 'dve', 'tri', 'const A="43";', 'const B = "44fads";',
            '  public function aBc(){', 'public function eDf($abc, $kva)',
            'public function gHch ($a, $ccc=null,\n    $d, $e="ble") ',
            'public function iJk (\n $abc, $ddd=null,\n $d, $e="ble") { ',
            'private function _zZz(){', 'private function xXx($abc, $kva)',
        ] 

        return a


if __name__ == '__main__':
    unittest.main()
