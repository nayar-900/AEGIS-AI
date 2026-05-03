import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
# ADDED NEW MODELS FOR COMPARISON
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from utils.data_processor import fetch_latest_earthquakes, purify_data

st.set_page_config(page_title="AI Training Module", layout="wide")

st.title("AI Model Training & Validation")
st.markdown("""
This module trains and compares multiple Machine Learning models to correlate earthquake **Magnitude** and **Depth**. 
We use **K-Fold Cross-Validation** and **Comparative Analysis** to select the most accurate predictor.
""")

# 1. Data Loading
st.header("1. Data Preparation")
if st.button("Fetch & Purify Training Data"):
    raw_df = fetch_latest_earthquakes()
    if raw_df is not None:
        df = purify_data(raw_df)
        st.session_state['train_df'] = df
        st.success(f"Prepared {len(df)} records for training.")
        st.write(df.head())
    else:
        st.error("Failed to fetch data.")

# 2. Training Logic
if 'train_df' in st.session_state:
    df = st.session_state['train_df']
    
    st.header("2. Model Training & Comparative Analysis")
    
    X = df[['depth', 'latitude', 'longitude']]
    y = df['magnitude']
    
    col1, col2 = st.columns(2)
    test_size = col1.slider("Test Set Size (Hold-out)", 0.1, 0.5, 0.2)
    n_trees = col2.number_input("Number of Trees (Random Forest)", 10, 500, 100)

    if st.button("Run Training & Compare Models"):
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # Define the model dictionary for comparison
        models = {
            "Random Forest": RandomForestRegressor(n_estimators=n_trees, random_state=42),
            "Linear Regression": LinearRegression(),
            "Decision Tree": DecisionTreeRegressor(random_state=42)
        }
        
        comparison_results = []
        best_r2 = -float('inf')
        best_model = None

        st.subheader("Comparative Performance Results")
        
        # Iterate through models to find the best performer
        for name, model in models.items():
            # Cross-Validation on the training set
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            
            # Final Fit and Prediction
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
            # Calculate Metrics
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            r2 = r2_score(y_test, preds)
            
            comparison_results.append({
                "Model": name, 
                "CV Accuracy (Avg)": round(cv_scores.mean(), 3),
                "RMSE": round(rmse, 4), 
                "R² Score": round(r2, 4)
            })

            # Keep track of the best model for saving
            if r2 > best_r2:
                best_r2 = r2
                best_model = model
                best_model_name = name
                best_preds = preds

        # Display Comparison Table
        st.table(pd.DataFrame(comparison_results))
        
        # Highlight the Winner
        st.success(f"**Best Performing Model:** {best_model_name} (R² Score: {best_r2:.2f})")

        # Display Metrics for the Best Model specifically
        st.subheader(f"Evaluation Metrics: {best_model_name}")
        m_col1, m_col2, m_col3 = st.columns(3)
        # Using index 0 or similar from comparison_results for the winner
        winner_data = next(item for item in comparison_results if item["Model"] == best_model_name)
        m_col1.metric("CV Accuracy", winner_data["CV Accuracy (Avg)"])
        m_col2.metric("RMSE", winner_data["RMSE"])
        m_col3.metric("R² Score", winner_data["R² Score"])
        
        # Save the Best Model (Persistency)
        if not os.path.exists('models'):
            os.makedirs('models')
        joblib.dump(best_model, 'models/earthquake_model.pkl')
        st.info(f"The optimized {best_model_name} has been saved as the primary intelligence engine.")

        # Visualizing the Prediction Accuracy of the Best Model
        st.subheader(f"Actual vs. Predicted Value ({best_model_name})")
        chart_data = pd.DataFrame({'Actual': y_test.values, 'Predicted': best_preds})
        st.line_chart(chart_data)