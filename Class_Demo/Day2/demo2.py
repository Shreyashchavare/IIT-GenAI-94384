import pandas as pd
import pandasql as ps

filepath = "emp_hdr.csv"
df = pd.read_csv(filepath)
print("Dataframe column Types: ")
print(df.dtypes)
print("\nEMP Data: ")
print(df)
query = "SELECT job, SUM(sal) total FROM data GROUP BY job"
result = ps.sqldf(query,{"data" : df})
print("Query result: ")
print(result)
