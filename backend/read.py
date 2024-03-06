import pandas as pd

# Load the dataset from the CSV file
file_path = '/home/vighnesh/Desktop/ml_todo/TestData - Sheet1.csv'
df = pd.read_csv(file_path)

# Display the original dataset
print("Original Dataset:")
print(df)

# Convert 'Finish_Date' to datetime format
df['Finish_Date'] = pd.to_datetime(df['Finish_Date'])

# Use a loop to update 'Priority' column
for i in range(len(df)):
    if df.at[i, "Priority"] == 'low':
        df.at[i, "Priority"] = 0
    elif df.at[i, "Priority"] == 'medium':
        df.at[i, "Priority"] = 1
    elif df.at[i, "Priority"] == 'high':
        df.at[i, "Priority"] = 2

# Display the modified dataset after updating 'Priority'
print("\nModified Dataset (After Updating Priority):")
print(df)

# Rename the 'Task' column to match the desired format
df['Task'] = ['Task' + str(i + 1) for i in range(len(df))]

# Reorder columns with 'Task' as the first one
df = df[['Task', 'Finish_Date', 'Priority', 'Completed']]

# Save the modified DataFrame back to the same file
df.to_csv(file_path, index=False)

# Display the final modified dataset
print("\nFinal Modified Dataset:")
print(df)
