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
st.title("📊 Care Transition Analytics")
st.subheader("HHS Unaccompanied Alien Children (UAC) Program")

st.write(
    "This dashboard provides a data-driven analysis of care transitions, "
    "CBP custody, transfers, HHS care, discharges, trends, and operational "
    "patterns within the HHS Unaccompanied Alien Children (UAC) program."
)

# ---------------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------------

csv_file = "HHS_Unaccompanied_Alien_Children_Program.csv"

if not os.path.exists(csv_file):

    # Try alternative filename if present
    alternative = "HHS_Unaccompanied_Alien_Children_Program(1).csv"

    if os.path.exists(alternative):
        csv_file = alternative
    else:
        st.error(
            "Dataset not found. Please make sure the correct CSV file "
            "is uploaded to the GitHub repository."
        )
        st.stop()

try:

    df = pd.read_csv(csv_file)

except Exception as e:

    st.error("The CSV file could not be read.")
    st.exception(e)
    st.stop()


# ---------------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------------

df.columns = df.columns.str.strip()

# Convert date column
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

# ---------------------------------------------------------
# REMOVE COMPLETELY EMPTY ROWS
# ---------------------------------------------------------

before_rows = len(df)

df = df.dropna(how="all").copy()

removed_rows = before_rows - len(df)

# ---------------------------------------------------------
# IDENTIFY NUMERIC COLUMNS
# ---------------------------------------------------------

numeric_columns = [
    "Children apprehended and placed in CBP custody*",
    "Children in CBP custody",
    "Children transferred out of CBP custody",
    "Children in HHS Care",
    "Children discharged from HHS Care"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# Sort chronologically
if "Date" in df.columns:
    df = df.sort_values("Date")


# ---------------------------------------------------------
# SUCCESS MESSAGE
# ---------------------------------------------------------

st.success(
    f"Dataset loaded successfully. {len(df):,} usable records available."
)

if removed_rows > 0:
    st.info(
        f"{removed_rows:,} completely blank rows were removed before analysis."
    )


# =========================================================
# DATASET OVERVIEW
# =========================================================

st.header("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Total Variables",
        len(df.columns)
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


# =========================================================
# DATA PREVIEW
# =========================================================

st.header("📋 Data Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)


# =========================================================
# DATA STRUCTURE
# =========================================================

st.header("🔎 Data Structure")

structure = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isna().sum().values,
    "Unique Values": df.nunique().values
})

st.dataframe(
    structure,
    use_container_width=True
)


# =========================================================
# KEY INSIGHTS
# =========================================================

st.header("💡 Key Insights")

if "Date" in df.columns:

    valid_dates = df["Date"].dropna()

    if len(valid_dates) > 0:

        st.write(
            f"• The dataset covers **{valid_dates.min().strftime('%B %d, %Y')} "
            f"to {valid_dates.max().strftime('%B %d, %Y')}**."
        )

st.write(
    f"• The cleaned dataset contains **{len(df):,} records**."
)

st.write(
    f"• The dataset contains **{len(df.columns)} variables**."
)

st.write(
    f"• There are **{int(df.isna().sum().sum()):,} missing values** "
    "across all variables."
)

st.write(
    f"• There are **{int(df.duplicated().sum()):,} duplicate rows**."
)


# =========================================================
# CARE TRANSITION ANALYSIS
# =========================================================

st.header("🏥 Care Transition & Outcome Analysis")

st.write(
    "The following visualizations examine movement through the UAC "
    "care pathway, including CBP custody, transfers, HHS care, "
    "and discharge."
)


# ---------------------------------------------------------
# PREPARE DATA FOR CHARTS
# ---------------------------------------------------------

available_numeric = [
    column
    for column in numeric_columns
    if column in df.columns
]


# =========================================================
# TOTALS
# =========================================================

st.subheader("📊 Overall Program Activity")

if available_numeric:

    totals = df[available_numeric].sum(
        numeric_only=True
    ).sort_values(
        ascending=False
    )

    totals_display = totals.rename(
        lambda x: x.replace(
            "Children ", ""
        )
    )

    st.bar_chart(
        totals_display
    )


# =========================================================
# DAILY TRENDS
# =========================================================

if "Date" in df.columns and available_numeric:

    st.subheader("📈 Care Transition Trends Over Time")

    chart_df = df[
        ["Date"] + available_numeric
    ].dropna(
        subset=["Date"]
    )

    chart_df = chart_df.set_index("Date")

    st.line_chart(
        chart_df,
        use_container_width=True
    )


# =========================================================
# CBP CUSTODY ANALYSIS
# =========================================================

st.subheader("👥 CBP Custody Analysis")

cbp_columns = [
    column
    for column in [
        "Children apprehended and placed in CBP custody*",
        "Children in CBP custody",
        "Children transferred out of CBP custody"
    ]
    if column in df.columns
]

if cbp_columns:

    cbp_df = df[cbp_columns].sum().sort_values(
        ascending=False
    )

    st.bar_chart(
        cbp_df,
        use_container_width=True
    )


# =========================================================
# HHS CARE ANALYSIS
# =========================================================

st.subheader("🏥 HHS Care & Discharge Analysis")

hhs_columns = [
    column
    for column in [
        "Children in HHS Care",
        "Children discharged from HHS Care"
    ]
    if column in df.columns
]

if hhs_columns:

    hhs_df = df[hhs_columns].sum()

    st.bar_chart(
        hhs_df,
        use_container_width=True
    )


# =========================================================
# DISCHARGE TREND
# =========================================================

if (
    "Date" in df.columns
    and "Children discharged from HHS Care" in df.columns
):

    st.subheader("📤 HHS Discharge Trend")

    discharge_df = df[
        [
            "Date",
            "Children discharged from HHS Care"
        ]
    ].dropna(
        subset=["Date"]
    )

    discharge_df = discharge_df.set_index(
        "Date"
    )

    st.line_chart(
        discharge_df,
        use_container_width=True
    )


# =========================================================
# TRANSFER TREND
# =========================================================

if (
    "Date" in df.columns
    and "Children transferred out of CBP custody" in df.columns
):

    st.subheader("🔄 Transfer Out of CBP Custody")

    transfer_df = df[
        [
            "Date",
            "Children transferred out of CBP custody"
        ]
    ].dropna(
        subset=["Date"]
    )

    transfer_df = transfer_df.set_index(
        "Date"
    )

    st.area_chart(
        transfer_df,
        use_container_width=True
    )


# =========================================================
# MISSING DATA ANALYSIS
# =========================================================

st.header("⚠️ Missing Data Analysis")

missing = df.isna().sum()

missing = missing[
    missing > 0
].sort_values(
    ascending=False
)

if len(missing) > 0:

    missing_table = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values,
        "Missing %": (
            missing.values / len(df) * 100
        ).round(2)
    })

    st.dataframe(
        missing_table,
        use_container_width=True
    )

    st.bar_chart(
        missing,
        use_container_width=True
    )

