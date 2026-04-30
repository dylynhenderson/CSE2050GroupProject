import unittest
from structures import HashMap
from student import Student
from course import Course


class TestHashMapBasic(unittest.TestCase):
    """Tests for basic put and get operations on the HashMap DH"""

    def setUp(self):
        self.hm = HashMap(5)

    def testPutAndGet(self):
        """Value stored with put is correctly returned by get DH"""
        self.hm.put("CSE1010", ["none"])
        self.assertEqual(self.hm.get("CSE1010"), ["none"])

    def testGetMissingKeyReturnsNone(self):
        """get returns None for a key never inserted DH"""
        self.assertIsNone(self.hm.get("CSE9999"))

    def testOverwriteExistingKey(self):
        """Putting a duplicate key updates the value DH"""
        self.hm.put("CSE2050", ["CSE1010"])
        self.hm.put("CSE2050", ["CSE1010", "MATH1010"])
        self.assertEqual(self.hm.get("CSE2050"), ["CSE1010", "MATH1010"])

    def testCountDoesNotIncreaseOnOverwrite(self):
        """Overwriting an existing key does not increment count DH"""
        self.hm.put("CSE2050", ["CSE1010"])
        countBefore = self.hm.count
        self.hm.put("CSE2050", ["CSE1010", "MATH1010"])
        self.assertEqual(self.hm.count, countBefore)


class TestHashMapCollisions(unittest.TestCase):
    """Tests for collision handling via separate chaining DH"""

    def testCollisionsStoredInSameBucket(self):
        """Multiple keys forced to the same bucket are all retrievable DH"""
        forcedCollisionMap = HashMap(1)
        forcedCollisionMap.put("keyA", "valueA")
        forcedCollisionMap.put("keyB", "valueB")
        forcedCollisionMap.put("keyC", "valueC")
        self.assertEqual(forcedCollisionMap.get("keyA"), "valueA")
        self.assertEqual(forcedCollisionMap.get("keyB"), "valueB")
        self.assertEqual(forcedCollisionMap.get("keyC"), "valueC")

    def testCollisionBucketContainsMultipleEntries(self):
        """Two integer keys that map to the same bucket are both stored there DH"""
        hm = HashMap(10)
        hm.put(0, "alpha")
        hm.put(10, "beta")
        self.assertGreater(len(hm.buckets[0]), 1)

    def testCollisionOverwritePreservesOtherKeys(self):
        """Overwriting one colliding key does not corrupt others DH"""
        forcedCollisionMap = HashMap(1)
        forcedCollisionMap.put("keyA", "original")
        forcedCollisionMap.put("keyB", "stays")
        forcedCollisionMap.put("keyA", "updated")
        self.assertEqual(forcedCollisionMap.get("keyA"), "updated")
        self.assertEqual(forcedCollisionMap.get("keyB"), "stays")


class TestHashMapRehashing(unittest.TestCase):
    """Tests for load-factor-triggered rehashing DH"""

    def testRehashDoublesTableSize(self):
        """Bucket count doubles once load factor reaches 0.8 DH"""
        hm = HashMap(5)
        initialSize = hm.size
        for i in range(4):
            hm.put(f"key{i}", f"val{i}")
        self.assertEqual(hm.size, initialSize * 2)

    def testRehashTriggersAtExact80Percent(self):
        """3 keys in size-5 table do not rehash; 4th does DH"""
        hm = HashMap(5)
        for i in range(3):
            hm.put(f"key{i}", i)
        self.assertEqual(hm.size, 5)
        hm.put("key3", 3)
        self.assertEqual(hm.size, 10)

    def testAllDataPreservedAfterRehash(self):
        """Every key inserted before rehash is still retrievable after DH"""
        hm = HashMap(5)
        insertedPairs = {f"course{i}": f"prereq{i}" for i in range(6)}
        for key, value in insertedPairs.items():
            hm.put(key, value)
        for key, expectedValue in insertedPairs.items():
            self.assertEqual(hm.get(key), expectedValue)

    def testCountIsCorrectAfterRehash(self):
        """Internal count accurately reflects unique keys after rehashing DH"""
        hm = HashMap(5)
        for i in range(6):
            hm.put(f"k{i}", i)
        self.assertEqual(hm.count, 6)

    def testMultipleRehashesStillReturnCorrectValues(self):
        """Data integrity maintained across multiple rehash cycles DH"""
        hm = HashMap(2)
        for i in range(20):
            hm.put(f"key{i}", i * 10)
        for i in range(20):
            self.assertEqual(hm.get(f"key{i}"), i * 10)


