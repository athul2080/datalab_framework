import streamlit as st
import pandas as pd
from utils import run_notebook

st.title("Synthetic Data Generation UI")

# Radio button to choose the model type
option = st.radio("Choose model type", ["Single Table", "Multi Table"])

# File uploader to upload the Excel file
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# If a file is uploaded
if uploaded_file:

    # Single Table Model
    if option == "Single Table":
        # Save uploaded file temporarily
        with open("uploaded_file.xlsx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Read and display the uploaded data
        st.subheader("Uploaded Data")
        df = pd.read_excel("uploaded_file.xlsx")
        st.dataframe(df)

        # Generate synthetic data using the notebook
        if st.button("Generate Synthetic Data"):
            # Run the Single Table Model notebook
            notebook_output = run_notebook("01_Tabular_Data.ipynb")
            st.text("Notebook executed successfully, here is the output script:")
            st.code(notebook_output, language="python")
            
            # You can now use the generated script here and call the synthetic data model
            # For example, replace below line with actual code to generate synthetic data
            # synthetic_df = your_function_from_notebook(df)

            # For now, display the uploaded df as a placeholder for synthetic data
            st.subheader("Synthetic Data Output")
            st.dataframe(df)

            # Optionally, provide a download button for the output
            st.download_button(
                "Download Synthetic Excel",
                df.to_excel("synthetic_output.xlsx", index=False),
                file_name="synthetic_output.xlsx"
            )

    # Multi Table Model
    else:  # Multi-table
        # Save the uploaded file temporarily
        with open("uploaded_file.xlsx", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Read the uploaded Excel file
        xls = pd.ExcelFile("uploaded_file.xlsx")
        tables = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

        st.subheader("Uploaded Tables")
        for name, df in tables.items():
            st.write(f"### {name}")
            st.dataframe(df)

        # Generate synthetic data using the notebook
        if st.button("Generate Synthetic Multi-Table Data"):
            # Run the Multi Table Model notebook
            notebook_output = run_notebook("02_Relational_Data.ipynb")
            st.text("Notebook executed successfully, here is the output script:")
            st.code(notebook_output, language="python")
            
            # You can now use the generated script here to generate synthetic data for multiple tables
            # For now, display the uploaded tables as a placeholder
            st.subheader("Synthetic Tables Output")
            for name, df in tables.items():
                st.write(f"### Synthetic: {name}")
                st.dataframe(df)

                st.download_button(
                    f"Download {name} Synthetic",
                    df.to_excel(f"{name}_synthetic.xlsx", index=False),
                    file_name=f"{name}_synthetic.xlsx"
                )
