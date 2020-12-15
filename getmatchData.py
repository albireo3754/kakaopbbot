import pandas as pd

from ConstURL import ConstURL

ConstURL = ConstURL()
print(ConstURL.api)
prodata = pd.read_csv('nickplusID.csv',index_col= 0 ,header=0)

