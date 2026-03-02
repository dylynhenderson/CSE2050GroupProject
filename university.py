from groupProject.course import Course
from groupProject.student import Student
import csv


class University:
    '''Create University object DH'''
    def __init__(self, stuL, corL):
        self.students = {}
        self.courses = {}
        for i in stuL:
            self.students[i.id] = i
        for i in corL:
            self.courses[i.courseCode] = i

            
    def addCourse(self,code,creds):
        """Add a course to the university DH"""
        self.courses[code] = Course(code, creds, [])
        
    def addStudent(self,name,id):
        """Add a student to the university DH"""
        self.students[id] = Student(name, id, {})
        
    def getStudent(self, id):
        """Return a student object given their ID DH"""
        return self.students.get(id, None)
    
    def getCourse(self, code):
        """Return a course object given its code DH"""
        return self.courses.get(code, None)
    
    def getCourseEnrollment(self,code):
        """Return the number of students enrolled in a course SM"""
        course = self.getCourse(code)
        if course:
            return course.getStudentCount()
        return 0
    
    def getStudentsInCourse(self, code):
        """Return a list of student IDs enrolled in a course SM"""
        course = self.getCourse(code)
        if course:
            return list(course.students.keys())
        return []
        