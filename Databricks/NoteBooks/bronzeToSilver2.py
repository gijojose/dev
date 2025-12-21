# Databricks notebook source
from pyspark.sql.functions import date_format, when, length, col
dbutils.widgets.text("bronzepath", "")
dbutils.widgets.text("silverpath", "")
dbutils.widgets.text("goldpath", "")


bronzepath = dbutils.widgets.get("bronzepath")
silverpath = dbutils.widgets.get("silverpath")
goldpath = dbutils.widgets.get("goldpath")

for f in dbutils.fs.ls(bronzepath):
  print(f.name)
  df = spark.read.parquet(bronzepath+'/'+f.name) 
  display(df)
