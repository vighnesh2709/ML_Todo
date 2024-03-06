import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from flask import Flask
import csv
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/<priority>/<finish_date>")
def testing(priority, finish_date):
    # Load the dataset from the CSV file
    file_path = '/home/vighnesh/Desktop/ml_todo/test_data_2.csv'
    df = pd.read_csv(file_path)

    # Convert 'Finish_Date' to datetime format
    df['Finish_Date'] = pd.to_datetime(df['Finish_Date'])

    # Drop unnecessary columns
    df = df.drop(['Task'], axis=1)

    # Define features and target variable
    X = df[['Priority', 'Finish_Date']]
    y = df['Completed']

    # Preprocess features (standardize 'Finish_Date' and one-hot encode 'Priority')
    preprocessor = ColumnTransformer(
        transformers=[
            ('date', StandardScaler(), ['Finish_Date']),
            ('priority', OneHotEncoder(handle_unknown='ignore'), ['Priority'])
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
    new_test_data = pd.DataFrame({'Priority': [priority], 'Finish_Date': [finish_date]})

    # Convert 'Finish_Date' to datetime format
    new_test_data['Finish_Date'] = pd.to_datetime(new_test_data['Finish_Date'])

    # Display the new data
    print("\nNew Data:")
    print(new_test_data)

    # Make predictions for the new value
    new_value_pred = model.predict(new_test_data)

    return f'<h1>Prediction for New Value: {new_value_pred[0]}</h1>'

@app.route("/add_todo/<task>/<priority>/<finish_Date>/<completed>")
def add_todo(task,priority,finish_Date,completed):
    
    file_path = '/home/vighnesh/Desktop/ml_todo/TestData - Sheet1.csv'
    new_data = [task, finish_Date, priority,completed]
    with open(file_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(new_data)




if __name__ == "__main__":
    app.run(debug=True)
