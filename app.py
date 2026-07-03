import streamlit as st
import pandas as pd
import plotly.express as px
px.defaults.template = "plotly"

st.set_page_config(
    page_title="Student Performance Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Analytics Dashboard")
st.write("Hello! We will be analyzing the performances of students through various graphs!!")

df = pd.read_csv("data/student-mat.csv", sep=";")

st.sidebar.header("FILTERS")

gender_filter = st.sidebar.selectbox(
    "SELECT GENDER",
    ["ALL"] + list(df["sex"].unique())
)

age_filter = st.sidebar.slider(
    "Select Age",
    min_value=int(df["age"].min()),
    max_value=int(df["age"].max()),
    value=(int(df["age"].min()), int(df["age"].max()))
)
result_filter = st.sidebar.selectbox(
    "RESULT",
    ["ALL", "PASSED", "FAILED"]
)
filtered_df = df.copy()
col1,col2,col3,col4=st.columns(4)
with col1:
    st.metric("Total Students", len(filtered_df))
with col2:
    st.metric("Average G3",round(filtered_df["G3"].mean(),2))
with col3:
    st.metric("Average Age",round(filtered_df["age"].mean(),2))
with col4:
    pass_rate=(filtered_df["G3"]>=10).mean()*100
    st.metric("Pass Rate %",round(pass_rate,2))

if gender_filter != "ALL":
    filtered_df = filtered_df[filtered_df["sex"] == gender_filter]

filtered_df = filtered_df[
    (filtered_df["age"] >= age_filter[0]) &
    (filtered_df["age"] <= age_filter[1])
]
if result_filter == "PASSED":
    filtered_df = filtered_df[filtered_df["G3"] >= 10]

elif result_filter == "FAILED":
    filtered_df = filtered_df[filtered_df["G3"] < 10]

st.subheader("Dataset Preview")
st.header("👥 Demographic Analysis")
st.dataframe(filtered_df)
st.divider()
age_count=filtered_df["age"].value_counts()
fig=px.bar(
           x=age_count.index,
           y=age_count.values,
           labels={"x":"AGE","y":"NO OF STUDENTS"},
           title="AGE DISTRIBUTION",
           color=age_count.index
           )
st.plotly_chart(fig, use_container_width=True)
gender=filtered_df["sex"].value_counts()
fig=px.bar(
           x=gender.index,
           y=gender.values,
           labels={"x":"GENDER","y":"NO OF PERSONS"},
           title="GENDER DISTRIBUTION CHART",
           color=gender.index
           )
st.plotly_chart(fig, use_container_width=True)
st.header("📚 Academic Performance Analysis")
fig=px.histogram(
                filtered_df,
                 x="G3",
                 title="THE GRADE DISTRIBUTION",
                 labels={"x":"FINAL GRADES"},
                 color="sex"
                 )
st.plotly_chart(fig, use_container_width=True)
fig=px.box(
           filtered_df,
           x="studytime",
           y="G3",
           labels={"x":"STUDY TIME","y":"G3"},
           title="STUDY TIME VS GRADE(G3)",
           color="studytime"
           )
st.plotly_chart(fig, use_container_width=True)
fig=px.box(
           filtered_df,
           x="failures",
           y="G3",
           title="FAILURES VS G3",
           labels={"x":"Past Class Failures","y":"GRADE G3"},
           color="failures"
           )
st.plotly_chart(fig, use_container_width=True)
fig=px.scatter(
            filtered_df,
            x="absences",
            y="G3",
            title="ABSENCES VS G3",
            labels={"x":"absences","y":"G3"},
            color="sex"
            )
st.plotly_chart(fig, use_container_width=True)
st.header("📈 Correlation Analysis")
corr=filtered_df.corr(numeric_only=True)
fig=px.imshow(
            corr,
            text_auto=True,
            title="CORRELATION HEATMAP"
            )
st.plotly_chart(fig, use_container_width=True)