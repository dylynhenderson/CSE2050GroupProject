from datetime import datetime

class Node:
    '''Node for the LinkedQueue DH'''
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedQueue:
    '''FIFO Queue implementation using a Linked List DH'''
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, item):
        '''Add an item to the back of the queue DH'''
        new_node = Node(item)
        if self.is_empty():
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def dequeue(self):
        '''Remove and return the front item DH'''
        if self.is_empty():
            raise ValueError("Queue is empty")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return data

    def is_empty(self):
        '''Check if queue is empty DH'''
        return self.size == 0

    def __len__(self):
        '''Return current size of queue DH'''
        return self.size


class Stack:
    '''LIFO Stack implementation using a Linked List DH'''
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, item):
        '''Push an item onto the top of the stack DH'''
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        '''Remove and return the top item DH'''
        if self.is_empty():
            raise ValueError("Stack is empty")
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data

    def peek(self):
        '''Return the top item without removing it DH'''
        if self.is_empty():
            raise ValueError("Stack is empty")
        return self.top.data

    def is_empty(self):
        '''Check if stack is empty DH'''
        return self.size == 0

    def __len__(self):
        '''Return current size of stack DH'''
        return self.size


class EnrollmentRecord:
    '''Structure to hold a student and their enrollment date DH'''
    def __init__(self, student, enroll_date):
        self.student = student
        self.enroll_date = enroll_date
        
class HashMap:
    """Hashmap implementation for prerequisites SM"""
    
    def __init__(self, size):
        """Initialize the hashmap with a given size SM"""
        self.size = size
        self.count = 0
        self.buckets = [[] for _ in range(size)]
        
    def _hash(self, key):
        """Private function to hash the key SM"""
        return hash(key) % self.size
    
    def put(self, key, value):
        """Sets values, if this value would make it 80% full, rehash SM and DH"""
        idx = self._hash(key)

        for pair in self.buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return

        self.buckets[idx].append([key, value])
        self.count += 1

        # load factor check
        if self.count / self.size >= 0.8:
            self._rehash()
        
    def get(self, key):
        """Gets values SM"""
        idx = self._hash(key)
        
        for pair in self.buckets[idx]:
            if pair[0] == key:
                return pair[1]
            
        return None
    
    def _rehash(self):
        """Rehashes the hashmap when load factor exceeds 0.8 (80%) SM"""
        oldBuckets = self.buckets

        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in oldBuckets:
            for key, value in bucket:
                idx = self._hash(key)
                self.buckets[idx].append([key, value])
                self.count += 1