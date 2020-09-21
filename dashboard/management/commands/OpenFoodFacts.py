#!/usr/bin/env python
# coding: utf-8

# In[4]:


# https://world.openfoodfacts.org/data

# import pandas 
import pandas as pd

# load csv file
df = pd.read_csv('C:\\Users\\Prince Dogra\\Desktop\\en.openfoodfacts.org.products.csv')

# selecting important fields out of dataset
df1 = df[['product_name','serving_size', 'fat_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'proteins_100g', 'salt_100g', 'sodium_100g', 'alcohol_100g']]

# ============================================================================
# df1.shape
# df1['product_name'].isna().sum()
# df1.drop(axis=1, columns=['additives','additives_tags', 'additives_en']) 
# ============================================================================

# remove empty fields
df1.dropna(axis=0, subset=['product_name'], inplace=True)
df1.dropna(axis=0, subset=['carbohydrates_100g'], inplace=True)

# drop first row
# df1.drop(axis=0, inplace=True)

# filling the empty fields in serving with empty string
df1['serving_size'].fillna('', inplace=True)

# filling the empty fields in fat_100g with 0.0 value
df1['fat_100g'].fillna(0.0, inplace=True)

# filling the empty fields in carbohydrates_100g with 0.0 value
df1['carbohydrates_100g'].fillna(0.0, inplace=True)

# filling the empty fields in sugars_100g with 0.0 value
df1['sugars_100g'].fillna(0.0, inplace=True)

# filling the empty fields in fiber_100g with 0.0 value
df1['fiber_100g'].fillna(0.0, inplace=True)

# filling the empty fields in proteins_100g with 0.0 value
df1['proteins_100g'].fillna(0.0, inplace=True)

# filling the empty fields in salt_100g with 0.0 value
df1['salt_100g'].fillna(0.0, inplace=True)

# filling the empty fields in sodium_100g with 0.0 value
df1['sodium_100g'].fillna(0.0, inplace=True)

# filling the empty fields in alcohol_100g with 0.0 value
df1['alcohol_100g'].fillna(0.0, inplace=True)

# storing clean data to new csv file
df1.to_csv('openfoodfacts_clean.csv')


# In[9]:


df1


# In[7]:


import pandas as pd

# load csv file
df = pd.read_csv('C:\\Users\\Prince Dogra\\food_data.csv')


# In[8]:


df.shape


# In[ ]:




