# Databricks notebook source
from pyspark.sql.functions import date_format, when, length, col
dbutils.widgets.text("bronzepath", "")
dbutils.widgets.text("silverpath", "")
dbutils.widgets.text("goldpath", "")

alltables = []
bronzepath = dbutils.widgets.get("bronzepath")
silverpath = dbutils.widgets.get("silverpath")
goldpath = dbutils.widgets.get("goldpath")


for f in dbutils.fs.ls(bronzepath):
    alltables.append(f.name)
    
    # Read the Parquet file into a DataFrame
    df = spark.read.parquet(bronzepath + "/" + f.name)
    for col in df.columns:
        if "Date" in col or "date" in col:
            df = df.withColumn(col, date_format("ModifiedDate", "yyyy-MM-dd"))
            print("Transformation applied on " + col + " "+f.name )
    
    # Check if the column 'PostalCode' exists before applying transformations
        if 'PostalCode' in col:
            df = df.withColumn(
                col,
                when((length(col) >= 5),col
                ).otherwise("Wrong Postal Code")
            )
            print("Transformation applied on " + col + " "+f.name )
    df.write.format("Delta").mode("overwrite").save(silverpath + "/" + f.name)