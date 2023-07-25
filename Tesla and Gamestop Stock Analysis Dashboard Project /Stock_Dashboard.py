# ============================ COURSE PROJECT =================================
# Tesla and GameStop Stock Analysis Dashboard Project
# Part 1: Use yfinance to Extract Stock Data
# Part 2: Use Webscraping to Extract Tesla Revenue Data
# Part 3: Use yfinance to Extract Stock Data
# Part 4: Use Webscraping to Extract GME Revenue Data
# Part 5: Plot Tesla Stock Graph
# Part 6: Plot GameStop Stock Graph

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.io as io
io.renderers.default='browser'

# For plotly plots to display in Spyder, you'll have to set the figures to display
# in your web browser (Spyder's display isn't good enough)
# Thus the reason for io.renderers.default='browser'

import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Use the following function to plot stock data with the plotly library.
# stock_data: a dataframe with stock data - must contain "Date" and "Close" columns
# revenue_data: a dataframe with revenue data - must contain "Date" and "Close" columns
# stock: name of the stock
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    
##############################################################################    
# 1. Extract Tesla stock data using the Ticker function.
##############################################################################

tesla = yf.Ticker('TSLA') # ticker object holding stock data for TSLA

teslaShareData = tesla.history(period = 'max')
# TSLA historical data. Period = 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 
# 1wk, 1mo, 3mo, max.
#
# Dataframe.index: Index = "Date" column 
# Dataframe.columns: Headers = ["Open", "High", "Low", ...]

print('Tesla Share Data: ')
print(teslaShareData.head())
# Prints the first 5 rows of the dataframe teslaShareData.

# Reset the index of the dataframe and display the first 5 rows.
teslaShareData = teslaShareData.reset_index()
# Resets the index from the "Date" column to a list of [0, 1, 2, ...]
# "Date" column now part of dataframe. 

print('Tesla Share Data (Indices Revised): ')
print(teslaShareData.head())

# Alternative approach:
    # teslaShareData.reset_index(inplace=True)
    # print(teslaShareData.head())
    # 
    # inplace=True: actively revises indices of the dataframe.
    # inplace=False: creates a copy of the dataframe, which you'll have to
    # assign.
##############################################################################
# 2. Use the request library to download Tesla revenue data.
# Save the text response in html_data
##############################################################################

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'    
response = requests.get(url) # retrieve data from server
html_data = response.text # stores the html code as a string

soup = BeautifulSoup(html_data,"html.parser")

##############################################################################
# Extract the table "Tesla Quarterly Revenue" and store it in dataframe
# 'tesla_revenue'. The dataframe should contain columns "Date" and "Revenue".
##############################################################################

# 2a. Determine the index of the table with the title "Tesla Quarterly Revenue"
theaders = soup.find_all('th') # extracts the table headers of all tables in a list
# soup.find_all('th'):
    # [ <th> ... </th>,
    #   <th> ... </th>,
    # ] - there will be 6 tables in the website.
    #
    # How I know 6?
    # View the source code of the site.
    # Ctrl+F --> "<thead>" --> Browser tells me there's 6 instances of this.

#print(theaders)
#print(theaders[1].text)

index = 0
for i, header in enumerate(theaders):
    # loop through each header, i.e. each element in the list theaders
    if header.text == 'Tesla Quarterly Revenue(Millions of US $)':
        #print('Index: ',i)
        #print(header)
        index = i
        # Assign the index of the element with 'Tesla Quarterly ...' into 'index'

# 2b. Extract the data from the table into dataframe tesla_revenue
columns = ['Date','Revenue']
tesla_revenue = pd.DataFrame(columns = columns) # set the columns of data frame

# Populate the dataframe
date = []
revenue = []

tablebody = soup.find_all('tbody') # Focus only on the stuff within <tbody> 
tesla_revbody = tablebody[index] # Consider only the <tbody> corresponding to Tesla Quarterly Revenue

# Loop through each row of the table, <tr> ... </tr>
for row in tesla_revbody.find_all('tr'):
    # tesla_revbody.find_all('tr')
    # [ <tr><td>2022-09-30</td><td>$21,454</td></tr>, 
    #   <tr><td>2022-06-30</td><td>$16,934</td></tr>
    #  ... ]
    
    # 1st row: <tr><td>2022-09-30</td><td>$21,454</td></tr>
    
    cell = row.find_all('td')
    # for 1st row, cell = row.find_all('td')
    # [ <td>2022-09-30</td>,
    #   <td>$21,454</td>]
    
    date.append(cell[0].text)
    revenue.append(cell[1].text)

tesla_revenue[columns[0]] = date
tesla_revenue[columns[1]] = revenue

