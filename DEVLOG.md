# Development Log – The Torchbearer

**Student Name:** Jun Law
**Student ID:** 132484882

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – 5/5/26: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

First, I will find all valid paths from the start that connect to the required relic chambers and reach the exit, then, I will implement Dijkstra's Algorithm to find the shortest distance from the start to every relic chamber. Using the information I have so far, I will built an optimal path that consumes the least amount of fuel from start to finish that satisfies the given constraints. I expect this step to be the most difficult part of the assignment since it involves tracking multiple things such as the best path so far, the least amount of fuel used, whether the required relic chambers have been visited, etc. To test, I will draw different graphs on my iPad, then run my code on the same inputs to verify my program behaves as expected. 

---


## Entry 2 – [5/7/26]: Failing to track distances in run_dijkstra()

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

A bug I encountered in run_dijkstra() was originally not having a data structure to track the distances from the source node. By failing to include this, I did not know how far each node was from the source, so my algorithm failed. In addition, this led me to try to use the heap to manage my distances from the source which is wrong. To fix it, I added a dictionary called distance, which I used to initialize all nodes to distance infinity. If a smaller distance from the source was found for a particular node, its distance would be updated. 

## Entry 3 – [5/9/26]: Wrong logic used with filter_required()
filter_required() is a helper method I added to filter out edges that are not located between two required nodes or a required node and the exit node, to be used in precompute_distances(). Previously, I had created a dictionary named result in precompute_distances and tried assigning the result of calling run_dijkstra(), which returns a dictionary, as an entry. This created a nested dictionary and it did not allow me to access the items in the result as I wished. I was able to fix this issue by simply assigning the result of calling run_dijkstra() to a variable instead, so now filter_required() is correct.

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 25 minutes |
| Part 2: Precomputation Design | 5 hours |
| Part 3: Algorithm Correctness | 1 hour |
| Part 4: Search Design | |
| Part 5: State and Search Space | 5 hours |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
