import unittest

from CodeNavigate import CodeNavigate

class TestClassContextHint(unittest.TestCase):

    #TODO controler class User_UserController extends IW_User_Core_Controller

    def test_getFilenameForOldClass(self):
        cch = CodeNavigate()

        actualResult = cch.getFilenameForOldClass('IW_User_ClickAndPrint_ClickAndPrintVo')

        self.assertEqual('./portal/user/impl/IW/User/ClickAndPrint/ClickAndPrintVo.php', actualResult)

if __name__ == '__main__':
    unittest.main()
