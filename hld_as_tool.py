# -*- coding: utf-8 -*-
"""HLD_AS tool.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_6v0HYyraqTCCjhM8PvdtFypVCdBoD1f
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO

# Streamlit Interface for Data Analysis
st.title("Data Analysis and Visualization Tool")

# File Upload
uploaded_file = st.file_uploader("Upload your data file (CSV or XLSX)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Load the data
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or XLSX file.")

        st.success("File uploaded and data loaded successfully!")

        # Data Summarization
        st.header("Data Summarization")

        st.subheader("Descriptive Statistics")
        st.write(df.describe())

        st.subheader("General Info")
        buffer = StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        # Data Querying
        st.header("Data Querying")

        st.subheader("Column-based Filters")
        column = st.selectbox("Select column to filter", options=df.columns)
        unique_values = df[column].unique() if column else []
        selected_values = st.multiselect("Select values to filter", options=unique_values)

        filtered_df = df[df[column].isin(selected_values)] if selected_values else df
        st.write("Filtered Data", filtered_df)

        st.subheader("Row-based Filters")
        row_start = st.number_input("Start Row", min_value=0, max_value=len(df)-1, step=1)
        row_end = st.number_input("End Row", min_value=row_start, max_value=len(df), step=1, value=len(df))

        if row_start < row_end:
            filtered_df = filtered_df.iloc[row_start:row_end]
            st.write("Filtered Data by Rows", filtered_df)
        else:
            st.warning("Ensure that start row is less than end row.")

        # Data Visualization
        st.header("Data Visualization")

        st.subheader("Plot Distribution")
        numeric_columns = df.select_dtypes(include=['number']).columns
        if not numeric_columns.empty:
            dist_column = st.selectbox("Select column for distribution plot", options=numeric_columns)
            bins = st.slider("Number of bins", min_value=5, max_value=50, value=20, step=1)
            color = st.color_picker("Pick a color", value="#4CAF50")

            if dist_column:
                fig, ax = plt.subplots()
                filtered_df[dist_column].plot(kind='hist', bins=bins, color=color, ax=ax, alpha=0.7)
                ax.set_title(f"Distribution of {dist_column}")
                ax.set_xlabel(dist_column)
                ax.set_ylabel("Frequency")
                st.pyplot(fig)
                plt.close(fig)
        else:
            st.warning("No numeric columns available for distribution plot.")

        st.subheader("Plot Trend")
        if len(numeric_columns) > 0:
            time_column = st.selectbox("Select time column", options=df.columns)
            value_column = st.selectbox("Select value column", options=numeric_columns)

            if time_column and value_column:
                try:
                    df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
                    df = df.dropna(subset=[time_column, value_column])
                    sorted_df = df.sort_values(time_column)

                    fig, ax = plt.subplots()
                    ax.plot(sorted_df[time_column], sorted_df[value_column], marker='o', linestyle='-', color=color)
                    ax.set_title(f"Trend of {value_column} over {time_column}")
                    ax.set_xlabel(time_column)
                    ax.set_ylabel(value_column)
                    st.pyplot(fig)
                    plt.close(fig)
                except Exception as e:
                    st.error(f"Error in plotting trend: {e}")
        else:
            st.warning("No suitable columns available for trend plot.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a file to proceed.")
