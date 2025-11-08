import streamlit as st
import pandas as pd

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

# Simple test
st.write("# North West Corner Method")
st.write("If you can see this, Streamlit is working!")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.m = 3
    st.session_state.n = 3

# Input section
st.write("## Step 1: Set Problem Size")
m = st.number_input("Number of Sources", 2, 10, 3)
n = st.number_input("Number of Destinations", 2, 10, 3)

st.write("## Step 2: Enter Supply")
supply = []
cols = st.columns(m)
for i in range(m):
    with cols[i]:
        supply.append(st.number_input(f"Source {i+1}", value=10.0, key=f"supply_{i}"))

st.write("## Step 3: Enter Demand")
demand = []
cols = st.columns(n)
for i in range(n):
    with cols[i]:
        demand.append(st.number_input(f"Dest {i+1}", value=10.0, key=f"demand_{i}"))

st.write("## Step 4: Enter Costs")
costs = []
for i in range(m):
    row = []
    cols = st.columns(n)
    for j in range(n):
        with cols[j]:
            row.append(st.number_input(f"S{i+1}→D{j+1}", value=1.0, key=f"cost_{i}_{j}"))
    costs.append(row)

st.write("---")

if st.button("Calculate"):
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    st.write(f"**Total Supply:** {total_supply}")
    st.write(f"**Total Demand:** {total_demand}")
    
    supply_copy = supply[:]
    demand_copy = demand[:]
    costs_copy = [r[:] for r in costs]
    
    source_labels = [f"S{i+1}" for i in range(m)]
    dest_labels = [f"D{j+1}" for j in range(n)]
    
    if total_supply > total_demand:
        st.warning("Adding dummy destination")
        demand_copy.append(total_supply - total_demand)
        for row in costs_copy:
            row.append(0)
        dest_labels.append("Dummy")
    elif total_demand > total_supply:
        st.warning("Adding dummy source")
        supply_copy.append(total_demand - total_supply)
        costs_copy.append([0] * n)
        source_labels.append("Dummy")
    
    allocation, total_cost = north_west_corner_method(supply_copy[:], demand_copy[:], costs_copy)
    
    st.write("## Results")
    st.write("### Allocation Matrix")
    df = pd.DataFrame(allocation, columns=dest_labels, index=source_labels)
    st.dataframe(df)
    
    st.write(f"### Total Cost: ${total_cost:.2f}")