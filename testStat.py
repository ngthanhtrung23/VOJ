from collections import defaultdict

problems = open('author.txt').read().strip().split('\n')

haveTests = open('haveTests.txt').read().strip().split('\n')

authorDict = defaultdict(lambda: [])

for problem in problems:
    [problemName, author] = problem.split(' ')
    authorDict[author].append(problemName)

stats = []

for author in authorDict.keys():
    missing = []

    owned = authorDict[author]

    for problemName in owned:
        if not (problemName in haveTests):
            missing.append(problemName)

    stats.append([author, owned, missing])

stats.sort(key=lambda item: len(item[2]), reverse=True)

s = ''

for item in stats:
    [author, owned, missing] = item
    s += author + ',' + str(len(owned)) + ',' + str(len(missing)) + ',' + '|'.join(missing) + '\n'

open('stats.csv', 'w').write('Author,Problems owned, Problems with tests missing (count), Problems with tests missing\n' + s)