class Course:
    """Course object DH"""
    def __init__(self, courseCode, cred, Students):
        """Create a course with a name, credit weight, and list of enrolled students DH"""
        self.courseCode = courseCode
        self.cred = cred
        self.students = {}
        for i in Students:
            self.students[i.id] = i
        
        
    def addStudent(self, s):
        """Enroll a student in the course DH"""
        self.students[s.id] = s
        
    def getStudentCount(self):
        """Return the number of students in the course DH"""
        return len(self.students)
    
    def showDict(self):
        """Testing method to show all students in the course DH"""
        for id, student in self.students.items():
            print(f"ID: {id}, Name: {student.name}")