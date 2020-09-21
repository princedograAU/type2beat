#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import re


# In[28]:


data = pd.read_csv("openfoodfacts_clean.csv")


# In[33]:


data.head()


# In[34]:


len(data)


# In[35]:


data.tail()


# In[36]:


data["serving_size"].fillna(1, inplace=True)


# In[37]:


# data.dropna(subset=["serving_size"], inplace=True)


# In[38]:


len(data)


# In[40]:


data["serving_size"] = data["serving_size"].apply(lambda x: (x[:x.find("(")]))
data


# In[41]:


data[data["serving_size"]==1]


# In[42]:


data.to_csv ('data_food.csv', index = False, header=True)


# In[43]:


data = pd.read_csv("data_food.csv")


# In[44]:


data.shape


# In[45]:


data


# In[22]:


data['serving_size'] = data['serving_size'].apply(lambda x: re.findall(".\d\sg|ml", x))


# In[23]:


data


# In[52]:


data = pd.read_csv("food_data_serving.csv")


# In[53]:


data


# In[49]:


data["serving_size"].fillna(1, inplace=True)


# In[50]:


data.shape


# In[51]:


data


# In[ ]:




