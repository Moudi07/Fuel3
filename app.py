import streamlit as st
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# Load the pre-trained SVR models
loaded_fuel_model = joblib.load(open("svr_model.sav", "rb"))
loaded_CO2_model = joblib.load(open("svr2_model.sav", "rb"))

# Load the fitted StandardScaler
loaded_scaler_fuel = joblib.load(open("scaled_data.sav", "rb"))
loaded_scaler_CO2 = joblib.load(open("new_scaled_data.sav", "rb"))

def fuel_prediction(inp):
    arr = np.asarray(inp)
    arr = arr.reshape(1, -1)

    arr_scaled = loaded_scaler_fuel.transform(arr)
    prediction = loaded_fuel_model.predict(arr_scaled)

    return round(prediction[0], 2)

def CO2_prediction(fuel_prediction_result):
    arr = np.asarray([fuel_prediction_result])
    arr = arr.reshape(1, -1)

    arr_scaled = loaded_scaler_CO2.transform(arr)
    prediction = loaded_CO2_model.predict(arr_scaled)

    return round(prediction[0], 2)

def input_converter(inp):
    vcl = ['Two-seater','Minicompact','Compact','Subcompact','Mid-size','Full-size','SUV: Small','SUV: Standard','Minivan','Station wagon: Small','Station wagon: Mid-size','Pickup truck: Small','Special purpose vehicle','Pickup truck: Standard']
    trans = ['AV','AM','M','AS','A']
    fuel = ["D","E","X","Z"]
    lst = []

    for i in range(6):
        if isinstance(inp[i], str):
            if inp[i] in vcl:
                lst.append(vcl.index(inp[i]))
            elif inp[i] in trans:
                lst.append(trans.index(inp[i]))
            elif inp[i] in fuel:
                if fuel.index(inp[i]) == 0:
                    lst.extend([1, 0, 0, 0])
                    break
                elif fuel.index(inp[i]) == 1:
                    lst.extend([0, 1, 0, 0])
                    break
                elif fuel.index(inp[i]) == 2:
                    lst.extend([0, 0, 1, 0])
                    break
                elif fuel.index(inp[i]) == 3:
                    lst.extend([0, 0, 0, 1])
        else:
            lst.append(inp[i])

    arr = np.asarray(lst)
    arr = arr.reshape(1, -1)

    with st.spinner("Predicting..."):
        with st.expander("Advanced Options"):
            st.markdown("You can customize the advanced options here.")
        with st.spinner("Processing..."):
            arr_scaled = loaded_scaler_fuel.transform(arr)

    fuel_prediction_result = loaded_fuel_model.predict(arr_scaled)
    CO2_prediction_result = CO2_prediction(fuel_prediction_result)

    return round(fuel_prediction_result[0], 2), CO2_prediction_result

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Fuel Consumption and CO2 Emissions Prediction",
        page_icon="✈️",
        layout="wide",
    )

    # Custom styles
    st.markdown(
        """
        <style>
            body {
                background-image: url('https://www.satisgps.com/wp-content/uploads/2019/12/Paliwo_artykul04-1.png.');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
            .main {
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .sidebar {
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .footer {
                padding: 10px;
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                text-align: center;
                border-radius: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Fuel Consumption and CO2 Emissions Prediction")

    st.sidebar.header("Input Values")

    # Use number input instead of slider
    vehicle_class = st.sidebar.selectbox("Vehicle Class", ['Two-seater','Minicompact','Compact','Subcompact','Mid-size','Full-size','SUV: Small','SUV: Standard','Minivan','Station wagon: Small','Station wagon: Mid-size','Pickup truck: Small','Special purpose vehicle','Pickup truck: Standard'])
    engine_size = st.sidebar.number_input("Engine Size", min_value=0.0, max_value=10.0, step=0.1, value=1.0)
    cylinders = st.sidebar.number_input("Cylinders", min_value=0, max_value=16, step=1, value=4)
    CO2_rating = st.sidebar.number_input("CO2 Rating", min_value=0.0, max_value=10.0, step=0.1, value=1.0)
    transmission = st.sidebar.selectbox("Transmission", ['AV', 'AM', 'M', 'AS', 'A'])
    fuel_type = st.sidebar.selectbox("Fuel Type", ["D", "E", "X", "Z"])

    user_input = [vehicle_class, engine_size, cylinders, transmission, CO2_rating, fuel_type]

    if st.button("Predict"):
        fuel_result, CO2_result = input_converter(user_input)
        st.success(f"The predicted fuel consumption is: {fuel_result} L/100km")
        st.success(f"The predicted CO2 emissions are: {CO2_result} g/km")

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p class='footer'>© 2023 Fuel Consumption App</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
