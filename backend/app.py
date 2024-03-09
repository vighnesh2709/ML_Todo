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
