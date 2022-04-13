import wbgapi as wb
import pandas as pd
import numpy as np
import os

# ML Libraries
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
import pickle

# Features or Columns for the model
cols = ['t-4', 't-3', 't-2', 't-1', 't0', 'host', 'impact']

# Dataframe to save the prepared input data for the model
model_data_df = None

# Selected Economic Indicators
economic_variables = {'NY.GDP.PCAP.CD': 'GDP Per Capita', 'ST.INT.ARVL': 'Tourism Arrival',
                      'NY.GDP.DEFL.KD.ZG': 'Inflation',
                      'PA.NUS.FCRF': 'Exchange Rate', 'GC.DOD.TOTL.GD.ZS': 'Debt', 'NY.GDP.MKTP.KD.ZG': 'GDP Growth',
                      'NE.TRD.GNFS.ZS': 'Trade', 'NE.IMP.GNFS.ZS': 'Import Goods', 'GC.TAX.TOTL.GD.ZS': 'Tax Revenue',
                      'CM.MKT.TRAD.GD.ZS': 'Stocks', 'BX.KLT.DINV.WD.GD.ZS': 'Foreign Investments',
                      'NE.DAB.TOTL.ZS': 'Gross National Expenditure', 'GC.REV.XGRT.GD.ZS': 'Revenue',
                      'SL.IND.EMPL.ZS': 'Employment', 'SL.UEM.TOTL.NE.ZS': 'Unemployment'}

alias_names = {'GER': 'DEU', 'FRG': 'DEU', 'NED': 'NLD', 'SUI': 'CHE', 'YUG': 'SRB', 'URS': 'RUS', 'GRE': 'GRC'}

year_list = [i for i in range(1960, 2021)]

summer_olympics_data = pd.read_csv("Datasets/summer.csv")
winter_olympics_data = pd.read_csv("Datasets/winter.csv")

summer_olympics_data = summer_olympics_data.replace(alias_names)
winter_olympics_data = winter_olympics_data.replace(alias_names)

winter_olympics_data.dropna(inplace=True)
summer_olympics_data.dropna(inplace=True)

summer_host_info = summer_olympics_data.groupby('country_code')['year'].apply(list).reset_index().explode('year')
winter_host_info = winter_olympics_data.groupby('country_code')['year'].apply(list).reset_index().explode('year')

summer_host_info = summer_host_info[(summer_host_info['year'] >= 1964) & (summer_host_info['year'] <= 2016)]
winter_host_info = winter_host_info[(winter_host_info['year'] >= 1964) & (winter_host_info['year'] <= 2016)]

games_df = pd.concat([summer_host_info, winter_host_info], axis=0)


# Get the economic data of olympic host countries
def populate_host_data(eco_df, games_df, host_value):
    host_list = eco_df.index

    for row in games_df.itertuples(index=False):
        row_values = []
        global model_data_df

        if row.country_code in host_list:
            host_year_value = eco_df.loc[row.country_code, row.year]
            before_values = eco_df.loc[row.country_code, [i for i in range(row.year - 4, row.year)]].to_list()
            for i in before_values:
                row_values.append(i)
            row_values.append(host_year_value)
            row_values.append(host_value)
            after_effects = eco_df.loc[row.country_code, [j for j in range(row.year + 1, row.year + 5)]]

            if np.average(after_effects) >= host_year_value:
                row_values.append(np.max(after_effects))
            else:
                row_values.append(np.min(after_effects))

            model_data_df = model_data_df.append(pd.Series(row_values, index=model_data_df.columns), ignore_index=True)


