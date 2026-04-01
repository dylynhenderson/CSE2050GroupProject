import unittest
from structures import LinkedQueue, EnrollmentRecord
from course import Course
from student import Student

# Linked Queue

class TestLinkedQueue(unittest.TestCase):
    '''Test cases for the LinkedQueue ADT DH'''
 
    def setUp(self):
        '''Set up a fresh LinkedQueue before each test DH'''
        self.q = LinkedQueue()
 
    def testQueueCreation(self):
        '''Test that a new LinkedQueue is empty on creation with size zero DH'''
        self.assertTrue(self.q.is_empty())
        self.assertEqual(len(self.q), 0)
 
    def testEnqueueIncreasesSize(self):
        '''Test that each enqueue call correctly increases the size of the queue DH'''
        self.q.enqueue("STU00001")
        self.assertEqual(len(self.q), 1)
        self.q.enqueue("STU00002")
        self.assertEqual(len(self.q), 2)
 
    def testDequeueFIFOOrder(self):
        '''Test that items are dequeued in the same order they were enqueued (FIFO) DH'''
        self.q.enqueue("first")
        self.q.enqueue("second")
        self.q.enqueue("third")
        self.assertEqual(self.q.dequeue(), "first")
        self.assertEqual(self.q.dequeue(), "second")
        self.assertEqual(self.q.dequeue(), "third")
 
    def testDequeueOnEmptyRaisesError(self):
        '''Test that dequeuing from an empty queue raises a ValueError DH'''
        with self.assertRaises(ValueError):
            self.q.dequeue()
 
    def testSizeTrackingAfterDequeue(self):
        '''Test that size decreases correctly after each dequeue operation DH'''
        self.q.enqueue("a")
        self.q.enqueue("b")
        self.q.dequeue()
        self.assertEqual(len(self.q), 1)
        self.q.dequeue()
        self.assertEqual(len(self.q), 0)
 
    def testIsEmptyAfterAllDequeued(self):
        '''Test that is_empty returns True once every item has been removed DH'''
        self.q.enqueue("only")
        self.q.dequeue()
        self.assertTrue(self.q.is_empty())
 
    def testIsNotEmptyAfterEnqueue(self):
        '''Test that is_empty returns False after at least one item is enqueued DH'''
        self.q.enqueue("something")
        self.assertFalse(self.q.is_empty())
 
    def testDequeueOnRefilledQueueRaisesError(self):
        '''Test that dequeue raises ValueError on an emptied-then-not-refilled queue DH'''
        self.q.enqueue("x")
        self.q.dequeue()
        with self.assertRaises(ValueError):
            self.q.dequeue()

# Enrollment and Waitlist