print('Tesla Quarterly Revenue (Millions of US $): ')
print(tesla_revenue)
print(tesla_revenue.loc[tesla_revenue.index[-1],'Date'])
print(tesla_revenue.loc[tesla_revenue.index[-1],'Revenue'])

# Remove punctuation, and NaN values.
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace('$','').str.replace(',','')    
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]   
print('Tesla Quarterly Revenue (Millions of US $) (Revised): ')
print(tesla_revenue)   
  
##############################################################################
# 3. Extract Gamestop stock data using the Ticker function.
##############################################################################
GME = yf.Ticker('GME') # ticker object holding stock data for TSLA

gme_Data = GME.history(period = 'max')
# GME historical data. Period = 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 
# 1wk, 1mo, 3mo, max.
#
# Dataframe.index: Index = "Date" column 
# Dataframe.columns: Headers = ["Open", "High", "Low", ...]

# Reset the index of the dataframe and display the first 5 rows.
gme_Data = gme_Data.reset_index()
# Resets the index from the "Date" column to a list of [0, 1, 2, ...]
# "Date" column now part of dataframe. 

print('GME Share Data (Indices Revised): ')
print(gme_Data.head())

# Alternative approach:
    # gme_Data.reset_index(inplace=True)
    # print(gme_Data.head())
    # 
    # inplace=True: actively revises indices of the dataframe.
    # inplace=False: creates a copy of the dataframe, which you'll have to
    # assign.

##############################################################################
# 4. Extract Gamestop revenue data using requests. Save the text of the
# response in the variable html_data
##############################################################################
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
response = requests.get(url) # retrieve data from server
html_data = response.text # stores the html code as a string

soup = BeautifulSoup(html_data,"html.parser")

##############################################################################
# Extract the table "Gamestop Quarterly Revenue" and store it in dataframe
# 'gme_revenue'. The dataframe should contain columns "Date" and "Revenue".
# Remove the commas and dollar signs from the "Revenue" column.
##############################################################################

# 4a. Determine the index of the table with the title "GamepStop Quarterly Revenue"
theaders2 = soup.find_all('th') # extracts the table headers of all tables in a list
# soup.find_all('th'):
    # [ <th> ... </th>,
    #   <th> ... </th>,
    # ] - there will be 6 tables in the website.
    #
    # How I know 6?
    # View the source code of the site.
    # Ctrl+F --> "<thead>" --> Browser tells me there's 6 instances of this.

#print(theaders)
print(theaders2[1].text)

index = 0
for i, header in enumerate(theaders2):
    # loop through each header, i.e. each element in the list theaders
    if header.text == 'GameStop Quarterly Revenue(Millions of US $)':
        print('Index: ',i)
        print(header)
        index = i
        # Assign the index of the element with 'GameStop Quarterly ...' into 'index'

# 4b. Extract the data from the table into dataframe gme_revenue
columns = ['Date','Revenue']
gme_revenue = pd.DataFrame(columns = columns) # set the columns of data frame

# Populate the dataframe
date = []
revenue = []

tablebody = soup.find_all('tbody') # Focus only on the stuff within <tbody> 
gme_revbody = tablebody[index] # Consider only the <tbody> corresponding to GameStop Quarterly Revenue

# Loop through each row of the table, <tr> ... </tr>
for row in gme_revbody.find_all('tr'):
    # gme_revbody.find_all('tr')
    # [ <tr><td>2020-04-30</td><td>$1,021</td></tr>, 
    #   <tr><td>2020-01-31</td><td>$2,194</td></tr>
    #  ... ]
    
    # 1st row: <tr><td>2020-04-30</td><td>$1,021</td></tr>
    
    cell = row.find_all('td')
    # for 1st row, cell = row.find_all('td')
    # [ <td>2020-04-30</td>,
    #   <td>$1,021</td>]
    
    date.append(cell[0].text)
    revenue.append(cell[1].text)

gme_revenue[columns[0]] = date
gme_revenue[columns[1]] = revenue

print('Check if the below line represents the revenue in 2017-04-30')
print(gme_revenue.loc[gme_revenue.index[-1],'Date'])
print(gme_revenue.loc[gme_revenue.index[-1],'Revenue'])

# Remove punctuation, and NaN values.
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace('$','').str.replace(',','')    
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]   
print('GameStop Quarterly Revenue (Millions of US $) (Revised): ')
print(gme_revenue)   

##############################################################################
# 5. Use make_graph function to graph the Tesla stock data. Provide a title for
# the graph. Note that the graph will show data up to June 2021.
##############################################################################
make_graph(teslaShareData, tesla_revenue, 'Tesla')

##############################################################################
# 6. Use make_graph function to graph the GameStop stock data. Provide a title for
# the graph. Note that the graph will show data up to June 2021.
##############################################################################
make_graph(gme_Data, gme_revenue, 'Gamestop')
