import requests, json, os
import pandas as pd
# from bs4 import BeautifulSoup

myroot = ''
# if not os.path.exists(myroot):
#     os.mkdir(myroot)
demofile = myroot+"demo2016-2013v2.csv"
datafile = myroot+"CarPriceData3.csv"
datafile2 = myroot+"CarPriceData4v2.csv"
years = [str(i) for i in range(2016,2012,-1)]
dflist = []
myacs = '/acs'
# mylist = ['CP02_001E', 'CP03_062E', 'CP03_086E', 'CP02_151E', 'CP05_033E', 'CP05_066E']

if not os.path.exists(demofile):
    for year in years:
        if int(year) == 2014:
            myacs=''
        # mynewlist = ['_'.join([x.split('_')[0], year, x.split('_')[1]]) for x in mylist]
        # if not os.path.exists(demofile):
        url = 'https://api.census.gov/data/'+year + myacs + '/acs1/profile?'
        params = {
            'get': ['DP03_0062E', 'DP03_0086E', 'DP02_0151E', 'DP02_0151PE', 'DP02_0001E', 'DP05_0033PE', 'DP05_0066PE'],
            # 'get': mynewlist,
            'for': ['county:*'],
            'key': ['5b621d2d6060f68caca5d564c726fbdccf99e93e']}

        url += '&'.join([key+'='+','.join(value) for key, value in params.items()])

        print(url)

        r = requests.get(url)

        mydata = json.loads(r.text)
        headers = mydata[0:1][0]
        df = pd.DataFrame(mydata[1:], columns=headers)
            # df.to_csv(demofile)
        # else:
        #     df = pd.read_csv(demofile, index_col=0)

        # df.drop(0, inplace=True)
        df.county = df.state.astype(int)*1000+df.county.astype(int)
        # df.columns= mylist
        # for i in [3,4,5]:
        #     df[mylist[i][:-2]+'PE'] = (df[mylist[i]].astype(float)/df[mylist[0]].astype(float)).round(1)
        df['year'] = int(year)+1
        print(df.head(10))
        dflist += [df]
    df = pd.concat(dflist)
    df = df.apply(pd.to_numeric, errors='coerce')
    # df = df.astype(float)
    # print(df.head(10))
    df = df[df > 0]
    df = df.dropna()
    # print(df.head(10))
    df.to_csv(demofile)
else:
    df = pd.read_csv(demofile, index_col=0)
    print(df.dtypes)
# print(df.head(10))

r = pd.read_csv(datafile, index_col=0)
headers = r.columns
r['year'] = pd.to_numeric(r[headers[3]].str.split('/').str[-1])
r.county = pd.to_numeric(r.county, errors='coerce')
r.dropna(subset=['county'])
df2 = pd.merge(r, df, how='inner', on=['county', 'year'])
df2.to_csv(datafile2)
