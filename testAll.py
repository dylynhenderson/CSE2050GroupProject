import unittest
from course import Course
from student import Student
from university import University
from enrollrecord import EnrollmentRecord
from datetime import *

class TestCourse(unittest.TestCase):
    '''Test cases for the Course class SM'''

    def setUp(self):
        '''Set up fresh Course and Student objects before each test SM'''
        self.s1 = Student("Alice", "STU00001", {})
        self.s2 = Student("Bob",   "STU00002", {})
        self.c  = Course("CSE2050", 3)

    def testCourseCreation(self):
        '''Test that a Course is correctly initialized SM'''
        self.assertEqual(self.c.courseCode, "CSE2050")
        self.assertEqual(self.c.cred, 3)
        self.assertIsInstance(self.c.enRec, EnrollmentRecord)
        self.assertEqual(len(self.c.students), 0)

    def testAddStudent(self):
        '''Test that Student objects are correctly added to the course roster SM'''
        self.c.addStudent(self.s1)
        self.assertIn(self.s1, self.c.students)

    def testNoDuplicateStudents(self):
        '''Test that duplicate Student objects are not added to the roster SM'''
        self.c.addStudent(self.s1)
        self.c.addStudent(self.s1)
        self.assertEqual(self.c.getStudentCount(), 1)

    def testGetStudentCount(self):
        '''Test that getStudentCount returns the correct number of students SM'''
        self.c.addStudent(self.s1)
        self.c.addStudent(self.s2)
        self.assertEqual(self.c.getStudentCount(), 2)


class TestStudent(unittest.TestCase):
    '''Test cases for the Student class SM'''

    def setUp(self):
        '''Set up fresh Student and Course objects before each test SM'''
        self.c1 = Course("CSE2050",  3)
        self.c2 = Course("MATH2010", 4)
        self.s  = Student("Alice", "STU00001", {})

    def testStudentCreation(self):
        '''Test that a Student is correctly initialized SM'''
        self.assertEqual(self.s.id,   "STU00001")
        self.assertEqual(self.s.name, "Alice")
        self.assertIsInstance(self.s.courses, dict)

    def testEnroll(self):
        '''Test that enrolling updates both the student record and the course roster SM and DH'''
        self.s.enroll(self.c1, "A")
        self.assertIn(self.c1, self.s.courses)
        self.assertEqual(self.s.courses[self.c1], "A")
        self.assertIn(self.s, self.c1.students)

    def testEnrollInvalidGrade(self):
        '''Test that enrolling with an invalid grade raises ValueError SM'''
        with self.assertRaises(ValueError):
            self.s.enroll(self.c1, "Z")

    def testUpdateGrade(self):
        '''Test that updateGrade correctly modifies an existing grade SM'''
        self.s.enroll(self.c1, "B")
        self.s.updateGrade(self.c1, "A")
        self.assertEqual(self.s.courses[self.c1], "A")
        self.assertRaises(ValueError, self.s.updateGrade, self.c1, "E")

    def testCalcGPAWeighted(self):
        '''Test that GPA is correctly weighted by credits SM'''
        self.s.enroll(self.c1, "A")   # 4.0 * 3 = 12.0
        self.s.enroll(self.c2, "B")   # 3.0 * 4 = 12.0  => 24/7 = 3.43
        self.assertAlmostEqual(self.s.calcGPA(), round(24.0 / 7, 2), places=2)

    def testCalcGPANoCourses(self):
        '''Test that calcGPA returns 0.0 with no courses, no division by zero SM'''
        self.assertEqual(self.s.calcGPA(), 0.0)

    def testGetCourses(self):
        '''Test that getCourses returns a list of Course objects SM'''
        self.s.enroll(self.c1, "A")
        self.s.enroll(self.c2, "B")
        courses = self.s.getCourses()
        self.assertIsInstance(courses, list)
        self.assertIn(self.c1, courses)
        self.assertIn(self.c2, courses)


