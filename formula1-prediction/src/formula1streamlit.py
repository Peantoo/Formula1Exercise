# formula1streamlit.py

import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import warnings

# Function to read CSV files
@st.cache_data
def load_data():
    lap_times = pd.read_csv('lap_times.csv')
    pit_stops = pd.read_csv('pit_stops.csv')
    races = pd.read_csv('races.csv')
    return lap_times, pit_stops, races

# Load data
lap_times, pit_stops, races = load_data()

# Filter races for the selected seasons (2014-2023)
races = races[(races['year'] >= 2014) & (races['year'] <= 2023)]

# Streamlit app
st.title('Race Lap Time Prediction')

# Select a race
race_id = st.selectbox('Select a race', races[['raceId', 'name']].apply(lambda x: f"{x['raceId']} - {x['name']}", axis=1))
race_id = int(race_id.split(' - ')[0])

# Filter drivers for the selected race
drivers = lap_times[lap_times['raceId'] == race_id]['driverId'].unique()
driver_id = st.selectbox('Select a driver', drivers)

# Filter data for the selected race and driver
def filter_race_driver_data(lap_times, pit_stops, race_id, driver_id):
    df = lap_times[(lap_times['raceId'] == race_id) & (lap_times['driverId'] == driver_id)].copy()
    pit_df = pit_stops[(pit_stops['raceId'] == race_id) & (pit_stops['driverId'] == driver_id)].copy()

    # Merge lap times with pit stops to adjust lap times
    df = df.merge(pit_df[['raceId', 'driverId', 'lap', 'milliseconds']], on=['raceId', 'driverId', 'lap'], how='left', suffixes=('', '_pit_stop'))
    df['is_pit_stop'] = df['milliseconds_pit_stop'].notnull().astype(int)
    df['milliseconds'] = df['milliseconds'] - df['milliseconds_pit_stop'].fillna(0)
    df = df.drop(columns=['milliseconds_pit_stop'])
    
    return df

filtered_data = filter_race_driver_data(lap_times, pit_stops, race_id, driver_id)

# Train ARIMA model
if st.button('Train Model'):
    st.write("Training model, please wait...")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        model = ARIMA(filtered_data['milliseconds'], order=(2, 1, 2))
        model_fit = model.fit()
    
    st.session_state['model_fit'] = model_fit
    st.session_state['filtered_data'] = filtered_data

    st.success("Model trained successfully!")

# Display the graph for training performance
if 'model_fit' in st.session_state:
    model_fit = st.session_state['model_fit']
    filtered_data = st.session_state['filtered_data']

    # Predict the in-sample data
    in_sample_pred = model_fit.predict()
    
    # Plot the actual and predicted values
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_data['lap'], filtered_data['milliseconds'], label='Actual')
    plt.plot(filtered_data['lap'], in_sample_pred, label='Predicted', linestyle='--')
    plt.xlabel('Lap')
    plt.ylabel('Milliseconds')
    plt.title('Actual vs Predicted Lap Times')
    plt.legend()
    st.pyplot(plt)

# Create a data entry grid
st.subheader("Enter Lap Times")
num_laps = st.number_input("Enter number of laps to populate", min_value=1, max_value=20, value=1)

# Auto-populate lap times
if st.button('Populate Laps'):
    min_time = filtered_data['milliseconds'].min()
    max_time = filtered_data['milliseconds'].max()
    lap_times_input = np.random.randint(min_time, max_time, num_laps)
    lap_times_df = pd.DataFrame({
        'lap': list(range(1, num_laps + 1)),
        'milliseconds': lap_times_input
    })
    st.session_state['lap_times'] = lap_times_df

# Manually enter lap times
if 'lap_times' in st.session_state:
    lap_times_df = st.session_state['lap_times']
else:
    lap_times_df = pd.DataFrame(columns=['lap', 'milliseconds'])

# Use st.data_editor for editable data
edited_df = st.data_editor(lap_times_df, num_rows="dynamic")
st.session_state['lap_times'] = edited_df

# Adjust for pit stops
pit_lap_numbers = st.text_input("Enter lap numbers with pit stops (comma-separated)")
if pit_lap_numbers:
    pit_lap_numbers = [int(x) for x in pit_lap_numbers.split(',')]
    pit_times = []
    for lap in pit_lap_numbers:
        pit_time = st.number_input(f"Enter pit stop time for lap {lap}", min_value=0, value=0)
        pit_times.append(pit_time)
    for lap, pit_time in zip(pit_lap_numbers, pit_times):
        edited_df.loc[edited_df['lap'] == lap, 'milliseconds'] -= pit_time
    st.session_state['lap_times'] = edited_df

# Predict next 5 laps
if st.button('Predict'):
    if 'lap_times' in st.session_state:
        lap_times_df = st.session_state['lap_times']
        if len(lap_times_df) < 5:
            st.warning("Too few laps to accurately predict the next 5, please enter at least 5 laps.")
        else:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                model = ARIMA(lap_times_df['milliseconds'], order=(2, 1, 2))
                model_fit = model.fit()
                predictions = model_fit.forecast(steps=5)
                
                last_lap = int(lap_times_df['lap'].iloc[-1])
                predicted_laps = list(range(last_lap + 1, last_lap + 6))
                
                prediction_df = pd.DataFrame({
                    'lap': predicted_laps,
                    'predicted_milliseconds': predictions
                })

                # Combine the actual and predicted data
                combined_laps = lap_times_df['lap'].tolist() + predicted_laps
                combined_times = lap_times_df['milliseconds'].tolist() + predictions.tolist()

                # Plot the combined data
                plt.figure(figsize=(10, 6))
                plt.plot(combined_laps, combined_times, color='blue', label='Actual')  # Combined line
                plt.plot(predicted_laps, predictions, color='orange', label='Predicted')  # Predicted line
                plt.plot(lap_times_df['lap'], lap_times_df['milliseconds'], color='blue', linestyle='', marker='o')  # Actual markers
                plt.plot(predicted_laps, predictions, color='orange', linestyle='', marker='o')  # Predicted markers
                plt.xlabel('Lap')
                plt.ylabel('Milliseconds')
                plt.title('Actual vs Predicted Lap Times')
                plt.legend()
                st.pyplot(plt)
                
            st.write("Predicted lap times for the next 5 laps:")
            st.dataframe(prediction_df)
    else:
        st.error("Please enter lap times before predicting.")




