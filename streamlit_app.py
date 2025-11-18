import streamlit as st
import pandas as pd
from model_single import generate_single_table_synthetic
from model_multi import generate_multi_table_synthetic

st.title("Synthetic Data Generation UI")

option = st.radio("Choose model type", ["Single Table", "Multi Table"])
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:

    if option == "Single Table":
        df = pd.read_excel(uploaded_file)

        st.subheader("Uploaded Data")
        st.dataframe(df)

        if st.button("Generate Synthetic Data"):
            synthetic = generate_single_table_synthetic(df)

            st.subheader("Synthetic Output")
            st.dataframe(synthetic)

            st.download_button(
                "Download Synthetic Excel",
                synthetic.to_excel("synthetic.xlsx", index=False),
                file_name="synthetic.xlsx"
            )

    else:  # Multi-table
        xls = pd.ExcelFile(uploaded_file)
        tables = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

        st.subheader("Uploaded Tables")
        for name, df in tables.items():
            st.write(f"### {name}")
            st.dataframe(df)

        if st.button("Generate Synthetic Multi-Table Data"):
            synthetic_tables = generate_multi_table_synthetic(tables)

            st.subheader("Synthetic Tables Output")
            for name, df in synthetic_tables.items():
                st.write(f"### {name}")
                st.dataframe(df)
                st.download_button(
                    f"Download {name} Synthetic",
                    df.to_excel(f"{name}_synthetic.xlsx", index=False),
                    file_name=f"{name}_synthetic.xlsx"
                )