else:

    st.success(
        "No missing values were detected."
    )


# =========================================================
# SUMMARY TABLE
# =========================================================

st.header("📊 Summary Statistics")

if available_numeric:

    summary = df[
        available_numeric
    ].describe().T

    summary = summary.rename(
        columns={
            "count": "Count",
            "mean": "Mean",
            "std": "Standard Deviation",
            "min": "Minimum",
            "25%": "25th Percentile",
            "50%": "Median",
            "75%": "75th Percentile",
            "max": "Maximum"
        }
    )

    st.dataframe(
        summary.round(2),
        use_container_width=True
    )


# =========================================================
# DOWNLOAD CLEANED DATASET
# =========================================================

st.header("⬇️ Download Cleaned Dataset")

csv_output = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Cleaned CSV",
    data=csv_output,
    file_name="HHS_UAC_cleaned.csv",
    mime="text/csv"
)


# =========================================================
# CONCLUSION
# =========================================================

st.header("📝 Conclusion")

st.write(
    "The dashboard provides an interactive overview of the HHS "
    "Unaccompanied Alien Children (UAC) dataset. The analysis "
    "examines movement through CBP custody, transfers into and "
    "through HHS care, discharge activity, temporal trends, "
    "and data completeness. These visualizations can help "
    "identify patterns in care transitions and potential "
    "operational bottlenecks."
)

st.success(
    "Dashboard analysis completed successfully."
)
