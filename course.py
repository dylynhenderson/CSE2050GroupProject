from datetime import datetime
from structures import LinkedQueue, EnrollmentRecord, HashMap


class Course:
    '''Course object updated for Milestone 2 DH and SM'''
    def __init__(self, courseCode, cred, maxStu=0, prereqs = 0):
        self.courseCode = courseCode
        self.cred = cred
        self.maxStudents = maxStu
        self.enrolled_roster = []
        self.waitlist = LinkedQueue()
        self.current_sort_key = None
        self.prereqs = prereqs

    def request_enroll(self, student, enroll_date=None):
        '''Enroll student or add to waitlist if full DH'''
        if enroll_date is None:
            enroll_date = datetime.now().strftime("%Y-%m-%d")
        
        for record in self.enrolled_roster:
            if record.student.id == student.id:
                return

        if len(self.enrolled_roster) < self.maxStudents:
            new_rec = EnrollmentRecord(student, enroll_date)
            self.enrolled_roster.append(new_rec)
            self.current_sort_key = None
        else:
            self.waitlist.enqueue(student)

    def sort_enrolled(self, by='id'):
        '''Sort roster using Selection Sort DH'''
        n = len(self.enrolled_roster)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                val_j = self._get_val(self.enrolled_roster[j], by)
                val_min = self._get_val(self.enrolled_roster[min_idx], by)
                if val_j < val_min:
                    min_idx = j
            self.enrolled_roster[i], self.enrolled_roster[min_idx] = \
                self.enrolled_roster[min_idx], self.enrolled_roster[i]
        self.current_sort_key = by

    def _get_val(self, record, key):
        '''Helper to extract sort keys DH'''
        if key == 'id': return record.student.id
        if key == 'name': return record.student.name
        return record.enroll_date

    def recursive_binary_search(self, roster, target_id, low, high):
        '''Locate student by ID using recursion DH'''
        if low > high:
            return -1
        mid = (low + high) // 2
        if roster[mid].student.id == target_id:
            return mid
        elif roster[mid].student.id > target_id:
            return self.recursive_binary_search(roster, target_id, low, mid - 1)
        else:
            return self.recursive_binary_search(roster, target_id, mid + 1, high)

    def drop(self, student_id):
        '''Drop student and promote from waitlist DH'''
        if self.current_sort_key != 'id':
            self.sort_enrolled('id')

        idx = self.recursive_binary_search(self.enrolled_roster, student_id, 0, len(self.enrolled_roster)-1)
        
        if idx != -1:
            self.enrolled_roster.pop(idx)
            if not self.waitlist.is_empty():
                next_student = self.waitlist.dequeue()
                self.request_enroll(next_student)