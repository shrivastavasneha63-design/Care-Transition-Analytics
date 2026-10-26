import streamlit as st
import pandas as pd
import os

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("Care Transition Analytics")
st.subheader("HHS Unaccompanied Alien Children (UAC) Program")

st.write(
    "This dashboard provides data-driven analysis of care transitions, "
    "transfers, discharge outcomes, placement performance, bottlenecks, "
    "and outcome stability."
)

# ---------------------------------------------------------
# FIND CSV FILE
# ---------------------------------------------------------
csv_file = "HHS_Unaccompanied_Alien_Children_Program(1).csv"

if not os.path.exists(csv_file):
    st.error(f"Dataset file not found: {csv_file}")
    st.write("Files available in the application folder:")
    st.write(os.listdir("."))
    st.stop()
# ---------------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------------
try:

    df = pd.read_csv(csv_file)

    st.success("Dataset loaded successfully.")

    # -----------------------------------------------------
    # BASIC CLEANING
    # -----------------------------------------------------
    df.columns = df.columns.astype(str).str.strip()

    # -----------------------------------------------------
    # DATASET OVERVIEW
    # -----------------------------------------------------
    st.header("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Records",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "Total Columns",
            f"{len(df.columns):,}"
        )

    with col3:
        st.metric(
            "Missing Values",
            f"{int(df.isna().sum().sum()):,}"
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            f"{int(df.duplicated().sum()):,}"
        )

    # -----------------------------------------------------
    # DATA PREVIEW
    # -----------------------------------------------------
    st.header("📋 Data Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    # -----------------------------------------------------
    # COLUMN INFORMATION
    # -----------------------------------------------------
    st.header("🔎 Data Structure")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isna().sum().values,
        "Unique Values": [
            df[col].nunique(dropna=True)
            for col in df.columns
        ]
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )

    # -----------------------------------------------------
    # MISSING DATA ANALYSIS
    # -----------------------------------------------------
    st.header("⚠️ Missing Data Analysis")

    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(
        ascending=False
    )

    if len(missing) > 0:

        missing_df = pd.DataFrame({
            "Column": missing.index,
            "Missing Values": missing.values
        })

        st.dataframe(
            missing_df,
            use_container_width=True
        )

        st.bar_chart(
            missing_df.set_index("Column")
        )

    else:
        st.success(
            "No missing values were detected in the dataset."
        )

    # -----------------------------------------------------
    # NUMERIC VARIABLES
    # -----------------------------------------------------
    st.header("📈 Numeric Analysis")

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        selected_numeric = st.selectbox(
            "Select a numeric variable",
            numeric_columns
        )

        st.subheader(
            f"Distribution of {selected_numeric}"
        )

        st.bar_chart(
            df[selected_numeric].value_counts()
            .sort_index()
        )

        st.subheader(
            f"Trend of {selected_numeric}"
        )

        st.line_chart(
            df[selected_numeric]
        )

    else:

        st.info(
            "No numeric variables were detected."
        )

    # -----------------------------------------------------
    # CATEGORICAL ANALYSIS
    # -----------------------------------------------------
    st.header("📊 Categorical Analysis")

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    if categorical_columns:

        selected_category = st.selectbox(
            "Select a categorical variable",
            categorical_columns
        )

        category_counts = (
            df[selected_category]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(10)
        )

        category_chart = pd.DataFrame({
            "Category": category_counts.index,
            "Count": category_counts.values
        })

        st.subheader(
            f"Distribution of {selected_category}"
        )

        st.bar_chart(
            category_chart.set_index("Category")
        )

        st.dataframe(
            category_chart,
            use_container_width=True
        )

    else:

        st.info(
            "No categorical variables were detected."
        )

    # -----------------------------------------------------
    # DATASET STATISTICS
    # -----------------------------------------------------
    st.header("📐 Dataset Statistics")

    try:

        statistics = df.describe(
            include="all"
        ).T

        st.dataframe(
            statistics,
            use_container_width=True
        )

    except Exception:

        st.info(
            "Detailed statistics could not be generated "
            "for all variables."
        )

    # -----------------------------------------------------
    # KEY INSIGHTS
    # -----------------------------------------------------
    st.header("💡 Key Insights")

    st.write(
        f"""
        - The dataset contains **{len(df):,} records**.
        - The dataset contains **{len(df.columns):,} variables**.
        - There are **{int(df.isna().sum().sum()):,} missing values**.
        - There are **{int(df.duplicated().sum()):,} duplicate rows**.
        """
    )

    if numeric_columns:

        st.subheader("Numeric Variables Identified")

        st.write(
            ", ".join(numeric_columns)
        )

    if categorical_columns:

        st.subheader("Categorical Variables Identified")

        st.write(
            ", ".join(categorical_columns)
        )

    # -----------------------------------------------------
    # CARE TRANSITION / OUTCOME SECTION
    # -----------------------------------------------------
    st.header("🏥 Care Transition & Outcome Analysis")

    st.write(
        "The following interactive analysis allows exploration "
        "of variables related to transfers, placements, "
        "discharges, and other care-transition outcomes."
    )

    if categorical_columns:

        outcome_column = st.selectbox(
            "Choose a variable for outcome analysis",
            categorical_columns,
            key="outcome_column"
        )

        outcome_counts = (
            df[outcome_column]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(10)
        )

        outcome_df = pd.DataFrame({
            "Outcome": outcome_counts.index,
            "Number of Records": outcome_counts.values
        })

        st.bar_chart(
            outcome_df.set_index("Outcome")
        )

        st.dataframe(
            outcome_df,
            use_container_width=True
        )

    # -----------------------------------------------------
    # DOWNLOAD CLEAN DATA
    # -----------------------------------------------------
    st.header("⬇️ Download Dataset")

    csv_download = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv_download,
        file_name="HHS_UAC_Analyzed.csv",
        mime="text/csv"
    )

    # -----------------------------------------------------
    # CONCLUSION
    # -----------------------------------------------------
    st.header("📝 Conclusion")

    st.write(
        "The dashboard provides an interactive overview of the "
        "HHS Unaccompanied Alien Children (UAC) dataset. It "
        "examines dataset structure, missing data, numerical "
        "patterns, categorical distributions, and variables "
        "relevant to care transitions, transfers, discharge "
        "outcomes, placement performance, and operational "
        "bottlenecks."
    )

except Exception as e:

    st.error(
        "The application could not read the dataset."
    )

    st.exception(e)
