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
        supply.append(st.number_input(f"Source {i+1}", value=None, step=1, format="%d", key=f"supply_{i}"))

st.write("## Step 3: Enter Demand")
demand = []
cols = st.columns(n)
for i in range(n):
    with cols[i]:
        demand.append(st.number_input(f"Dest {i+1}", value=None, step=1, format="%d", key=f"demand_{i}"))

st.write("## Step 4: Enter Costs")
costs = []
for i in range(m):
    row = []
    cols = st.columns(n)
    for j in range(n):
        with cols[j]:
            row.append(st.number_input(f"S{i+1}→D{j+1}", value=None, step=1, format="%d", key=f"cost_{i}_{j}"))
    costs.append(row)

st.write("---")

# Display original cost matrix with supply and demand
if not (None in supply or None in demand or any(None in row for row in costs)):
    st.write("## Original Cost Matrix")
    source_labels = [f"S{i+1}" for i in range(m)]
    dest_labels = [f"D{j+1}" for j in range(n)]

    # Create cost matrix dataframe with supply column
    cost_df = pd.DataFrame(costs, columns=dest_labels, index=source_labels)
    cost_df['Supply'] = supply
    cost_df_display = cost_df.copy()

    # Add demand row
    demand_row = demand + [sum(supply)]
    cost_df_display.loc['Demand'] = demand_row

    st.dataframe(cost_df_display, use_container_width=True)

st.write("---")

if st.button("Calculate"):
    # Check if all values are entered
    if None in supply or None in demand or any(None in row for row in costs):
        st.error("Please enter all values before calculating!")
    else:
        total_supply = sum(supply)
        total_demand = sum(demand)
    
    st.write(f"**Total Supply:** {total_supply}")
    st.write(f"**Total Demand:** {total_demand}")
    
    supply_copy = supply[:]
    demand_copy = demand[:]
    costs_copy = [r[:] for r in costs]
    
    source_labels_calc = [f"S{i+1}" for i in range(m)]
    dest_labels_calc = [f"D{j+1}" for j in range(n)]
    
    if total_supply > total_demand:
        st.warning("Adding dummy destination")
        demand_copy.append(total_supply - total_demand)
        for row in costs_copy:
            row.append(0)
        dest_labels_calc.append("Dummy")
    elif total_demand > total_supply:
        st.warning("Adding dummy source")
        supply_copy.append(total_demand - total_supply)
        costs_copy.append([0] * len(dest_labels_calc))
        source_labels_calc.append("Dummy")
    
    allocation, total_cost = north_west_corner_method(supply_copy[:], demand_copy[:], costs_copy)
    
    st.write("## Results")
    
    # Create combined matrix showing costs with allocations
    st.write("### Initial Basic Feasible Solution")
    st.write("*Format: Cost (Allocation in top-right)*")
    
    # Create HTML table for better formatting
    html_table = "<table style='border-collapse: collapse; margin: 20px 0;'>"
    
    # Header row
    html_table += "<tr><th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'>Source/Dest</th>"
    for dest in dest_labels_calc:
        html_table += f"<th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'>{dest}</th>"
    html_table += "<th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'>Supply</th></tr>"
    
    # Data rows
    for i, source in enumerate(source_labels_calc):
        html_table += f"<tr><td style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'><strong>{source}</strong></td>"
        for j in range(len(dest_labels_calc)):
            cost = costs_copy[i][j]
            alloc = allocation[i][j]
            
            # Create cell with cost and allocation
            cell_style = "border: 1px solid #ddd; padding: 12px; position: relative; min-width: 80px; min-height: 60px;"
            if alloc > 0:
                cell_content = f"""
                <div style='position: relative;'>
                    <span style='position: absolute; top: -8px; right: -4px; background-color: #4CAF50; color: white; 
                    padding: 2px 6px; border-radius: 3px; font-size: 12px; font-weight: bold;'>{alloc:.0f}</span>
                    <span style='font-size: 16px;'>{cost:.0f}</span>
                </div>
                """
            else:
                cell_content = f"<span style='font-size: 16px;'>{cost:.0f}</span>"
            
            html_table += f"<td style='{cell_style}'>{cell_content}</td>"
        
        # Supply column
        supply_val = supply_copy[i] if i < len(supply_copy) else 0
        html_table += f"<td style='border: 1px solid #ddd; padding: 8px; background-color: #fff3cd;'><strong>{supply_val:.0f}</strong></td></tr>"
    
    # Demand row
    html_table += "<tr><td style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'><strong>Demand</strong></td>"
    for j in range(len(dest_labels_calc)):
        demand_val = demand_copy[j]
        html_table += f"<td style='border: 1px solid #ddd; padding: 8px; background-color: #fff3cd;'><strong>{demand_val:.0f}</strong></td>"
    html_table += "<td style='border: 1px solid #ddd; padding: 8px;'></td></tr>"
    
    html_table += "</table>"
    
    st.markdown(html_table, unsafe_allow_html=True)
    
    # Simple allocation matrix
    st.write("### Allocation Matrix (Simple View)")
    df = pd.DataFrame(allocation, columns=dest_labels_calc, index=source_labels_calc)
    st.dataframe(df, use_container_width=True)
    
    st.write(f"### Total Transportation Cost: ${total_cost:.2f}")