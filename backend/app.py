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
@app.route("/get_tasks")
def Landing():
    file_path = '/home/vighnesh/Desktop/ML_Todo/backend/TestData - Sheet1.csv'
    df = pd.read_csv(file_path)
    nan_rows = df[df["Completed"].isnull()]
    json_result = nan_rows.to_json(orient='records')
    json_object = json.loads(json_result)

    return jsonify(json_object)



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

    return (predicted_value_str)



@app.route("/add_todo/<task>/<priority_input>/<finish_Date>/<completed>",methods=['POST'])
def add_todo(task, priority_input, finish_Date, completed):
    try:
        completed = None if completed.lower() == 'null' else completed

        file_path = '/home/vighnesh/Desktop/ML_Todo/backend/TestData - Sheet1.csv'

        if priority_input == 'low':
            priority = 0
        elif priority_input == 'medium':
            priority = 1
        else:
            priority = 2

        df = pd.read_csv(file_path)

        id = len(df) + 1

        prediction=testing(priority_input,finish_Date)

        new_data = [id, task, finish_Date, priority, completed,prediction]
        with open(file_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(new_data)
    except Exception as e:
        print({e})
        '''
        nan_rows = df[df["Completed"].isnull()]
        json_result = nan_rows.to_json(orient='records')
        json_object = json.loads(json_result)

        return jsonify(json_object)
    except Exception as e:
        app.logger.error(f"Error in add_todo route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500'''


@app.route("/completed/<Task>/<Date>/<id>")
def Completed(Task, Date, id):
    file_path = '/home/vighnesh/Desktop/ML_Todo/backend/TestData - Sheet1.csv'
    df = pd.read_csv(file_path)

    # Convert 'id' to an integer
    id = int(id) - 1

    if 0 <= id < len(df):
        if (df.loc[id, "Task"] == Task) and (df.loc[id, "Finish_Date"] == Date):
            # Update the "Completed" column value to 1 using loc
            df.loc[id, "Completed"] = 1

            # Save the updated DataFrame back to the CSV file
            try:
                df.to_csv(file_path, index=False)
            except Exception as e:
                return jsonify({"error": f"Failed to write to CSV file: {e}"}), 500  # 500 Internal Server Error

            # Return a JSON response with the updated row
            updated_row = df.loc[id].to_dict()
            return jsonify({"message": "Data updated successfully", "updated_row": updated_row})
        else:
            # If the conditions are not met, return an error message
            return jsonify({"error": "Invalid Task or Date"}), 400  # 400 Bad Request
    else:
        # If the index is out of bounds, return an error message
        return jsonify({"error": "Invalid index"}), 400  # 400 Bad Request



if __name__ == "__main__":
    app.run(debug=True)

