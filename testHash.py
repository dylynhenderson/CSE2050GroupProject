from university import University, loadprerequisites
from structures import HashMap
import unittest

class TestHashMap(unittest.TestCase):
    
    def test_set_and_get(self):
        """Test basic set and get functionality of HashMap SM"""
        hm = HashMap(5)
        hm.set('key1', 'value1')
        hm.set('key2', 'value2')
        self.assertEqual(hm.get('key1'), 'value1')
        self.assertEqual(hm.get('key2'), 'value2')
        self.assertIsNone(hm.get('nonexistent'))

    def test_overwrite_value(self):
        """"Test that setting a key that already exists overwrites the value SM"""
        hm = HashMap(5)
        hm.set('key1', 'value1')
        hm.set('key1', 'new_value')
        self.assertEqual(hm.get('key1'), 'new_value')

    def test_collision_handling(self):
        """Test that HashMap can handle collisions SM"""
        hm = HashMap(1)  # Force collisions
        hm.set('key1', 'value1')
        hm.set('key2', 'value2')  # This will collide with key1
        self.assertEqual(hm.get('key1'), 'value1')
        self.assertEqual(hm.get('key2'), 'value2')
        
class TestLoadPrerequisites(unittest.TestCase):

    def setUp(self):
        """Load hashmap once per test SM"""
        self.prereqMap = loadprerequisites("cse_prerequisites.csv")

    def test_basic_values(self):
        """Check correct single prerequisites SM"""
        self.assertEqual(self.prereqMap.get("CSE2050"), ["CSE1010"])
        self.assertEqual(self.prereqMap.get("CSE2102"), ["CSE2050"])
        self.assertEqual(self.prereqMap.get("CSE2500"), ["CSE2050"])

    def test_empty_prerequisites(self):
        """Courses with no prerequisites SM"""
        self.assertEqual(self.prereqMap.get("CSE1010"), [])
        self.assertEqual(self.prereqMap.get("CSE2600"), [])
        self.assertEqual(self.prereqMap.get("CSE3140"), [])
        self.assertEqual(self.prereqMap.get("CSE3666"), [])

    def test_multiple_dependents(self):
        """Course used by multiple others SM"""
        self.assertEqual(self.prereqMap.get("CSE3100"), ["CSE2050"])
        self.assertEqual(self.prereqMap.get("CSE3150"), ["CSE3100"])
        self.assertEqual(self.prereqMap.get("CSE3500"), ["CSE3100"])

    def test_all_courses_exist(self):
        """Ensure all courses exist in hashmap SM"""
        courses = [
            "CSE1010", "CSE2050", "CSE2102", "CSE2500",
            "CSE2600", "CSE3100", "CSE3140",
            "CSE3150", "CSE3500", "CSE3666"
        ]

        for course in courses:
            self.assertIsNotNone(self.prereqMap.get(course))

    def test_nonexistent_course(self):
        """Invalid course returns None SM"""
        self.assertIsNone(self.prereqMap.get("CSE9999"))

    def test_all_values_are_lists(self):
        """Every value must be a list SM"""
        for bucket in self.prereqMap.buckets:
            for key, value in bucket:
                self.assertIsInstance(value, list)

    def test_no_empty_strings(self):
        """Ensure no empty string prereqs exist SM"""
        for bucket in self.prereqMap.buckets:
            for key, value in bucket:
                self.assertNotIn("", value)

if __name__ == '__main__':
    unittest.main()