class TestEnrollmentAndWaitlist(unittest.TestCase):
    '''Test cases for course capacity, enrollment, and waitlist behavior DH'''
 
    def setUp(self):
        '''Set up a Course with capacity 2 and four Student objects before each test DH'''
        self.c = Course("CSE2050", 3, maxStu=2)
        self.s1 = Student("Alice",   "STU00001")
        self.s2 = Student("Bob",     "STU00002")
        self.s3 = Student("Charlie", "STU00003")
        self.s4 = Student("Diana",   "STU00004")
 
    def testEnrollUpToCapacity(self):
        '''Test that students are added directly to the roster when capacity has not been reached DH'''
        self.c.request_enroll(self.s1)
        self.c.request_enroll(self.s2)
        self.assertEqual(len(self.c.enrolled_roster), 2)
        self.assertTrue(self.c.waitlist.is_empty())
 
    def testOverflowGoesToWaitlist(self):
        '''Test that students beyond course capacity are placed on the waitlist instead of the roster DH'''
        self.c.request_enroll(self.s1)
        self.c.request_enroll(self.s2)
        self.c.request_enroll(self.s3)
        self.c.request_enroll(self.s4)
        self.assertEqual(len(self.c.enrolled_roster), 2)
        self.assertEqual(len(self.c.waitlist), 2)
 
    def testWaitlistFIFOPromotion(self):
        '''Test that the first student added to the waitlist is the first to be promoted on a drop DH'''
        self.c.request_enroll(self.s1)
        self.c.request_enroll(self.s2)
        self.c.request_enroll(self.s3)  # first on waitlist
        self.c.request_enroll(self.s4)  # second on waitlist
 
        self.c.drop(self.s1.id)
 
        enrolled_ids = [r.student.id for r in self.c.enrolled_roster]
        self.assertIn(self.s3.id, enrolled_ids)
        self.assertEqual(len(self.c.waitlist), 1)
 
    def testDropPromotesFromWaitlist(self):
        '''Test that dropping an enrolled student automatically enrolls the next waitlisted student DH'''
        self.c.request_enroll(self.s1)
        self.c.request_enroll(self.s2)
        self.c.request_enroll(self.s3)  # goes to waitlist
 
        self.c.drop(self.s1.id)
 
        enrolled_ids = [r.student.id for r in self.c.enrolled_roster]
        self.assertIn(self.s3.id, enrolled_ids)
        self.assertTrue(self.c.waitlist.is_empty())
 
    def testDropWithEmptyWaitlistShrinsRoster(self):
        '''Test that dropping with no waitlisted students simply reduces the roster size by one DH'''
        self.c.request_enroll(self.s1)
        self.c.request_enroll(self.s2)
        self.c.drop(self.s1.id)
        self.assertEqual(len(self.c.enrolled_roster), 1)
 
    def testNoDuplicateEnrollment(self):
        '''Test that enrolling the same student twice does not create duplicate roster entries DH'''
        self.c.request_enroll(self.s1)
        self.c.request_enroll(self.s1)
        self.assertEqual(len(self.c.enrolled_roster), 1)
 
    def testEnrollmentRecordStoredCorrectly(self):
        '''Test that request_enroll stores an EnrollmentRecord with the correct student in the roster DH'''
        self.c.request_enroll(self.s1)
        self.assertIsInstance(self.c.enrolled_roster[0], EnrollmentRecord)
        self.assertEqual(self.c.enrolled_roster[0].student.id, self.s1.id)

# Sorting

class TestSorting(unittest.TestCase):
    '''Test cases for enrolled roster sorting by id, name, and enrollment date DH'''
 
    def setUp(self):
        '''Set up a Course with five students enrolled in shuffled order before each test DH'''
        self.c = Course("CSE2050", 3, maxStu=5)
        self.s1 = Student("Charlie", "STU00003")
        self.s2 = Student("Alice",   "STU00001")
        self.s3 = Student("Eve",     "STU00005")
        self.s4 = Student("Bob",     "STU00002")
        self.s5 = Student("Diana",   "STU00004")
 
        # Enroll with explicit dates so date sorting is testable
        self.c.request_enroll(self.s1, "2026-03-03")
        self.c.request_enroll(self.s2, "2026-03-01")
        self.c.request_enroll(self.s3, "2026-03-05")
        self.c.request_enroll(self.s4, "2026-03-02")
        self.c.request_enroll(self.s5, "2026-03-04")
 
    def testSortById(self):
        '''Test that sort_enrolled by id produces a roster sorted by student ID ascending DH'''
        self.c.sort_enrolled('id')
        ids = [r.student.id for r in self.c.enrolled_roster]
        self.assertEqual(ids, sorted(ids))
 
    def testSortByName(self):
        '''Test that sort_enrolled by name produces a roster sorted alphabetically by student name DH'''
        self.c.sort_enrolled('name')
        names = [r.student.name for r in self.c.enrolled_roster]
        self.assertEqual(names, sorted(names))
 
    def testSortByDate(self):
        '''Test that sort_enrolled by date produces a roster sorted by enrollment date ascending DH'''
        self.c.sort_enrolled('date')
        dates = [r.enroll_date for r in self.c.enrolled_roster]
        self.assertEqual(dates, sorted(dates))
 
    def testSortUpdatesCurrentSortKey(self):
        '''Test that sort_enrolled sets current_sort_key to the key that was used DH'''
        self.c.sort_enrolled('id')
        self.assertEqual(self.c.current_sort_key, 'id')
        self.c.sort_enrolled('name')
        self.assertEqual(self.c.current_sort_key, 'name')
 
    def testSortPreservesAllRecords(self):
        '''Test that sorting does not add or remove any records from the enrolled roster DH'''
        self.c.sort_enrolled('id')
        self.assertEqual(len(self.c.enrolled_roster), 5)
 
    def testSortByIdTwiceStillCorrect(self):
        '''Test that sorting by id on an already id-sorted roster leaves the order unchanged DH'''
        self.c.sort_enrolled('id')
        ids_first = [r.student.id for r in self.c.enrolled_roster]
        self.c.sort_enrolled('id')
        ids_second = [r.student.id for r in self.c.enrolled_roster]
        self.assertEqual(ids_first, ids_second)

