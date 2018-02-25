import unittest
from model import models

class TestProcesses(unittest.TestCase):

    def setUp(self):
        self.mongo = models.Mongo()

    def test_aggregation(self):
        result = self.mongo.get_processes().aggregate([{"$group": {"_id": "$assunto", "total": { "$sum": 1}}}])
        #result = self.mongo.get_varas().aggregate([{"$group": {"_id": "$done", "count": { "$sum": 1}}}])
        for d in result:
            print(d)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()