import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from scripts.db_config import DB_CONFIG

st.set_page_config(page_title="JOSAA Data Portal", layout="wide")

@st.cache_data
def load_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT * FROM seat_allotment"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()
df["gender"] = df["gender"].astype(str).str.strip()

df["gender"] = df["gender"].replace({
    "Female-only (including Supernumerary)": "Female-only"
})

st.title("JOSAA Data Analysis Portal")
st.divider()
st.header("Rank Predictor")

col1, col2, col3, col4 = st.columns(4)

with col1:
    user_rank = st.number_input("Enter JEE Advanced Rank", min_value=1, step=1)

with col2:
    pred_year = st.selectbox("Use data from year", sorted(df["year"].unique(), reverse=True))

with col3:
    pred_seat_type = st.selectbox("Category", sorted(df["seat_type"].unique()))

with col4:
    pred_gender = st.selectbox("Gender", sorted(df["gender"].unique()))

branch_keyword = st.text_input(
    "Branch preference keyword",
    placeholder="Computer Science / Electrical / Mathematics / Mechanical"
)

predict_df = df[
    (df["year"] == pred_year) &
    (df["closing_rank"] >= user_rank)
]

predict_df = predict_df[
    predict_df["seat_type"] == pred_seat_type
]


if pred_gender == "Female-only":
    predict_df = predict_df[
        predict_df["gender"].str.contains("Female", case=False, na=False)
    ]
else:
    predict_df = predict_df[
        predict_df["gender"].str.contains("Gender-Neutral", case=False, na=False)
    ]

if branch_keyword:
    predict_df = predict_df[
        predict_df["academic_program"].str.contains(branch_keyword, case=False, na=False)
    ]

predict_df = (
    predict_df.sort_values("closing_rank")
    .drop_duplicates(subset=["institute", "academic_program"])
    .head(30)
)

if st.button("Find Possible Options"):
    st.subheader("Possible IIT + Branch Options")
    st.dataframe(
        predict_df[
            [
                "year",
                "round_no",
                "institute",
                "academic_program",
                "seat_type",
                "gender",
                "opening_rank",
                "closing_rank"
            ]
        ],
        use_container_width=True
    )
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Rank Predictor",
        "Branch Trends",
        "IIT Comparison",
        "Category Comparison",
        "Gender Comparison"
    ]
)


col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Years Covered", df["year"].nunique())
col3.metric("Institutes", df["institute"].nunique())
col4.metric("Programs", df["academic_program"].nunique())

st.sidebar.header("Filters")

year = st.sidebar.multiselect("Year", sorted(df["year"].unique()), default=sorted(df["year"].unique()))
seat_type = st.sidebar.multiselect("Seat Type", sorted(df["seat_type"].unique()), default=["OPEN"])
gender = st.sidebar.multiselect(
    "Gender",
    sorted(df["gender"].unique()),
    default=[sorted(df["gender"].unique())[0]]
)

filtered = df[
    (df["year"].isin(year)) &
    (df["seat_type"].isin(seat_type)) &
    (df["gender"].isin(gender))
]

st.subheader("Filtered Data")
st.dataframe(filtered.head(100))

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="josaa_filtered_data.csv",
    mime="text/csv"
)

st.subheader("Top 15 Most Competitive Programs")

top_programs = (
    filtered.groupby(["institute", "academic_program"])["closing_rank"]
    .min()
    .reset_index()
    .sort_values("closing_rank")
    .head(15)
)

