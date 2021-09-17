import pandas as pd
from prophet import Prophet

df = pd.read_csv('max_series2_fuku.csv')

# tokyo emergency
# m = Prophet(changepoints=['2021-01-04', '2021-01-11', '2021-4-19',
#                         '2021-4-26', '2021-07-05', '2021-07-12'], changepoint_prior_scale=0.7)

# osaka emergency
# m = Prophet(changepoints=['2021-01-11', '2021-01-18', '2021-4-19',
#                          '2021-4-26', '2021-07-26', '2021-08-02'], changepoint_prior_scale=0.7)

# sapporo emergency
# m = Prophet(changepoints=['2021-05-10', '2021-05-17'], changepoint_prior_scale=0.7)

# sendai emergency
m = Prophet()

# fukuoka emergency
# m = Prophet(changepoints=['2021-01-11', '2021-01-18', '2021-05-10',
#                          '2021-05-17', '2021-08-09'], changepoint_prior_scale=0.7)

# from 2020-11
m.fit(df[43:84])

future = m.make_future_dataframe(periods=4, freq='W')
print(future.tail())

forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

forecast.to_csv('test_output_fuku_no_emer.csv', index_label='week')