# Get the economic data of olympic non-host countries
def populate_non_host_data(eco_df, year_list, host_value):
    def get_impact_value(rowdata):
        yrs_list = rowdata[:-1].to_list()
        mean_value = rowdata['mean']
        if mean_value >= yrs_list[0]:
            return max(yrs_list)
        else:
            return min(yrs_list)

    for yr in year_list:
        global model_data_df

        before_df = pd.DataFrame(columns=cols)

        before_df[cols[:4]] = eco_df[[i for i in range(yr - 4, yr)]]
        after_df = eco_df[[i for i in range(yr, yr + 5)]]

        after_df['mean'] = after_df.mean(axis=1)
        after_df['max_impact'] = after_df.apply(get_impact_value, axis=1)

        before_df[cols[4]] = eco_df[yr]
        before_df[cols[5]] = host_value
        before_df[cols[6]] = after_df['max_impact']

        model_data_df = pd.concat([model_data_df, before_df], axis=0, ignore_index=True)


# Method to get the indicator data for all countries
def get_indicator_data(indicator):
    eco_df = wb.data.DataFrame(indicator, skipAggs=True)
    eco_df = eco_df.rename(columns=lambda x: int(x.replace('YR', '')))
    eco_df = eco_df.transpose().fillna(method='backfill').fillna(method='ffill').transpose()
    eco_df.dropna(inplace=True)
    return eco_df


def get_train_test_split(data, cols):
    X_train, X_test, y_train, y_test = train_test_split(data[cols[0:6]], data[cols[6]], test_size=0.3, random_state=42)
    return (X_train, X_test, y_train, y_test)


def scale_data(inputdata):
    # Scale the data before applying the model
    scaler = StandardScaler()
    scaler.fit(inputdata)
    inputdata = scaler.transform(inputdata)
    return inputdata


def get_lr_score(input_data_df, cols):
    # Scale the data before applying the model
    scaler = StandardScaler()
    scaler.fit(input_data_df[cols[0:6]])
    input_data_df[cols[0:6]] = scaler.transform(input_data_df[cols[0:6]])

    print('Training Linear Regression ...')

    # Splitting the data set
    X_train, X_test, y_train, y_test = get_train_test_split(input_data_df, cols)

    # Training different Linear Regression model

    # Vanilla Linear Regression
    lr_model = LinearRegression().fit(X_train, y_train)

    # Ridge Regression
    # lr_model = linear_model.Ridge(alpha=1.0).fit(X_train, np.log(y_train))

    # Lasso Regression
    # lr_model = linear_model.Lasso(alpha=1.0).fit(X_train, np.log(y_train))

    # Bayesian Ridge Regression
    # lr_model = linear_model.BayesianRidge().fit(X_train, y_train)

    # Gamma Regressor
    # lr_model = linear_model.GammaRegressor().fit(X_train, y_train)

    # Tweedie Regression
    # lr_model = linear_model.TweedieRegressor(power=2, alpha=1.0, link='log').fit(X_train, y_train)

    # Make predictions and return the score
    # User to inverse log transform
    # pred = np.exp(lr_model.predict(X_test))
    pred = lr_model.predict(X_test)

    print("MSE : ", np.sqrt(mean_squared_error(y_test, pred)))

    return lr_model, np.sqrt(mean_squared_error(y_test, pred))


