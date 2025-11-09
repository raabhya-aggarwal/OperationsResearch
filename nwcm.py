import numpy as np
import pandas as pd

def north_west_corner_method(supply, demand, costs):
    """
    Implements the North West Corner Method for transportation problems.
    
    Parameters:
    supply (list): List of supply values for each source.
    demand (list): List of demand values for each destination.
    costs (2D list): Cost matrix where costs[i][j] is the cost from source i to destination j.
    
    Returns:
    allocation (2D list): Allocation matrix showing how much is shipped from each source to each destination.
    total_cost (float): Total transportation cost.
    """
    m = len(supply)  # Number of sources
    n = len(demand)  # Number of destinations
    allocation = [[0 for _ in range(n)] for _ in range(m)]
    
    i = 0  # Start from first source
    j = 0  # Start from first destination
    
    while i < m and j < n:
        # Allocate the minimum of remaining supply and demand
        alloc = min(supply[i], demand[j])
        allocation[i][j] = alloc
        supply[i] -= alloc
        demand[j] -= alloc
        
        # Move to next cell
        if supply[i] == 0:
            i += 1  # Move down to next source
        else:
            j += 1  # Move right to next destination
    
    # Calculate total cost
    total_cost = 0
    for x in range(m):
        for y in range(n):
            total_cost += allocation[x][y] * costs[x][y]
    
    return allocation, total_cost

def main():
    # Input number of sources and destinations
    m = int(input("Enter the number of sources (rows): "))
    n = int(input("Enter the number of destinations (columns): "))
    
    # Input supply values
    supply = []
    print("Enter supply values for each source:")
    for i in range(m):
        supply.append(float(input(f"Supply for source {i+1}: ")))
    
    # Input demand values
    demand = []
    print("Enter demand values for each destination:")
    for j in range(n):
        demand.append(float(input(f"Demand for destination {j+1}: ")))
    
    # Input cost matrix
    costs = []
    print("Enter the cost matrix (row by row):")
    for i in range(m):
        row = []
        for j in range(n):
            row.append(float(input(f"Cost from source {i+1} to destination {j+1}: ")))
        costs.append(row)
    
    # Calculate totals
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    # Handle unbalanced problem by adding dummy
    source_labels = [f"Source {i+1}" for i in range(m)]
    dest_labels = [f"Destination {j+1}" for j in range(n)]
    if total_supply > total_demand:
        # Add dummy destination
        demand.append(total_supply - total_demand)
        for row in costs:
            row.append(0)  # Cost to dummy is 0
        n += 1
        dest_labels.append("Dummy Destination")
        print("Added dummy destination to balance the problem.")
    elif total_demand > total_supply:
        # Add dummy source
        supply.append(total_demand - total_supply)
        dummy_row = [0] * n  # Costs from dummy are 0
        costs.append(dummy_row)
        m += 1
        source_labels.append("Dummy Source")
        print("Added dummy source to balance the problem.")
    else:
        print("The problem is balanced.")
    
    # Create Pandas DataFrames for tables
    supply_df = pd.DataFrame([supply], columns=source_labels, index=["Supply"])
    demand_df = pd.DataFrame(demand, columns=["Demand"], index=dest_labels)
    costs_df = pd.DataFrame(costs, columns=dest_labels, index=source_labels)
    
    print("\nSupply Table:")
    print(supply_df)
    print("\nDemand Table:")
    print(demand_df)
    print("\nCosts Table:")
    print(costs_df)
    
    # Run North West Corner Method
    allocation, total_cost = north_west_corner_method(supply.copy(), demand.copy(), costs)
    
    # Create allocation DataFrame
    allocation_df = pd.DataFrame(allocation, columns=dest_labels, index=source_labels)
    print("\nAllocation Table:")
    print(allocation_df)
    
    print(f"\nTotal Cost: {total_cost:.2f}")

if __name__ == "__main__":
    main()