class TestUniversity(unittest.TestCase):
    '''Test cases for the University class DH'''

    def setUp(self):
        '''Set up a fresh University before each test DH'''
        self.uni = University()

    def testUniversityCreation(self):
        '''Test that a University initializes with empty dicts DH'''
        self.assertIsInstance(self.uni.students, dict)
        self.assertIsInstance(self.uni.courses,  dict)

    def testAddCourse(self):
        '''Test that addCourse creates and returns a Course object DH'''
        c = self.uni.addCourse("CSE2050", 3)
        self.assertIn("CSE2050", self.uni.courses)
        self.assertEqual(c.courseCode, "CSE2050")

    def testDuplicateCourse(self):
        '''Test that adding a duplicate course returns the original without overwriting DH'''
        c1 = self.uni.addCourse("CSE2050", 3)
        c2 = self.uni.addCourse("CSE2050", 99)
        self.assertIs(c1, c2)
        self.assertEqual(c1.cred, 3)

    def testAddStudent(self):
        '''Test that addStudent creates and returns a Student object DH'''
        s = self.uni.addStudent("STU00001", "Alice")
        self.assertIn("STU00001", self.uni.students)
        self.assertEqual(s.name, "Alice")

    def testDuplicateStudent(self):
        '''Test that adding a duplicate student returns the original without overwriting DH'''
        s1 = self.uni.addStudent("STU00001", "Alice")
        s2 = self.uni.addStudent("STU00001", "Other")
        self.assertIs(s1, s2)
        self.assertEqual(s1.name, "Alice")

    def testInvalidStudentId(self):
        '''Test that an invalid student ID raises ValueError DH'''
        with self.assertRaises(ValueError):
            self.uni.addStudent("BAD001", "Alice")

    def testEmptyStudentName(self):
        '''Test that an empty student name raises ValueError DH'''
        with self.assertRaises(ValueError):
            self.uni.addStudent("STU00001", "")

    def testGetStudent(self):
        '''Test that getStudent returns the correct Student object DH'''
        self.uni.addStudent("STU00001", "Alice")
        self.assertEqual(self.uni.getStudent("STU00001").name, "Alice")

    def testGetNonexistentStudent(self):
        '''Test that getStudent returns None for an unknown ID DH'''
        self.assertIsNone(self.uni.getStudent("STU99999"))

    def testGetCourse(self):
        '''Test that getCourse returns the correct Course object DH'''
        self.uni.addCourse("CSE2050", 3)
        self.assertEqual(self.uni.getCourse("CSE2050").courseCode, "CSE2050")

    def testGetNonexistentCourse(self):
        '''Test that getCourse returns None for an unknown code DH'''
        self.assertIsNone(self.uni.getCourse("FAKE999"))

    def testGetCourseEnrollment(self):
        '''Test that getCourseEnrollment returns the correct count DH'''
        self.uni.addCourse("CSE2050", 3)
        s1 = self.uni.addStudent("STU00001", "Alice")
        s2 = self.uni.addStudent("STU00002", "Bob")
        s1.enroll(self.uni.getCourse("CSE2050"), "A")
        s2.enroll(self.uni.getCourse("CSE2050"), "B")
        self.assertEqual(self.uni.getCourseEnrollment("CSE2050"), 2)

    def testGetStudentsInCourseReturnsObjects(self):
        '''Test that getStudentsInCourse returns Student objects DH'''
        self.uni.addCourse("CSE2050", 3)
        s = self.uni.addStudent("STU00001", "Alice")
        s.enroll(self.uni.getCourse("CSE2050"), "A")
        result = self.uni.getStudentsInCourse("CSE2050")
        self.assertIsInstance(result[0], Student)

    def testGetStudentsInNonexistentCourse(self):
        '''Test that getStudentsInCourse returns empty list for unknown course DH'''
        self.assertEqual(self.uni.getStudentsInCourse("FAKE999"), [])

class TestEnrollmentRecord(unittest.TestCase):
    """Testing for EnrollmentRecord SM"""
    
    def setUp(self):
        """create a student and a roster SM"""
        self.s = Student("Sam", 3258039)
        self.e = EnrollmentRecord(10)
        
    def testCreated(self):
        """Testing the object is properly created SM"""
        self.assertIsInstance(self.e, EnrollmentRecord )
    
    def testAdd(self):
        """Testing adding a student to a record"""
        self.e.addToRecord(self.s)
        self.assertIn(self.s.id, self.e.eDict)
        
    
    def testMaxCap(self):
        """Testing that the .isFull() method works as intended SM"""
        #create 2 objects
        er = EnrollmentRecord(5)
        notFull = EnrollmentRecord(5)
        
        #populate 1 EnrollmentRecord fully
        for i in range(5):
            s = Student(i,i)
            er.addToRecord(s)
        
        #one is full, one is empty
        self.assertEqual(er.isFull(), True)
        self.assertEqual(notFull.isFull(), False)
        
    def testGetEnrollDate(self):
        """Testing that getEnrollDate returns the date based off an id, or raises error if student is not enrolled SM"""
        d = EnrollmentRecord(5)
        stu = Student("Sam", 3258049)
        dateEx = d.addToRecord(stu)
        with self.assertRaises(ValueError):
            d.getEnrollDate(3258050)
        self.assertEqual(d.getEnrollDate(3258049), dateEx)
        
        
    
if __name__ == "__main__":
    unittest.main()