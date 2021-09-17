import pandas as pd
import numpy as np

perc_max = pd.read_csv('perc_max_fuku.csv', index_col=0)

mean_max = []
var_max = []
mid_max = []

for i in range(7):
    maxt = np.array(perc_max.iloc[:, i].values.tolist())
    mid_max.append(np.median(maxt))
    sum1m = maxt.sum()
    maxt2 = maxt * maxt
    sum2m = maxt2.sum()
    meanm = sum1m/len(maxt)
    mean_max.append(meanm)
    var_max.append(sum2m/len(maxt)-meanm**2)

stat = pd.DataFrame({
    'mean_max': mean_max,
    'var_max': var_max,
    'mid_max': mid_max
})

stat.index = ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun']
stat.to_csv('stat2_fuku.csv', index_label='week')