# Binary Search and Drop

class TestBinarySearchAndDrop(unittest.TestCase):
    '''Test cases for recursive binary search and the drop method DH'''
 
    def setUp(self):
        '''Set up a Course with five enrolled students sorted by ID before each test DH'''
        self.c = Course("CSE2050", 3, maxStu=5)
        self.s1 = Student("Alice",   "STU00001")
        self.s2 = Student("Bob",     "STU00002")
        self.s3 = Student("Charlie", "STU00003")
        self.s4 = Student("Diana",   "STU00004")
        self.s5 = Student("Eve",     "STU00005")
 
        for s in [self.s3, self.s1, self.s5, self.s2, self.s4]:
            self.c.request_enroll(s)
 
        self.c.sort_enrolled('id')
 
    def testBinarySearchFindsFirst(self):
        '''Test that recursive binary search correctly finds the student at index 0 DH'''
        idx = self.c.recursive_binary_search(
            self.c.enrolled_roster, "STU00001", 0, len(self.c.enrolled_roster) - 1
        )
        self.assertEqual(idx, 0)
 
    def testBinarySearchFindsMiddle(self):
        '''Test that recursive binary search correctly finds the student at the middle index DH'''
        idx = self.c.recursive_binary_search(
            self.c.enrolled_roster, "STU00003", 0, len(self.c.enrolled_roster) - 1
        )
        self.assertEqual(idx, 2)
 
    def testBinarySearchFindsLast(self):
        '''Test that recursive binary search correctly finds the student at the last index DH'''
        idx = self.c.recursive_binary_search(
            self.c.enrolled_roster, "STU00005", 0, len(self.c.enrolled_roster) - 1
        )
        self.assertEqual(idx, 4)
 
    def testBinarySearchNotFound(self):
        '''Test that recursive binary search returns -1 when the target ID is not in the roster DH'''
        idx = self.c.recursive_binary_search(
            self.c.enrolled_roster, "STU99999", 0, len(self.c.enrolled_roster) - 1
        )
        self.assertEqual(idx, -1)
 
    def testBinarySearchEmptyRoster(self):
        '''Test that recursive binary search returns -1 when the roster is empty DH'''
        empty_course = Course("CSE3100", 3, maxStu=5)
        idx = empty_course.recursive_binary_search(
            empty_course.enrolled_roster, "STU00001", 0, len(empty_course.enrolled_roster) - 1
        )
        self.assertEqual(idx, -1)
 
    def testBinarySearchSingleElementFound(self):
        '''Test that recursive binary search works correctly on a one-element roster where the target is present DH'''
        c = Course("CSE3100", 3, maxStu=1)
        s = Student("Alice", "STU00001")
        c.request_enroll(s)
        c.sort_enrolled('id')
        idx = c.recursive_binary_search(c.enrolled_roster, "STU00001", 0, len(c.enrolled_roster) - 1)
        self.assertEqual(idx, 0)
 
    def testBinarySearchSingleElementNotFound(self):
        '''Test that recursive binary search returns -1 on a one-element roster where the target is absent DH'''
        c = Course("CSE3100", 3, maxStu=1)
        s = Student("Alice", "STU00001")
        c.request_enroll(s)
        c.sort_enrolled('id')
        idx = c.recursive_binary_search(c.enrolled_roster, "STU99999", 0, len(c.enrolled_roster) - 1)
        self.assertEqual(idx, -1)
 
    def testDropRemovesStudent(self):
        '''Test that drop correctly removes the target student from the enrolled roster DH'''
        self.c.drop("STU00003")
        enrolled_ids = [r.student.id for r in self.c.enrolled_roster]
        self.assertNotIn("STU00003", enrolled_ids)
 
    def testDropDecreasesRosterSize(self):
        '''Test that drop reduces the enrolled roster size by exactly one DH'''
        before = len(self.c.enrolled_roster)
        self.c.drop("STU00002")
        self.assertEqual(len(self.c.enrolled_roster), before - 1)
 
    def testDropNonexistentStudentNoChange(self):
        '''Test that attempting to drop a student not in the roster leaves the roster unchanged DH'''
        before = len(self.c.enrolled_roster)
        self.c.drop("STU99999")
        self.assertEqual(len(self.c.enrolled_roster), before)
 
    def testDropPromotesNextWaitlistedStudent(self):
        '''Test that dropping a student when the waitlist is non-empty promotes the next student into the roster DH'''
        c = Course("CSE2050", 3, maxStu=2)
        s1 = Student("Alice",   "STU00001")
        s2 = Student("Bob",     "STU00002")
        s3 = Student("Charlie", "STU00003")
 
        c.request_enroll(s1)
        c.request_enroll(s2)
        c.request_enroll(s3)  # goes to waitlist
 
        c.drop("STU00001")
 
        enrolled_ids = [r.student.id for r in c.enrolled_roster]
        self.assertIn("STU00003", enrolled_ids)
        self.assertTrue(c.waitlist.is_empty())
 
    def testDropResortsByIdWhenNotSorted(self):
        '''Test that drop still works correctly when the roster is not pre-sorted by ID DH'''
        self.c.sort_enrolled('name')  # sort by something other than id
        self.c.drop("STU00004")
        enrolled_ids = [r.student.id for r in self.c.enrolled_roster]
        self.assertNotIn("STU00004", enrolled_ids)

