# Databricks notebook source
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid')

weekly_df = pd.read_csv("https://storagegijo.blob.core.windows.net/fmcgsales/weekly_df_final_for_modeling.csv")
display(weekly_df)
                        

# COMMAND ----------

df_weeklysales = weekly_df[['week_number', 'sku', 'units_sold', 'year']].groupby(['week_number', 'sku', 'year']).sum().reset_index().sort_values(by=['week_number', 'year'])
display(df_weeklysales)

# COMMAND ----------

display(weekly_df)

# COMMAND ----------

weekly_df['sku']
weekly_df.loc[[1,100,1000,20000,30000]].set_index('sku').loc['JU-021']


# COMMAND ----------

weekly_df.columns