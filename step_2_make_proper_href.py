import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('dis_man_1.csv')

# Define a function to prepend the base URL to each href value
def add_base_url(href):
    base_url = 'https://shop.adidas.jp'
    return f'{base_url}{href}'

# Apply the function to create a new column with the complete URLs
df['complete_url'] = df['href'].apply(add_base_url)

# Print the modified DataFrame
# print(df)
df.to_csv('dis_man_1_href.csv', index=False)
