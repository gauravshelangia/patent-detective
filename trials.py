# this file contains the code, which I have written for trial or testing purpose.

import seaborn as sns
avg_inventors[:10]
index = ['US','FR','GB','AT','CH','CA','AU']
columns = ['country_code','filing_year']
shortned_avg_inventors = pd.DataFrame(avg_inventors[:300],columns=columns, )
asd = shortned_avg_inventors.dropna()
# plt.pcolor(shorted_avg_inventors)
plt.yticks(asd, asd.index)
# plt.xticks(shorted_avg_inventors , shorted_avg_inventors.columns)
# plt.show()
