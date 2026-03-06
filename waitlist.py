from typing import Optional, Iterable, Any

class Node:
    
    def __init__(self, item, link: Optional['Node'] = None) -> None:
        """Initiliazes"""
        self.item = item
        self.link = link
        
    def __repr__(self) -> str:
        """Returns Representation"""
        return f"Node({self.item})"
    
    
class LinkedList:
    def __init__(self, items: Optional[Iterable[Any]] = None) -> None:
        """Initializes the LinkedList. If items is provided, it will be added to the list in order."""
        self._head = None
        self.size = 0
        self._tail = self.get_tail()
        if items is not None:
            for item in items:
                self.add_last(item)
        
    def add_first(self, item):
        """Adds an item to the beginning of the list."""
        newNode = Node(item, self._head)
        self._head = newNode
        self.size += 1
        
    def remove_first(self):
        """Removes and returns the first item in the list. Raises an error if the list is empty."""
        if self._head is None:
            raise RuntimeError()
        item = self._head.item
        self._head = self._head.link
        self.size -= 1
        return item
    
    def get_head(self):
        """Returns the first item in the list, or None if the list is empty."""
        if self._head is None:
            return None
        return self._head.item
    
    def get_tail(self):
        """Returns the last item in the list, or None if the list is empty."""
        if self._head is None:
            return None
        current = self._head
        while current.link is not None:
            current = current.link
        return current.item
    
    def add_last(self, item):
        """Adds an item to the end of the list."""
        newNode = Node(item)
        if self._head is None:
            self._head = newNode
        else:
            current = self._head
            while current.link is not None:
                current = current.link
            current.link = newNode
        self.size += 1
        
    def remove_last(self):
        """Removes and returns the last item in the list. Raises an error if the list is empty."""
        if self._head is None:
            raise RuntimeError()

        if self._head.link is None:
            item = self._head.item
            self._head = None
            self.size -= 1
            return item

        current = self._head
        while current.link.link is not None:
            current = current.link

        item = current.link.item
        current.link = None
        self.size -= 1
        return item
        
        
        
    def __len__(self):
        """Returns the number of items in the list."""
        return self.size
