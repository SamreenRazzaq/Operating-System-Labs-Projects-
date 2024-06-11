import threading
import time
import random

class Node:
    def _init_(self, value):
        self.value = value
        self.next = None

class SinglyLinkedList:
    def _init_(self):
        self.head = None
        self.semaphore = threading.Semaphore()

    def search(self, value, thread_id):
        with self.semaphore:
            current = self.head
            while current:
                if current.value == value:
                    print(f"Searcher {thread_id}: Value {value} found in the list: {self.list_to_str()}")
                    return
                current = current.next
            print(f"Searcher {thread_id}: Value {value} not found in the list: {self.list_to_str()}")

    def insert(self, value, thread_id):
        with self.semaphore:
            new_node = Node(value)
            if not self.head:
                self.head = new_node
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_node
            print(f"Inserter {thread_id}: Inserting {value}: {self.list_to_str()}")

    def delete(self, value, thread_id):
        with self.semaphore:
            if not self.head:
                print(f"Deleter {thread_id}: List is empty. Cannot delete.")
                return

            if self.head.value == value:
                self.head = self.head.next
                print(f"Deleter {thread_id}: Value {value} found and deleted: {self.list_to_str()}")
            else:
                current = self.head
                while current.next and current.next.value != value:
                    current = current.next

                if current.next:
                    current.next = current.next.next
                    print(f"Deleter {thread_id}: Value {value} found and deleted: {self.list_to_str()}")
                else:
                    print(f"Deleter {thread_id}: Value {value} not found. Cannot delete.")

    def list_to_str(self):
        values = []
        current = self.head
        while current:
            values.append(current.value)
            current = current.next
        return str(values)

def searcher_thread(linked_list, thread_id, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(0.1, 1))  # Simulate some work
        value = random.randint(1, 100)
        linked_list.search(value, thread_id)

def inserter_thread(linked_list, thread_id, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(0.1, 1))  # Simulate some work
        value = random.randint(1, 100)
        linked_list.insert(value, thread_id)

def deleter_thread_function(linked_list, thread_id, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(0.1, 1))  # Simulate some work
        if linked_list.head:
            value = linked_list.head.value
            linked_list.delete(value, thread_id)

def main():
    linked_list = SinglyLinkedList()
    stop_event = threading.Event()

    # Create searcher, inserter, and deleter threads
    searcher_threads = [threading.Thread(target=searcher_thread, args=(linked_list, i, stop_event)) for i in range(3)]
    inserter_threads = [threading.Thread(target=inserter_thread, args=(linked_list, i, stop_event)) for i in range(2)]
    deleter_thread = threading.Thread(target=deleter_thread_function, args=(linked_list, 0, stop_event))

    # Start threads
    for thread in searcher_threads + inserter_threads + [deleter_thread]:
        thread.start()

    # Run for a limited time
    time.sleep(10)  # Adjust the time as needed

    # Set the stop event to signal threads to stop
    stop_event.set()

    # Wait for threads to finish
    for thread in searcher_threads + inserter_threads + [deleter_thread]:
        thread.join()

if __name__ == "_main_":
    main()
