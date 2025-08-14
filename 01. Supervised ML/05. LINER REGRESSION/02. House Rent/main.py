import streamlit as st
import pickle
import pandas as pd

# Load trained model
with open("rent_prediction.pkl", "rb") as obj1:
    model_bundle = pickle.load(obj1)

model = model_bundle['model']
x_scaler = model_bundle['x_scaler']
y_scaler = model_bundle['y_scaler']
features = model_bundle['features']

# Title
st.title("🏠 House Rent Prediction App")

# Inputs
BHK = st.number_input("Enter number of BHK:", min_value=0, max_value=10, value=2)
Size = st.number_input("Enter size in sq.ft:", min_value=0, max_value=5000, value=1000)
Area_Type = st.selectbox("Area Type:", ["Super built-up  Area", "Built-up  Area", "Plot  Area", "Carpet  Area"])
City = st.selectbox("Select City:", ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"])
Furnishing = st.selectbox("Furnishing Status:", ["Furnished", "Semi-Furnished", "Unfurnished"])
Bathroom = st.number_input("Enter number of bathrooms:", min_value=1, max_value=5, value=2)
Tenant_Preferred = st.selectbox("Tenant Preferred:", ["Bachelors", "Family"])
Current_Floor = st.number_input("Enter your current floor number:", min_value=0, max_value=50, value=2)
Total_Floors = st.number_input("Total Floors in the building:", min_value=Current_Floor, max_value=100, value=10)

# Feature Engineering for Tenant Type
tenant_bachelors = 1 if Tenant_Preferred == "Bachelors" else 0
tenant_family = 1 if Tenant_Preferred == "Family" else 0

# Construct DataFrame
input_dict = {
    'BHK': BHK,
    'Size': Size,
    'Area Type': Area_Type,
    'City': City,
    'Furnishing Status': Furnishing,
    'Bathroom': Bathroom,
    'Tenant_Bachelors': tenant_bachelors,
    'Tenant_Family': tenant_family,
    'Current_Floor': Current_Floor,
    'Total_Floors': Total_Floors
}
input_df = pd.DataFrame([input_dict])

# One-hot encoding (to match training)
input_encoded = pd.get_dummies(input_df)

# Ensure all expected features are present
input_encoded = input_encoded.reindex(columns=x_scaler.feature_names_in_, fill_value=0)

# Scale input
input_scaled = x_scaler.transform(input_encoded)

if st.button("Calculate Rent"):
    # Predict
    prediction_scaled = model.predict(input_scaled)

    # Inverse scale
    final_prediction = y_scaler.inverse_transform([[prediction_scaled[0]]])[0][0]

    # Output
    st.success(f"Predicted Monthly Rent: ₹ {round(final_prediction, 2)}")

