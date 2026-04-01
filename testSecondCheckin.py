import unittest
from university import University

class TestSearchByID(unittest.TestCase):
    
    def setUp(self):
        u = University()
        self.obj = u

    # Test: target is in the middle
    def test_found_middle(self):
        data = ["STU001", "STU002", "STU003", "STU004", "STU005"]
        self.assertEqual(self.obj.search_by_id(data, "STU003", 0, len(data)-1), 2)

    # Test: target is first element
    def test_found_first(self):
        data = ["STU001", "STU002", "STU003", "STU004", "STU005"]
        self.assertEqual(self.obj.search_by_id(data, "STU001", 0, len(data)-1), 0)

    # Test: target is last element
    def test_found_last(self):
        data = ["STU001", "STU002", "STU003", "STU004", "STU005"]
        self.assertEqual(self.obj.search_by_id(data, "STU005", 0, len(data)-1), 4)

    # Test: target not in list
    def test_not_found(self):
        data = ["STU001", "STU002", "STU003", "STU004", "STU005"]
        self.assertEqual(self.obj.search_by_id(data, "STU999", 0, len(data)-1), -1)

    # Test: empty list
    def test_empty_list(self):
        data = []
        self.assertEqual(self.obj.search_by_id(data, "STU001", 0, len(data)-1), -1)

    # Test: single element (found)
    def test_single_element_found(self):
        data = ["STU001"]
        self.assertEqual(self.obj.search_by_id(data, "STU001", 0, len(data)-1), 0)

    # Test: single element (not found)
    def test_single_element_not_found(self):
        data = ["STU001"]
        self.assertEqual(self.obj.search_by_id(data, "STU002", 0, len(data)-1), -1)
        
        
if __name__ == "_main__":
    unittest.main()