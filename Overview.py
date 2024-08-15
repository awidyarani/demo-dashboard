import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Demo Dashboard",
    page_icon="📊",
    layout="wide"
)

#Judul Dashboard
st.title("Financial Insight Dashboard")
st.subheader("Loan Performance and Trends")
st.divider()

#Side Bar
st.sidebar.header("Dashboard Filters and Fitures")
st.sidebar.subheader("Features")
st.sidebar.markdown(
'''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

# Overiew
# Panggil data
loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_"," ")

# Summary Data/Overview
with st.container(border=True): # untuk menambahkan border
    st.subheader("Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Loans", f"{loan['id'].count():,.0f}", help="Total Number of Loans")
        st.metric("Total Loan Amount", f"${loan['loan_amount'].sum():,.0f}", help="Sum of Loans Amount")

    with col2:
        st.metric("Average Interest Rate", f"{loan['interest_rate'].mean():,.2f}%", help="Average of Percentage of the loan amount that borrowers has to pay")
        st.metric("Average Loan Amount", f"${loan['loan_amount'].mean():,.0f}", help="Average of all loan amount")


#Grafik Time Series
#Panggil data
with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(["Loans Issue Over Time", "Loan Amount Over Time", "Issue Date Analysis"])
    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
        line_count = px.line(
        loan_date_count,
        markers=True,
        title="Number of Loans Issued Over Time",
        labels={
            "issue_date": "Issue Date",
            "value": "Number of Loans"
        },
        color_discrete_sequence=["lightpink"]
        ).update_layout(showlegend = False)

        st.plotly_chart(line_count)

    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
        line_sum = px.line(
        loan_date_sum,
        markers=True,
        labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
        },
        color_discrete_sequence=["lightpink"],
        template='seaborn',
        title="Loans Amount Over Time",
        ).update_layout(showlegend = False)

        st.plotly_chart(line_sum)

    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
        line_dist = px.bar(
        loan_day_count,
        category_orders= { # Mengatur urutan categori (hari)
            'issue_weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        },
        title='Distribution of Loans by Day of the Week',
        labels={
            'value':'Number of Loans',
            'issue_weekday':'Day of the Week'
        },
        template='seaborn',
        color_discrete_sequence=["lightpink"]
        ).update_layout(showlegend = False)

        st.plotly_chart(line_dist)

#Loan Performance

st.subheader("Loan Performace")

with st.expander("Click Here to Expand"):
    col3, col4 = st.columns(2)

    with col3:
        pie_condition = px.pie(
        loan,
        names = 'loan_condition',
        hole = 0.4,
        title = "Distribution of Loans by Condition",
        template='seaborn',
        color_discrete_sequence=["lightpink" , "lightblue"]
        ).update_traces(textinfo='percent + value')

        st.plotly_chart(pie_condition)

    with col4:
        grade = loan['grade'].value_counts().sort_index()
        bar_condition = px.bar(
        grade,
        title= "Distribution of Loans by Grade",
        labels={
            'grade' : "Grade",
            'value' : "Number of Loans"
        },
        color_discrete_sequence=["lightpink"]
        ).update_layout(showlegend = False)

        st.plotly_chart(bar_condition)

st.divider()

