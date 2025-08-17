"""
Web Interface using Streamlit.

This app loads an Excel file (default or uploaded), displays its sheets in tabs,
allows filtering on columns, and styles the display.

Rules:
- Follows PEP8 style.
- Includes docstrings for all functions.
- Applies pylint recommended conventions.
"""
# pylint: disable=C0114,C0103,R0914,R0915,C0411,E1120,C0301

import streamlit as st
import pandas as pd
import click
import subprocess
import os

# pd.set_option("io.excel.xlsx.writer", "openpyxl")
# pd.options.mode.use_inf_as_na = True  # pour la compatibilité NaN/inf

# try:
#     import pyarrow
#     pd.options.io.excel.engine = "openpyxl"
# except ImportError:
#     pass


@click.command()
@click.argument("xls_file", default="file.xlsx")
def run_app(xls_file):
    """
    Run the Streamlit app with the given Excel file as argument.
    """
    # Pass the Excel file path via an environment variable
    env = {"STREAMLIT_XLS_FILE": xls_file}
    full_env = os.environ.copy()
    full_env.update(env)
    subprocess.run(
        ["streamlit", "run", "app.py"],
        env=full_env,
        check=True,
    )

def main():
    """
    Main Streamlit application logic.
    """
    st.set_page_config(
        page_title="DATA Web Interface",
        page_icon=":gear:",
        layout="wide"
    )

    st.image("resources/logo.jpg", width=150)
    st.title("DATA Web Interface")

    DEFAULT_FILE = "file.xlsx"
    xls_file = os.environ.get("STREAMLIT_XLS_FILE", DEFAULT_FILE)
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    def clean_dataframe(df):
        """
        Clean the dataframe by removing columns starting with 'Unnamed'
        and replacing NaN/None values with '--'.
        """
        return df.fillna("--")

    def style_first_col_and_header(df):
        """
        Style the dataframe to highlight the first column with a green background
        and the header with a blue background.
        """
        styled = df.style.apply(
            lambda x: ['background-color: lightgreen' if x.name == df.columns[0] else '' for _ in x],
            axis=1
        ).set_table_styles(
            [{'selector': 'th', 'props': [('background-color', 'lightblue')]}]
        )
        return styled

    if uploaded_file:
        main_df = pd.read_excel(uploaded_file, engine='openpyxl')
        FILE_FOR_SHEETS = uploaded_file
    else:
        try:
            main_df = pd.read_excel(xls_file, engine='openpyxl')
            st.info(f"File loaded: {xls_file}")
            FILE_FOR_SHEETS = xls_file
        except (FileNotFoundError, ValueError) as err:
            st.error(f"Error loading file: {err}")
            main_df = None
            FILE_FOR_SHEETS = None

    if main_df is not None and FILE_FOR_SHEETS is not None:
        try:
            xls = pd.ExcelFile(FILE_FOR_SHEETS, engine='openpyxl')
            sheet_names = xls.sheet_names
        except (FileNotFoundError, ValueError) as err:
            st.error(f"Error reading sheets: {err}")
            sheet_names = []

        if sheet_names:
            tabs = st.tabs(sheet_names)
            for i, sheet in enumerate(sheet_names):
                with tabs[i]:
                    sheet_df = pd.read_excel(xls, sheet_name=sheet)
                    sheet_df = clean_dataframe(sheet_df)
                    st.subheader(f"Data Preview - {sheet}")
                    st.dataframe(
                        style_first_col_and_header(sheet_df),
                        use_container_width=True
                    )

                    columns = sheet_df.columns.tolist()
                    selected_column = st.selectbox(
                        f"Select a column to filter ({sheet})", columns, key=f"col_{sheet}"
                    )
                    filter_value = st.text_input(
                        f"Filter {selected_column} by value ({sheet})", key=f"filter_{sheet}"
                    )

                    if filter_value:
                        filtered_df = sheet_df[
                            sheet_df[selected_column].astype(str).str.contains(
                                filter_value, case=False, na=False
                            )
                        ]
                        st.subheader("Filtered Results")
                        st.dataframe(
                            style_first_col_and_header(filtered_df),
                            use_container_width=True
                        )
        else:
            st.subheader("Data Preview")
            st.dataframe(
                style_first_col_and_header(main_df),
                use_container_width=True
            )

            columns = main_df.columns.tolist()
            selected_column = st.selectbox("Select a column to filter", columns)
            filter_value = st.text_input(f"Filter {selected_column} by value")

            if filter_value:
                filtered_df = main_df[
                    main_df[selected_column].astype(str).str.contains(
                        filter_value, case=False, na=False
                    )
                ]
                st.subheader("Filtered Results")
                st.dataframe(
                    style_first_col_and_header(filtered_df),
                    use_container_width=True
                )

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1].endswith(".xlsx"):
        run_app()
    else:
        main()
