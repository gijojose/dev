# Databricks notebook source
storage_account_name = "storagegijo"
container_name = "files"
file_name ="cars.csv"
storage_account_access_key ="RQVhOrnWbE02++dlmxLB73I2IUnABrkp2Vifp1ofcOhGw6CrAAVo+g1staBeYb7szbp/zSnU+FlR+AStMkQYvA=="
file_type ="csv"
file_location = "wasbs://"+container_name+"@"+storage_account_name+".blob.core.windows.net/"+""+file_name



# COMMAND ----------

spark.conf.set("fs.azure.account.key."+storage_account_name+".blob.core.windows.net", storage_account_access_key)
df=spark.read.format('csv').option("header", "true").option("inferSchema", "true").load(file_location)
display(df)

# COMMAND ----------

from pyspark.sql.functions import col, lit
df_updated = df.withColumn("mileage", col("mileage")+100)
display(df_updated)


# COMMAND ----------

# MAGIC %md
# MAGIC Create and Select table
# MAGIC

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

employee_schema = StructType([StructField("EmployeeID", IntegerType(), True), StructField("FirstName", StringType(), True), StructField("LastName", StringType(), True), StructField("Gender", StringType(), True), StructField("Salary", IntegerType(), True), StructField("Department", StringType(), True)])

df_employee = spark.createDataFrame([(1, "John", "Doe", "Male", 10000, "IT"), 
                                     (2, "Jane", "Doe", "Female", 12000, "HR"), 
                                     (3, "Mike", "Smith", "Male", 15000, "IT"), 
                                     (4, "Sara", "Johnson", "Female", 18000, "Finance"),
                                    (5, "Peter", "Parker", "Male", 20000, "IT"),
                                    (6, "Bruce", "Wayne", "Male", 25000, "IT")
                                    ],employee_schema)
display(df_employee)

# COMMAND ----------

from pyspark.sql.functions import when,col
df_employee2 = df_employee.withColumn("Gender", when(col("Gender") == "Male", "M").otherwise("F"))
display(df_employee2)

# COMMAND ----------

df_employeeFiltered = df_employee2.filter(df_employee2.FirstName.contains("J") | df_employee2.FirstName.contains("M") | df_employee2.FirstName.contains("S"))
display(df_employeeFiltered)

# COMMAND ----------

df_employeeFiltered.createOrReplaceTempView("employee_filtered_view")



# COMMAND ----------

# MAGIC %sql
# MAGIC select * from employee_filtered_view ;

# COMMAND ----------

File_Name ="5000 Sales Records.csv"
File_Type ="csv"
Storage_Account_Name ="storagegijo01"
Storage_Account_Access_Key ="utI6iF3AhfRLW0fZR5Db5yqu6Tg/+B3YLvd2gRUFiDvwmHLA3A/KLqW4f8Jo+83bVxmLNFEJa/0Y+AStDWIZww=="
Container_Name ="cont01"
File_Location = "wasbs://"+Container_Name+"@"+Storage_Account_Name+".blob.core.windows.net/"+"Files/"+File_Name

# COMMAND ----------

spark.conf.set("fs.azure.account.key."+Storage_Account_Name+".blob.core.windows.net", Storage_Account_Access_Key)
df = spark.read.format(File_Type).option("header", "true").option("inferSchema", "true").load(File_Location)
display(df)

# COMMAND ----------

df.createOrReplaceTempView("sales_records_view")



# COMMAND ----------

# MAGIC %sql
# MAGIC select * from sales_records_view ;
# MAGIC select country, ROUND(sum(`Total Profit`),2) as total_profit from sales_records_view
# MAGIC group by country
# MAGIC order by total_profit desc ;

# COMMAND ----------

from pyspark.sql.functions import when, col, lit
df_employee2 = df_employee.withColumn("Gender", when(col("Gender") == "Male", "M").otherwise("F"))
df3=df.withColumn("Profit_Type", lit(""))
df3=df3.withColumn("Profit_Type", when(col("Units Sold") > 5000, "High").when(col("Units Sold") < 5000, "Medium").otherwise("Low"))
display(df3)