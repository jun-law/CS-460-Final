# The Torchbearer

**Student Name:** Jun Law
**Student ID:** 132484882
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  - A single shortest-path run from S is insufficient due to having the additional constraint that there must be a minimum cost path constructed from the start to exit that must pass through set of required nodes. A SSP run is too broad since it only records all distances from the start to every node, and will not be able to know how to select the shortest route between each required node

- **What decision remains after all inter-location costs are known:**
  - After all inter-location costs are known, the algorithm must decide which path to take from the start that visits all required nodes and ends at exit that will minimize the total cost of fuel consumed

- **Why this requires a search over orders (one sentence):**
  - The algorithm requires a search over orders because each connection from each required source node to the other nodes may have different costs, leading to the need to check over each these different combinations to find the best path with the minimum cost.
---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| (char) | The algorithm must start running from S, the given start node, so it must be a source |
| (char) | Every chamber relic node is also a source node because the shortest path from it to every other source node must be computed in order to ensure each chamber relic is included in the final path | 

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Dictionary |
| What the keys represent | A given source node |
| What the values represent | A list containing pairs (char, int) representing the neighboring nodes to the given source node, and the cost needed to get to this neighbor from the given source |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Dictionaries allow for immediate access when using a key to look up the corresponding value |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** k + 2
- **Cost per run:** O(mlog(n))
- **Total complexity:** (k + 2) * O(mlog(n))
- **Justification (one line):** The total number of runs is the total number of source nodes: number required nodes + start node + exit node = k + 2, combined with the cost for each run, O(mlog(n))

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  - At the beginning of each iteration, every finalized node, v in S contains the shortest path, dist[v] possible from the source, x to itself 

- **For nodes not yet finalized (not in S):**
  - At the beginning of each iteration, every node, u that has not been finalized yet and is not in S, contains the shortest path found, dist[u] from the source, x to itself, where all nodes in between have been finalized and are in S.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  - {Q} init {P}: assume Q is true
  - u = source, set dist[u] = 0 because it is the source, x itself
  - No nodes have been added to S yet, nodes between x and x is an empty set

- **Maintenance : why finalizing the min-dist node is always correct:**
  - {P && B} S {P}: Assume {P && B} true. 
  - If the node being processed does not have an optimal distance, skip it
  - Check all neighbors of current node, if better path found to it from u, update neighbor's distance to smaller value
  - Before next iteration begins: all distances of nodes have updated as appropriate, {P && B} S {P} holds

  ***do i need to talk about both cases? mention nonnegative edge weights too

- **Termination : what the invariant guarantees when the algorithm ends:**
  - {P && !B} => R: assume {P && !B} is true
  - Every node, finalized and not finalized contain the shortest distance from the source to itself, and the heap is empty
  - This means the shortest paths from the source to each node is found
  - This is postcondition R, the result of Dijkstra's, {P && !B} => R holds

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

- Routing decisions will be unable to locate the best path without first knowing the correct shortest distances to each location from the initial starting point.  

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** Running Dijkstra does not work when the graph has negative edge weights
- **Counter-example setup:** 

**Entrance:** S | **Relic chambers:** B, C | **Exit:** T

| From \ To | B   |  C  |  T  |
|-----------|-----|---- |-----|
| S         | 2   |  1  | --  |
| B         | --  | -20 |  1  |
| C         | 1   | --  | 1   |

- **What greedy picks:** S -> C -> B -> T. cost = 1 + 1 + 1 = 3
- **What optimal picks:** S -> B -> C -> T, cost = 2 + (-20) + 1 = -19
- **Why greedy loses:** Greedy loses because once it encounters the best immediate edge weight, it makes that edge a permanent part of the solution. This fails to consider future better possibilities that may reduce the cost, such as negative edges. In my example, the greedy thinks the weight of of S -> C = 1 is optimal, when the actual optimal weight from S -> C is S -> B -> C = -19

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- The algorithm must explore the different orders of paths that will minimize the fuel cost traveling from the start node, visiting every required node, and ending at the exit node. 

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | int | Tracks where the current node is |
| Relics already collected | relics_visited_order | list | Tracks the order in which the relics have already been visited/collected |
| Fuel cost so far | cost_so_far | int | Tracks cost accumulated so far from the source node to the current node |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | List |
| Operation: check if relic already collected | Time complexity: O(n)|
| Operation: mark a relic as collected | Time complexity: O(1)|
| Operation: unmark a relic (backtrack) | Time complexity: O(1)|
| Why this structure fits | Lists preserve elements in the order they are appended, which makes it convenient to track the order of when each node was visited/collected. Lists also allow for quick removal of a specific element using remove(x), and checking whether an item exists is made convenient with the "in" keyword |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** (k + 2) * O(mlog(n))
- **Why:** Each Dijkstra run costs O(mlog(n)), and will be run k + 2 times where k is, the number of required relic chambers, with an additional 2 to account for the start and exit nodes. 

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** The global minimum cost seen so far and the cost to get to the current node from the start node
- **When it is used:** It is used after the check for the base case and before the recursive case.
- **What it allows the algorithm to skip:** If the cost so far accumulated by the current node is greater than or equal to the global minimum seen so far

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** The current node (current_loc), the fuel cost from the start to the current node (cost_so_far), the best minimum cost found so far (min_cost), the order of nodes that have been visited so far(relics_visited_order), and required nodes left to visit (relics_remaining)
- **What the lower bound accounts for:** The lower bound accounts for potential future better possibilities, meaning the bound will change to the current cost if it is lower

- **Why it never overestimates:** Since the function immediately eliminates (prunes) costs that are greater than or equal to the lower bound, and updates ONLY if the cost is smaller, it will never overestimate. 

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- Pruning is safe because the global minimum cost is always tracked in min_cost, and it updates only if there is a smaller cost found
- If a cost that is not smaller than min_cost is encountered, it is eliminated immediately, so pruning may only update min_cost to strictly smaller values 

---

## References

> Bullet list. If none beyond lecture notes, write that. (redoing this part)

- Dijkstra’s Algorithm with Adjacency Lists | by Joshua Clark. Used to better understand how Dijkstra's works with adjacency lists in run_dijkstra(). Verified by running run_dijkstra() after finishing implementation, which matched the high level concepts in this article. 

- heapq — Heap queue algorithm — Python 3.14.5rc1 documentation. Used to reference how to use heap methods in run_dijkstra(). Verified by testing heapq.push() and heapq.pop() works in my code. 

- Python - Pair iteration in list - GeeksforGeeks. Used to better understand how to traverse pairs in run_dijkstra(). Verified correctness by printing loop for pairs during testing

- Youtube video: 7.3 Traveling Salesman Problem - Branch and Bound (Abdul Bari). Used to better understand the concept of branch and bound and what needs to be pruned. Verified by running _explore() after implementation, the logic matches with my code. 

- Loop Through a Nested Dictionary in Python - GeeksforGeeks. Used to reference the syntax for how to loop through a nested dictionary. Verified by running _explore(), the correct values are accessed within my nested dictionary.

- Python - Copy Lists, W3Schools. Used to understand how to use list.copy() in _explore(). Verified by seeing whether values were copies from my old list into my new list.  

- Python List/Array Methods, W3Schools. Used to check correct usage of List methods in _explore(). Verified by running explore() to make sure lists were being manipulated correctly. 

- The in Operator in Python (for List, String, Dictionary) | note.nkmk.me. Used to learn more about the "in" keyword for part 3a, confirmed the time complexity is O(n) for Lists. Verified with my own knowledge of data structures: every element in the list must have been checked over, which is linear. 