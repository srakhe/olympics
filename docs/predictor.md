## Predictor:

### [Time Series Forecasting](../scripts/modeling/forecast.py):

- This script was used to perform time series forecasting for economic data pertaining to the olympics.
- This was required since we needed future economic data of countries as an input to our predictor.
- Forecasting was performed for all the countries for all given economic indicators.

### [Predictor Modeling](../scripts/modeling/model_builder.py):

- This scripts builds prediction models for various economic indicators.
- These models are then saved as pickle files for use in the application.
- These pickle files can be found [here](../data/models).