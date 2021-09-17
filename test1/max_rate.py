import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

population = pd.read_csv('population.csv', index_col=0, usecols=['日付', '福岡天神'])

# from 2020-01-06(Mon)
mon = population[5:607:7]['福岡天神'].values.tolist()
tue = population[6:607:7]['福岡天神'].values.tolist()
wed = population[7:607:7]['福岡天神'].values.tolist()
thur = population[8:607:7]['福岡天神'].values.tolist()
fri = population[9:607:7]['福岡天神'].values.tolist()
sat = population[10:607:7]['福岡天神'].values.tolist()
sun = population[11:607:7]['福岡天神'].values.tolist()

week_len = len(mon)
date_mon = pd.date_range(start='20200106', periods=week_len, freq='7D')

weekdf2 = pd.DataFrame(columns=['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun', 'max', 'min'])
for i in range(week_len):
    maxpop = max(np.array([mon[i], tue[i], wed[i], thur[i], fri[i], sat[i], sun[i]]))
    minpop = min(np.array([mon[i], tue[i], wed[i], thur[i], fri[i], sat[i], sun[i]]))
    new = pd.DataFrame({'mon': mon[i]/maxpop,
                        'tue': tue[i]/maxpop,
                        'wed': wed[i]/maxpop,
                        'thur': thur[i]/maxpop,
                        'fri': fri[i]/maxpop,
                        'sat': sat[i]/maxpop,
                        'sun': sun[i]/maxpop,
                        'max': maxpop,
                        'min': minpop}, index=[0])
    weekdf2=weekdf2.append(new, ignore_index=True)

weekdf2.index=date_mon
weekdf2.to_csv('perc_max_fuku.csv', index_label='date_mon')

