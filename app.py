import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
st.markdown(
    """
    **HHS Unaccompanied Alien Children (UAC) Program**

    Data-driven analysis of care transitions, transfer efficiency,
    discharge outcomes, placement performance, bottlenecks and
    outcome stability.
    """
)

st.divider()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    possible_files = [
        "HHS_Unaccompanied_Alien_Children_Program.csv",
        "HHS_Unaccompanied_Alien_Children_Program(1).csv",
        "HHS_Unaccompanied_Alien_Children_Program%281%29.csv",
        "data/HHS_Unaccompanied_Alien_Children_Program.csv"
    ]

    for file in possible_files:
        try:
            return pd.read_csv(file)
        except:
            pass

    return None


df = load_data()

# ---------------------------------------------------------
# DATA UPLOAD FALLBACK
# ---------------------------------------------------------
if df is None:

    st.warning(
        "The dataset was not found automatically. "
        "Please upload the CSV file below."
    )

    uploaded_file = st.file_uploader(
        "Upload HHS UAC dataset",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

    else:
        st.info(
            "Upload the HHS UAC CSV dataset to activate the dashboard."
        )
        st.stop()

# ---------------------------------------------------------
# BASIC CLEANING
# ---------------------------------------------------------
df.columns = [
    str(col).strip().replace(" ", "_").replace("-", "_")
    for col in df.columns
]

# Remove completely empty rows/columns
df = df.dropna(axis=0, how="all")
df = df.dropna(axis=1, how="all")

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("Dashboard Controls")

st.sidebar.write(
    f"**Records:** {len(df):,}"
)

st.sidebar.write(
    f"**Variables:** {len(df.columns):,}"
)

# Date column detection
date_columns = []

for col in df.columns:
    if "date" in col.lower():
        date_columns.append(col)

selected_date = None

if date_columns:

    selected_date = st.sidebar.selectbox(
        "Select date variable",
        date_columns
    )

    try:
        df[selected_date] = pd.to_datetime(
            df[selected_date],
            errors="coerce"
        )

        valid_dates = df[selected_date].dropna()

        if len(valid_dates) > 0:

            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()

            date_range = st.sidebar.date_input(
                "Date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            if isinstance(date_range, tuple) and len(date_range) == 2:

                start_date, end_date = date_range

                filtered_df = df[
                    (df[selected_date].dt.date >= start_date)
                    &
                    (df[selected_date].dt.date <= end_date)
                ]

            else:
                filtered_df = df.copy()

        else:
            filtered_df = df.copy()

    except:
        filtered_df = df.copy()

else:
    filtered_df = df.copy()

# ---------------------------------------------------------
# DATA OVERVIEW
# ---------------------------------------------------------
st.header("1. Data Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Total Variables",
        f"{len(filtered_df.columns):,}"
    )

with col3:
    missing_values = int(
        filtered_df.isna().sum().sum()
    )

    st.metric(
        "Missing Values",
        f"{missing_values:,}"
    )

with col4:
    duplicate_rows = int(
        filtered_df.duplicated().sum()
    )

    st.metric(
        "Duplicate Rows",
        f"{duplicate_rows:,}"
    )

# ---------------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------------
with st.expander("View dataset"):

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )

# ---------------------------------------------------------
# NUMERIC VARIABLES
# ---------------------------------------------------------
numeric_columns = filtered_df.select_dtypes(
    include=np.number
).columns.tolist()

# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

def calculate_ratio(numerator, denominator):

    if denominator == 0:
        return 0

    return (numerator / denominator) * 100


# Transfer-related columns
transfer_columns = [
    col for col in filtered_df.columns
    if "transfer" in col.lower()
]

discharge_columns = [
    col for col in filtered_df.columns
    if "discharge" in col.lower()
]

placement_columns = [
    col for col in filtered_df.columns
    if "placement" in col.lower()
]

reunification_columns = [
    col for col in filtered_df.columns
    if "reunif" in col.lower()
]

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------
st.header("2. Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# KPI 1
with kpi1:

    if transfer_columns:
        value = filtered_df[transfer_columns[0]].notna().sum()
    else:
        value = len(filtered_df)

    st.metric(
        "Transfer Activity",
        f"{value:,}"
    )

# KPI 2
with kpi2:

    if discharge_columns:
        value = filtered_df[discharge_columns[0]].notna().sum()
    else:
        value = 0

    st.metric(
        "Discharge Activity",
        f"{value:,}"
    )

# KPI 3
with kpi3:

    if placement_columns:
        value = filtered_df[placement_columns[0]].notna().sum()
    else:
        value = 0

    st.metric(
        "Placement Activity",
        f"{value:,}"
    )

# KPI 4
with kpi4:

    if reunification_columns:
        value = filtered_df[reunification_columns[0]].notna().sum()
    else:
        value = 0

    st.metric(
        "Reunification Activity",
        f"{value:,}"
    )

# ---------------------------------------------------------
# TRANSFER / DISCHARGE ANALYSIS
# ---------------------------------------------------------
st.header("3. Care Transition Analysis")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Transfer Variables")

    if transfer_columns:

        transfer_summary = pd.DataFrame({
            "Variable": transfer_columns,
            "Non-Missing Records": [
                filtered_df[c].notna().sum()
                for c in transfer_columns
            ]
        })

        st.dataframe(
            transfer_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No transfer-specific variable was automatically identified."
        )


with col2:

    st.subheader("Discharge Variables")

    if discharge_columns:

        discharge_summary = pd.DataFrame({
            "Variable": discharge_columns,
            "Non-Missing Records": [
                filtered_df[c].notna().sum()
                for c in discharge_columns
            ]
        })

        st.dataframe(
            discharge_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No discharge-specific variable was automatically identified."
        )

# ---------------------------------------------------------
# PLACEMENT ANALYSIS
# ---------------------------------------------------------
st.header("4. Placement Outcome Analysis")

if placement_columns:

    selected_placement = st.selectbox(
        "Select placement variable",
        placement_columns
    )

    placement_counts = (
        filtered_df[selected_placement]
        .value_counts(dropna=False)
        .head(15)
    )

    if len(placement_counts) > 0:

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        placement_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Placement Outcome Distribution"
        )

        ax.set_xlabel(
            "Placement Category"
        )

        ax.set_ylabel(
            "Number of Records"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        st.pyplot(fig)

else:

    st.info(
        "No placement variable was automatically identified."
    )

# ---------------------------------------------------------
# NUMERIC ANALYSIS
# ---------------------------------------------------------
st.header("5. Numerical Performance Analysis")

if numeric_columns:

    selected_numeric = st.selectbox(
        "Select numerical variable",
        numeric_columns
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Average",
            f"{filtered_df[selected_numeric].mean():.2f}"
        )

    with col2:

        st.metric(
            "Median",
            f"{filtered_df[selected_numeric].median():.2f}"
        )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    filtered_df[selected_numeric].dropna().plot(
        kind="hist",
        bins=20,
        ax=ax
    )

    ax.set_title(
        f"Distribution of {selected_numeric}"
    )

    ax.set_xlabel(
        selected_numeric
    )

    ax.set_ylabel(
        "Frequency"
    )

    plt.tight_layout()

    st.pyplot(fig)

else:

    st.info(
        "No numerical variables were detected in the dataset."
    )

# ---------------------------------------------------------
# MISSING DATA / DATA QUALITY
# ---------------------------------------------------------
st.header("6. Data Quality Analysis")

missing = (
    filtered_df.isna()
    .sum()
    .sort_values(ascending=False)
)

missing = missing[missing > 0]

if len(missing) > 0:

    missing_percentage = (
        missing / len(filtered_df) * 100
    )

    missing_table = pd.DataFrame({
        "Missing Records": missing,
        "Missing Percentage": missing_percentage.round(2)
    })

    st.dataframe(
        missing_table,
        use_container_width=True
    )

else:

    st.success(
        "No missing values detected in the filtered dataset."
    )

# ---------------------------------------------------------
# BOTTLENECK DETECTION
# ---------------------------------------------------------
st.header("7. Bottleneck Detection")

bott
