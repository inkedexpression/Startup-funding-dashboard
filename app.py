import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit import columns

st.set_page_config(layout='wide',page_title='Startup analysis')

df = pd.read_csv('startup_cleaned3.csv')
df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
df['month']=df['Date'].dt.month
df['year'] = df['Date'].dt.year


def load_investor_details(investor):
    st.title(investor)

    #load last 5 investor
    last_5_df = df[df['investors'].str.contains(investor)].head()[['Date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Last 5 Investment')
    st.info('amount in crores')
    st.dataframe(last_5_df)
    col1,col2 = st.columns(2)
    with col1:
        # big invest

        big_invest = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Top 5 Big investment')
        fig, ax = plt.subplots()
        ax.bar(big_invest.index,big_invest.values)

        st.pyplot(fig)
        # sector
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Top 5 Sector investment')
        fig1, ax1 = plt.subplots()
        ax1 .pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')
        st.pyplot(fig1)
     #stage
    col3 , col4 = st.columns(2)
    with col3:
        stage = df[df['investors'].str.contains('Axis Bank')].groupby('round')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('top 5 Stage')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage, labels=stage.index, autopct='%0.01f%%')
        st.pyplot(fig2)

    #city
    with col4:
        city = df[df['investors'].str.contains('Axis Bank')].groupby('city')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('top 5 City Invested')
        fig3, ax3 = plt.subplots()
        ax3.pie(city, labels=city.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    col5,col6 = st.columns(2)
    with col5:
        df['year'] = df['Date'].dt.year
        year = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('Year on Year investment ')
        fig4, ax4 = plt.subplots()
        ax4.plot( year.index, year.values)
        st.pyplot(fig4)

def load_overal_analysis():
    st.title('Overal Analysis')
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        # toatal invest amount
        total_amt_invested = round(df['amount'].sum())
        st.metric('total',str(total_amt_invested)  + ' Cr')
    with col2:
        # max
        max_amt_invested = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('maximun',str(max_amt_invested)+' Cr')

    with col3:
        avg_invest = df.groupby('startup')['amount'].max().mean()
        st.metric('avrage',str(round(avg_invest))+' Cr')

    with col4:
        num_funded = df['startup'].nunique()
        st.metric('total funded startups',str(num_funded))

    st.header('month on month graph ')
    selected_option = st.selectbox('select type',['total','count'])
    if selected_option == 'total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = df['month'].astype('str') + '-' + df['year'].astype('str')
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig5)






st.title('INDIAN  STARTUP  DASHBOARD')

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('select',['OverAll Analysis','Startup Analysis','Investor Analysis'])

if option == 'OverAll Analysis':
        load_overal_analysis()

elif option == 'Startup Analysis':
    st.sidebar.selectbox('select',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('find Startup details')
else:
    df['investors'] = df['investors'].astype(str)
    selected_inverstor = st.sidebar.selectbox('Select',sorted(set(df['investors'].str.split(',').sum())))
    st.title('Investor Analysis')
    btn2 = st.sidebar.button('find Investor details')
    if btn2:
        load_investor_details(selected_inverstor)