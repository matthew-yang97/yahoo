import pandas as pd
import numpy as np
from prophet import Prophet

names = ['渋谷', '新宿', '丸の内', '品川', '下北沢', '八王子', '大阪難波', '札幌大通', '仙台駅', '福岡天神']
names_e = ['shibuya', 'shinjyuku', 'marunouchi', 'shinagawa', 'shimokitazawa', 'hachiouji', 'osaka', 'sapporo', 'sendai', 'fukuoka']
dfPop = pd.read_csv('population2.csv')

dateResult = pd.date_range(start='2021-09-08', periods=9, freq='1D')
dfResult = pd.DataFrame()


def max_calc(df, city, filename):

    # from 2020-01-06 to 2021-09-05
    mon = df[5:614:7][names[city]].values.tolist()
    tue = df[6:614:7][names[city]].values.tolist()
    wed = df[7:614:7][names[city]].values.tolist()
    thur = df[8:614:7][names[city]].values.tolist()
    fri = df[9:614:7][names[city]].values.tolist()
    sat = df[10:614:7][names[city]].values.tolist()
    sun = df[11:614:7][names[city]].values.tolist()

    week_len = len(mon)
    week_rate = np.empty([week_len, 7])
    week_max = []
    for i in range(week_len):
        maxpop = max(np.array([mon[i], tue[i], wed[i], thur[i], fri[i], sat[i], sun[i]]))
        week_max.append(maxpop)
        week_rate[i] = [mon[i] / maxpop, tue[i] / maxpop, wed[i] / maxpop, thur[i] / maxpop, fri[i] / maxpop,
                        sat[i] / maxpop, sun[i] / maxpop]

    rate_mean = np.mean(week_rate, axis=0)
    stat = pd.DataFrame({
        'mean_max': rate_mean.tolist(),
    })
    stat.index = ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun']
    stat.to_csv('rate_' + names_e[city] + '.csv', index_label='week')

    date_mon = pd.date_range(start='20200106', periods=week_len, freq='7D')
    weekMax_df = pd.DataFrame({'y': week_max})
    weekMax_df.index = date_mon

    weekMax_df.to_csv(filename, index_label='ds')

    return rate_mean


def max_pred(df, filename_pred, city):
    m = Prophet()

    '''
    if city < 6:
        m = Prophet(changepoints=['2021-01-04', '2021-01-11', '2021-4-19', '2021-4-26', '2021-07-05', '2021-07-12'],
                    changepoint_prior_scale=0.5)
    if city == 6:
        m = Prophet(changepoints=['2021-01-11', '2021-01-18', '2021-4-19', '2021-4-26', '2021-07-26', '2021-08-02'],
                    changepoint_prior_scale=0.5)
    if city == 7:
        m = Prophet(changepoints=['2021-05-10', '2021-05-17'], changepoint_prior_scale=0.5)
    if city == 9:
        m = Prophet(changepoints=['2021-01-11', '2021-01-18', '2021-05-10', '2021-05-17', '2021-08-09'],
                    changepoint_prior_scale=0.5)
    '''

    # from 2020-09-14 to 2021-09-05
    dfsub = df[36:87]
    ori_mean = dfsub['y'].mean()
    ori_std = dfsub['y'].std()
    dfsub['y'] = (dfsub['y'] - dfsub['y'].mean()) / dfsub['y'].std()
    m.fit(dfsub)
    future = m.make_future_dataframe(periods=2, freq='W')
    forecast = m.predict(future)
    forecast['yhat'] = forecast['yhat'] * ori_std + ori_mean
    forecast['yhat_lower'] = forecast['yhat_lower'] * ori_std + ori_mean
    forecast.to_csv(filename_pred, index_label='week')

    return forecast


def diff_calc(max_file, city, rate_mean):
    maxf = pd.read_csv(max_file)
    date_all = pd.date_range(start='2020-09-14', periods=357, freq='1D')
    gt = dfPop[257:614][names[city]].values.tolist()
    df_diff = pd.DataFrame({'y': gt})
    pred = []
    for w in range(51):
         this_week = (maxf.iloc[w]['yhat'] * rate_mean).tolist()
         if city == 4 or city == 5 or city == 8:
             this_week = (maxf.iloc[w]['yhat_lower'] * rate_mean).tolist()
         pred += this_week
    df_diff['pred'] = pred
    df_diff['diff'] = np.array(gt) - np.array(pred)
    df_diff['rate'] = np.array(gt) / np.array(pred)
    df_diff['error'] = np.abs(np.array(gt) - np.array(pred)) / np.array(gt)
    df_diff.index = date_all
    df_diff.to_csv('diff_' + names_e[city] + '.csv', index_label='date')


for i in range(10):
    filename = 'max_' + names_e[i] + '.csv'
    rate_i = max_calc(dfPop, i, filename)
    dfmax = pd.read_csv(filename)

    filename_pred = 'pred_max_' + names_e[i] + '.csv'
    max_forecast = max_pred(dfmax, filename_pred, i)

    diff_calc(filename_pred, i, rate_i)

    pred = (max_forecast.iloc[-2]['yhat'] * rate_i[2:]).tolist()
    pred = pred + (max_forecast.iloc[-1]['yhat'] * rate_i[:4]).tolist()

    if i == 4 or i == 5 or i == 8:
        pred = (max_forecast.iloc[-2]['yhat_lower'] * rate_i[2:]).tolist()
        pred = pred + (max_forecast.iloc[-1]['yhat_lower'] * rate_i[:4]).tolist()

    dfResult[names_e[i] + '_yhat'] = pred

    '''
    dfInfer = np.array(dfPop[607:][names[i]].values.tolist())
    dfResult[names_e[i]+'_y'] = dfInfer

    error = np.abs(np.array(dfInfer) - np.array(pred)) / np.array(dfInfer)
    dfResult[names_e[i]+'_error'] = error
    '''

dfResult.index = dateResult
dfResult.to_csv('base98.csv', index_label='date')

