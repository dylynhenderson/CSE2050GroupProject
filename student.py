class Student():
    '''Object representing a student. SM'''
    _grade_points = {
            'A': 4.0,
            'A-': 3.7,
            'B+': 3.3,
            'B': 3.0,
            'B-': 2.7,
            'C+': 2.3,
            'C': 2.0,
            'C-': 1.7,
            'D+': 1.3,
            'D': 1.0,
            'F': 0.0
        }
    
    
    def __init__(self, name, id, courses=None):
        '''Initialize a student with name, id, and all currently enrolled courses SM'''
        self.name = name
        self.id = id
        if courses is not None:
            self.courses = courses
        else:
            self.courses = {}
        
    def enroll(self,course,grade):
        '''Enroll the student in a new course with a grade and update list of students SM and DH'''
        if grade not in self._grade_points:
            raise ValueError(f"Invalid grade: {grade}")
        self.courses[course] = grade
        course.addStudent(self)
        
    def updateGrade(self, course, grade):
        '''If a student is already enrolled in a course, update their grade SM'''
        if grade not in self._grade_points:
            raise ValueError(f"Invalid grade: {grade}")
        if course in self.courses:
            self.courses[course] = grade
        else:
            raise ValueError(f"Student not enrolled in course: {course.courseCode}")
            
    def calcGPA(self):
        '''Calculate the students gpa SM'''
        totalPoints = 0.0
        totalCreds = 0
        for course, grade in self.courses.items():
            totalPoints += self._grade_points.get(grade, 0.0) * course.cred
            totalCreds += course.cred
        if totalCreds > 0:
            return round(totalPoints / totalCreds, 2) 
        else:
            return 0.0
        
    def getCourses(self):
        '''Return a list of courses the student is enrolled in DH'''
        return list(self.courses.keys())
    
    def getCourseInfo(self):
        '''Return a list of tuples with course code, course object, and grade for all courses the student is enrolled in DH'''
        return [(c.courseCode, self.courses[c], c.cred) for c in self.courses]
        
    def printCourses(self):
        '''Testing method to print all courses and grades SM'''
        for course, grade in self.courses.items():
            print(f"Course: {course.name}, Grade: {grade}")