def get_rf_score(input_data_df, cols):
    param_grid = {
        'bootstrap': [True],
        'max_depth': [10, 20, 30, 40, 50],
        'max_features': [2, 3],
        'min_samples_leaf': [3, 4, 5],
        'min_samples_split': [8, 10, 12],
        'n_estimators': [100, 200]
    }

    print('Training Random Forest Regression ...')

    # Splitting the data set
    X_train, X_test, y_train, y_test = get_train_test_split(input_data_df, cols)

    # Hyperparameter Tuning
    grid_search = GridSearchCV(estimator=RandomForestRegressor(), param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_

    # Training the model
    rf_model = RandomForestRegressor(n_estimators=best_params['n_estimators'],
                                     min_samples_split=best_params['min_samples_split'],
                                     min_samples_leaf=best_params['min_samples_leaf'],
                                     max_features=best_params['max_features'],
                                     max_depth=best_params['max_depth'], bootstrap=best_params['bootstrap'])

    # rf_model = RandomForestRegressor(n_estimators = 100, max_depth= 5, bootstrap=True)
    rf_model.fit(X_train, y_train)

    # Prediction
    pred = rf_model.predict(X_test)

    print("MSE : ", np.sqrt(mean_squared_error(y_test, pred)))

    return rf_model, np.sqrt(mean_squared_error(y_test, pred))


def get_svr_score(input_data_df, cols):
    # Scale the data before applying the model
    scaler = StandardScaler()
    scaler.fit(input_data_df[cols[0:6]])
    input_data_df[cols[0:6]] = scaler.transform(input_data_df[cols[0:6]])

    param_grid = {'C': [0.1, 1, 10, 100, 1000],
                  'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
                  'kernel': ['rbf', 'poly']}

    print('Training Support Vector Regression ...')

    # Splitting the data set
    X_train, X_test, y_train, y_test = get_train_test_split(input_data_df, cols)

    # Hyperparameter Tuning
    grid_search = GridSearchCV(SVR(), param_grid, refit=True, verbose=1, cv=3)
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_

    # Training the model
    svr_model = SVR(C=best_params['C'], gamma=best_params['gamma'], kernel=best_params['kernel'])
    svr_model.fit(X_train, y_train)

    # Prediction
    pred = svr_model.predict(X_test)

    print("MSE : ", np.sqrt(mean_squared_error(y_test, pred)))

    return svr_model, np.sqrt(mean_squared_error(y_test, pred))


def get_xgb_score(input_data_df, cols):
    parameters = {'loss': ['ls', 'lad', 'huber', 'quantile'],
                  'learning_rate': (0.05, 0.25, 0.50, 1),
                  'criterion': ['friedman_mse', 'mse', 'mae'],
                  'max_features': ['auto', 'sqrt', 'log2'],
                  'n_estimators': [100, 200, 500],
                  'max_depth': [1, 2],
                  'min_samples_leaf': [5, 10],
                  'min_samples_split': [5, 10]
                  }

    print('Training Gradient Boosting Regressor ...')

    # Splitting the data set
    X_train, X_test, y_train, y_test = get_train_test_split(input_data_df, cols)

    '''

    Ignoring # Hyperparameter tuning because it is computationally expensive.


    grid_search = GridSearchCV(GradientBoostingRegressor(), parameters, cv=3, verbose=2)
    grid_search.fit(X_train,y_train)
    best_params = model.best_params_

    # Training the model
    xgb_model = GradientBoostingRegressor(loss=best_params['loss'], learning_rate=best_params['learning_rate'],
                                    criterion=best_params['criterion'], max_features=best_params['max_features'],
                                    n_estimators=best_params['n_estimators'], max_depth=best_params['max_depth'],
                                    min_samples_leaf=best_params['min_samples_leaf'],
                                    min_samples_split=best_params['min_samples_split']).fit(X_train, y_train)
    '''

    xgb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=10, loss='squared_error').fit(
        X_train, y_train)

    # Prediction
    pred = xgb_model.predict(X_test)

    print("MSE : ", np.sqrt(mean_squared_error(y_test, pred)))

    return xgb_model, np.sqrt(mean_squared_error(y_test, pred))


def get_mlp_score(input_data_df, cols):
    parameter_space = {
        'hidden_layer_sizes': [(20, 20), (10,), ],
        'activation': ['tanh', 'relu'],
        'solver': ['sgd', 'adam'],
        'alpha': [0.1, 0.05],
        'learning_rate': ['constant', 'adaptive'],
    }

    print('Training Multi Layer Perceptron ...')

    # Scale the data before applying the model
    scaler = StandardScaler()
    scaler.fit(input_data_df[cols[0:6]])
    input_data_df[cols[0:6]] = scaler.transform(input_data_df[cols[0:6]])

    # Splitting the data set
    X_train, X_test, y_train, y_test = get_train_test_split(input_data_df, cols)

    # Hyperparameter Tuning
    grid_search = GridSearchCV(MLPRegressor(random_state=1, max_iter=50), parameter_space, n_jobs=-1, cv=5, verbose=2)
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_

    # Training the model
    mlp_model = MLPRegressor(max_iter=50,
                             hidden_layer_sizes=best_params['hidden_layer_sizes'],
                             activation=best_params['activation'],
                             solver=best_params['solver'],
                             alpha=best_params['alpha'],
                             learning_rate=best_params['learning_rate']).fit(X_train, y_train)

    # Prediction
    pred = mlp_model.predict(X_test)

    print("MSE : ", np.sqrt(mean_squared_error(y_test, pred)))

    return mlp_model, np.sqrt(mean_squared_error(y_test, pred))


