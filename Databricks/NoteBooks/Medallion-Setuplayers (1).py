# Databricks notebook source
# MAGIC %md
# MAGIC *Bronze*
# MAGIC

# COMMAND ----------

# MAGIC %scala
# MAGIC val storageAccountName = dbutils.secrets.get(scope = "newScopeDataBricks", key = "StorageAccountName")
# MAGIC val appID = dbutils.secrets.get(scope = "newScopeDataBricks", key = "appID")
# MAGIC val secret = dbutils.secrets.get(scope = "newScopeDataBricks", key = "Secret")
# MAGIC val fileSystemName = "files"
# MAGIC val tenantID = dbutils.secrets.get(scope = "newScopeDataBricks", key = "tenantID")
# MAGIC
# MAGIC // Debug statements to verify secrets
# MAGIC println(s"Storage Account Name: $storageAccountName")
# MAGIC println(s"App ID: $appID")
# MAGIC println(s"Secret: $secret")
# MAGIC println(s"Tenant ID: $tenantID")
# MAGIC
# MAGIC // Check if any secret is null or empty
# MAGIC if (storageAccountName == null || storageAccountName.isEmpty ||
# MAGIC     appID == null || appID.isEmpty ||
# MAGIC     secret == null || secret.isEmpty ||
# MAGIC     tenantID == null || tenantID.isEmpty) {
# MAGIC   throw new IllegalArgumentException("One or more secrets are null or empty. Please check the secret values.")
# MAGIC } else {
# MAGIC   val configs = Map(
# MAGIC     s"fs.azure.account.auth.type" -> "OAuth",
# MAGIC     s"fs.azure.account.oauth.provider.type" -> "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
# MAGIC     s"fs.azure.account.oauth2.client.id" -> appID,
# MAGIC     s"fs.azure.account.oauth2.client.secret" -> secret,
# MAGIC     s"fs.azure.account.oauth2.client.endpoint" -> s"https://login.microsoftonline.com/$tenantID/oauth2/token"
# MAGIC   )
# MAGIC
# MAGIC   // Check if the directory is already mounted
# MAGIC   val mountPoint = "/mnt/files"
# MAGIC
# MAGIC   // Unmount if already mounted
# MAGIC   if (dbutils.fs.mounts().map(_.mountPoint).contains(mountPoint)) {
# MAGIC     dbutils.fs.unmount(mountPoint)
# MAGIC   }
# MAGIC
# MAGIC   // Mount the ADLS Gen2 storage
# MAGIC   dbutils.fs.mount(
# MAGIC     source = s"abfss://$fileSystemName@$storageAccountName.dfs.core.windows.net/",
# MAGIC     mountPoint = mountPoint,
# MAGIC     extraConfigs = configs
# MAGIC   )
# MAGIC }

# COMMAND ----------

# MAGIC %md
# MAGIC *Silver*

# COMMAND ----------

# MAGIC %scala
# MAGIC val storageAccountName = dbutils.secrets.get(scope ="newScopeDataBricks", key ="StorageAccountName")
# MAGIC val appID = dbutils.secrets.get(scope = "newScopeDataBricks", key = "appID")
# MAGIC val secret = dbutils.secrets.get(scope = "newScopeDataBricks", key = "Secret")
# MAGIC val fileSystemName = "silver"
# MAGIC val tenantID = dbutils.secrets.get(scope = "newScopeDataBricks", key = "tenantID")
# MAGIC
# MAGIC val configs = Map(
# MAGIC   s"fs.azure.account.auth.type" -> "OAuth",
# MAGIC   s"fs.azure.account.oauth.provider.type" -> "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
# MAGIC   s"fs.azure.account.oauth2.client.id" -> appID,
# MAGIC   s"fs.azure.account.oauth2.client.secret" -> secret,
# MAGIC   s"fs.azure.account.oauth2.client.endpoint" -> s"https://login.microsoftonline.com/$tenantID/oauth2/token"
# MAGIC )
# MAGIC
# MAGIC // Check if the directory is already mounted
# MAGIC val mountPoint = "/mnt/silver"
# MAGIC
# MAGIC // Mount the ADLS Gen2 storage
# MAGIC dbutils.fs.mount(
# MAGIC   source = s"abfss://"+fileSystemName+"@"+storageAccountName+".dfs.core.windows.net/",
# MAGIC   mountPoint = mountPoint,
# MAGIC   extraConfigs = configs
# MAGIC )

# COMMAND ----------

# MAGIC %md
# MAGIC *Gold*

# COMMAND ----------

# MAGIC %scala
# MAGIC val storageAccountName = dbutils.secrets.get(scope ="newScopeDataBricks", key ="StorageAccountName")
# MAGIC val appID = dbutils.secrets.get(scope = "newScopeDataBricks", key = "appID")
# MAGIC val secret = dbutils.secrets.get(scope = "newScopeDataBricks", key = "Secret")
# MAGIC val fileSystemName = "gold"
# MAGIC val tenantID = dbutils.secrets.get(scope = "newScopeDataBricks", key = "tenantID")
# MAGIC
# MAGIC val configs = Map(
# MAGIC   s"fs.azure.account.auth.type" -> "OAuth",
# MAGIC   s"fs.azure.account.oauth.provider.type" -> "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
# MAGIC   s"fs.azure.account.oauth2.client.id" -> appID,
# MAGIC   s"fs.azure.account.oauth2.client.secret" -> secret,
# MAGIC   s"fs.azure.account.oauth2.client.endpoint" -> s"https://login.microsoftonline.com/$tenantID/oauth2/token"
# MAGIC )
# MAGIC
# MAGIC // Check if the directory is already mounted
# MAGIC val mountPoint = "/mnt/gold"
# MAGIC
# MAGIC // Mount the ADLS Gen2 storage
# MAGIC dbutils.fs.mount(
# MAGIC   source = s"abfss://"+fileSystemName+"@"+storageAccountName+".dfs.core.windows.net/",
# MAGIC   mountPoint = mountPoint,
# MAGIC   extraConfigs = configs
# MAGIC )