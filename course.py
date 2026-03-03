class Course:
    '''Course object DH'''
    def __init__(self, courseCode, cred, Students=None):
        '''Create a course with a code, credit weight, and list of enrolled students DH'''
        self.courseCode = courseCode
        self.cred = cred
        self.students = []
        if Students:
            for i in Students:
                self.addStudent(i)
        
    def addStudent(self, s):
        '''Enroll a student in the course DH'''
        if s not in self.students:
            self.students.append(s)
        
    def getStudentCount(self):
        '''Return the number of students in the course DH'''
        return len(self.students)
    
    def showDict(self):
        '''Testing method to show all students in the course DH'''
        for student in self.students:
            print(f"ID: {student.id}, Name: {student.name}")