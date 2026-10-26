import streamlit as st
import pandas as pd
import os

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================
st.title("📊 Care Transition Analytics")
st.subheader("HHS Unaccompanied Alien Children (UAC) Program")

st.write(
    "An interactive dashboard for exploring care transitions, "
    "CBP custody, transfers, HHS care, and discharge activity "
    "within the HHS Unaccompanied Alien Children (UAC) Program."
)

# =========================================================
# FIND THE CORRECT DATASET
# =========================================================

possible_files = [
    "HHS_Unaccompanied_Alien_Children_Program.csv",
    "HHS_Unaccompanied_Alien_Children_Program(1).csv",
    "HHS_UAC_cleaned.csv"
]

csv_file = None

for file in possible_files:
    if os.path.exists(file):
        csv_file = file
        break

if csv_file is None:
    st.error("❌ UAC dataset was not found in the repository.")
    st.write("CSV files currently available:")

    available = [
        f for f in os.listdir(".")
        if f.lower().endswith(".csv")
    ]

    st.write(available)
    st.stop()

# =========================================================
# LOAD DATA
# =========================================================

try:
    df = pd.read_csv(csv_file)

except Exception as e:
    st.error("Unable to read the CSV dataset.")
    st.exception(e)
    st.stop()

# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)

# Remove completely empty rows
original_rows = len(df)

df = df.dropna(how="all").copy()

removed_rows = original_rows - len(df)

# =========================================================
# IDENTIFY DATE COLUMN
# =========================================================

date_column = None

for column in df.columns:

    if str(column).strip().lower() == "date":
        date_column = column
        break

if date_column:

    df[date_column] = pd.to_datetime(
        df[date_column],
        errors="coerce"
    )

# =========================================================
# IDENTIFY NUMERIC COLUMNS
# =========================================================

for column in df.columns:

    if column != date_column:

        converted = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        # Only replace the column if it contains
        # a reasonable amount of numeric data
        if converted.notna().sum() > 0:
            df[column] = converted

# =========================================================
# SUCCESS MESSAGE
# =========================================================

st.success(
    f"Dataset loaded successfully — {len(df):,} records."
)

if removed_rows > 0:
    st.info(
        f"{removed_rows:,} completely empty rows were removed."
    )

# =========================================================
# DATASET OVERVIEW
# =========================================================

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
    "Data Type": [
        str(df[column].dtype)
        for column in df.columns
    ],
    "Missing Values": [
        int(df[column].isna().sum())
        for column in df.columns
    ],
    "Unique Values": [
        int(df[column].nunique(dropna=True))
        for column in df.columns
    ]
})

st.dataframe(
    structure,
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
        "Missing Percentage": (
            missing.values / len(df) * 100
        ).round(2)
    })

    st.dataframe(
        missing_table,
        use_container_width=True
    )

    st.bar_chart(
        missing_table.set_index("Column")[
            "Missing Values"
        ]
    )

else:

    st.success(
        "No missing values were detected."
    )

# =========================================================
# NUMERIC VARIABLES
# =========================================================

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

# =========================================================
# PROGRAM ACTIVITY
# =========================================================

st.header("📈 Program Activity")

if numeric_columns:

    totals = (
        df[numeric_columns]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        totals,
        use_container_width=True
    )

    st.subheader("Program Activity Summary")

    totals_table = pd.DataFrame({
        "Indicator": totals.index,
        "Total": totals.values
    })

    st.dataframe(
        totals_table,
        use_container_width=True
    )

else:

    st.info(
        "No numeric variables were detected."
    )

# =========================================================
# TIME-BASED ANALYSIS
# =========================================================

if date_column and numeric_columns:

    st.header("📅 Trends Over Time")

    trend_data = df[
        [date_column] + numeric_columns
    ].copy()

    trend_data = trend_data.dropna(
        subset=[date_column]
    )

    trend_data = trend_data.sort_values(
        date_column
    )

    if not trend_data.empty:

        trend_data = trend_data.set_index(
            date_column
        )

        st.line_chart(
            trend_data,
            use_container_width=True
        )

# =========================================================
# SELECT INDICATOR
# =========================================================

st.header("🔍 Indicator Analysis")

if numeric_columns:

    selected_indicator = st.selectbox(
        "Select an indicator",
        numeric_columns
    )

    indicator_data = df[
        [date_column, selected_indicator]
    ].copy() if date_column else df[
        [selected_indicator]
    ].copy()

    if date_column:

        indicator_data = indicator_data.dropna(
            subset=[date_column]
        )

        indicator_data = indicator_data.sort_values(
            date_column
        )

        indicator_data = indicator_data.set_index(
            date_column
        )

    st.line_chart(
        indicator_data,
        use_container_width=True
    )

