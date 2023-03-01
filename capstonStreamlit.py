#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import streamlit as st

siteHeader = st.container()
SF = st.container()
OtherCounties = st.container()
Correlation = st.container()
Density = st.container()
NewConstr = st.container()


with siteHeader:
    st.header('Are high housing costs in San Francisco a result of population growth?')
    
    st.markdown('Before COVID hit, the population in San Francisco was on the rise. A lot of houses are jammed together to accomodate many people in the city. Despite the high demand for housing, the cost of living in the city was extremely high. It is not surprising to say that the influx of people contributed to the rising housing prices. In this project, we aim to establish a connection between population growth and housing costs by analyzing publicly available data from the city, the US Census, and a real estate company called Zillow.')
    
    st.write("##")

    

# # Population

with SF:
    st.subheader('Population and House sale price in San Francisco')
    
    saleSF = pd.read_csv('salesf.csv', index_col=0)
    population = pd.read_csv('population.csv')

    # Population and house price 
    fig, ax1 = plt.subplots(figsize = (10,6))

    ax1.plot(pd.to_datetime(population['YEAR']), population['POPULATION'], 'r-o')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Population')

    ax2 = ax1.twinx()
    ax2.plot(pd.to_datetime(saleSF.index[2::12]), saleSF[2::12])
    ax2.set_ylabel('House sale price')
    ax2.set_xticks(saleSF.index[2::24])
    ax2.yaxis.set_major_formatter('${x:,.0f}')

    fig.autofmt_xdate()
    plt.grid()

    st.pyplot(fig)

    st.markdown("Since 2004, the population has been increasing, despite the financial market crash in 2008. The house prices declined during the crash, they later rebounded with the financial recovery. It may be useful to examine other counties to obtain a broader understanding of how population growth relates to house prices.")  
    st.write("##")

# # Other counties
with OtherCounties:
    
    st.markdown("Try your state and county!")

    saleprice = pd.read_csv('sale_all.csv', index_col=(0,1))
    pop = pd.read_csv('pop_all.csv', index_col=(0,1))
    
    reset_pop = pop.reset_index()
    
    states = sorted(reset_pop['State'].dropna().unique())    
    state = st.selectbox('Choose your state:', options = states, index=4)

    counties = sorted(reset_pop[reset_pop['State']==state]['RegionName'].dropna().unique())
    county = st.selectbox('Choose your county:', options=counties, index=0)

    yourCounty = (county, state)

    x1 = saleprice.columns[2::12]
    Y1 = saleprice
    x2 = pop['Year'].unique()
    Y2 = pop['Population']

    fig, ax1 = plt.subplots(figsize = (10,6))
    
    ax1.plot(x2, Y2.loc[yourCounty], 'o-', color='r', label='Population')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Population')
    
    ax2 = ax1.twinx()
    
    ax2.plot(x1, Y1.loc[yourCounty, x1], color='b', label='House Price')
    ax2.set_xticks(x1[::2])
    ax2.set_ylabel('House sale price')
    ax2.yaxis.set_major_formatter('${x:,.0f}')
    
    ax2.grid(axis='y')
    
    fig.autofmt_xdate()
    
    st.pyplot(fig)

    st.markdown('Not all counties have complete data for the period. In some counties, house prices and population exhibit opposing trends. It is not always accurate to assume that house prices increase with population growth or that population growth drives house prices up.')

    st.write("##")
    
# # Correlation

