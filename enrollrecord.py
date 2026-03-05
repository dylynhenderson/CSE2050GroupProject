from datetime import *
from course import Course
from student import Student

class EnrollmentRecord():
    """Object representing a "course roster" of students and the date/time they enrolled in course"""
    
    def __init__(self):
        self.eDict = {}
    
    
    def addToRecord(self, Student):
        """Add a student to this course Dictionary with the date as the value"""
        self.eDict[Student.id] = datetime.now()
        return self.eDict
    