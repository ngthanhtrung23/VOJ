import os, json, re
from collections import defaultdict

statementPath = './statement'

filenames = os.listdir(statementPath)

c = defaultdict(list)

for name in filenames:
    content = open(statementPath + '/' + name).read()

    c[content.count('subsubsection')].append(name)

arr = []

for k in c.keys():
    arr.append([k, len(c[k])])

arr.sort(key=lambda item: item[1], reverse=True)

for item in arr:
    print(item)

pattern = 'subsubsection{(.+?)}'
subsectionInfoFolderPath = './subsectionsInfo'

for k in c.keys():
    subsectionInfoPath = subsectionInfoFolderPath + '/' + str(k) + 'subsections.csv'

    open(subsectionInfoPath, 'w').close()

    for name in c[k]:
        content = open(statementPath + '/' + name).read()

        matches = list(map(lambda text: text.strip(), re.findall(pattern, content)))

        open(subsectionInfoPath, 'a').write(name + ',' + ','.join(matches) + '\n')