class Student():
    """Object representing a student. SM"""
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
    
    
    def __init__(self, name, id, Courses):
        """Initialize a student with name, id, and all currently enrolled courses SM"""
        self.name = name
        self.id = id
        self.courses = Courses
        
    def enroll(self,course,grade):
        """Enroll the student in a new course with a grade SM"""
        self.courses[course] = grade
        
    def updateGrade(self, course, grade):
        """If a student is already enrolled in a course, update their grade SM"""
        if course in self.courses:
            self.courses[course] = grade
            
    def calcGPA(self):
        """Calculate the students gpa SM"""

        total_points = 0
        total_courses = len(self.courses)
        
        for grade in self.courses.values():
            total_points += self._grade_points.get(grade, 0)
        
        return total_points / total_courses if total_courses > 0 else 0.0
        
        
    def printCourses(self):
        """Testing method to print all courses and grades SM"""
        for course, grade in self.courses.items():
            print(f"Course: {course.name}, Grade: {grade}")