# =========================================================
# CBP CUSTODY ANALYSIS
# =========================================================

st.header("👥 CBP Custody Analysis")

cbp_keywords = [
    "apprehended",
    "cbp custody",
    "transferred out"
]

cbp_columns = [
    column
    for column in numeric_columns
    if any(
        keyword in column.lower()
        for keyword in cbp_keywords
    )
]

if cbp_columns:

    cbp_data = df[
        cbp_columns
    ].sum().sort_values(
        ascending=False
    )

    st.bar_chart(
        cbp_data,
        use_container_width=True
    )

    st.dataframe(
        pd.DataFrame({
            "CBP Indicator": cbp_data.index,
            "Total": cbp_data.values
        }),
        use_container_width=True
    )

else:

    st.info(
        "No CBP-specific numeric indicators were detected."
    )

# =========================================================
# HHS CARE ANALYSIS
# =========================================================

st.header("🏥 HHS Care Analysis")

hhs_columns = [
    column
    for column in numeric_columns
    if "hhs" in column.lower()
]

if hhs_columns:

    hhs_data = df[
        hhs_columns
    ].sum().sort_values(
        ascending=False
    )

    st.bar_chart(
        hhs_data,
        use_container_width=True
    )

    st.dataframe(
        pd.DataFrame({
            "HHS Indicator": hhs_data.index,
            "Total": hhs_data.values
        }),
        use_container_width=True
    )

else:

    st.info(
        "No HHS-specific numeric indicators were detected."
    )

# =========================================================
# TRANSFER ANALYSIS
# =========================================================

transfer_columns = [
    column
    for column in numeric_columns
    if "transfer" in column.lower()
]

if transfer_columns:

    st.header("🔄 Transfer Analysis")

    transfer_data = df[
        transfer_columns
    ].sum().sort_values(
        ascending=False
    )

    st.bar_chart(
        transfer_data,
        use_container_width=True
    )

# =========================================================
# DISCHARGE ANALYSIS
# =========================================================

discharge_columns = [
    column
    for column in numeric_columns
    if "discharged" in column.lower()
]

if discharge_columns:

    st.header("📤 Discharge Analysis")

    discharge_data = df[
        discharge_columns
    ].sum().sort_values(
        ascending=False
    )

    st.bar_chart(
        discharge_data,
        use_container_width=True
    )

    st.dataframe(
        pd.DataFrame({
            "Discharge Indicator": discharge_data.index,
            "Total": discharge_data.values
        }),
        use_container_width=True
    )

# =========================================================
# STATISTICAL SUMMARY
# =========================================================

st.header("📐 Statistical Summary")

if numeric_columns:

    statistics = df[
        numeric_columns
    ].describe().T

    statistics = statistics.round(2)

    st.dataframe(
        statistics,
        use_container_width=True
    )

# =========================================================
# KEY INSIGHTS
# =========================================================

st.header("💡 Key Insights")

st.write(
    f"**1. Dataset size:** The dashboard contains "
    f"**{len(df):,} records** across "
    f"**{len(df.columns)} variables**."
)

st.write(
    f"**2. Data quality:** The dataset contains "
    f"**{int(df.isna().sum().sum()):,} missing values** "
    f"and **{int(df.duplicated().sum()):,} duplicate rows**."
)

if numeric_columns:

    highest_indicator = (
        df[numeric_columns]
        .sum()
        .idxmax()
    )

    highest_value = (
        df[numeric_columns]
        .sum()
        .max()
    )

    st.write(
        f"**3. Highest cumulative indicator:** "
        f"**{highest_indicator}** has the highest "
        f"cumulative recorded value "
        f"(**{highest_value:,.0f}**)."
    )

if date_column:

    valid_dates = df[date_column].dropna()

    if not valid_dates.empty:

        st.write(
            f"**4. Time coverage:** The available date "
            f"records span from **"
            f"{valid_dates.min().strftime('%d %b %Y')}** "
            f"to **"
            f"{valid_dates.max().strftime('%d %b %Y')}**."
        )

# =========================================================
# CONCLUSION
# =========================================================

st.header("📝 Conclusion")

st.write(
    "This dashboard provides an interactive analysis of the "
    "HHS Unaccompanied Alien Children (UAC) Program dataset. "
    "It examines program activity, CBP custody, transfers, "
    "HHS care, discharge activity, trends over time, and "
    "data quality. The visualizations allow users to explore "
    "patterns in care transitions and identify areas that may "
    "require further operational analysis."
)

# =========================================================
# DOWNLOAD
# =========================================================

st.header("⬇️ Download Analyzed Dataset")

download_data = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=download_data,
    file_name="HHS_UAC_Analyzed.csv",
    mime="text/csv"
)

st.success(
    "✅ Dashboard analysis completed successfully."
)
