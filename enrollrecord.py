from datetime import *
from student import Student

class EnrollmentRecord():
    """Object representing a "course roster" of students and the date/time they enrolled in course SM"""
    
    def __init__(self, maxStudents):
        self.eDict = {}
        self.maxStudents = maxStudents
    
    
    def addToRecord(self, Student):
        """Add a student to this course Dictionary with the date as the value SM"""
        if Student.id in self.eDict:
            raise ValueError("Student already in course")
        self.eDict[Student.id] = datetime.now()
        return self.eDict[Student.id]
    
    
    def isFull(self):
        """Returns T/F if the len of eDict (# of students enrolled) is either under or at SM"""
        if len(self.eDict) == self.maxStudents:
            return True
        elif len(self.eDict) < self.maxStudents:
            return False
        else:
            return True
        
        
    def getEnrollDate(self, id):
        """Return the date Enrolled SM"""
        if id not in self.eDict:
            raise ValueError("Student Not Enrolled in course")
        
        return self.eDict[id]
    
    def __len__(self):
        return len(self.eDict)
    
    def makeList(self):
        l = []
        for x in self.eDict:
            l.append(x)
        return l
    
    
    
x = EnrollmentRecord(5)
x.addToRecord(Student("Sam", 3258049))

print(x.getEnrollDate(3258049))
        