from fileinput import filename
from course import Course
from student import Student
from structures import EnrollmentRecord, HashMap
import csv

class University:
    '''Create University object DH'''
    def __init__(self):
        self.students = {}
        self.courses = {}
            
    def addCourse(self, code, creds, capacity=0):
        '''Add a course to the university DH'''
        if code not in self.courses:
            self.courses[code] = Course(code, creds, capacity)
        return self.courses[code]
        
    def addStudent(self, student_id, name):
        '''Add a student to the university DH'''
        if len(student_id) != 8:
            raise ValueError(f"Invalid ID: {student_id}")
        if not student_id.startswith('STU'):
            raise ValueError(f"Invalid ID: {student_id}")
        if name == "":
            raise ValueError("Name cannot be empty.")
        if student_id not in self.students:
            self.students[student_id] = Student(name, student_id)
        return self.students[student_id]
        
    def getStudent(self, id):
        '''Return a student object given their ID DH'''
        return self.students.get(id, None)
    
    def getCourse(self, code):
        '''Return a course object given its code DH'''
        return self.courses.get(code, None)
    
    def getCourseEnrollment(self, code):
        '''Return the number of students enrolled in a course SM'''
        course = self.getCourse(code)
        return course.getStudentCount() if course else 0
    
    def getStudentsInCourse(self, code):
        '''Return a list of student IDs enrolled in a course SM and DH'''
        course = self.getCourse(code)
        if course:
            return [record.student for record in course.enrolled_roster]
        return []
    
    def getAllGPAs(self):
        '''Return a list of all student GPAs in the university DH'''
        return [s.calcGPA() for s in self.students.values()]
    
    def meanGPA(self):
        ''''Calculate and return the mean GPA of all students in the university DH'''
        gpas = self.getAllGPAs()
        return round(sum(gpas) / len(gpas), 2) if gpas else 0.0

    def modeGPA(self):
        '''Calculate and return the mode GPA of all students in the university DH'''
        gpas = self.getAllGPAs()
        return max(set(gpas), key=gpas.count) if gpas else 0.0
        
    def medianGPA(self):
        '''Calculate and return the median GPA of all students in the university DH'''
        gpas = sorted(self.getAllGPAs())
        n = len(gpas)
        if n == 0:
            return 0.0
        mid = n // 2
        return round((gpas[mid - 1] + gpas[mid]) / 2, 2) if n % 2 == 0 else gpas[mid]
        
    def getCommonStudents(self, code1, code2):
        '''Return a list of student IDs enrolled in both courses DH'''
        s1 = set(s.id for s in self.getStudentsInCourse(code1))
        s2 = set(s.id for s in self.getStudentsInCourse(code2))
        return [self.students[sid] for sid in s1 & s2]

    def search_by_id(self, idList, targetID, left, right):
        """Recursive Binary Search to find an ID in a list SM"""
        if left > right:
            return -1
    
        mid = (left + right) // 2
    
        if idList[mid] == targetID:
            return mid
        elif targetID < idList[mid]:
            return self.search_by_id(idList, targetID, left, mid - 1)
        else:
            return self.search_by_id(idList, targetID, mid + 1, right)
    
    
def loadUniversity(enrollmentFile, catalogFile, prereqFile):
    '''Load students, course catalog, and prerequisites into the University system DH'''
    uni = University()

    with open(catalogFile, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uni.addCourse(row['course_id'], int(row['credits']), int(row['capacity']))

    with open(prereqFile, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            courseId = row.get('course_id', '').strip()
            prereqId = row.get('prerequisite', '').strip()
            if courseId and courseId in uni.courses and prereqId:
                uni.courses[courseId].prerequisites.put(courseId, prereqId)

    with open(enrollmentFile, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sId = row['student_id']
            cId = row['course_id']
            grade = row.get('grade', '').strip()
 
            if sId not in uni.students:
                uni.addStudent(sId, f"Student_{sId[3:]}")
 
            student = uni.students[sId]
            if cId in uni.courses:
                course_obj = uni.courses[cId]
                student.courses[course_obj] = grade if grade else "IP" 
                try:
                    course_obj.request_enroll(student, "2026-01-01")
                except Exception:
                    pass

    return uni
   
def loadprerequisites(filename):
    '''Read CSV file and return a HashMap of course prerequisites SM and DH'''
    prereqMap = HashMap(10)
    with open(filename, newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            course = row.get('course_id', '').strip()
            prereq = row.get('prerequisite', '').strip()
            if not course:
                continue
            if prereq:
                existing = prereqMap.get(course)
                prereqMap.put(course, (existing or []) + [prereq])
            else:
                if prereqMap.get(course) is None:
                    prereqMap.put(course, [])
    return prereqMap