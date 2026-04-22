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
            
    def addCourse(self, code, creds):
        '''Add a course to the university DH'''
        if code not in self.courses:
            self.courses[code] = Course(code, creds)
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
        if course:
            return course.getStudentCount()
        return 0
    
    def getStudentsInCourse(self, code):
        '''Return a list of student IDs enrolled in a course SM'''
        course = self.getCourse(code)
        if course:
            return list(EnrollmentRecord.makeList())
        return []
    
    def getAllGPAs(self):
        '''Return a list of all student GPAs in the university DH'''
        gpas = []
        for s in self.students.values():
            gpas.append(s.calcGPA())
        return gpas
    
    def meanGPA(self):
        ''''Calculate and return the mean GPA of all students in the university DH'''
        gpas = self.getAllGPAs()
        if gpas:
            return round(sum(gpas) / len(gpas), 2)
        else:
            return 0.0

    def modeGPA(self):
        '''Calculate and return the mode GPA of all students in the university DH'''
        gpas = self.getAllGPAs()
        if not gpas:
            return 0.0
        return max(set(gpas), key=gpas.count)
        
    def medianGPA(self):
        '''Calculate and return the median GPA of all students in the university DH'''
        gpas = sorted(self.getAllGPAs())
        n = len(gpas)
        if n == 0:
            return 0.0
        mid = n // 2
        if n % 2 == 0:
            return round((gpas[mid - 1] + gpas[mid]) / 2, 2)
        else:
            return gpas[mid]
        
    def getCommonStudents(self, code1, code2):
        '''Return a list of student IDs enrolled in both courses DH'''
        s1 = set(s.id for s in self.getStudentsInCourse(code1))
        s2 = set(s.id for s in self.getStudentsInCourse(code2))
        return [self.students[id] for id in s1 & s2]
    
    def search_by_id(self, idList, targetID, left, right):
        """Recursive Binary Search to find an ID in a list SM"""
        if left > right:
            return -1
    
        mid = (left + right) // 2
    
        # If target is found
        if idList[mid] == targetID:
            return mid
    
        # Search left half
        elif targetID < idList[mid]:
            return self.search_by_id(idList, targetID, left, mid - 1)
    
        # Search right half
        else:
            return self.search_by_id(idList, targetID, mid + 1, right)
    
    
    
def loadUniversity(dataCsv, catalogCsv):
    '''Read CSV files and return a fully populated University object DH'''
    uni = University()

    # Load courses from course_catalog.csv
    catalogFile = open(catalogCsv)
    catalog = csv.DictReader(catalogFile)
    for row in catalog:
        code    = row['course_code']
        credits = int(row['credits'])
        uni.addCourse(code, credits)
    catalogFile.close()

    # Load students from university_data.csv
    dataFile = open(dataCsv)
    data = csv.DictReader(dataFile)
    for row in data:
        id   = row['student_id']
        name = row['name']

        try:
            student = uni.addStudent(id, name)
        except ValueError as e:
            print(f"[SKIP] {e}")
            continue

        # courses field looks like: "CSE1010:A;MATH2010:B+;CSE2050:C"
        # split by ; to get each course entry
        coursesList = row['courses'].strip(';').split(';')

        for entry in coursesList:
            # entry looks like "CSE1010:A"
            # split by : to get code and grade
            parts = entry.split(':')
            code  = parts[0]
            grade = parts[1]

            course = uni.getCourse(code)
            if course is None:
                course = uni.addCourse(code, 0)

            try:
                student.enroll(course, grade)
            except ValueError as e:
                print(f"[SKIP] {e}")

    dataFile.close()
    return uni


   
def loadprerequisites(filename):
    '''Read CSV file and return a HashMap of course prerequisites SM'''
    prereqMap = HashMap(10)

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}

            course = row.get("course_id")
            prereq = row.get("prerequisite")

            if course is None:
                continue

            if prereq == "" or prereq is None:
                if prereqMap.get(course) is None:
                    prereqMap.put(course, [])
                continue

            existing = prereqMap.get(course)

            if existing is None:
                prereqMap.put(course, [prereq])
            else:
                existing.append(prereq)
                prereqMap.put(course, existing)

    return prereqMap