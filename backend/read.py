import pandas as pd
import json

# Load the dataset from the CSV file
file_path = '/home/vighnesh/Desktop/ML_Todo/backend/TestData - Sheet1.csv'
df = pd.read_csv(file_path)

'''# Filter rows with NaN values in the 'Completed' column
nan_rows = df[df["Completed"].isnull()]

# Convert the DataFrame to JSON
json_result = nan_rows.to_json(orient='records')

json_object = json.loads(json_result)'''
