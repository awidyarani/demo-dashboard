import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Demo Dashboard",
    page_icon="📊",
    layout="wide"
)

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


# Panggil data
loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_"," ")

# Financial Analysis
st.subheader("Financial Analysis")

condition = st.selectbox(
    "Select Loan Condition",
    ("Good Loan", "Bad Loan")
)

with st.container(border=True):
    tab4, tab5 = st.tabs(["Loan Amount Distribution", "Loan Amount Distribution by Purpose"])
    
    # Untuk menentukan dari select box apakah yg dipilih good atau bad
    loan_condition = loan[loan['loan_condition'] == condition]

    with tab4:
        hist_loan = px.histogram(
            loan_condition,
            x = 'loan_amount', 
            color = 'term', 
            nbins = 20,
            title = 'Loan Amount Distribution',
            template='seaborn',
            labels={
                'loan_amount':'Loan Amount',
                'term':'Loan Term'},
            color_discrete_sequence=["lightpink","lightblue"]
        )
        st.plotly_chart(hist_loan)


    with tab5:
        box_loan = px.box(
        loan_condition,
        x = 'purpose',
        y = 'loan_amount',
        color = 'term',
        color_discrete_sequence=['lightpink', 'lightblue'],
        title='Loan Amount Distribution by Purpose',
        labels={
            'loan_amount': 'Loan Amount',
            'term': 'Loan Term',
            'purpose': 'Loan Purpose'
        },
        )
        st.plotly_chart(box_loan)