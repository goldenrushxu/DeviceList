import pandas as pd
from datetime import datetime

with open("config_devicelist", 'r', encoding='utf8') as f:
    conf = f.readlines()
#more to do:
#1. auto duplicate XB terminals with :WH connection points
# VVVVV 3. write a log file to record what has been done to a the specific file

fpath = conf[0].lstrip('filename:').rstrip('\n')
df = pd.read_excel(fpath)
df.drop(df[df['Device Tag'].duplicated()].index, inplace=True)      #delete duplicated items
df.sort_values('Device Tag',inplace=True)                             #sort by locations

Locs_del= conf[1].lstrip('Locations to delete:').rstrip('\n').split(",")
for i in Locs_del:
    filt = df['Location'] == i
    df.drop(df[filt].index, inplace=True)      #delete duplicated items

Cont_del= conf[2].lstrip('Contents to delete:').rstrip('\n').strip(' ').split(",")
for i in Cont_del:
    filt = df['Device Tag'].str.contains(i)
    df.drop(df[filt].index, inplace=True)      #delete items with unwanted contents 


filt = df['Device Tag'].str.contains('-W') | ~(df['Device Tag'].str.contains('-'))  
df.drop(df[filt].index, inplace=True)      #delete duplicated items


temp = df['Location'].value_counts()._info_axis.sort_values()
with open((fpath.rstrip('.xls') + ".txt"), 'w', encoding='utf8') as f:
    for i in temp:
        divider = "===" + str(i) + "===\n"
        f.write(divider)
        df_string = df.loc[df['Location'] == i]['Device Tag'].to_string(header = False, index = False)        #filter all the labels inside a location
        df_string = df_string.replace(' ','').replace("'",'').replace("+"+i,'')             #delete all the ' symbles, and also space
        f.write(df_string + "\n")         #write to the file


print("Over!, time:",datetime.now().strftime("%H:%M:%S"))