class TestPrerequisiteEnrollment(unittest.TestCase):
    '''Verify that enrollment correctly enforces prerequisite rules DH'''

    def setUp(self):
        self.c = Course("CSE2050", 3, 5)
        self.s = Student("Test Student", "STU00001")

    def testPrereqSuccess(self):
        '''Student with the prerequisite can enroll DH'''
        self.c.prerequisites.put("CSE2050", "CSE1010")
        self.s.courses["CSE1010"] = "A"
        self.c.request_enroll(self.s)
        self.assertEqual(len(self.c.enrolled_roster), 1)

    def testPrereqMissingRaisesException(self):
        '''Exception raised when student lacks prerequisite DH'''
        self.c.prerequisites.put("CSE2050", "CSE1010")
        with self.assertRaises(Exception):
            self.c.request_enroll(self.s)

    def testPrereqMetButCourseFull(self):
        '''Student moves to waitlist if prereq is met but roster is full DH'''
        self.c.maxStudents = 0
        self.c.prerequisites.put("CSE2050", "CSE1010")
        self.s.courses["CSE1010"] = "B"
        self.c.request_enroll(self.s)
        self.assertEqual(len(self.c.waitlist), 1)

    def testNoCourseNoPrereqSucceeds(self):
        '''Course with no prerequisite allows enrollment DH'''
        c = Course("CSE3666", 3, 5)  # No prereq stored
        self.c.request_enroll(self.s)   # Should not raise

    def testStudentEnrollRollbackOnFailedPrereq(self):
        '''Student.enroll rolls back course entry when prereq check fails DH'''
        self.c.prerequisites.put("CSE2050", "CSE1010")
        with self.assertRaises(Exception):
            self.s.enroll(self.c, "A")
        # Course must NOT remain in student.courses after a failed enroll
        self.assertNotIn(self.c, self.s.courses)

    def testCourseObjectKeyPrereqCheck(self):
        '''Prereq check works when prior course is stored as a Course object key DH'''
        prereqCourse = Course("CSE1010", 3, 5)
        # Enroll student in CSE1010 first (stores Course object as key)
        prereqCourse.request_enroll(self.s)
        self.s.courses[prereqCourse] = "A"
        # Now enroll in CSE2050
        self.c.prerequisites.put("CSE2050", "CSE1010")
        self.c.request_enroll(self.s)
        self.assertEqual(len(self.c.enrolled_roster), 1)


