import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Care Transition Analytics")
st.subheader("HHS Unaccompanied Alien Children (UAC) Program")

st.write(
    "This dashboard provides data-driven analysis of care transitions, "
    "transfers, discharge outcomes, placement performance, bottlenecks, "
    "and outcome stability."
)

# Find CSV file
csv_files = [f for f in os.listdir(".") if f.lower().endswith(".csv")]

if not csv_files:
    st.warning("No CSV dataset found in the repository.")
    st.info("Please upload the project CSV file to the GitHub repository.")
    st.stop()

csv_file = csv_files[0]

try:
    df = pd.read_csv(csv_file)

    st.success("Dataset loaded successfully.")

    st.header("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", len(df))

    with col2:
        st.metric("Total Columns", len(df.columns))

    with col3:
        st.metric("Missing Values", int(df.isna().sum().sum()))

    st.header("Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.header("Key Insights")

    st.write("### Dataset Statistics")
    st.dataframe(df.describe(include="all").T, use_container_width=True)

    st.write("### Missing Data Analysis")

    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if len(missing) > 0:
        st.bar_chart(missing)
    else:
        st.success("No missing values were detected.")

    st.write("### Numeric Variables")

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if numeric_columns:
        selected_column = st.selectbox(
            "Select a numeric variable",
            numeric_columns
        )

        st.line_chart(df[selected_column])
    else:
        st.info("No numeric variables were found.")

    st.header("Conclusion")

    st.write(
        "The analysis provides an overview of the available UAC program "
        "data and highlights patterns related to care transitions, "
        "transfers, discharge outcomes, placement performance, and "
        "potential operational bottlenecks."
    )

except Exception as e:
    st.error("The application could not read the dataset.")
    st.exception(e)
