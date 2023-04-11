import pandas as pd

# Load each CSV file into a pandas DataFrame
df_a = pd.read_csv('/Users/rockpang/blip/website/dataset/new_sm_summs1.csv')
df_b = pd.read_csv('/Users/rockpang/blip/website/dataset/new_va_summs1.csv')
df_c = pd.read_csv('/Users/rockpang/blip/website/dataset/new_vr_summs1.csv')

# Concatenate the DataFrames together vertically
df_concatenated = pd.concat([df_a, df_b, df_c])
print(df_a.columns)
# Write the concatenated DataFrame to a new CSV file
# df_concatenated.to_csv('/Users/rockpang/blip/website/dataset/overall.csv', index=False)
