import statsmodels.formula.api as smf
import pandas as pd

names_e = ['shibuya', 'shinjyuku', 'marunouchi', 'shinagawa', 'shimokitazawa', 'hachiouji',
           'osaka', 'sapporo', 'sendai', 'fukuoka']
externalcol = ['in_GW', 'in_S', 'in_emer', 'start_emer', 'end_emer']
wordcol = [['recipe', 'remote', 'takeout', 'delivery', 'remote_nomi', 'ticket'],
           ['recipe', 'remote', 'takeout', 'remote_nomi', 'delivery', 'ticket'],
           ['manga', 'delivery', 'bicycle', 'ticket'],
           ['manga', 'delivery', 'bicycle'],
           ['recipe', 'game', 'convenient', 'remote_nomi', 'takeout', 'delivery'],
           ['delivery', 'manga', 'recipe', 'takeout', 'remote', 'remote_nomi'],
           ['delivery', 'recipe', 'takeout', 'remote_nomi', 'ticket', 'remote'],
           ['manga', 'bicycle', 'delivery'],
           ['delivery', 'takeout', 'recipe', 'bicycle', 'manga', 'ticket'],
           ['delivery', 'manga', 'bicycle', 'takeout', 'recipe']]
formulas = ['rate~in_GW+in_S+in_emer+start_emer+end_emer+recipe+remote+takeout+delivery+remote_nomi+ticket',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+recipe+remote+takeout+remote_nomi+delivery+ticket',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+manga+delivery+bicycle+ticket',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+manga+delivery+bicycle',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+recipe+game+convenient+remote_nomi+takeout+delivery',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+delivery+manga+recipe+takeout+remote+remote_nomi',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+delivery+recipe+takeout+remote_nomi+ticket+remote',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+manga+bicycle+delivery',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+delivery+takeout+recipe+bicycle+manga+ticket',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+delivery+manga+bicycle+takeout+recipe']

df = pd.DataFrame()

worddf = pd.read_csv('word.csv')

for i in range(10):
    externalfile = 'external_' + names_e[i] + '.csv'
    difffile = 'diff_' + names_e[i] + '.csv'
    data_x = pd.read_csv(externalfile)[257:614][externalcol]
    data_x.index = range(len(data_x))
    data_x2 = pd.DataFrame()
    for w in range(len(wordcol[i])):
        data_x2 = pd.concat([data_x2, worddf[257:614][wordcol[i][w]]], axis=1)
    data_x2.index = range(len(data_x2))

    '''
    mean_i = []
    std_i = []
    for w in range(len(wordcol[i])):
        mean_i.append(data_x2[wordcol[i][w]].mean())
        std_i.append(data_x2[wordcol[i][w]].std())
        data_x2[wordcol[i][w]] = (data_x2[wordcol[i][w]] - data_x2[wordcol[i][w]].mean()) / data_x2[wordcol[i][w]].std()
    '''

    data_y = pd.read_csv(difffile)['rate']

    data = pd.concat([data_x, data_x2, data_y], axis=1)

    m = smf.ols(formula=formulas[i], data=data).fit()
    pred_x = pd.read_csv(externalfile)[616:][externalcol]
    pred_x.index = range(len(pred_x))
    print(pred_x.tail())
    pred_x2 = pd.DataFrame()
    for w in range(len(wordcol[i])):
        pred_x2 = pd.concat([pred_x2, worddf[616:][wordcol[i][w]]], axis=1)
    pred_x2.index = range(len(pred_x2))
    print(pred_x2)
    '''
    for w in range(len(wordcol[i])):
        pred_x2[wordcol[i][w]] = (pred_x2[wordcol[i][w]] - mean_i[w]) / std_i[w]
    '''
    pred_x = pd.concat([pred_x, pred_x2], axis=1)
    pred_y = m.predict(pred_x)

    print(pred_y)

    df[names_e[i]] = pred_y

df.to_csv('regression2.csv')