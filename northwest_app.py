import streamlit as st
import pandas as pd
import numpy as np

# Function for North West Corner Method (unchanged from previous code)
def north_west_corner_method(supply, demand, costs):
    m = len(supply)
    n = len(demand)
    allocation = [[0 for _ in range(n)] for _ in range(m)]
    i = 0
    j = 0
    while i < m and j < n:
        alloc = min(supply[i], demand[j])
        allocation[i][j] = alloc
        supply[i] -= alloc
        demand[j] -= alloc
        if supply[i] == 0:
            i += 1
        else:
            j += 1
    total_cost = 0
    for x in range(m):
        for y in range(n):
            total_cost += allocation[x][y] * costs[x][y]
    return allocation, total_cost

# Streamlit App
st.title("North West Corner Method Calculator")
st.markdown("**Solve transportation problems using the North West Corner Method. Input your data below and compute the initial basic feasible solution.**")

# Sidebar for Inputs
st.sidebar.header("Input Parameters")
m = st.sidebar.number_input("Number of Sources (Rows)", min_value=1, max_value=10, value=2, step=1, help="Enter the number of supply sources.")
n = st.sidebar.number_input("Number of Destinations (Columns)", min_value=1, max_value=10, value=2, step=1, help="Enter the number of demand destinations.")

# Supply Input
st.sidebar.subheader("Supply Values")
supply = []
for i in range(m):
    val = st.sidebar.number_input(f"Supply for Source {i+1}", min_value=0.0, value=10.0, step=1.0, key=f"supply_{i}")
    supply.append(val)

# Demand Input
st.sidebar.subheader("Demand Values")
demand = []
for j in range(n):
    val = st.sidebar.number_input(f"Demand for Destination {j+1}", min_value=0.0, value=10.0, step=1.0, key=f"demand_{j}")
    demand.append(val)

# Cost Matrix Input (using Data Editor for better UX)
st.sidebar.subheader("Cost Matrix")
costs_df = pd.DataFrame(np.zeros((m, n)), columns=[f"Dest {j+1}" for j in range(n)], index=[f"Source {i+1}" for i in range(m)])
costs_edited = st.sidebar.data_editor(costs_df, num_rows="fixed", key="costs_editor")
costs = costs_edited.values.tolist()

# Compute Button
if st.sidebar.button("Compute Allocation", type="primary"):
    with st.spinner("Computing..."):
        # Validate Inputs
        if sum(supply) == 0 or sum(demand) == 0:
            st.error("Supply and demand values must be positive.")
        elif any(c < 0 for row in costs for c in row):
            st.error("Costs must be non-negative.")
        else:
            # Handle Unbalanced Problem
            total_supply = sum(supply)
            total_demand = sum(demand)
            source_labels = [f"Source {i+1}" for i in range(m)]
            dest_labels = [f"Destination {j+1}" for j in range(n)]
            
            if total_supply > total_demand:
                demand.append(total_supply - total_demand)
                for row in costs:
                    row.append(0)
                n += 1
                dest_labels.append("Dummy Destination")
                st.warning("Added dummy destination to balance the problem.")
            elif total_demand > total_supply:
                supply.append(total_demand - total_supply)
                costs.append([0] * n)
                m += 1
                source_labels.append("Dummy Source")
                st.warning("Added dummy source to balance the problem.")
            else:
                st.success("The problem is balanced.")
            
            # Display Input Tables
            st.header("Input Summary")
            supply_df = pd.DataFrame([supply], columns=source_labels, index=["Supply"])
            demand_df = pd.DataFrame(demand, columns=["Demand"], index=dest_labels)
            costs_df_updated = pd.DataFrame(costs, columns=dest_labels, index=source_labels)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Supply Table")
                st.dataframe(supply_df.style.format("{:.2f}"))
            with col2:
                st.subheader("Demand Table")
                st.dataframe(demand_df.style.format("{:.2f}"))
            
            st.subheader("Costs Table")
            st.dataframe(costs_df_updated.style.format("{:.2f}"))
            
            # Compute and Display Results
            allocation, total_cost = north_west_corner_method(supply.copy(), demand.copy(), costs)
            allocation_df = pd.DataFrame(allocation, columns=dest_labels, index=source_labels)
            
            st.header("Results")
            st.subheader("Allocation Table")
            st.dataframe(allocation_df.style.format("{:.2f}").background_gradient(cmap="Blues"))
            
            st.success(f"**Total Cost: ${total_cost:.2f}**")
else:
    st.info("Enter your inputs in the sidebar and click 'Compute Allocation' to see results.")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit. For educational purposes.*")