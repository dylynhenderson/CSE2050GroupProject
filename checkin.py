from student import Student
from course import Course

def checkIn():
    '''Demonstration for lab check-in DH'''
    test_course = Course("CSE2050", 3, maxStu=2)
    
    s1 = Student("Alice", "STU001")
    s2 = Student("Charlie", "STU003")
    s3 = Student("Bob", "STU002")
    s4 = Student("Diana", "STU004")

    print("Step 1: Filling capacity...")
    test_course.request_enroll(s1)
    test_course.request_enroll(s2)
    print(f"Enrolled: {[r.student.name for r in test_course.enrolled_roster]}")

    print("\nStep 2: Adding 2 to waitlist...")
    test_course.request_enroll(s3)
    test_course.request_enroll(s4)
    print(f"Waitlist count: {len(test_course.waitlist)}")

    print("\nStep 3: Sorting by ID and dropping Charlie...")
    test_course.sort_enrolled('id')
    print(f"Sorted IDs: {[r.student.id for r in test_course.enrolled_roster]}")
    
    test_course.drop("STU003") 
    
    print(f"\nStep 4: Resulting roster (Bob should be promoted):")
    print(f"New Enrolled: {[r.student.name for r in test_course.enrolled_roster]}")
    print(f"Remaining Waitlist: {len(test_course.waitlist)}")

if __name__ == "__main__":
    checkIn()