import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def run_ml_pipeline():
    print("Loading data...")
    df = pd.read_csv('property_data.csv')

    print("Performing EDA...")
    # Basic EDA metrics
    print(df.describe())
    
    # Save a price distribution plot
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Price'], kde=True, bins=30)
    plt.title('Property Price Distribution')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.savefig('price_distribution.png')
    print("Saved price distribution plot to 'price_distribution.png'")

    print("Preparing data for modeling...")
    # Features (X) and Target (y)
    # Exclude Property_ID and Price_Segment/Price_per_sqft (as they leak info about Price)
    features = ['Location', 'Area_sqft', 'Bedrooms', 'Bathrooms', 'Age', 
                'Parking', 'Gym', 'Swimming_Pool', 'Security', 'Property_Type', 
                'Floor', 'Total_Floors']
    
    X = df[features].copy()
    y = df['Price']

    # Handle missing values if any
    X['Bedrooms'] = X['Bedrooms'].fillna(X['Bedrooms'].median())

    # Categorical columns that need encoding
    categorical_cols = ['Location', 'Parking', 'Gym', 'Swimming_Pool', 'Security', 'Property_Type']

    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_cols)
        ],
        remainder='passthrough'
    )

    # Modeling pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    print("Splitting dataset into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Linear Regression model...")
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n--- Model Results ---")
    print(f"R-squared: {r2:.4f}")
    print(f"Mean Absolute Error (MAE): Rs. {mae:,.2f}")

    # Save model
    joblib.dump(model, 'house_price_model.pkl')
    print("Model saved to 'house_price_model.pkl'")

    # Sample Prediction
    sample = X_test.iloc[[0]]
    actual_price = y_test.iloc[0]
    predicted_price = model.predict(sample)[0]
    
    print(f"\n--- Sample Prediction to Answer Business Question ---")
    print(f"Property Details: {sample.to_dict('records')[0]}")
    print(f"Expected Market Price (Predicted): Rs. {predicted_price:,.2f}")
    print(f"Actual Price: Rs. {actual_price:,.2f}")

if __name__ == "__main__":
    run_ml_pipeline()
