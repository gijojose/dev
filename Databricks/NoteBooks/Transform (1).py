# Databricks notebook source
alltables = []
bronzepath = "/mnt/bronze/SalesLT"
silverpath = "/mnt/silver/SalesLT"
goldpath = "/mnt/gold/SalesLT"

for f in dbutils.fs.ls(silverpath):
    print(f.path)