import unittest
from structures import HashMap
from student import Student
from course import Course


class TestHashMapBasic(unittest.TestCase):
    """Tests for basic put and get operations on the HashMap DH"""

    def setUp(self):
        """Initialize a small HashMap before each test DH"""
        self.hm = HashMap(5)

    def testPutAndGet(self):
        """Verify that a value stored with put is correctly returned by get DH"""
        self.hm.put("CSE1010", ["none"])
        self.assertEqual(self.hm.get("CSE1010"), ["none"])

    def testGetMissingKeyReturnsNone(self):
        """Verify that get returns None for a key that was never inserted DH"""
        self.assertIsNone(self.hm.get("CSE9999"))

    def testOverwriteExistingKey(self):
        """Verify that putting a duplicate key updates the value rather than adding a new entry DH"""
        self.hm.put("CSE2050", ["CSE1010"])
        self.hm.put("CSE2050", ["CSE1010", "MATH1010"])
        self.assertEqual(self.hm.get("CSE2050"), ["CSE1010", "MATH1010"])

    def testCountDoesNotIncreaseOnOverwrite(self):
        """Verify that overwriting an existing key does not increment the internal count DH"""
        self.hm.put("CSE2050", ["CSE1010"])
        countBefore = self.hm.count
        self.hm.put("CSE2050", ["CSE1010", "MATH1010"])
        self.assertEqual(self.hm.count, countBefore)


class TestHashMapCollisions(unittest.TestCase):
    """Tests for collision handling via separate chaining DH"""

    def testCollisionsStoredInSameBucket(self):
        """Verify that multiple keys hashing to the same bucket are all retrievable DH"""
        forcedCollisionMap = HashMap(1)
        forcedCollisionMap.put("keyA", "valueA")
        forcedCollisionMap.put("keyB", "valueB")
        forcedCollisionMap.put("keyC", "valueC")
        self.assertEqual(forcedCollisionMap.get("keyA"), "valueA")
        self.assertEqual(forcedCollisionMap.get("keyB"), "valueB")
        self.assertEqual(forcedCollisionMap.get("keyC"), "valueC")

    def testCollisionBucketContainsMultipleEntries(self):
        """Verify that two integer keys that always map to the same bucket are both stored there DH"""
        hm = HashMap(10)
        hm.put(0, "alpha")
        hm.put(10, "beta")
        self.assertGreater(len(hm.buckets[0]), 1)

    def testCollisionOverwritePreservesOtherKeys(self):
        """Verify that overwriting one colliding key does not corrupt the others DH"""
        forcedCollisionMap = HashMap(1)
        forcedCollisionMap.put("keyA", "original")
        forcedCollisionMap.put("keyB", "stays")
        forcedCollisionMap.put("keyA", "updated")
        self.assertEqual(forcedCollisionMap.get("keyA"), "updated")
        self.assertEqual(forcedCollisionMap.get("keyB"), "stays")


class TestHashMapRehashing(unittest.TestCase):
    """Tests for load-factor-triggered rehashing behavior DH"""

    def testRehashDoublesTableSize(self):
        """Verify that the bucket count doubles once the load factor reaches 0.8 DH"""
        hm = HashMap(5)
        initialSize = hm.size
        for i in range(4):
            hm.put(f"key{i}", f"val{i}")
        self.assertEqual(hm.size, initialSize * 2)

    def testRehashTriggersAtExact80Percent(self):
        """Verify that 3 keys in a size-5 table do not trigger a rehash but the 4th does DH"""
        hm = HashMap(5)
        for i in range(3):
            hm.put(f"key{i}", i)
        self.assertEqual(hm.size, 5)
        hm.put("key3", 3)
        self.assertEqual(hm.size, 10)

    def testAllDataPreservedAfterRehash(self):
        """Verify that every key inserted before the rehash is still retrievable after it DH"""
        hm = HashMap(5)
        insertedPairs = {f"course{i}": f"prereq{i}" for i in range(6)}
        for key, value in insertedPairs.items():
            hm.put(key, value)
        for key, expectedValue in insertedPairs.items():
            self.assertEqual(hm.get(key), expectedValue)

    def testCountIsCorrectAfterRehash(self):
        """Verify that the internal count accurately reflects the number of unique keys after rehashing DH"""
        hm = HashMap(5)
        for i in range(6):
            hm.put(f"k{i}", i)
        self.assertEqual(hm.count, 6)

    def testMultipleRehashesStillReturnCorrectValues(self):
        """Verify that data integrity is maintained across multiple rehash cycles DH"""
        hm = HashMap(2)
        for i in range(20):
            hm.put(f"key{i}", i * 10)
        for i in range(20):
            self.assertEqual(hm.get(f"key{i}"), i * 10)

class TestPrerequisiteEnrollment(unittest.TestCase):
    '''Verify that enrollment correctly enforces prerequisite rules DH'''

    def setUp(self):
        '''Setup a course and a student for enrollment testing DH'''
        self.c = Course("CSE2050", 3, 1) # Cap of 1
        self.s = Student("STU01", "Test Student")

    def testPrereqSuccess(self):
        '''Ensure student can enroll if they have the prerequisite DH'''
        self.c.prerequisites.put("CSE2050", "CSE1010")
        self.s.courses["CSE1010"] = "A" # Add to history
        
        self.c.request_enroll(self.s)
        self.assertEqual(len(self.c.enrolled_roster), 1)

    def testPrereqMissingRaisesException(self):
        '''Ensure Exception is raised when student lacks prerequisite DH'''
        self.c.prerequisites.put("CSE2050", "CSE1010")
        # Student history is empty
        
        with self.assertRaises(Exception):
            self.c.request_enroll(self.s)

    def testPrereqMetButCourseFull(self):
        '''Ensure student moves to waitlist if prereq is met but roster is full DH'''
        self.c.maxStudents = 0 # Force waitlist
        self.c.prerequisites.put("CSE2050", "CSE1010")
        self.s.courses["CSE1010"] = "B"
        
        self.c.request_enroll(self.s)
        self.assertEqual(len(self.c.waitlist), 1)

if __name__ == "__main__":
    unittest.main()