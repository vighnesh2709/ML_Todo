import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from flask import Flask, jsonify
import csv
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
@app.route("/<priority_input>/<finish_date>")
def testing(priority_input, finish_date):
    # Load the data
    file_path = '/home/vighnesh/Desktop/ML_Todo/backend/TestData - Sheet1.csv'
    df = pd.read_csv(file_path)

    # Convert 'Finish_Date' to datetime format
    df['Finish_Date'] = pd.to_datetime(df['Finish_Date'])

    # Drop unnecessary columns
    df = df.drop(['Task'], axis=1)

    # Print the number of NaN values in the 'Completed' column
    nan_count = df['Completed'].isna().sum()
    print(f"Number of NaN values in 'Completed' column: {nan_count}")

    # Handle NaN values in the 'Completed' column
    df = df.dropna(subset=['Completed'])

    # Print the number of rows dropped
    rows_dropped = nan_count
    print(f"Number of rows dropped: {rows_dropped}")

    # Define features and target variable
    X = df[['Priority', 'Finish_Date']]
    y = df['Completed']

    # Preprocess features (standardize 'Finish_Date' and one-hot encode 'Priority')
    preprocessor = ColumnTransformer(
        transformers=[
            ('date', StandardScaler(), ['Finish_Date']),
            ('priority', OneHotEncoder(handle_unknown='ignore', categories='auto'), ['Priority'])
        ],
        remainder='passthrough'
    )

    # Create a pipeline with logistic regression model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression())
    ])

    # Train the model
    model.fit(X, y)

    # Create a new DataFrame with the input features for a new value
    if priority_input == 'low':
        Priority = 0
    elif priority_input == 'medium':
        Priority = 1
    elif priority_input == 'high':
        Priority = 2
    else:
        print("Invalid priority option. Please choose 'low', 'medium', or 'high'.")

    new_test_data = pd.DataFrame({'Priority': [Priority], 'Finish_Date': [finish_date]})

    # Convert 'Finish_Date' to datetime format
    new_test_data['Finish_Date'] = pd.to_datetime(new_test_data['Finish_Date'])

    # Display the new data
    print("\nNew Data:")
    print(new_test_data)

    # Make predictions for the new value
    new_value_pred = model.predict(new_test_data)

    # Convert the predicted value to an integer
    predicted_value_str = int(new_value_pred[0])

    print(f"The predicted value is {predicted_value_str}")

    return f"<h1>The predicted value is {predicted_value_str}</h1>"


@app.route("/add_todo/<task>/<priority>/<finish_Date>/<completed>")
def add_todo(task, priority, finish_Date, completed):
    try:
        completed = None if completed.lower() == 'null' else completed

        # Ensure file_path is correct without leading whitespace
        file_path = '/home/vighnesh/Desktop/ML_Todo/backend/TestData - Sheet1.csv'

        new_data = [task, finish_Date, priority, completed]
        with open(file_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(new_data)

        df = pd.read_csv(file_path)
        nan_rows = df[df["Completed"].isnull()]
        json_result = nan_rows.to_json(orient='records')
        json_object = json.loads(json_result)

        return jsonify(json_object)
    except Exception as e:
        app.logger.error(f"Error in add_todo route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
