import streamlit as st
import pandas as pd
import plotly.express as px

# Add an image to the top of the homepage
st.image("gif2.gif", use_container_width=True) 

# App Title
st.markdown('<h1 style="color: red; text-transform: uppercase;">📊 Excel Data Visualizer</h1>', unsafe_allow_html=True)

# Sidebar image
st.sidebar.image("gif.gif", use_container_width=True)

# Sidebar
st.sidebar.markdown('<div style="font-size:24px; font-weight:bold; color:#4CAF50; margin-bottom:10px;">📋 Task Manager</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:16px; color:#555555; margin-bottom:20px;">Make your data speak! 🚀</div>', unsafe_allow_html=True)

# File Upload
uploaded_file = st.sidebar.file_uploader(
    "Upload your data file (Excel, CSV, or Text)", 
    type=["xlsx", "xls", "csv", "txt"]
)

if uploaded_file:
    # Read uploaded file
    try:
        # Detect file type and load data
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            data = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            data = pd.read_csv(uploaded_file, delimiter="\t")  # Assuming tab-delimited
        st.sidebar.success("File uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")

    # Data Preview
    st.header("📋 Data Preview")
    st.write(data)

    # Column Selection
    st.sidebar.subheader("Select Columns for Visualization")
    numeric_columns = data.select_dtypes(include=["number"]).columns
    if len(numeric_columns) > 0:
        x_axis = st.sidebar.selectbox("X-axis", options=numeric_columns, index=0)
        y_axis = st.sidebar.selectbox("Y-axis", options=numeric_columns, index=1)
    else:
        st.sidebar.error("No numeric columns found in the file.")

    # Chart Type Selection
    st.sidebar.subheader("Select Chart Type")
    chart_type = st.sidebar.radio("Chart Type", options=["Scatter", "Line", "Bar", "Box", "Pie"])

    # Generate Chart
    if chart_type == "Pie":
        st.sidebar.subheader("Select Column for Pie Chart")
        pie_column = st.sidebar.selectbox("Column for Pie Chart", options=data.columns)
        if pie_column:
            pie_data = data[pie_column].value_counts().reset_index()
            pie_data.columns = [pie_column, "Count"]
            fig = px.pie(pie_data, names=pie_column, values="Count", title=f"Pie Chart of {pie_column}")
            st.plotly_chart(fig, use_container_width=True)
    elif x_axis and y_axis:
        st.header("📈 Data Visualization")
        if chart_type == "Scatter":
            fig = px.scatter(data, x=x_axis, y=y_axis, title=f"Scatter Plot of {x_axis} vs {y_axis}")
        elif chart_type == "Line":
            fig = px.line(data, x=x_axis, y=y_axis, title=f"Line Chart of {x_axis} vs {y_axis}")
        elif chart_type == "Bar":
            fig = px.bar(data, x=x_axis, y=y_axis, title=f"Bar Chart of {x_axis} vs {y_axis}")
        elif chart_type == "Box":
            fig = px.box(data, x=x_axis, y=y_axis, title=f"Box Plot of {x_axis} vs {y_axis}")
        
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload a file to proceed.")

# Footer
st.markdown("Developed by Haritha PV")
