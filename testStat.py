from collections import defaultdict
import os

problems = open('author.txt').read().strip().split('\n')

haveTests = open('haveTests.txt').read().strip().split('\n')

authorDict = defaultdict(lambda: [])

for problem in problems:
    [problemName, author] = problem.split(' ')
    authorDict[author].append(problemName)

stats = []

for author in authorDict.keys():
    missing = []
    empty = []

    owned = authorDict[author]

    for problemName in owned:
        if not (problemName in haveTests):
            missing.append(problemName)
        elif not len(os.listdir('./tests/' + problemName)):
            empty.append(problemName)

    stats.append([author, owned, missing, empty])

stats.sort(key=lambda item: len(item[2]) + len(item[3]), reverse=True)

s = ''

for item in stats:
    [author, owned, missing, empty] = item
    s += author + ',' + str(len(owned)) + ',' + str(len(missing)) + ',' + str(len(empty)) + ',' + '|'.join(missing) + ',' + '|'.join(empty) + '\n'

open('stats.csv', 'w').write('Author,Problems owned, Problems with tests missing (count),Problems with 0 test (count),Problems with tests missing, Problems with 0 test\n' + s)