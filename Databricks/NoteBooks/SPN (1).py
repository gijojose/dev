# Databricks notebook source
# MAGIC %scala
# MAGIC val storageAccountName = dbutils.secrets.get(scope ="keyvaultscope", key ="StorageAccountName")
# MAGIC val appID = dbutils.secrets.get(scope = "keyvaultscope", key = "appID")
# MAGIC val secret = dbutils.secrets.get(scope = "keyvaultscope", key = "Secret")
# MAGIC val fileSystemName = dbutils.secrets.get(scope = "keyvaultscope", key = "FileSystemName")
# MAGIC val tenantID = dbutils.secrets.get(scope = "keyvaultscope", key = "tenantID")
# MAGIC

# COMMAND ----------

# MAGIC %scala
# MAGIC spark.conf.set("fs.azure.account.auth.type." + storageAccountName + ".dfs.core.windows.net", "OAuth")
# MAGIC spark.conf.set("fs.azure.account.oauth.provider.type." + storageAccountName + ".dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.id." + storageAccountName + ".dfs.core.windows.net", appID)
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.secret." + storageAccountName + ".dfs.core.windows.net", secret)
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.endpoint." + storageAccountName + ".dfs.core.windows.net", "https://login.microsoftonline.com/" + tenantID + "/oauth2/token")

# COMMAND ----------

# MAGIC %scala
# MAGIC
# MAGIC
# MAGIC val df = spark.read.format("csv")
# MAGIC   .option("header", "true")
# MAGIC   .load(s"abfss://"+fileSystemName+"@"+storageAccountName+".dfs.core.windows.net/cars.csv")
# MAGIC
# MAGIC display(df)
# MAGIC

# COMMAND ----------

# MAGIC %scala
# MAGIC val fileSystemName = "yourFileSystemName"
# MAGIC val storageAccountName = "yourStorageAccountName"
# MAGIC val clientId = "yourClientId"
# MAGIC val tenantId = "yourTenantId"
# MAGIC val clientSecret = "yourClientSecret"
# MAGIC
# MAGIC spark.conf.set("fs.azure.account.auth.type." + storageAccountName + ".dfs.core.windows.net", "OAuth")
# MAGIC spark.conf.set("fs.azure.account.oauth.provider.type." + storageAccountName + ".dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.id." + storageAccountName + ".dfs.core.windows.net", clientId)
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.secret." + storageAccountName + ".dfs.core.windows.net", clientSecret)
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.endpoint." + storageAccountName + ".dfs.core.windows.net", s"https://login.microsoftonline.com/$tenantId/oauth2/token")
# MAGIC
# MAGIC val df = spark.read.format("csv")
# MAGIC   .option("header", "true")
# MAGIC   .load(s"abfss://$fileSystemName@$storageAccountName.dfs.core.windows.net/Files/cars.csv")
# MAGIC
# MAGIC display(df)

# COMMAND ----------

# MAGIC %scala
# MAGIC df.createOrReplaceTempView("cars")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from cars

# COMMAND ----------

# MAGIC %scala
# MAGIC val storageAccountName = dbutils.secrets.get(scope ="myscope_gijo", key ="StorageAccountName")
# MAGIC val appID = dbutils.secrets.get(scope = "myscope_gijo", key = "appID")
# MAGIC val secret = dbutils.secrets.get(scope = "myscope_gijo", key = "Secret")
# MAGIC val fileSystemName = dbutils.secrets.get(scope = "myscope_gijo", key = "FileSystemName")
# MAGIC val tenantID = dbutils.secrets.get(scope = "myscope_gijo", key = "tenantID")
# MAGIC
# MAGIC // Set up the configurations
# MAGIC val configs = Map(
# MAGIC   s"fs.azure.account.auth.type" -> "OAuth",
# MAGIC   s"fs.azure.account.oauth.provider.type" -> "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
# MAGIC   s"fs.azure.account.oauth2.client.id" -> appID,
# MAGIC   s"fs.azure.account.oauth2.client.secret" -> secret,
# MAGIC   s"fs.azure.account.oauth2.client.endpoint" -> s"https://login.microsoftonline.com/$tenantID/oauth2/token"
# MAGIC )
# MAGIC
# MAGIC // Check if the directory is already mounted
# MAGIC val mountPoint = "/mnt/files"
# MAGIC if (dbutils.fs.mounts().map(_.mountPoint).contains(mountPoint)) {
# MAGIC   dbutils.fs.unmount(mountPoint)
# MAGIC }
# MAGIC
# MAGIC // Mount the ADLS Gen2 storage
# MAGIC dbutils.fs.mount(
# MAGIC   source = s"abfss://"+fileSystemName+"@"+storageAccountName+".dfs.core.windows.net/",
# MAGIC   mountPoint = mountPoint,
# MAGIC   extraConfigs = configs
# MAGIC )
# MAGIC
# MAGIC val df4 = spark.read.format("csv")
# MAGIC   .option("header", "true")
# MAGIC   .load("/mnt/files/Files/cars.csv")
# MAGIC
# MAGIC display(df4)

# COMMAND ----------

# MAGIC %scala
# MAGIC dbutils.widgets.dropdown(
# MAGIC   "input",
# MAGIC   "true",
# MAGIC   Array("true", "false")
# MAGIC )

# COMMAND ----------

outputvalue = dbutils.widgets.get("input")
print(outputvalue)