#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interactive Data Visualization App")
st.write("Upload an Excel or CSV file to create interactive graphs.")

# File upload
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Determine file type and read data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("Data Preview:")
    st.dataframe(df)

    # Sidebar options for customizing the plot
    st.sidebar.header("Customize Your Plot")
    chart_type = st.sidebar.selectbox(
        "Select Chart Type",
        options=["Scatter", "Line", "Bar", "Histogram", "Pie", "Box", "Pair Plot"]
    )

    # Conditional logic for column selection based on the chart type
    if chart_type in ["Scatter", "Line", "Bar", "Box"]:
        x_axis = st.sidebar.selectbox("Select X-axis", options=df.columns)
        y_axis = st.sidebar.selectbox("Select Y-axis", options=df.columns)
        color = st.sidebar.selectbox("Select Column for Color (Optional)", options=[None] + list(df.columns))
    elif chart_type == "Histogram":
        x_axis = st.sidebar.selectbox("Select X-axis", options=df.columns)
        color = st.sidebar.selectbox("Select Column for Color (Optional)", options=[None] + list(df.columns))
        y_axis = None  # Not needed for histograms
    elif chart_type == "Pie":
        x_axis = st.sidebar.selectbox("Select Column for Categories", options=df.columns)
        y_axis = st.sidebar.selectbox("Select Column for Values", options=df.columns)
        color = None  # Not applicable for pie charts
    elif chart_type == "Pair Plot":
        selected_columns = st.sidebar.multiselect("Select Columns for Pair Plot", options=df.columns)

    # Create the selected type of plot
    if chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color, title=f"{y_axis} vs {x_axis}")
    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis, color=color, title=f"{y_axis} vs {x_axis} (Line Chart)")
    elif chart_type == "Bar":
        # Group data by x_axis and calculate the mean of y_axis
        aggregated_df = df.groupby(x_axis, as_index=False)[y_axis].mean()
        fig = px.bar(aggregated_df, x=x_axis, y=y_axis, color=color, title=f"Average of {y_axis} grouped by {x_axis}")
    elif chart_type == "Histogram":
        fig = px.histogram(df, x=x_axis, color=color, title=f"Distribution of {x_axis}")
    elif chart_type == "Pie":
        fig = px.pie(df, names=x_axis, values=y_axis, title=f"Pie Chart of {x_axis} by {y_axis}")
    elif chart_type == "Box":
        fig = px.box(df, x=x_axis, y=y_axis, color=color, title=f"Box Plot of {y_axis} by {x_axis}")
    elif chart_type == "Pair Plot" and selected_columns:
        fig = px.scatter_matrix(df, dimensions=selected_columns, title="Pair Plot")

    # Display the plot if created
    if 'fig' in locals():
        st.plotly_chart(fig)

else:
    st.write("Please upload a file to proceed.")


# In[ ]:




