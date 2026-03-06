from enrollrecord import EnrollmentRecord

class Course:
    '''Course object DH'''
    def __init__(self, courseCode, cred, Students=None, maxStu = 0):
        '''Create a course with a code, credit weight, an EnrollmentRecord, and max student capacity DH and SM'''
        self.courseCode = courseCode
        self.cred = cred
        #self.students = []
        self.maxStudents = maxStu
        self.enRec = EnrollmentRecord(maxStu)
        if Students:
            for i in Students:
                self.addStudent(i)
        
    def addStudent(self, s):
        '''Enroll a student in the course, provided the course roster is not >= maxStu DH'''
        #add functionality to add student to an EnrollmentRecord for each course, provided ER.len < max
        self.enRec.addToRecord(s)
        
    def getStudentCount(self):
        '''Return the number of students in the course DH'''
        #changed to interact with an EnrollmentRecord
        return len(self.enRec)
    
    def showDict(self):
        '''Testing method to show all students in the course DH'''
        #Test EnrollRecord for Course c 
        for student in self.students:
            print(f"ID: {student.id}, Name: {student.name}")