# Care-Transition-Analytics
Data-driven analysis of the HHS Unaccompanied Alien Children (UAC) Program, focusing on care transitions, transfer efficiency, discharge outcomes, placement performance, bottlenecks, and outcome stability.
# Care Transition Efficiency & Placement Outcome Analytics

## Project Overview

This project analyzes the HHS Unaccompanied Alien Children (UAC) Program dataset to evaluate how effectively children move through the care pipeline, from initial transfer from Customs and Border Protection (CBP) custody through HHS care and eventual discharge.

The project reframes the dataset from a simple capacity-monitoring perspective into a process-efficiency and outcome-analysis framework.

The analysis focuses on:

- Transfer efficiency
- Discharge effectiveness
- Placement outcomes
- Pipeline throughput
- Backlog accumulation
- Reunification outcomes
- Outcome stability
- Identification of potential process bottlenecks

## Objectives

The major objectives of this project are:

1. Analyze the movement of children through the HHS care pipeline.
2. Evaluate transfer and discharge efficiency.
3. Identify delays and potential bottlenecks.
4. Examine placement and reunification outcomes.
5. Measure consistency and stability of outcomes.
6. Develop actionable insights that can support process improvement.
7. Present the findings through an interactive Streamlit dashboard.

## Key Performance Indicators

### 1. Transfer Efficiency Ratio
Measures the efficiency and speed of movement from CBP custody to HHS care.

### 2. Discharge Effectiveness Index
Evaluates successful discharge and placement outcomes.

### 3. Pipeline Throughput
Measures the overall movement of children through the care system.

### 4. Backlog Accumulation Rate
Helps identify periods associated with increasing delays or unresolved cases.

### 5. Outcome Stability Score
Measures consistency in placement and discharge outcomes over time.

## Dashboard Features

The Streamlit dashboard provides:

- Care pipeline visualization
- Transfer and discharge efficiency analysis
- Placement outcome analysis
- Bottleneck detection
- Outcome trend analysis
- Date-range filtering
- Ratio-based metric views
- Visual threshold alerts
- Interactive charts and summary indicators

## Dataset

The project uses the HHS Unaccompanied Alien Children Program dataset.

The dataset contains information related to children entering and moving through the Office of Refugee Resettlement care system.

Source:

https://healthdata.gov/National/HHS-Unaccompanied-Alien-Children-Program/ehpz-xc9n

## Methodology

The analysis follows these major stages:

1. Data loading
2. Data cleaning
3. Data validation
4. Exploratory data analysis
5. KPI construction
6. Trend analysis
7. Bottleneck identification
8. Outcome stability analysis
9. Dashboard development
10. Recommendations

## Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Jupyter Notebook
- GitHub

## Project Structure

```text
Care-Transition-Analytics/
│
├── app.py
├── HHS_UAC_cleaned.csv
├── requirements.txt
├── README.md
│
├── Care_Transition_Analytics_FINAL_Report_CLEAN.pdf
├── Care_Transition_Analytics_FINAL_Report_CLEAN.docx
├── Executive_Summary_FINAL.docx
│
├── VIDEO_SCRIPT.md
│
└── figures/
    ├── ...
