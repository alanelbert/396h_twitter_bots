import pandas as pd
import json
import numpy as np

if __name__ == '__main__':

    with open('data/twibot-22.csv', 'r') as f:
        rawcsv = f.read()

    botidents = {ele.split(',')[0] : ele.split(',')[1] for ele in rawcsv.split('\n')[1:-1]}
    
    listfiles = ['data/list1.json', 'data/list2.json', 'data/list5.json']

    print("labels loaded!")
    for lfile in listfiles:

        print(lfile)

        labels = []
        text = []

        with open(lfile, 'r') as f:
            data = json.load(f)
    
        for id in data:
            for ele in data[id]:
                text += [ele['text']]
                labels += [botidents[id]]
        
    pd.DataFrame(
        {
        "labels": labels,
        "text": text
        }
    ).to_csv('data/processed2.csv', columns=['labels', 'text'], index=False)

    #pd.DataFrame(data=np.array([labels, text]).transpose()).to_csv('data/processed.csv', columns=['labels', 'texts'])
    