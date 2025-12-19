import pandas as pd

"""Q3:
    Given a CSV file Products.csv with columns:
    Write a Python program to:

    a) Read the CSV

    b) Print each row in a clean format

    c) Total number of rows

    d) Total number of products priced above 500
    e) Average price of all products
    f) List all products belonging to a specific category (user input)
    g) Total quantity of all items in stock"""
# read csv
df = pd.read_csv("products.csv")

# print each row 
print("\n---- Product Deatails ----")
for i, r in df.iterrows():
    print(r['product_id'], r['product_name'], r['price'], r['category'], r['quantity'])

# c) number of rows
total_rows = len(df)
print(f"\nTotal number of rows: {total_rows}")

# d) Total number of products priced above 500

above_500 = df[df['price'] > 500]
print(f"Number of products priced above 500: {len(above_500)}")

# e) average price of all products 
avg_price = df['price'].mean()
print(f"Average price of all products: {avg_price}")

# f) List of all product belonging to specific category(user input)
category = input("\n Enter a category to filter products: ")
filtered = df[df['category'].str.lower() == category.lower()]

print(f"\nProduct in a category '{category}': ")
if filtered.empty:
    print("No products found in this category.")
else:
    print(filtered)

# g) Total quantity of all items in stock
total_quantity = df['quantity'].sum()
print(f"\nTotal quantity of all items in stock:{total_quantity}")
