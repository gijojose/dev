# Databricks notebook source
# MAGIC %scala
# MAGIC def readFileFromADLS(appID: String,
# MAGIC                       secret: String,
# MAGIC                       StorageAccountName: String,
# MAGIC                       FileSystemName: String,
# MAGIC                       tenantID: String,
# MAGIC                       fileName: String,
# MAGIC                       fileType: String): 
# MAGIC                       org.apache.spark.sql.DataFrame = {
# MAGIC     val appIDValue = dbutils.secrets.get(scope = "newScopeDataBricks", key = appID)
# MAGIC     val secretValue = dbutils.secrets.get(scope = "newScopeDataBricks", key = secret)
# MAGIC     val StorageAccountNameValue = dbutils.secrets.get(scope = "newScopeDataBricks", key = StorageAccountName)
# MAGIC     val tenantIDValue = dbutils.secrets.get(scope = "newScopeDataBricks", key = tenantID)
# MAGIC
# MAGIC     spark.conf.set(s"fs.azure.account.auth.type.$StorageAccountNameValue.dfs.core.windows.net", "OAuth")
# MAGIC     spark.conf.set(s"fs.azure.account.oauth.provider.type.$StorageAccountNameValue.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
# MAGIC     spark.conf.set(s"fs.azure.account.oauth2.client.id.$StorageAccountNameValue.dfs.core.windows.net", appIDValue)
# MAGIC     spark.conf.set(s"fs.azure.account.oauth2.client.secret.$StorageAccountNameValue.dfs.core.windows.net", secretValue)
# MAGIC     spark.conf.set(s"fs.azure.account.oauth2.client.endpoint.$StorageAccountNameValue.dfs.core.windows.net", s"https://login.microsoftonline.com/$tenantIDValue/oauth2/token")
# MAGIC
# MAGIC     val filePath = s"abfss://$FileSystemName@$StorageAccountNameValue.dfs.core.windows.net/$fileName"
# MAGIC     val df = spark.read.format(fileType).option("header", "true").load(filePath)
# MAGIC     df
# MAGIC }
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %scala
# MAGIC val df = readFileFromADLS(
# MAGIC   appID = "appID",
# MAGIC   secret = "secret",
# MAGIC   StorageAccountName = "storageAccountName",
# MAGIC   FileSystemName = "files",
# MAGIC   tenantID = "tenantID",
# MAGIC   fileName ="global_student_migration.csv",
# MAGIC   fileType = "csv"
# MAGIC )
# MAGIC
# MAGIC df.createOrReplaceTempView("global_student_migration")
# MAGIC

# COMMAND ----------

import pandas as pd
from pyspark.sql.functions import lit
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

df3 = spark.sql("""
    SELECT distinct a.origin_country, a.destination_country, c.Count AS CountryCount, t.TotalCountSum  AS Total, ROUND((c.Count/t.TotalCountSum)*100,2) AS Percentage
    FROM global_student_migration a 
    INNER JOIN (
        SELECT origin_country, SUM(TotalCount) AS TotalCountSum 
        FROM (
            SELECT origin_country, destination_country, COUNT(*) AS TotalCount 
            FROM global_student_migration 
            GROUP BY origin_country, destination_country
        ) 
        GROUP BY origin_country
    ) t ON a.origin_country = t.origin_country
    INNER JOIN (
        SELECT origin_country, destination_country, COUNT(*) AS Count 
        FROM global_student_migration 
        GROUP BY origin_country, destination_country
    ) c ON c.origin_country = a.origin_country AND c.destination_country = a.destination_country
    order by a.origin_country
""")
display(df3)

df4=df3.toPandas()
df4.describe()

sns.set(style="darkgrid")
plt.rcParams['figure.figsize'] = (15, 10)
sns.barplot(x="origin_country", y="Total", data=df4)
plt.xticks(rotation=90)
plt.title("Percentage of Students who migrated from each country")
plt.xlabel("Country")
plt.ylabel("Total")
plt.tight_layout
plt.show()




# COMMAND ----------

# MAGIC %scala
# MAGIC spark.udf.register("readFileFromADLS", readFileFromADLS)

# COMMAND ----------



