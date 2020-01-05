import os, re

statementPath = './statement'
extractedPath = './extracted'
subsectionInfoFolderPath = './subsectionsInfo'
lines = open(subsectionInfoFolderPath + '/3subsections.csv').read().strip().split('\n')

pattern = '\\\subsubsection{.+?}'
compiledPattern = re.compile(pattern)

for line in lines:
    name = line.split(',')[0]

    content = open(statementPath + '/' + name).read()

    name = name.split('.')[0]

    extractedProblemFolder = extractedPath + '/' + name

    try:
        os.mkdir(extractedProblemFolder)
    except Exception as e:
        # print(e)
        pass

    parts = compiledPattern.split(content)
    # print(name, len(parts))

    if (len(parts) != 4):
        print("Couldn't find 4 parts for " + name)
        continue

    [statement, input, output, notes] = parts
    open(extractedProblemFolder + '/statement.tex', 'w').write(statement.strip())
    open(extractedProblemFolder + '/input.tex', 'w').write(input.strip())
    open(extractedProblemFolder + '/output.tex', 'w').write(output.strip())
    open(extractedProblemFolder + '/notes.tex', 'w').write(notes.strip())