import pandas as pd

# Load dataset
input_filename = "/Users/matthewrickard/Desktop/Python/YearTest1.csv"
output_filename = "/Users/matthewrickard/Desktop/Python/remaining_amounts.csv"
df = pd.read_csv(input_filename)

# Ensure the date column is of datetime type with format 'YYYY/MM'
df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m')

# Preliminary step: Calculate the sum of amounts by year
df['Year'] = df['Date'].dt.year
yearly_sum = df.groupby('Year')['Amount'].sum()

# Set a small threshold for floating-point precision
threshold = 1e-9

# Identify and exclude years where the sum of amounts is close to zero
zero_sum_years = yearly_sum[abs(yearly_sum) < threshold].index
print(f"Years with zero sum: {zero_sum_years}")

df = df[~df['Year'].isin(zero_sum_years)]

# Function to filter out offsetting values and return remaining amounts
def filter_offsetting_values(df):
    used_indices = set()
    amount_dict = {}

    for i, row in df.iterrows():
        amount = row['Amount']

        if i not in used_indices:
            if -amount in amount_dict:
                offsetting_index = amount_dict[-amount].pop(0)
                if not amount_dict[-amount]:  # Remove key if list is empty
                    del amount_dict[-amount]
                used_indices.add(i)
                used_indices.add(offsetting_index)
            else:
                if amount not in amount_dict:
                    amount_dict[amount] = []
                amount_dict[amount].append(i)

    remaining_indices = list(set(df.index) - used_indices)
    return df.loc[remaining_indices]

# Step 1: Filter offsetting values by month
df['YearMonth'] = df['Date'].dt.to_period('M')
filtered_by_month_dfs = []

for name, group in df.groupby('YearMonth'):
    filtered_group = filter_offsetting_values(group)
    filtered_by_month_dfs.append(filtered_group)

# Combine all filtered groups from the first step
filter1_df = pd.concat(filtered_by_month_dfs)

# Step 2: Filter offsetting values by year from filter1_df
filter1_df['Year'] = filter1_df['Date'].dt.year
filtered_by_year_dfs = []

for name, group in filter1_df.groupby('Year'):
    filtered_group = filter_offsetting_values(group)
    filtered_by_year_dfs.append(filtered_group)

# Combine all filtered groups from the second step
filter2_df = pd.concat(filtered_by_year_dfs)

# Step 3: Filter offsetting values for all remaining data from filter2_df
final_filtered_df = filter_offsetting_values(filter2_df)

# Select the remaining amounts with their corresponding document numbers and dates
remaining_df = final_filtered_df.loc[:, ['Date', 'Document Number', 'Amount']]

# Sort the remaining rows by date in chronological order
remaining_df = remaining_df.sort_values(by='Date')

# Convert date to 'YYYY/MM' format
remaining_df['Date'] = remaining_df['Date'].dt.strftime('%Y/%m')

# Export results to a CSV file
remaining_df.to_csv(output_filename, index=False)
print(f"Exported remaining amounts to {output_filename}")

print("Processing finished.")
