from app.Initiator import Initiator
import unittest


class TestCodeInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def test_uhunt(self):
        try:
            uhunt = Initiator("uhunt")
            uhunt.generate_code(787, "py", False)
        except Exception as e:
            self.assertIsNone(e)


if __name__ == "__main__":
    unittest.main()
