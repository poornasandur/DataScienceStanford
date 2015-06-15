# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import cs109style
cs109style.customize_mpl()
cs109style.customize_css()

# special IPython command to prepare the notebook for matplotlib
%matplotlib inline 

from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt
import requests
from pattern import web


# <markdowncell>

# ## Fetching population data from Wikipedia
# 
# In this example we will fetch data about countries and their population from Wikipedia.
# 
# http://en.wikipedia.org/wiki/List_of_countries_by_past_and_future_population has several tables for individual countries, subcontinents as well as different years. We will combine the data for all countries and all years in a single panda dataframe and visualize the change in population for different countries.
# 
# ###We will go through the following steps:
# * fetching html with embedded data
# * parsing html to extract the data
# * collecting the data in a panda dataframe
# * displaying the data
# 
# To give you some starting points for your homework, we will also show the different sub-steps that can be taken to reach the presented solution.

# <markdowncell>

# ## Fetching the Wikipedia site

# <codecell>

url = 'http://en.wikipedia.org/wiki/List_of_countries_by_past_and_future_population'
website_html = requests.get(url).text
#print website_html

# <markdowncell>

# ## Parsing html data

# <codecell>

def get_population_html_tables(html):
    """Parse html and return html tables of wikipedia population data."""

    dom = web.Element(html)

    ### 0. step: look at html source!
    
    #### 1. step: get all tables
    tbls = dom.by_class('sortable wikitable')
    

    #### 2. step: get all tables we care about

    return tbls

tables = get_population_html_tables(website_html)
print "table length: %d" %len(tables)
for t in tables:
    print t.attributes

# <codecell>

def table_type(tbl):
    ### Extract the table type
    return tbl('th')[0].content

# group the tables by type
tables_by_type = defaultdict(list)  # defaultdicts have a default value that is inserted when a new key is accessed
for tbl in tables:
    tables_by_type[table_type(tbl)].append(tbl)

print tables_by_type

# <markdowncell>

# ## Extracting data and filling it into a dictionary

# <codecell>

def get_countries_population(tables):
    """Extract population data for countries from all tables and store it in dictionary."""
    
    result = defaultdict(dict)

    # 1. step: try to extract data for a single table
    for table in tables:
        #print tables[0]
        tbl = table
        table_headers = tbl('th')
        table_headers = [str(x.content) for x in table_headers]
        first_header = table_headers[0]
        years = [int(x) for x in table_headers if x.isdigit()]
        year_indices = [idx for idx,x in enumerate(table_headers) if x.isdigit()]
        #print first_header
        #print table_headers
        #print years
        #print year_indices
    
        rows = tbl('tr')[1:]
        for row in rows:
            country_name = row('td')[0]('a')[0].content        
            population_by_year = [int(row('td')[index].content.replace(',','')) for index in year_indices]
            #print country_name
            #print population_by_year
            sub_dict = dict(zip(years,population_by_year))
            #print sub_dict
            
                                  
            #print country_name
            result[country_name].update(sub_dict)
    # 2. step: iterate over all tables, extract headings and actual data and combine data into single dict
    #print len(tables)
    
    
    return result


result = get_countries_population(tables_by_type['Country or territory'])
#print result

# <markdowncell>

# ## Creating a dataframe from a dictionary

# <codecell>

# create dataframe

df = pd.DataFrame.from_dict(result, orient='index')
# sort based on year
df.sort(axis=1,inplace=True)
print df

# <markdowncell>

# ## Some data accessing functions for a panda dataframe

# <codecell>

subtable = df.iloc[0:2, 0:2]
print "subtable"
print subtable
print ""

column = df[1955]
print "column"
print column
print ""

row = df.ix[0] #row 0
print "row"
print row
print ""

rows = df.ix[:2] #rows 0,1
print "rows"
print rows
print ""

element = df.ix[0,1955] #element
print "element"
print element
print ""

# max along column
print "max"
print df[1950].max()
print ""

# axes
print "axes"
print df.axes
print ""

row = df.ix[0]
print "row info"
print row.name
print row.index
print ""

countries =  df.index
print "countries"
print countries
print ""

print "Austria"
print df.ix['Austria']

# <markdowncell>

# ## Plotting population of 4 countries

# <codecell>

plotCountries = ['Austria', 'Germany', 'United States', 'France']
    
for country in plotCountries:
    row = df.ix[country]
    plt.plot(row.index, row, label=row.name ) 
    
plt.ylim(ymin=0) # start y axis at 0

plt.xticks(rotation=70)
plt.legend(loc='best')
plt.xlabel("Year")
plt.ylabel("# people (million)")
plt.title("Population of countries")

# <markdowncell>

# ## Plot 5 most populous countries from 2010 and 2060

# <codecell>

def plot_populous(df, year):
    # sort table depending on data value in year column
    df_by_year = df.sort(year, ascending=False)
    
    plt.figure()
    for i in range(5):  
        row = df_by_year.ix[i]
        plt.plot(row.index, row, label=row.name ) 
            
    plt.ylim(ymin=0)
    
    plt.xticks(rotation=70)
    plt.legend(loc='best')
    plt.xlabel("Year")
    plt.ylabel("# people (million)")
    plt.title("Most populous countries in %d" % year)

plot_populous(df, 2010)
plot_populous(df, 2050)

# <codecell>


