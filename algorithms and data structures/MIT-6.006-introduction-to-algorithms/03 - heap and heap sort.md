[TOC]

# heap and heap sort

main motivation: 

> priority queue

implements a set S of elements, and each of the elements is associated with a key and able to do operation to it similar to a queue, eg insert, delete and etc and should be asymptotically fast.

operations:

1. insert(S, x) - insert element x to set S
2. max(S) - return element of S with largest key
3. extract_max(S) - return element of S with largest key and removes it from S
4. increment_key(S, x, k) - increase the value of x's key to new value k

a heap is an implementation of a priority queue, an array visualized as a nearly complete (to fit any arbitrary size, else for the example it must have 15 elements instead of 10) binary tree.

```python
heap_example = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
'''
visualizing it
      16
   /      \
  14      10
 /   \   /   \
 8   7   9   3
/ \ /
2 4 1
'''
```

heap as a tree:

- root of the tree (first element) - i = 1
- parent(i) = i / 2
- left(i) = 2i
- right(i) = 2i + 1

max-heap property: key of a node is >= the keys of its children; min-heap property: key of a node is <= the keys of its children. its our best interest to maintain the property when we modifies the data structure to preserve the functionalities.

## building and maintaining a heap

heap operations

- build max heap: complexity its n instead of n log(n) with careful analysis
- max heapify(A, i): correct a **single violation** of the heap property in a subtree's root (where A is the array and i is the index)
- heap size: return array size

max heapify assumes that the trees rooted at left(i) and right(i) are max heaps and correct the violation by exchanging with the max child thus with the assumption the time complexity is O(log N)

```pseudocode
build_max_heap(A):
	for i = n / 2 down to 1:
		do max_heapify(A, i)
```

Q: why we can start from n / 2?

A: element A[n/2 ... n] are all leaves

### proof of build max heap complexity is n instead of nlog(n)

observation: max heapify takes O(1) for nodes that are one level above the leaves and in general O(l) time for nodes that are l levels above the leaves. thus total amount of work required
$$
\sum n/4 * (1c) + n/8 * (2c) + n/16 * (3c) + ... + 1 * (log(c))
\\
\text{set: } n/4 = 2^k
\\
\sum c*2^k(1/2^0 + 2/2^1 + 3/2^2 + ... + (k+1)/2^k)
\\
\text{essentially } 2 < (1/2^0 + 2/2^1 + 3/2^2 + ... + (k+1)/2^k) <3
\\
\text{thus complexity is } O((n/4) * 3) \approx O(n)
$$

### heap sort

```pseudocode
# overall n(log(n))
build_max_heap(unordered_Array), O(n)
find max element A[1] O(1)
swap elements A[n] with A[1] O(1)
	max element is at th end of the array
discard node n from heap by decrementing heap size 
new root may violate violate max heap properties but children are max heaps - run max heapify O(log(n))
repeat n
```

