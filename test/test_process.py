import unittest
from model import models

class TestProcesses(unittest.TestCase):

    def setUp(self):
        self.mongo = models.Mongo()

    def test_find_one(self):
        p = models.Process()
        p = p.find_one(self.mongo.get_processes(), '1002283-37.2017.8.26.0081')
        self.assertIsInstance(p, models.Process)


if __name__ == '__main__':
    unittest.main()