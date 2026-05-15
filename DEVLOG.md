# Development Log – The Torchbearer

**Student Name:** Jun Law
**Student ID:** 132484882
---

## Entry 1 – 5/5/26: Initial Plan

First, I will find all valid paths from the start that connect to the required relic chambers and reach the exit, then, I will implement Dijkstra's Algorithm to find the shortest distance from the start to every relic chamber. Using the information I have so far, I will built an optimal path that consumes the least amount of fuel from start to finish that satisfies the given constraints. I expect this step to be the most difficult part of the assignment since it involves tracking multiple things such as the best path so far, the least amount of fuel used, whether the required relic chambers have been visited, etc. To test, I will draw different graphs on my iPad, then run my code on the same inputs to verify my program behaves as expected. 

---


## Entry 2 – [5/7/26]: Failing to track distances in run_dijkstra()

A bug I encountered in run_dijkstra() was originally not having a data structure to track the distances from the source node. By failing to include this, I did not know how far each node was from the source, so my algorithm failed. In addition, this led me to try to use the heap to manage my distances from the source which is wrong. To fix it, I added a dictionary called distance, which I used to initialize all nodes to distance infinity. If a smaller distance from the source was found for a particular node, its distance would be updated. 


## Entry 3 – [5/9/26]: Wrong logic used with filter_required()
filter_required() is a helper method I added to filter out edges that are not located between two required nodes or a required node and the exit node, to be used in precompute_distances(). Previously, I had created a dictionary named result in precompute_distances and tried assigning the result of calling run_dijkstra(), which returns a dictionary, as an entry. This created a nested dictionary and it did not allow me to access the items in the result as I wished. I was able to fix this issue by simply assigning the result of calling run_dijkstra() to a variable instead, so now filter_required() is correct.

---

## Entry 4 – [5/14/26]: Post-Implementation Reflection

If I had more time, I would try to optimize my bound function in _explore(), since I am currently using brute force to prune correctly. While my method works, time complexity is an important factor to consider when writing algorithms. By optimizing the bound function, I would be able to make my algorithm much more efficient. 

---

## Final Entry – [5/14/26]: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 30 minutes |
| Part 2: Precomputation Design | 5 hours |
| Part 3: Algorithm Correctness | 1 hour |
| Part 4: Search Design | 1 hour |
| Part 5: State and Search Space | 30 minutes |
| Part 6: Pruning | 5 hours |
| Part 7: Implementation | 30 minutes |
| README and DEVLOG writing | 2 hours |
| **Total** | 15 hours, 30 min |