fig = px.bar(
    top_programs,
    x="closing_rank",
    y="academic_program",
    color="institute",
    orientation="h",
    title="Top Programs by Best Closing Rank"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()
st.header("Top Institutes by Competitiveness")

iit_rankings = (
    filtered.groupby("institute")["closing_rank"]
    .min()
    .reset_index()
    .sort_values("closing_rank")
    .head(15)
)

fig_iit = px.bar(
    iit_rankings,
    x="closing_rank",
    y="institute",
    orientation="h",
    title="Top Institutes by Best Closing Rank"
)

st.plotly_chart(fig_iit, use_container_width=True)
st.divider()
st.header("Top Branches by Competitiveness")

branch_rankings = (
    filtered.groupby("academic_program")["closing_rank"]
    .min()
    .reset_index()
    .sort_values("closing_rank")
    .head(15)
)

fig_branch = px.bar(
    branch_rankings,
    x="closing_rank",
    y="academic_program",
    orientation="h",
    title="Most Competitive Branches"
)

st.plotly_chart(fig_branch, use_container_width=True)



st.divider()
st.header("Branch Trend Analysis")

branch_search = st.text_input(
    "Search branch for trend",
    placeholder="Computer Science / Electrical / Mathematics / Data Science"
)

trend_df = df[
    (df["seat_type"] == "OPEN") &
    (df["gender"].str.contains("Gender", case=False, na=False))
]

if branch_search:
    trend_df = trend_df[
        trend_df["academic_program"].str.contains(branch_search, case=False, na=False)
    ]

trend_df = (
    trend_df.groupby(["year", "institute"])["closing_rank"]
    .min()
    .reset_index()
)

if branch_search:
    fig2 = px.line(
        trend_df,
        x="year",
        y="closing_rank",
        color="institute",
        markers=True,
        title=f"{branch_search} Closing Rank Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Enter a branch keyword to view trend.")

st.divider()
st.header("IIT-wise Comparison")

selected_iits = st.multiselect(
    "Select IITs to compare",
    sorted(df["institute"].unique()),
    default=sorted(df["institute"].unique())[:3]
)

comparison_branch = st.text_input(
    "Branch keyword for IIT comparison",
    placeholder="Computer / Electrical / Mechanical / Civil"
)

compare_df = df[
    (df["institute"].isin(selected_iits)) &
    (df["seat_type"] == "OPEN") &
    (df["gender"].str.contains("Gender", case=False, na=False))
]

if comparison_branch:
    compare_df = compare_df[
        compare_df["academic_program"].str.contains(
            comparison_branch,
            case=False,
            na=False
        )
    ]

compare_df = (
    compare_df.groupby(["year", "institute"])["closing_rank"]
    .min()
    .reset_index()
)

if comparison_branch and len(compare_df) > 0:
    fig3 = px.line(
        compare_df,
        x="year",
        y="closing_rank",
        color="institute",
        markers=True,
        title=f"IIT Comparison for {comparison_branch}"
    )

    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Select IITs and enter a branch keyword.")    

st.divider()
st.header("Category-wise Cutoff Comparison")

category_branch = st.text_input(
    "Branch keyword for category comparison",
    placeholder="Computer / Electrical / Mechanical / Civil"
)

category_df = df[
    df["gender"].str.contains("Gender", case=False, na=False)
]

if category_branch:
    category_df = category_df[
        category_df["academic_program"].str.contains(
            category_branch,
            case=False,
            na=False
        )
    ]

category_df = (
    category_df.groupby(["year", "seat_type"])["closing_rank"]
    .min()
    .reset_index()
)

if category_branch and len(category_df) > 0:
    fig4 = px.line(
        category_df,
        x="year",
        y="closing_rank",
        color="seat_type",
        markers=True,
        title=f"Category-wise Closing Rank Trend for {category_branch}"
    )

    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Enter a branch keyword to compare categories.")  

st.divider()
st.header("Female-only vs Gender-neutral Comparison")

gender_branch = st.text_input(
    "Branch keyword for gender comparison",
    placeholder="Computer / Electrical / Mathematics / Civil"
)

gender_df = df[df["seat_type"] == "OPEN"]

if gender_branch:
    gender_df = gender_df[
        gender_df["academic_program"].str.contains(
            gender_branch,
            case=False,
            na=False
        )
    ]

gender_df = (
    gender_df.groupby(["year", "gender"])["closing_rank"]
    .min()
    .reset_index()
)

if gender_branch and len(gender_df) > 0:
    fig5 = px.line(
        gender_df,
        x="year",
        y="closing_rank",
        color="gender",
        markers=True,
        title=f"Gender-wise Closing Rank Trend for {gender_branch}"
    )

    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Enter a branch keyword to compare gender-wise trends.")