import unittest
from university import University

class TestSearchByID(unittest.TestCase):
    """Tests to verify progress SM"""
    
    def setUp(self):
        """Setup an object to test on SM"""
        u = University()
        self.obj = u


    def test_found_middle(self):
        """Test object at middle index SM"""
        data = ["STU001", "STU002", "STU003", "STU004", "STU005"]
        self.assertEqual(self.obj.search_by_id(data, "STU003", 0, len(data)-1), 2)


    def test_found_first(self):
        """Test id at index 0 SM"""
        data = ["STU001", "STU002", "STU003", "STU004", "STU005"]
        self.assertEqual(self.obj.search_by_id(data, "STU001", 0, len(data)-1), 0)


    def test_found_last(self):
        """Test  id at last index SM"""
        data = ["STU001", "STU002", "STU003", "STU004", "STU005"]
        self.assertEqual(self.obj.search_by_id(data, "STU005", 0, len(data)-1), 4)

    
    def test_not_found(self):
        """Test id no in list SM"""
        data = ["STU001", "STU002", "STU003", "STU004", "STU005"]
        self.assertEqual(self.obj.search_by_id(data, "STU999", 0, len(data)-1), -1)


    def test_empty_list(self):
        """Test behavior on an empty list SM"""
        data = []
        self.assertEqual(self.obj.search_by_id(data, "STU001", 0, len(data)-1), -1)


    def test_single_element_found(self):
        """Test one element successful search SM"""
        data = ["STU001"]
        self.assertEqual(self.obj.search_by_id(data, "STU001", 0, len(data)-1), 0)

    def test_single_element_not_found(self):
        """Test one element, failed search SM"""
        data = ["STU001"]
        self.assertEqual(self.obj.search_by_id(data, "STU002", 0, len(data)-1), -1)
        
        
if __name__ == "__main__":
    unittest.main()