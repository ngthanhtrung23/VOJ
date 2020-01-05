import os, re
import shutil

from unidecode import unidecode
from collections import defaultdict

statementPath = './statement'
extractedPath = './extracted'
subsectionInfoFolderPath = './subsectionsInfo'


def format(word):
    return ''.join(c if c.isalnum() else '' for c in unidecode(word.decode('utf-8'))).strip().lower().replace(' ','').replace('textbf', '')

def analyze():
    wordArr = []
    wordCount = defaultdict(int)

    for i in range(1, 8):
        lines = open(subsectionInfoFolderPath + '/' + str(i) + 'subsections.csv').read().strip().split('\n')

        words = []

        for line in lines:
            words += line.split(',')[1:]

        words = list(map(format, words))

        for word in words:
            wordCount[word] += 1

    for word in wordCount.keys():
        if word:
            wordArr.append([word, wordCount[word]])

    wordArr.sort(key=lambda item: item[1], reverse=True)

    for word in wordArr:
        print(word)

def extract3Sections():
    lines = open(subsectionInfoFolderPath + '/3subsections.csv').read().strip().split('\n')

    pattern = '\\\subsubsection{.+}'
    compiledPattern = re.compile(pattern)

    for line in lines:
        name = line.split(',')[0]

        content = open(statementPath + '/' + name).read()

        name = name.split('.')[0]

        extractedProblemFolder = extractedPath + '/' + name

        parts = compiledPattern.split(content)
        # print(name, len(parts))

        if (len(parts) != 4):
            print("Couldn't find 4 parts for " + name)
            continue

        try:
            os.mkdir(extractedProblemFolder)
        except Exception as e:
            # print(e)
            pass

        [statement, input, output, notes] = parts
        open(extractedProblemFolder + '/statement.tex', 'w').write(statement.strip())
        open(extractedProblemFolder + '/input.tex', 'w').write(input.strip())
        open(extractedProblemFolder + '/output.tex', 'w').write(output.strip())
        open(extractedProblemFolder + '/notes.tex', 'w').write(notes.strip())

def extractNSections(n):
    pattern = '(\\\subsubsection{.+})'
    pattern2 = '\\\subsubsection{(.+)}'

    compiledPattern = re.compile(pattern)

    lines = open(subsectionInfoFolderPath + '/' + str(n) + 'subsections.csv').read().strip().split('\n')

    statementKeywords = ['debai', 'yeucau', 'hanche', 'constraints', 'constraint', 'limit', 'phanbogioihantest']
    inputKeywords = ['input', 'dulieuvao', 'dulieu', 'quycachnhapdulieu']
    outputKeywords = ['output', 'ketqua', 'dulieura', 'quycachghiketqua']

    for line in lines:
        name = line.split(',')[0]

        content = open(statementPath + '/' + name).read()

        name = name.split('.')[0]

        extractedProblemFolder = extractedPath + '/' + name

        try:
            shutil.rmtree(extractedProblemFolder)
        except Exception:
            pass

        parts = list(filter(lambda c: c, map(lambda c: c.strip(), compiledPattern.split(content))))

        statement = ''
        input = ''
        output = ''
        notes = ''

        # print(parts)

        start = 0

        while start < len(parts):
            partMatches = re.search(pattern2, parts[start])

            if not partMatches:
                statement += parts[start] + '\n'
                start += 1
            else:
                break

        for i in range(start, len(parts) - 1, 2):
            try:
                subsectionMatches = re.search(pattern2, parts[i])
                if not subsectionMatches:
                    continue
                subsectionName = subsectionMatches.group(1).strip()
                formattedSubsectionName = format(subsectionName)
                subsectionContent = parts[i + 1].strip() + '\n'

                content = subsectionName + '\n' + subsectionContent
                if formattedSubsectionName in statementKeywords:
                    statement += content
                elif formattedSubsectionName in inputKeywords:
                    input += content
                elif formattedSubsectionName in outputKeywords:
                    output += content
                else:
                    notes += content
            except Exception as e:
                print(e)
                print(parts)
                exit(0)

        if not (statement and input and output and notes):
            print("Couldn't find 4 parts for " + name)
            # if not statement:
            #     print('statement')
            # if not input:
            #     print('input')
            # if not output:
            #     print('output')
            # if not notes:
            #     print('notes')
            continue

        try:
            os.mkdir(extractedProblemFolder)
        except Exception as e:
            # print(e)
            pass

        open(extractedProblemFolder + '/statement.tex', 'w').write(statement.strip())
        open(extractedProblemFolder + '/input.tex', 'w').write(input.strip())
        open(extractedProblemFolder + '/output.tex', 'w').write(output.strip())
        open(extractedProblemFolder + '/notes.tex', 'w').write(notes.strip())

# analyze()
# extract3Sections()
for i in range(4, 8):
    extractNSections(i)