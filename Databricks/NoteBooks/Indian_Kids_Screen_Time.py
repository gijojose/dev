# Databricks notebook source
# MAGIC %scala
# MAGIC def readFileFromADLS(appID: String,
# MAGIC                       secret: String,
# MAGIC                       StorageAccountName: String,
# MAGIC                       FileSystemName: String,
# MAGIC                       tenantID: String,
# MAGIC                       fileName: String,
# MAGIC                       fileType: String): 
# MAGIC                       Unit = {
# MAGIC     val appIDValue = dbutils.secrets.get(scope = "newScopeDataBricks", key = appID)
# MAGIC     val secretValue = dbutils.secrets.get(scope = "newScopeDataBricks", key = secret)
# MAGIC     val StorageAccountNameValue = dbutils.secrets.get(scope = "newScopeDataBricks", key = StorageAccountName)
# MAGIC     val tenantIDValue = dbutils.secrets.get(scope = "newScopeDataBricks", key = tenantID)
# MAGIC     val filenamewithoutpath = fileName.substring(0,fileName.length - 4)
# MAGIC     spark.conf.set(s"fs.azure.account.auth.type.$StorageAccountNameValue.dfs.core.windows.net", "OAuth")
# MAGIC     spark.conf.set(s"fs.azure.account.oauth.provider.type.$StorageAccountNameValue.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
# MAGIC     spark.conf.set(s"fs.azure.account.oauth2.client.id.$StorageAccountNameValue.dfs.core.windows.net", appIDValue)
# MAGIC     spark.conf.set(s"fs.azure.account.oauth2.client.secret.$StorageAccountNameValue.dfs.core.windows.net", secretValue)
# MAGIC     spark.conf.set(s"fs.azure.account.oauth2.client.endpoint.$StorageAccountNameValue.dfs.core.windows.net", s"https://login.microsoftonline.com/$tenantIDValue/oauth2/token")
# MAGIC
# MAGIC     val filePath = s"abfss://$FileSystemName@$StorageAccountNameValue.dfs.core.windows.net/$fileName"
# MAGIC     val df = spark.read.format(fileType).option("header", "true").load(filePath)
# MAGIC     df.write.format("delta").save(s"/mnt/delta/$filenamewithoutpath")
# MAGIC
# MAGIC }

# COMMAND ----------

# MAGIC %scala
# MAGIC
# MAGIC  readFileFromADLS(
# MAGIC   appID = "appID",
# MAGIC   secret = "secret",
# MAGIC   StorageAccountName = "storageAccountName",
# MAGIC   FileSystemName = "files",
# MAGIC   tenantID = "tenantID",
# MAGIC   fileName ="Indian_Kids_Screen_Time.csv",
# MAGIC   fileType = "csv"
# MAGIC )
# MAGIC

# COMMAND ----------

import pandas as pd
from pyspark.sql.functions import lit
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from pyspark.sql.functions import col, lit
df = (spark.read.format("delta").load("/mnt/delta/Indian_Kids_Screen_Time")).toPandas()
display(df)


# COMMAND ----------

df.tail()

# COMMAND ----------

df.shape

# COMMAND ----------

df.tail()

# COMMAND ----------

df.describe()

# COMMAND ----------

df.columns

# COMMAND ----------

df.duplicated().sum()
df.isnull().sum()


# COMMAND ----------

df.info()

# COMMAND ----------

# Set style
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['Avg_Daily_Screen_Time_hr'] = pd.to_numeric(df['Avg_Daily_Screen_Time_hr'], errors='coerce')
df['Educational_to_Recreational_Ratio'] = pd.to_numeric(df['Educational_to_Recreational_Ratio'], errors='coerce')
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 1. Average Screen Time by Age
sns.barplot(x='Age', y='Avg_Daily_Screen_Time_hr', data=df, palette='Blues_d')
plt.title('Average Daily Screen Time by Age')
plt.xlabel('Age')
plt.ylabel('Average Screen Time (hrs)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

sns.countplot(data=df, x='Primary_Device',order = df['Primary_Device'].value_counts().index, palette = 'pastel')
plt.title('Primary Device')
plt.xlabel('Primary Device')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

sns.histplot(df['Educational_to_Recreational_Ratio'], kde=True, bins=20, color='skyblue')
plt.title('Distribution of Educational to Recreational Screen Time Ratio')
plt.xlabel('Edu/Recreational Ratio')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()



# COMMAND ----------

sns.countplot(data=df, y='Health_Impacts',order = df['Health_Impacts'].value_counts().index, palette = 'Set3')
plt.title('Health Impacts')
plt.xlabel('Count')
plt.ylabel('Helth Impacts')
plt.xticks(rotation=45)      
plt.tight_layout()
plt.show()





# COMMAND ----------

sns.violinplot(x='Urban_or_Rural', y='Avg_Daily_Screen_Time_hr', data=df, palette='muted')
plt.title('Screen Time Distribution by Health Impacts')
plt.xlabel('Urban_or_Rural')
plt.ylabel('Average Daily Screen Time (hrs)')
plt.xticks(rotation=45)  
plt.tight_layout()
plt.show()