import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

def testing(priority, finish_date):
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
    new_test_data = pd.DataFrame({'Priority': [priority], 'Finish_Date': [finish_date]})

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

    return(f"<h1>the predicted value is {predicted_value_str}</h1>")

# Example usage
new_priority = 2
new_finish_date = '2024-03-01'
result = testing(new_priority, new_finish_date)
print(result)
