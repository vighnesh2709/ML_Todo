import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

def Testing():
    file_path = '/home/vighnesh/Desktop/ML_Todo/backend/TestData - Sheet1.csv'
    df = pd.read_csv(file_path)
    print(df)

Testing()
