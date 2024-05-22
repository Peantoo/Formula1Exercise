# Formula1Exercise
Fun prediction exercise

Formula 1 Lap Time Prediction Project
Project Overview
This project aims to predict the next 5 lap times for a selected driver in a specific race event using time-series forecasting. The goal is to build a model that can provide accurate predictions based on the driver's previous lap times, accounting for the effects of pit stops.

Data Description
The project utilizes seven datasets from several F1 seasons:

lap_times: Contains all lap times of all cars during all races.
qualifying: Contains all lap times of all cars obtained during qualifying events.
sprint_results: Contains all lap times of all cars obtained during sprints.
pit_stops: Contains all laps in which pit stops happened and the pit stop times for each car.
results: Includes each car's/driver's results for each event and each season.
races: Includes all event names (name), seasons (year) with raceId as a unique identifier.
status: Describes causes for a car retiring/not completing an event.
Data Preparation
The data from seasons 2014-2023 (the last 10 years) was selected.
A unique identifier for each car/driver was used.
The lap times dataset was merged with the pit stops dataset to adjust lap times by removing the pit stop durations.
The final dataset included columns describing season year, event name, car number, and lap times.
Data Cleaning and Aggregation
Merged tables based on common keys to generate a large dataset with lap time as the target variable.
Adjusted lap times for pit stops to ensure accurate modeling of the driver's performance.
Selected features that correlate well with lap time, such as lap number and pit stop status.
Model Approach
Choosing ARIMA for Time-Series Forecasting
Why ARIMA?
ARIMA (AutoRegressive Integrated Moving Average) was chosen for this project due to its suitability for time-series forecasting with limited historical data. The primary goal was to predict the next 5 laps based on the previous laps. ARIMA's ability to adjust its predictions based on prior performance makes it robust against changes, preventing over-smoothing.

Advantages of ARIMA:
Simplicity: ARIMA models are simpler and faster to train compared to complex models like LSTMs.
Limited Data Requirement: ARIMA performs well even with limited historical data, which is crucial in a race scenario where only a few laps of data are available.
Adaptability: The model adjusts predictions based on the recent performance, making it robust against sudden changes.
Comparison with LSTM
While LSTM (Long Short-Term Memory) models are powerful for capturing long-term dependencies in time-series data, they require extensive historical data and computational resources. LSTMs are better suited for long-term projects with abundant data. However, for this exercise, ARIMA was preferred due to its simplicity and effectiveness with limited data.

Strengths of LSTM:
Capturing Long-Term Dependencies: LSTMs excel at capturing complex patterns over long sequences.
Flexibility: LSTMs can handle a variety of time-series problems, including those with non-linear dependencies.
Why ARIMA Was Better for This Task:
Temporal Nature: The task was to predict the next 5 laps, not other variables, making ARIMA's short-term forecasting ability ideal.
Data Constraints: Limited historical data from a single race event favored ARIMA over LSTM.
Ease of Implementation: ARIMA was easier to implement and tune for quick predictions.
Model Training, Evaluation, and Visualization
Training Process
An ARIMA model was trained on the adjusted lap times.
The model's performance was validated using a portion of the data reserved for testing.
Metrics such as Mean Squared Error (MSE) were used to evaluate the model's accuracy.
The model's predictions were visualized using line charts to compare actual vs. predicted lap times.
Handling Pit Stops
Pit stops were accounted for by removing their duration from the lap times, ensuring that the model's predictions reflected the driver's actual performance on the track.

Visualization
Line charts were used to visualize the actual and predicted lap times.
The graph displayed a single continuous line, with actual values in blue and predicted values in orange, ensuring clarity and continuity.
Future Validation
To further validate the model's performance, it can be applied to another race event and driver. This would test the model's generalizability and robustness across different race conditions and driver performances.

Conclusion
Achievements
Successfully built a time-series forecasting model using ARIMA to predict the next 5 lap times for a selected driver.
Integrated data from multiple sources and adjusted for pit stops to ensure accurate predictions.
Created a user-friendly Streamlit application to interactively select races and drivers, train the model, and visualize predictions.
Areas for Improvement
Extended Data: Incorporating data from more races and drivers to enhance model training and validation.
Feature Engineering: Exploring additional features such as weather conditions, tire types, and track characteristics.
Advanced Models: Experimenting with more complex models like LSTMs for long-term forecasting tasks.
