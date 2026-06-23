# CQueue<T>

CQueue<T> is a generic class that implements the ICollection<T> interface.

### Description

The CQueue<T> class is a dynamic collection of T type data, which is organized as a queue that operates on the FIFO (first in, first out) principle.

### Declaration

```
   template<typename T>
   class CQueue : public ICollection<T>

```

### Header

```
   #include <Generic\Queue.mqh>

```

```
Inheritance Hierarchy
   ICollection
       CQueue

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds an element to a queue |
| Enqueue | Adds an element to a queue |
| Count | Returns the number of elements in the queue |
| Contains | Determines whether the queue contains an element with the specified value |
| TrimExcess | Sets the capacity of a queue to the actual number of elements, and thus frees up unused memory |
| CopyTo | Copies all elements of a queue to the specified array starting at the specified index |
| Clear | Removes all elements from a queue |
| Remove | Removes the first occurrence of the specified element from the queue |
| Dequeue | Returns the starting element and removes it from the queue |
| Peek | Returns the starting element without removing it from the queue |
