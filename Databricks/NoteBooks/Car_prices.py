# Databricks notebook source
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from pyspark.sql.functions import col, lit
df = pd.read_csv("https://storagegijo.blob.core.windows.net/files/car_prices.csv")
display(df)

# COMMAND ----------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from pyspark.sql.functions import col


# COMMAND ----------

df[df['make']=='NO_VALUE']

# COMMAND ----------

for col  in df.columns:
    df[col].fillna(value='No_Value', inplace=True)
    df[col] = df[col].astype(str).str.upper()



# COMMAND ----------


df['wmi']=df['vin'].str.slice(0,3)

wmi_mapping = (
    df.loc[(df['make'] != 'NO_VALUE') & (df['wmi'] != 'NO_VALUE'),['wmi','make']].set_index('wmi')['make'].to_dict()
)

initial_count = df[df['make']== 'NO_VALUE'].shape[0]
print("Initial make column value null count : ", initial_count)



print("Number of valid mappings in WMI_mapping:", len(wmi_mapping))


def map_make(row):
    if row['make'] == 'NO_VALUE':
        wmi_value = row['wmi']
        if wmi_value in wmi_mapping:
            return wmi_mapping[wmi_value]
    return row['make']

df['make'] = df.apply(map_make, axis=1)

initial_count = df[df['make'] == 'NO_VALUE'].shape[0]
print("Final make column value null count : ", initial_count)


# COMMAND ----------

df[df.isnull().any(axis=1)]

# COMMAND ----------

df.shape
pd.melt(df)

# COMMAND ----------

df.pivot(index=None,columns='make',values='sellingprice')

# COMMAND ----------

import pandas as pd
pd.reset_option('display.max_rows', None)
df['make'].str.contains('AUDI').sum()
df['make'].str.count('AUDI').sum()
df[['make', 'year']].apply(lambda x: '_'.join(x.astype(str)), axis=1)

# COMMAND ----------



# COMMAND ----------

df.set_index(['month','year'])