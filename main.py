from groupProject.course import Course
from groupProject.student import Student
from groupProject.university import University
import csv 
import unittest


class testAll(unittest.TestCase):
    # Create some students
    s1 = Student("Alice", "S001", {})
    s2 = Student("Bob", "S002", {})
    s3 = Student("Charlie", "S003", {})
    
    l = [s1,s2,s3]
    
    # Create some courses
    c1 = Course("Math", 3, l[:2]) 
    c2 = Course("History", 4, l[1:])
    c3 = Course("Science", 3, l)
    
    
    
    def testStuCount(self):
        pass
        
    def testDictRet(self):
        """Test that the student dictionary in courses is correct SM"""
        self.assertIn("S001", self.c1.students)
        self.assertIn("S002", self.c1.students)
        self.assertIn("S002", self.c2.students)
        self.assertIn("S003", self.c2.students)
        self.assertIn("S001", self.c3.students)
        self.assertIn("S003", self.c3.students)
        
        
    def testUniv(self):
        """Test that the university correctly stores students and courses SM"""
        u = University([self.s1, self.s2, self.s3], [self.c1, self.c2, self.c3])
        self.assertIn("S001", u.students)
        self.assertIn("S002", u.students)
        self.assertIn("S003", u.students)
        self.assertIn("Math", u.courses)
        self.assertIn("History", u.courses)
        self.assertIn("Science", u.courses)
        
    def testSepMeths(self):
        pass
    
        

unittest.main()
    
    


