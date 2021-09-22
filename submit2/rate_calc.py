import statsmodels.formula.api as smf
import pandas as pd

names_e = ['shibuya', 'shinjyuku', 'marunouchi', 'shinagawa', 'shimokitazawa', 'hachiouji',
           'osaka', 'sapporo', 'sendai', 'fukuoka']
externalcol = ['in_GW', 'in_S', 'in_emer', 'start_emer', 'end_emer']
wordcol = [['recipe', 'remote', 'takeout', 'delivery', 'remote_nomi', 'ticket'],
           ['recipe', 'remote', 'takeout', 'remote_nomi', 'delivery', 'ticket'],
           ['manga', 'delivery', 'bicycle'],
           ['manga', 'delivery', 'bicycle'],
           ['recipe', 'game', 'convenient', 'remote_nomi', 'takeout', 'delivery'],
           ['delivery', 'manga', 'recipe', 'takeout', 'remote', 'remote_nomi'],
           ['delivery', 'recipe', 'takeout', 'remote_nomi', 'ticket', 'remote'],
           ['manga', 'bicycle', 'delivery'],
           ['delivery', 'takeout', 'recipe', 'bicycle', 'manga', 'ticket'],
           ['delivery', 'manga', 'bicycle', 'takeout', 'recipe']]
formulas = ['rate~in_GW+in_S+in_emer+start_emer+end_emer+recipe+remote+takeout+delivery+remote_nomi+ticket+shibuya',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+recipe+remote+takeout+remote_nomi+delivery+ticket+shinjyuku',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+manga+delivery+bicycle',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+manga+delivery+bicycle+shinagawa',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+recipe+game+convenient+remote_nomi+takeout+delivery+shimokitazawa',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+delivery+manga+recipe+takeout+remote+remote_nomi+hachiouji',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+delivery+recipe+takeout+remote_nomi+ticket+remote+osaka',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+manga+bicycle+delivery+sapporo',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+delivery+takeout+recipe+bicycle+manga+ticket+sendai',
            'rate~in_GW+in_S+in_emer+start_emer+end_emer+delivery+manga+bicycle+takeout+recipe+fukuoka']
start_index2 = [257, 257, 257, 257, 257,
                257, 243, 257, 257, 306]

df = pd.DataFrame()

worddf = pd.read_csv('word.csv')
weatherdf = pd.read_csv('weather_to21.csv')

for i in range(10):
    externalfile = 'external_' + names_e[i] + '.csv'
    difffile = 'diff_' + names_e[i] + '.csv'
    data_x = pd.read_csv(externalfile)[start_index2[i]:614][externalcol]
    data_x.index = range(len(data_x))
    data_x2 = pd.DataFrame()
    for w in range(len(wordcol[i])):
        data_x2 = pd.concat([data_x2, worddf[start_index2[i]:614][wordcol[i][w]]], axis=1)
    data_x2.index = range(len(data_x2))

    data_x3 = weatherdf[start_index2[i]:614][names_e[i]]
    data_x3.index = range(len(data_x3))

    '''
    mean_i = []
    std_i = []
    for w in range(len(wordcol[i])):
        mean_i.append(data_x2[wordcol[i][w]].mean())
        std_i.append(data_x2[wordcol[i][w]].std())
        data_x2[wordcol[i][w]] = (data_x2[wordcol[i][w]] - data_x2[wordcol[i][w]].mean()) / data_x2[wordcol[i][w]].std()
    '''

    data_y = pd.read_csv(difffile)['rate']

    if i == 2:
        data = pd.concat([data_x, data_x2, data_y], axis=1)
    else:
        data = pd.concat([data_x, data_x2, data_x3, data_y], axis=1)

    m = smf.ols(formula=formulas[i], data=data).fit()
    pred_x = pd.read_csv(externalfile)[616:][externalcol]
    pred_x.index = range(len(pred_x))
    print(pred_x.tail())
    pred_x2 = pd.DataFrame()
    for w in range(len(wordcol[i])):
        pred_x2 = pd.concat([pred_x2, worddf[616:][wordcol[i][w]]], axis=1)
    pred_x2.index = range(len(pred_x2))
    print(pred_x2)
    pred_x3 = weatherdf[616:625][names_e[i]]
    pred_x3.index = range(len(pred_x3))
    '''
    for w in range(len(wordcol[i])):
        pred_x2[wordcol[i][w]] = (pred_x2[wordcol[i][w]] - mean_i[w]) / std_i[w]
    '''
    if i == 2:
        pred_x = pd.concat([pred_x, pred_x2], axis=1)
    else:
        pred_x = pd.concat([pred_x, pred_x2, pred_x3], axis=1)
    pred_y = m.predict(pred_x)

    print(pred_y)

    df[names_e[i]] = pred_y

df.to_csv('regression3.csv')