class TestMergeSort(unittest.TestCase):
    """Tests for the Merge Sort implementation DH"""

    def setUp(self):
        """Create a course and enroll four students in non-sorted order DH"""
        self.c = Course("CSE2050", 3, 10)
        data = [
            ("STU00003", "Charlie", "2024-03-01"),
            ("STU00001", "Alice",   "2024-01-01"),
            ("STU00004", "Dave",    "2024-04-01"),
            ("STU00002", "Bob",     "2024-02-01"),
        ]
        for sid, name, date in data:
            self.c.request_enroll(Student(name, sid), date)

    def testMergeSortById(self):
        """Merge sort by ID produces ascending order DH"""
        self.c.sort_enrolled('id', algorithm='merge')
        ids = [r.student.id for r in self.c.enrolled_roster]
        self.assertEqual(ids, sorted(ids))

    def testMergeSortByName(self):
        """Merge sort by name produces alphabetical order DH"""
        self.c.sort_enrolled('name', algorithm='merge')
        names = [r.student.name for r in self.c.enrolled_roster]
        self.assertEqual(names, sorted(names))

    def testMergeSortByDate(self):
        """Merge sort by date produces chronological order DH"""
        self.c.sort_enrolled('date', algorithm='merge')
        dates = [r.enroll_date for r in self.c.enrolled_roster]
        self.assertEqual(dates, sorted(dates))

    def testMergeSortPreservesAllRecords(self):
        """Merge sort does not drop or duplicate any enrollment records DH"""
        before = {r.student.id for r in self.c.enrolled_roster}
        self.c.sort_enrolled('id', algorithm='merge')
        after = {r.student.id for r in self.c.enrolled_roster}
        self.assertEqual(before, after)
        self.assertEqual(len(self.c.enrolled_roster), 4)

    def testMergeSortAlreadySorted(self):
        """Merge sort on an already-sorted roster returns the same order DH"""
        self.c.sort_enrolled('id', algorithm='merge')
        first_pass = [r.student.id for r in self.c.enrolled_roster]
        self.c.sort_enrolled('id', algorithm='merge')
        second_pass = [r.student.id for r in self.c.enrolled_roster]
        self.assertEqual(first_pass, second_pass)

    def testMergeSortSingleElement(self):
        """Merge sort on a one-element roster does not crash DH"""
        c = Course("CSE1010", 3, 5)
        c.request_enroll(Student("Only One", "STU00001"), "2024-01-01")
        c.sort_enrolled('id', algorithm='merge')
        self.assertEqual(len(c.enrolled_roster), 1)


class TestQuickSort(unittest.TestCase):
    """Tests for the Quick Sort implementation DH"""

    def setUp(self):
        """Create a course and enroll four students in non-sorted order DH"""
        self.c = Course("CSE2050", 3, 10)
        data = [
            ("STU00003", "Charlie", "2024-03-01"),
            ("STU00001", "Alice",   "2024-01-01"),
            ("STU00004", "Dave",    "2024-04-01"),
            ("STU00002", "Bob",     "2024-02-01"),
        ]
        for sid, name, date in data:
            self.c.request_enroll(Student(name, sid), date)

    def testQuickSortById(self):
        """Quick sort by ID produces ascending order DH"""
        self.c.sort_enrolled('id', algorithm='quick')
        ids = [r.student.id for r in self.c.enrolled_roster]
        self.assertEqual(ids, sorted(ids))

    def testQuickSortByName(self):
        """Quick sort by name produces alphabetical order DH"""
        self.c.sort_enrolled('name', algorithm='quick')
        names = [r.student.name for r in self.c.enrolled_roster]
        self.assertEqual(names, sorted(names))

    def testQuickSortByDate(self):
        """Quick sort by date produces chronological order DH"""
        self.c.sort_enrolled('date', algorithm='quick')
        dates = [r.enroll_date for r in self.c.enrolled_roster]
        self.assertEqual(dates, sorted(dates))

    def testQuickSortPreservesAllRecords(self):
        """Quick sort does not drop or duplicate any enrollment records DH"""
        before = {r.student.id for r in self.c.enrolled_roster}
        self.c.sort_enrolled('id', algorithm='quick')
        after = {r.student.id for r in self.c.enrolled_roster}
        self.assertEqual(before, after)
        self.assertEqual(len(self.c.enrolled_roster), 4)

    def testQuickSortAlreadySorted(self):
        """Quick sort on an already-sorted roster returns the same order DH"""
        self.c.sort_enrolled('id', algorithm='quick')
        first_pass = [r.student.id for r in self.c.enrolled_roster]
        self.c.sort_enrolled('id', algorithm='quick')
        second_pass = [r.student.id for r in self.c.enrolled_roster]
        self.assertEqual(first_pass, second_pass)

    def testQuickSortSingleElement(self):
        """Quick sort on a one-element roster does not crash DH"""
        c = Course("CSE1010", 3, 5)
        c.request_enroll(Student("Only One", "STU00001"), "2024-01-01")
        c.sort_enrolled('id', algorithm='quick')
        self.assertEqual(len(c.enrolled_roster), 1)


if __name__ == "__main__":
    unittest.main()