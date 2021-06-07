[TOP]

# interview quetsion tips

## 1. easy data structure

linked list

```python
# use list as linked list
ll = [1, 2, 3, 4]
# traverse
for i, num in enumerate(ll):
    ...
```

stack

```python
# use list as stack
st = []
# add to stack
st.append(sti)
# pop from stack
st.pop(-1)
```

queue

```python
# use list as queue
q = []
# add to queue
q.append(qi)
# dequeue
q.pop(0)
```

## 2. sorting algorithms

## 3. DP

## 4. trees

BST traversing

```python
def traverse_tree(node):
    # inorder
    traverse_tree(node.left)
    print(node.val)
    traverse_tree(node.right)
    
    # preorder
    print(node.val)
    traverse(node.left)
    traverse(node.right)
    
    # post order
    traverse(node.left)
    traverse(node.right)
    print(node.val)
```

if we extend to N child tree

```python
def traverse_N_child_tree(node):
    for child_node in node.child:
        traverse(child_node)
```

## 5. two pointers problem

```python
# template
# initialize two pointers
i = 0
j = 1
while i < len(data):
    if j == len(data):
        break
    if insert_logic_here:
        # ...
    else:
        # move pointers
        i += 1
        j += 1
```

## 6. hash table

associative array abstract data type, where keys are mapped to values. a hash table uses a hash function to compute index or hash code into an array of buckets or slots from which the desired value can be found. during the lookup the key is hashed and the resulting hash indicates where the corresponding value is stored.

ideally hash function will assign each key to a unique bucket but most hash table designs employ an imperfect hash function which might cause hash collisions. this is expected unless **all** keys is known ahead of time and no additional keys during processing, we can then use a perfect hash function to prevent collisions. the average cost is independent of the number of elements stored.
$$
load factor = n / k \\
$$
where n is the number of entries occupied in the hash table, and k is the number of buckets. as load factor increases the hash table becomes slower. a solution is to double the size of the table when certain load factor bound is reached. besides load factor we need to know if the entries are distributed evenly within each bucket. in general low load factor means that there is probably wasted memory creating buckets.

we need to weight between the search cost and the cost of generating hash. there is only sorting in pseudo order(can be iterated). there is no efficient way to locate an entry whose key is nearest to given key.

### 6.1 python dict

python dict guarantees insertion order (in 3.7 version change). pythondict keys only takes in immutables or to be precise anything that is hashable (has implemented \__hash__).