from university import loadUniversity
from student import Student

def main():
    '''Main demo for Milestones 1-3 DH'''

    print("Loading university data...")
    enrollments = "enrollments_CSE10.csv"
    catalog     = "course_catalog_CSE10_with_capacity.csv"
    prereqs     = "cse_prerequisites.csv"
    uni = loadUniversity(enrollments, catalog, prereqs)
    print(f"  Loaded {len(uni.students)} students and {len(uni.courses)} courses.\n")

    sampleCode1 = list(uni.courses.keys())[0]
    sampleCode2 = list(uni.courses.keys())[1]
    sampleId    = list(uni.students.keys())[0]

    print(f"Students in {sampleCode1}")
    for s in uni.getStudentsInCourse(sampleCode1)[:10]:
        print(f"  {s.id}  {s.name}")

    print(f"\nGPA for {sampleId}")
    s = uni.getStudent(sampleId)
    print(f"  {s.name}: {s.calcGPA()}")

    print(f"\nCourse info for {sampleId}")
    print(f"  {'Code':<12} {'Grade':<8} Credits")
    for code, grade, creds in s.getCourseInfo():
        print(f"  {code:<12} {grade:<8} {creds}")

    print(f"\nUniversity GPA Stats")
    print(f"  Mean GPA:   {uni.meanGPA()}")
    print(f"  Mode GPA:   {uni.modeGPA()}")
    print(f"  Median GPA: {uni.medianGPA()}")

    print(f"\nStudents in both {sampleCode1} and {sampleCode2}")
    common = uni.getCommonStudents(sampleCode1, sampleCode2)
    for s in common[:10]:
        print(f"  {s.id}  {s.name}")

    print("\n=== Milestone 3 Demo ===\n")

    # Show loaded prerequisites
    print("Loaded prerequisites:")
    for code, course in uni.courses.items():
        prereq = course.prerequisites.get(code)
        if prereq:
            print(f"  {code} requires: {prereq}")

    print("\n--- Prerequisite Enforcement ---")

    cse2050 = uni.getCourse("CSE2050")
    if cse2050:
        noPrereqStudent = Student("New Student", "STU99998")
        print(f"\nAttempting to enroll {noPrereqStudent.name} in CSE2050 (no CSE1010):")
        try:
            cse2050.request_enroll(noPrereqStudent)
            print("  Enrolled (no prereq required or already met)")
        except Exception as e:
            print(f"  Blocked — {e}")

        noPrereqStudent.courses["CSE1010"] = "B"
        print(f"\nGiving {noPrereqStudent.name} CSE1010 credit and retrying:")
        try:
            cse2050.request_enroll(noPrereqStudent)
            print(f"  Successfully enrolled {noPrereqStudent.name} in CSE2050")
        except Exception as e:
            print(f"  Blocked — {e}")

    print("\n--- Student.enroll() rollback demo ---")
    cse3100 = uni.getCourse("CSE3100")
    if cse3100:
        rollbackStudent = Student("Rollback Test", "STU99997")
        print(f"Courses before failed enroll: {list(rollbackStudent.courses.keys())}")
        try:
            rollbackStudent.enroll(cse3100, "A")
        except Exception as e:
            print(f"  Enroll raised: {e}")
        print(f"Courses after failed enroll (should still be empty): {list(rollbackStudent.courses.keys())}")

    print("\n--- Merge Sort Demo (CSE1010 roster by ID) ---")
    cse1010 = uni.getCourse("CSE1010")
    if cse1010 and cse1010.enrolled_roster:
        cse1010.sort_enrolled('id', algorithm='merge')
        print("  Top 5 by ID:")
        for rec in cse1010.enrolled_roster[:5]:
            print(f"    {rec.student.id}  {rec.student.name}")

        cse1010.sort_enrolled('name', algorithm='merge')
        print("  Top 5 by Name:")
        for rec in cse1010.enrolled_roster[:5]:
            print(f"    {rec.student.id}  {rec.student.name}")

    print("\n--- Quick Sort Demo (CSE1010 roster) ---")
    if cse1010 and cse1010.enrolled_roster:
        cse1010.sort_enrolled('id', algorithm='quick')
        print("  Top 5 by ID:")
        for rec in cse1010.enrolled_roster[:5]:
            print(f"    {rec.student.id}  {rec.student.name}")

        cse1010.sort_enrolled('date', algorithm='quick')
        print("  Top 5 by Enrollment Date:")
        for rec in cse1010.enrolled_roster[:5]:
            print(f"    {rec.student.id}  date={rec.enroll_date}")


if __name__ == "__main__":
    main()