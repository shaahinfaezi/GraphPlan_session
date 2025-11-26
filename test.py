import time
from Domains.SatelliteDomain import SatelliteDomain
from Problems.SatelliteProblem import SatelliteProblem
from Domains.TireDomain import TireDomain
from Problems.TireProblem import Tire
from Domains.CakeDomain import CakeDomain
from Problems.CakeProblem import CakeProblem
from Domains.BlockWorld import BlockDomain
from Problems.block import Block

from PlanningGraph.PlanningGraph import PlanningGraph
from Planners.GraphPlanner import GraphPlanner
from Planners.ForwardPlanner import ForwardPlanner
from Planners.BackwardPlanner import BackwardPlanner



# Test with Cake Problem for plotting
print("Testing Cake Problem (Plotting):")
domain = CakeDomain()
problem = CakeProblem(domain)
planning_graph = PlanningGraph(problem)
max_levels = 10
for _ in range(max_levels):
    planning_graph.expand_graph()
    if planning_graph.check_goal_achievable(planning_graph.goal) or planning_graph.has_levelled_off():
        break   






# # Test with Cake Problem for planning
# print("\nTesting Cake Problem (Planning):")
# domain = CakeDomain()
# problem = CakeProblem(domain)

# # Timing GraphPlanner
# start_time = time.time()
# planner = GraphPlanner(problem)
# solution = planner.search()
# end_time = time.time()
# graph_planner_time = end_time - start_time

# if solution:
#     print("Solution found (GraphPlanner):", solution)
# else:
#     print("No solution found (GraphPlanner)")
# print(f"Time taken by GraphPlanner: {graph_planner_time:.8f} seconds")

# # Timing ForwardPlanner
# start_time = time.time()
# planner = ForwardPlanner(problem)
# solution = planner.search()
# end_time = time.time()
# forward_planner_time = end_time - start_time

# print("\nSolution using ForwardPlanner:", solution)
# print(f"Time taken by ForwardPlanner: {forward_planner_time:.8f} seconds")  