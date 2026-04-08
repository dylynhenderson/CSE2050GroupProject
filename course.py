from datetime import datetime
from structures import LinkedQueue, Stack, EnrollmentRecord

class Course:
    '''Course object updated for Milestone 2 DH and SM'''

    def __init__(self, courseCode, cred, maxStu=0):
        '''Initialize a course with a code, credit weight, capacity, an empty roster, and a waitlist DH'''
        self.courseCode = courseCode
        self.cred = cred
        self.maxStudents = maxStu
        self.enrolled_roster = []
        self.waitlist = LinkedQueue()
        self.current_sort_key = None
        self._waitlisted_ids = set()
        self._undo_stack = Stack()

    def request_enroll(self, student, enroll_date=None):
        '''Enroll a student directly if space exists, otherwise place them on the waitlist.
        
        Duplicate enrollments and duplicate waitlist entries are both silently ignored.
        Successful direct enrollments are pushed to the undo stack DH'''
        if enroll_date is None:
            enroll_date = datetime.now().strftime("%Y-%m-%d")

        for record in self.enrolled_roster:
            if record.student.id == student.id:
                return

        if len(self.enrolled_roster) < self.maxStudents:
            record = EnrollmentRecord(student, enroll_date)
            self.enrolled_roster.append(record)
            self.current_sort_key = None
            self._undo_stack.push(('enroll', record))
        else:
            if student.id not in self._waitlisted_ids:
                self.waitlist.enqueue(student)
                self._waitlisted_ids.add(student.id)

    def drop(self, student_id, enroll_date_for_replacement=None):
        '''Remove a student from the roster by ID and promote the next waitlisted student if any.
        
        If the roster is not currently sorted by ID it is automatically re-sorted
        before the binary search runs.
        Successful drops are pushed to the undo stack DH'''
        if self.current_sort_key != 'id':
            self.sort_enrolled('id')

        idx = self.recursive_binary_search(
            self.enrolled_roster, student_id, 0, len(self.enrolled_roster) - 1
        )

        if idx != -1:
            removed = self.enrolled_roster.pop(idx)
            self.current_sort_key = None
            self._undo_stack.push(('drop', removed))
            if not self.waitlist.is_empty():
                next_student = self.waitlist.dequeue()
                self._waitlisted_ids.discard(next_student.id)
                self.request_enroll(next_student, enroll_date_for_replacement)

    def undo(self):
        '''Reverse the most recent enroll or drop operation.
        
        Undo enroll: removes the last enrolled student from the roster.
        Undo drop: re-adds the dropped student directly to the roster DH'''
        if self._undo_stack.is_empty():
            raise ValueError("Nothing to undo")

        action, record = self._undo_stack.pop()

        if action == 'enroll':
            if record in self.enrolled_roster:
                self.enrolled_roster.remove(record)
                self.current_sort_key = None
        elif action == 'drop':
            self.enrolled_roster.append(record)
            self.current_sort_key = None

    def sort_enrolled(self, by='id', algorithm='selection'):
        '''Sort the enrolled roster by the given key using the chosen algorithm. DH'''
        if algorithm == 'selection':
            self._selection_sort(by)
        elif algorithm == 'insertion':
            self._insertion_sort(by)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}. Use 'selection' or 'insertion'.")
        self.current_sort_key = by

    def _selection_sort(self, by):
        '''Sort enrolled_roster in-place using Selection Sort DH'''
        n = len(self.enrolled_roster)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self._get_val(self.enrolled_roster[j], by) < self._get_val(self.enrolled_roster[min_idx], by):
                    min_idx = j
            self.enrolled_roster[i], self.enrolled_roster[min_idx] = \
                self.enrolled_roster[min_idx], self.enrolled_roster[i]

    def _insertion_sort(self, by):
        '''Sort enrolled_roster in-place using Insertion Sort DH'''
        for i in range(1, len(self.enrolled_roster)):
            key_rec = self.enrolled_roster[i]
            key_val = self._get_val(key_rec, by)
            j = i - 1
            while j >= 0 and self._get_val(self.enrolled_roster[j], by) > key_val:
                self.enrolled_roster[j + 1] = self.enrolled_roster[j]
                j -= 1
            self.enrolled_roster[j + 1] = key_rec

    def _get_val(self, record, key):
        '''Return the sort key value for a given EnrollmentRecord DH'''
        if key == 'id':
            return record.student.id
        if key == 'name':
            return record.student.name
        return record.enroll_date

    def recursive_binary_search(self, roster, target_id, low, high):
        '''Recursively locate a student by ID in a roster sorted by student ID. 
        Returns the index of the matching EnrollmentRecord, or -1 if not found DH'''
        if low > high:
            return -1
        mid = (low + high) // 2
        if roster[mid].student.id == target_id:
            return mid
        elif roster[mid].student.id > target_id:
            return self.recursive_binary_search(roster, target_id, low, mid - 1)
        else:
            return self.recursive_binary_search(roster, target_id, mid + 1, high)

    def getStudentCount(self):
        '''Return the number of students currently enrolled in the course DH'''
        return len(self.enrolled_roster)