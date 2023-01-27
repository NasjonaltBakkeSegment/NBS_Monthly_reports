#!/usr/bin/env python
# coding: utf-8

# # Monitoring data downloads from colhub portals

# In[1]:


import pathlib
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import copy
from IPython.display import Markdown as md

plt.rcParams["figure.figsize"] = (20,15)
plt.rcParams.update({'font.size': 22})


# In[2]:


# show all rows, all columns
pd.set_option("max_rows", None)
pd.set_option("max_columns", None)
pd.set_option('max_colwidth', None)


# In[3]:


logsdir = pathlib.Path('../data')


# In[4]:


def get_product_type(product):
    if product[0:2] == 'S1':
        type = product.split('_')[2]
    elif product[0:2] == 'S2':
        type = product.split('_')[1]
        if not type.startswith('M'):
            type = 'Unknown'
    elif product[0:2] == 'S3':
        tmp = product.split('_')
        if tmp[1] == 'SL':
            type = 'SLSTR_L' + tmp[2]
        elif tmp[1] == 'SR':
            type = 'SRAL_L' + tmp[2]
        elif tmp[1] == 'OL':
            type = 'OLCI_L' + tmp[2]
        else:
            type = 'Unknown'
    else:
        type = 'Unknown'
    if 'DTERRENG' in product:
        type = type + '_DTERRENG'
    return type


# In[5]:


def get_data(file):
    data = pd.read_csv(file, header=None, names=['download_time', 'user', 'product', 'size', 'download_duration']                        , parse_dates=['download_time'], index_col='download_time')
    data['satellite'] = data['product'].apply(lambda x: x[0:2])
    data['product_type'] = data['product'].apply(get_product_type)
    return data[data['product_type'] != 'Unknown']


# In this section the perfomance of the FrontEnds is analyzed, for both colhub.met.no and colhub-archive.met.no. The FEs perfomance is translated as user accesibility to the data which is one of the main goals for the project. 

# ## Portal: colhub.met.no

# In[6]:


csvfile = logsdir / 'NBS_frontend-global_outputs.csv'
nbs_global = get_data(csvfile)


# The first portal to analyze is colhub.met.no. The target of the analysis is to check the amount of data downloaded by users, but also the number of users accessing the datahub. Below the historical amount of data per day is represented.

# In[7]:


# Number of products downloaded per day
nbs_global.groupby(nbs_global.index.date).count()['product_type'].plot(ylabel='Number of products', rot=70)


# The same data is also represented below, with a difference. This time the data is not accounted by numer, but by volume. Although both graphs show similar trends, they are not exactly equal due to the variability in the ratio volume per product. For instance, the seasonality of optical products could have an impact in the total volume of products.

# In[8]:


# Volume downloaded per day (in Tb)
total = nbs_global.groupby(nbs_global.index.date).sum()['size']/1024/1024/1024/1024
total.plot(ylabel='Volume downloaded in Tb', rot=70)


# The table below is also interesting. It shows the amount of products downloaded for each the different Sentinel products. As expected, S1 and S2 are the most used Sentinels. S3 is slightly used, while S5p is not used.

# In[9]:


# Nb of products downloaded per satellite / product
col_table1 = nbs_global.groupby(['satellite', 'product_type']).size()
col_table1


# The following table shows the total downloaded volume of data in Tb per month. Here the seasonality of some Sentinel products can affect the final numbers.

# In[10]:


# Monthly total retrieval in Tb
col_table2 = nbs_global.groupby([nbs_global.index.year, nbs_global.index.month]).sum()['size']/1024/1024/1024/1024
col_table2


# The number of users accessing and using the datahub is also important to be known. The plot below show the number of users per day. Some variability is represented in its numbers. Nevertheless, colhub.met.no is used by 15 to 20 users per day. 

# In[11]:


# Number of unique users that downloaded each day
nbs_global.groupby(nbs_global.index.date).agg({"user": "nunique"}).plot(ylabel='Number of unique users')


# ## Portal: colhub-archive.met.no

# In[12]:


csvfile = logsdir / 'NBS_frontend-AOI_outputs.csv'
nbs_AOI = get_data(csvfile)


# Similar to colhub.met.no, here it is presented the performance of colhub-archive.met.no. First the number of products downloaded per day. As shown in the plot below, some days the number of products downloaded is null. This is a correct value which is not reflecting the performance of the FE. The archive is not as frequently accessed as colhub.met.no. Only those users looking for historical data will used this portal.

# In[13]:


# Number of products downloaded per day
nbs_AOI.groupby(nbs_AOI.index.date).count()['product_type'].plot(ylabel='Number of products', rot=70)


# As explained and shown in the previous section, the total volume downloaded is also shown in the graphic below.  

# In[14]:


# Volume downloaded per day (in Tb)
total = nbs_AOI.groupby(nbs_AOI.index.date).sum()['size']/1024/1024/1024/1024
total.plot(ylabel='Volume downloaded in Tb', rot=70)


# It is still interesting to see the number of products downloaded per product type. As shown in the previous section, S1 and S2 still are the most popular Sentinels.

# In[15]:


# Nb of products downloaded per satellite / product
col_table3 = nbs_AOI.groupby(['satellite', 'product_type']).size()
col_table3


# The table below shows the monthly retrieved volume of data in Tb.

# In[16]:


# Monthly total retrieval in Tb
col_table4 = nbs_AOI.groupby([nbs_AOI.index.year, nbs_AOI.index.month_name()]).sum()['size']/1024/1024/1024/1024
col_table4


# The last graphic show the number of users accessing and downloading data from the portal. Again, the dicontinuity in numbers of users it is not a sign of the portal performance.

# In[17]:


# Number of unique users that downloaded each day
nbs_AOI.groupby(nbs_AOI.index.date).agg({"user": "nunique"}).plot(ylabel='Number of unique users', rot=70)


# In[ ]:




