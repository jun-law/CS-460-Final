"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Jun Law
Student ID: 132484882

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq

# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    ""
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    return "- A single shortest-path run from S is insufficient due to having the additional constraint that there must be a minimum cost path constructed from the start to exit that must pass through set of required nodes. A SSP run is too broad since it only records all distances from the start to every node, and will not be able to know how to select the shortest route between each required node.\n - After all inter-location costs are known, the algorithm must decide which path to take from the start that visits all required nodes and ends at exit that will minimize the total cost of fuel consumed.\n - The algorithm requires a search over orders because each connection from each required source node to the other nodes may have different costs, leading to the need to check over each these different combinations to find the best path with the minimum cost."

# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """

    # add source node
    sources = []
    sources.append(spawn)
    # print(sources)

    # add required nodes
    for relic in relics:
        sources.append(relic)

    # add exit node
    sources.append(exit_node)

    # remove duplicates
    sources = set(sources)
    sources = list(sources)

    # print(sources)
    return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """

    # dictionary: min distance from source to each node
    distance = {}
    # set all source nodes to infinity
    for key in graph: 
        distance[key] = float('inf')

        # add all neighbor nodes of each node
        for elements in graph[key]:
            neighbor = elements[0] 
            if neighbor not in distance:
                distance[neighbor] = float('inf')  

    # set start node to distance 0
    distance[source] = 0

    # min heap
    heap = []
    heapq.heappush(heap, (0, source))

    while (not len(heap) == 0):
        # remove element
        curr, u = heapq.heappop(heap)

        # skip non-optimal lengths
        if curr > distance[u]:
            continue
        
        # traverse all neighbors of node
        for v, w in graph[u]: 
            # if shorter path to neighbor found, update distance
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                # add neighbor to heap
                heapq.heappush(heap, (distance[v], v))

    return distance


def precompute_distances(graph, spawn, required, exit_node):
    """
    Parameters
    ----------

    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    """
    # grab source nodes
    source_list = select_sources(spawn, required, exit_node)

    # all results
    solution_list = {}

    # run Dijkstras on every source
    for source in source_list:
        result = run_dijkstra(graph, source)
        
        # filter result from Dijkstra's
        solution = filter_required(result, exit_node, required)
        
        # build solution
        solution_list[source] = solution
        
    return solution_list

# helper: remove paths containing nodes that are not required
def filter_required(dict, exit_node, required):
    
    # track required paths only
    filtered = {}
    # check every required node's neighbor
    for node in dict:

        # copy required nodes into new dictionary
        if (node == exit_node) or (node in required):
            filtered[node] = dict[node]
            
    return filtered

# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.


    """
    return "DO THIS PLSSSSSS"


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    """
    return "- **The failure mode:** Running Dijkstra does not work when the graph has negative edge weights\n. - **Counter-example setup:** **Entrance:** S | **Relic chambers:** B, C | **Exit:** T. \n- **What greedy picks:** S -> C -> B -> T. cost = 1 + 1 + 1 = 3. \n- **What optimal picks:** S -> B -> C -> T, cost = 2 + (-20) + 1 = -19. - **Why greedy loses:** Greedy loses because once it encounters the best immediate edge weight, it makes that edge a permanent part of the solution. This fails to consider future better possibilities that may reduce the cost, such as negative edges. In my example, the greedy thinks the weight of of S -> C = 1 is optimal, when the actual optimal weight from S -> C is S -> B -> C = -19. \n - The algorithm must explore the different order of paths that will minimize the fuel cost traveling from the start node, visiting every required node, and ending at the exit node. "


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    
    # track visited nodes and optimal route
    visited = []
    optimal_route = []

    # call recursive helper
    _explore(dist_table, spawn, relics, visited, 0, exit_node, optimal_route)

    # check if valid solution exists, empty case works
    if len(optimal_route) != 0:
        solution = min_cost, optimal_route
    else:
        solution = float('inf'), []
    
    return solution

# track global best min cost
min_cost = float('inf')

def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.


    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    
    # best minimum cost encountered so far
    global min_cost
    # run DFS on graph

    # base case: reached exit and visited all required nodes
    if (current_loc == exit_node) and (len(relics_remaining) == 0):

        # update best solution
        if (len(best) != 0):
            best.clear()
        
        for relic in relics_visited_order:
            best.append(relic)

        # update minimum cost
        min_cost = cost_so_far
        return
    
    
    """
    GRADED COMMENT: 
    This pruning condition is always safe because the best minimum cost is ALWAYS tracked inside the global minimum variable: min_cost.
    Each time, if the current cost is NOT better than the global minimum, the current path will be eliminated, while the global minimum
    value remains untouched and is still the best minimum cost found so far. 
    """
    # bound function (pruning condition)
    if cost_so_far >= min_cost:
        return

    # recursive case: explore every neighbor
    else:
        # access inner dictionary containing neighbor info
        inner = dist_table[current_loc]

        # visit every neighbor that has not been visited yet
        for neighbor, cost in inner.items():
            if (neighbor not in relics_visited_order):

                # run into exit node early, not all relics visited
                if (neighbor == exit_node) and (len(relics_remaining) != 0):
                    continue

                # run into exit node, all required relics visited
                if (neighbor == exit_node) and (len(relics_remaining) == 0):
                   
                   # update cost
                   cost_so_far += cost
                   _explore(dist_table, neighbor, relics_remaining, relics_visited_order, cost_so_far, exit_node, best)
                   
                # neighbor is NOT the exit node
                else:
                    # update relics left to visit and relics visited
                    relics_remaining.remove(neighbor)
                    relics_visited_order.append(neighbor)
                    
                    # update cost so far
                    cost_so_far += cost
                    
                    # recursive call         
                    _explore(dist_table, neighbor, relics_remaining, relics_visited_order, cost_so_far, exit_node, best)
                
                    # undo, backtrack to last step
                    relics_remaining.append(neighbor)
                    relics_visited_order.remove(neighbor)

                    # prevent nan output
                    if cost_so_far == float('inf'):
                        continue
                    # update cost
                    cost_so_far -= cost


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.


    """
    # get distances between all required nodes
    table = precompute_distances(graph, spawn, relics, exit_node)
    # final optimal path
    final_result = find_optimal_route(table, spawn, relics, exit_node)
    
    return final_result


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":

    _run_tests()
    """
        
        
        spawn = 'A'
        relics = ['B', 'C', 'C']
        exit_node = 'F'
        select_sources(spawn, relics, exit_node)

    
    graph_1 = {
        'S': [('C', 2), ('B', 1), ('D', 2)],
        'B': [('D', 1000), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
        }
        
    required = ['B', 'C']
    select_sources('S', required, 'T')
    table = precompute_distances(graph_1, 'S', required, 'T')

    temp = []
    visited = []

    # all arguments for explore() given inside of find_optimal_route()
    # we call explore() in there now
    # _explore(table, 'S', required, visited, 0, 'T', temp)

    # find_optimal_route(table, 'S', required, 'T')

    solve(graph_1, 'S', required, 'T')
    """