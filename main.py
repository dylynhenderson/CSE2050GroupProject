from university import loadUniversity

def main():
    '''Main function to demonstrate university data loading and functionality DH'''
    print("Loading university data...")
    uni = loadUniversity("university_data.csv", "course_catalog.csv")
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

if __name__ == "__main__":
    main()
