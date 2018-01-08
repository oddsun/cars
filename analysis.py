import pandas as pd
import os, time
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col as sc

# from sklearn import linear_model as lm

dates = [str(x) for x in range(2017, 2010, -1)]

print(dates)

myroot = ''
filename = "CarPriceData.csv"
filename2 = "CarPriceData2.csv"
filename4 = "CarPriceData4v2.csv"

if not os.path.exists(myroot + filename4):

    if not os.path.exists(myroot + filename2):

        if not os.path.exists(myroot + filename):
            data = [pd.read_csv(myroot + date + '/' + filename, index_col=0) for date in dates]
            mytable = pd.concat(data)
            mytable.to_csv(myroot + filename)
        else:
            mytable = pd.read_csv(myroot + filename, index_col=0)

        headers = mytable.columns
        for i in [4, 5, -1]:
            mytable[headers[i]] = pd.to_numeric(mytable[headers[i]].str.split(' ').str[1].str.replace(',', ''))

        mytable['State'] = mytable[headers[2]].str.split(':').str[1].str.split('-').str[0].str.strip()
        mytable['City'] = mytable[headers[2]].str.split(':').str[1].str.split('-').str[1].str.strip()

        mystrings = [' SOUTH', ' NORTH', ' EAST', ' WEST']
        for mystr in mystrings:
            mytable.City = mytable.City.str.replace(mystr, '')

        mytable.to_csv(myroot + filename2)

    else:
        mytable = pd.read_csv(myroot + filename2, index_col=0)

else:
    mytable = pd.read_csv(myroot + filename4, index_col=0)

headers = list(mytable.columns)
headers[0:12] = ['Name', 'Title', 'Loc', 'AucD', 'ActP', 'RepCost', 'Odometer', 'PDmg', 'SDmg', 'PSold', 'State',
                 'City']
mytable.columns = headers
mytable['year'] = mytable.AucD.str.split('/').str[-1]
mytable.PDmg = mytable.PDmg.str.lower()

mytable.DP02_0001E = mytable.DP02_0001E.astype(float) / 1000.0

myheaders = ['DP05_0066PE', 'DP05_0033PE', 'DP03_0086E', 'DP02_0151E', 'DP02_0151PE', 'DP02_0001E',
             'DP03_0062E']

regressors = headers[4:5] + myheaders
mytable2 = mytable.dropna(axis=0, how='any', subset=regressors)
mytable2 = mytable2.sort_values(by=['year', 'county'], ascending=False)
print(mytable2.head(10))
regressors += ['Intercept']
startt = time.time()
results = smf.ols(formula="PSold ~ ActP", data=mytable2, missing='drop').fit(cov_type='cluster',
                                                                             cov_kwds={'groups': mytable2.county},
                                                                             use_t=True)
print(time.time() - startt)
results2 = smf.ols(formula="PSold ~ ActP + C(Loc)+C(year)+C(PDmg)+C(Name)", data=mytable2,
                   missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.county})
print(time.time() - startt)
results3 = smf.ols(formula="PSold ~ ActP + DP05_0066PE +C(year)+C(PDmg)+C(Name)", data=mytable2,
                   missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.county})
print(time.time() - startt)
results32 = smf.ols(formula="PSold ~ ActP + DP05_0033PE +C(year)+C(PDmg)+C(Name)", data=mytable2,
                    missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.county})
print(time.time() - startt)
results41 = smf.ols(formula="PSold ~ ActP + DP02_0151PE +C(year)+C(PDmg)+C(Name)", data=mytable2,
                    missing='drop').fit(cov_type='HC1')
print(time.time() - startt)
results4 = smf.ols(formula="PSold ~ ActP + DP02_0151PE +C(year)+C(PDmg)+C(Name)", data=mytable2,
                   missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.county})
print(time.time() - startt)
results5 = smf.ols(formula="PSold ~ ActP + DP03_0086E +C(year)+C(PDmg)+C(Name)", data=mytable2,
                   missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.county})
print(time.time() - startt)
results6 = smf.ols(formula="PSold ~ ActP + DP02_0001E +C(year)+C(PDmg)+C(Name)", data=mytable2,
                   missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.county})
print(time.time() - startt)
results52 = smf.ols(formula="PSold ~ ActP + DP03_0062E +C(year)+C(PDmg)+C(Name)", data=mytable2,
                    missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.county})
print(time.time() - startt)
results7 = smf.ols(formula="PSold ~ ActP + DP02_0151PE + DP02_0001E + C("
                           "year)+C(PDmg)+C(Name)", data=mytable2,
                   missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.county})
print(time.time() - startt)
results8 = smf.ols(formula="PSold ~ ActP + DP02_0151PE + DP02_0001E + C("
                           "year)+C(PDmg)+C(Name)", data=mytable2,
                   missing='drop').fit(cov_type='cluster', cov_kwds={'groups': mytable2.Name})
print(time.time() - startt)
tble = sc([results, results2, results3, results32, results5, results41, results4, results6, results52, results7, results8],
          regressor_order=regressors, stars=True, float_format='%0.2f',
          model_names=['I', 'II', 'III', 'IV', 'V', 'VI', 'VI(2)', 'VII', 'VIII', 'IX', 'X'],
          info_dict={'N': lambda x: "{0:d}".format(int(x.nobs)),
                     'R2': lambda x: "{:.2f}".format(x.rsquared)})
mylist = [i for i in range(0, 16)] + [-2, -1]
tble.tables[0] = tble.tables[0].iloc[mylist, :]
print(type(tble.tables[0]))
print(tble)

# demofile = myroot+"demo2016v4.csv"
# df = pd.read_csv(demofile, index_col=0)
# df.drop(0, inplace=True)
# df.drop(columns=['NAME', 'state', 'county'], inplace=True)
# df = df.astype(float)
# # print(df.head(10))
df = mytable[myheaders]
print(df.corr())


avgprice = mytable.groupby(by='State')[headers[-3]].mean()
salescount = mytable.groupby(by='State')[headers[-3]].count()
# print(avgprice)
# plt.bar(avgprice.keys(), avgprice.values)
# plt.bar(salescount.keys(), salescount.values)
# plt.show()
#
# plt.plot(mytable[headers[5]], mytable[headers[-3]], 'ro')
# plt.show()
# print(mytable.head(10))

# fig, ax1 = plt.subplots()
# ax1.bar(avgprice.keys(), avgprice.values, position=1)
# ax2 = ax1.twinx()
# ax2.bar(salescount.keys(), salescount.values, color='orange', position=0)
# plt.show()

# fig = plt.figure()
# ax = avgprice.plot(kind='bar', color='orange', position=1)
# ax2 = ax.twinx()  # Create another axes that shares the same x-axis as ax.
# salescount.plot(kind='bar', color='blue', ax=ax2, position=0)
# plt.show()

# print(results3.summary())