with Correlation:
    
    st.subheader('Correlation between population and house prices')
    st.markdown('We will utilize Pearson correlation coefficients to determine the degree of correlation between house prices and population growth. To provide a basis for comparison, the scatter plot includes all other counties that possess sufficient data to calculate correlation.')
    
    corr = pd.read_csv('corr.csv', index_col = (0,1))

    county = ('San Francisco County','CA')
    
    z = np.polyfit(corr[corr['Population Increase Rate']<0.25]['Population Increase Rate'], corr[corr['Population Increase Rate']<0.25]['Correlation Coefficient'], 1)
    p = np.poly1d(z)
    xp = np.linspace(-0.25, 0.25,20)
    
    plt.subplots(figsize=(10,6))
    plt.scatter(corr['Population Increase Rate'], corr['Correlation Coefficient'])
    plt.xlim((-0.5, 1.5))
    plt.plot(xp, p(xp), 'r')
    plt.scatter(corr.loc[county]['Population Increase Rate'], corr.loc[county]['Correlation Coefficient'], color='r')
    plt.title('Correlation between population and house price')
    plt.ylabel('Correlation')
    plt.xlabel('Population Growth Rate')
    
    st.pyplot(plt)

    st.markdown('For some counties, the correlation between population growth and house prices is not particularly strong, indicating that population increase may not be the sole primary factor driving housing prices. In some other counties, there is even a negative correlation. In San Francisco (depicted by the red dot), the correlation coefficient is a relatively high 0.79. Generally, counties with higher rates of population growth tend to display higher correlations, and San Francisco is among them.')  
    st.write("##")


# # House Price and Population Density
with Density:
    
    st.subheader('Density and House price')
    st.markdown('We will analyze how house prices are influenced by population density, since San Francisco is one of the cities with a high population density.')

    saleprice_fillna = saleprice.fillna(method='ffill', axis=1)
    saleprice_yearly = saleprice_fillna.loc[:][saleprice.columns[5::12]]
    
    den = []
    pri = []

    for county in list(Y1.index):
        d = pop.loc[county]['Density'][-1]
        p = saleprice_yearly.loc[county][-1]
        if str(d) != 'nan' and str(p) != 'nan':
            den.append(d)
            pri.append(p)

    np.corrcoef(den, pri)

    z = np.polyfit(den, pri, 1)
    p = np.poly1d(z)
    xp = np.linspace(0,70000,200)

    plt.subplots(figsize=(10,6))
    plt.plot(xp, p(xp), 'r')
    plt.scatter(den, pri)
    plt.scatter(pop.loc['San Francisco County','CA']['Density'][-1], saleprice_yearly.loc['San Francisco County','CA'][-1], color='r')
    plt.xlabel('Density')
    plt.ylabel('House Price ($)')
    
    st.pyplot(plt)


    st.markdown("As a general trend, there is a positive, but not strong correlation between population density and house prices (Pearson coefficient: 0.27). San Francisco (red dot) is far from the fitting line. Even when compared to counties in the New York Area (dots with a density greater than 30000), the housing prices in San Francisco appear significantly higher.")
    st.markdown("While the combination of high population density and population growth may influence high housing prices, it is not apparent that population density is one of primary factors contributing to San Francisco's elevated housing prices.")

    st.write("##")

        
with NewConstr:
    st.subheader('Newly built residential units')
    st.markdown('With the continuous population growth, the scarcity of available residential units may contribute to a rise in housing costs. By examining city permit data, we can determine whether San Francisco has been providing new residential units to accommodate the influx of new residents.')
    
    pop_newcon = pd.read_csv('newcon.csv', index_col=0)

    pop_newcon.plot(x = 'index', y=["New Residential Units Cumulated", "Population Increase Cumulated"], kind="line", rot=60, figsize=(10,6), 
          xlabel='Year', color={"New Residential Units Cumulated": "blue", "Population Increase Cumulated": "red"})
    plt.savefig('pop_newcon_cumulated.png')
    plt.xticks(np.linspace(2000,2018,10))
    plt.grid(axis='y')
    
    st.pyplot(plt)
    
    st.markdown('San Francisco County has been constructing new residential units. However, the housing prices in San Francisco have continued to rise. This may indicate that either the new constructions are still insufficient or that the scarcity of houses is not a primary factor determining housing prices in San Francisco.')
    
    st.markdown('While we can confirm that population growth may be a contributing factor to housing prices, it is important to recognize that other variables can also have a significant impact on the housing costs. Factors such as economy or job opportunities may also play a significant role in driving the housing market.')