# Studnet

class TestStudent(unittest.TestCase):
    '''Test cases for the Student class DH'''
 
    def setUp(self):
        '''Set up fresh Student and Course objects before each test DH'''
        self.c1 = Course("CSE2050",  3, maxStu=5)
        self.c2 = Course("MATH2010", 4, maxStu=5)
        self.s  = Student("Alice", "STU00001", {})
 
    def testStudentCreation(self):
        '''Test that a Student is correctly initialized with name, id, and empty course dict DH'''
        self.assertEqual(self.s.id,   "STU00001")
        self.assertEqual(self.s.name, "Alice")
        self.assertIsInstance(self.s.courses, dict)
 
    def testEnroll(self):
        '''Test that enrolling a student updates the student course record and course roster DH'''
        self.s.enroll(self.c1, "A")
        self.assertIn(self.c1, self.s.courses)
        self.assertEqual(self.s.courses[self.c1], "A")
        enrolled_ids = [r.student.id for r in self.c1.enrolled_roster]
        self.assertIn(self.s.id, enrolled_ids)
 
    def testEnrollInvalidGrade(self):
        '''Test that enrolling with an invalid grade raises a ValueError DH'''
        with self.assertRaises(ValueError):
            self.s.enroll(self.c1, "Z")
 
    def testUpdateGrade(self):
        '''Test that updateGrade correctly modifies an existing grade and raises on an invalid one DH'''
        self.s.enroll(self.c1, "B")
        self.s.updateGrade(self.c1, "A")
        self.assertEqual(self.s.courses[self.c1], "A")
        self.assertRaises(ValueError, self.s.updateGrade, self.c1, "E")
 
    def testCalcGPAWeighted(self):
        '''Test that GPA is correctly weighted by credit hours across multiple courses DH'''
        self.s.enroll(self.c1, "A")   # 4.0 * 3 = 12.0
        self.s.enroll(self.c2, "B")   # 3.0 * 4 = 12.0  => 24/7 = 3.43
        self.assertAlmostEqual(self.s.calcGPA(), round(24.0 / 7, 2), places=2)
 
    def testCalcGPANoCourses(self):
        '''Test that calcGPA returns 0.0 for a student with no enrolled courses DH'''
        self.assertEqual(self.s.calcGPA(), 0.0)
 
    def testGetCourses(self):
        '''Test that getCourses returns a list containing all courses the student is enrolled in DH'''
        self.s.enroll(self.c1, "A")
        self.s.enroll(self.c2, "B")
        courses = self.s.getCourses()
        self.assertIsInstance(courses, list)
        self.assertIn(self.c1, courses)
        self.assertIn(self.c2, courses)
 
 
if __name__ == "__main__":
    unittest.main()