path = './testmodel/'
if not os.path.exists(path):
    os.mkdir(path)

for key, value in economic_variables.items():
    print("-----------------------" + key + ":" + value + "--------------------------")

    global model_data_df
    model_data_df = pd.DataFrame(columns=cols)
    eco_df = get_indicator_data(key)

    saved_models = {'lr': None, 'rf': None, 'svr': None, 'xgb': None, 'mlp': None}
    model_performance = {'lr': None, 'rf': None, 'svr': None, 'xgb': None, 'mlp': None}

    host_country_df = eco_df[eco_df.index.isin(games_df.country_code.unique())]
    populate_host_data(host_country_df, games_df, 1)

    nonhost_country_df = eco_df[~eco_df.index.isin(games_df.country_code.unique())]
    populate_non_host_data(nonhost_country_df, games_df.year.to_list(), 0)

    model_data_df[cols] = np.cbrt(model_data_df[cols])

    print("Model Training and Hyperparameter Tuning...")

    saved_models['lr'], model_performance['lr'] = get_lr_score(model_data_df, cols)
    #     saved_models['rf'], model_performance['rf'] = get_rf_score(model_data_df, cols)
    #     saved_models['svr'], model_performance['svr'] = get_svr_score(model_data_df, cols)
    #     saved_models['xgb'], model_performance['xgb'] = get_xgb_score(model_data_df, cols)
    #     saved_models['mlp'], model_performance['mlp'] = get_mlp_score(model_data_df, cols)

    #     print("Linear Regression : ", model_performance['lr'])
    #     print("Random Forest : ", model_performance['rf'])
    #     print("Support Vector Regression : " ,model_performance['svr'])
    #     print("Gradient Boosting Regression : " ,model_performance['xgb'])
    #     print("Multi Layer Perceptron : " ,model_performance['mlp'])

    #     max_key = max(model_performance, key=model_performance.get)
    #     print("Model Performance : ", model_performance['lr'])

    # Saving the model
    filename = path + value + '.pkl'
    with open(filename, 'wb') as file:
        pickle.dump(saved_models['lr'], file)

# Adding 2019 and 2020 actual values to the forecasted data.
for key, value in economic_variables.items():
    print("running...")
    eco_df = get_indicator_data(key)
    forecast_data = pd.read_csv(value + ".csv")
    forecast_data[str(2020)] = eco_df[2020].values
    forecast_data[str(2019)] = eco_df[2019].values
    forecast_data.to_csv(value + ".csv")

for key, value in economic_variables.items():
    loaded_model = pickle.load(open('./testmodel/' + value + '.pkl', 'rb'))
    test_data = pd.read_csv('./time_series/' + value + '.csv').set_index('Unnamed: 0')
    yrs = ['2024', '2025', '2026', '2027', '2028']

    # Cube root Transformation
    test_data[test_data.columns] = np.cbrt(test_data[test_data.columns])

    # Standard Scaling
    test_data = test_data.transpose()
    scaler = StandardScaler()
    scaler.fit(test_data)
    test_data.loc[:] = scaler.transform(test_data)
    test_data = test_data.transpose()

    inputdata = test_data.loc[:, yrs]
    inputdata['host'] = 1

    input_row = inputdata.loc['AUS'].values.reshape(1, -1)
    predicted_value = loaded_model.predict(input_row)
    print("Predicted " + value + " : ", predicted_value ** 3)
