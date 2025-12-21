# Databricks notebook source
parquet_file_path = "/mnt/silver/SalesLT/Address"

# Read the Parquet file into a DataFrame
df = spark.read.format('delta').load(parquet_file_path)

# Display the DataFrame
display(df)

# COMMAND ----------

dbutils.widgets.text("bronzepath", "")
dbutils.widgets.text("silverpath", "")
dbutils.widgets.text("goldpath", "")

alltables = []
bronzepath = dbutils.widgets.get("bronzepath")
silverpath = dbutils.widgets.get("silverpath")
goldpath = dbutils.widgets.get("goldpath")

for f in dbutils.fs.ls(silverpath):
    # Read the Parquet file into a DataFrame
    df = spark.read.format('delta').load(f.path)
    headers =[]
    headers = df.columns
    Temp = ""
    
    for header in headers:
        Temp = ''.join(['_' + c if c.isupper() and i > 0 and header[i-1].islower() else c for i, c in enumerate(header)])
        df = df.withColumnRenamed(header, Temp)
        
    df.write.format("delta").save(goldpath + "/" + f.name)
    Temp = ""
        