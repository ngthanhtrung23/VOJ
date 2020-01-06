import os, re
import shutil

from unidecode import unidecode
from collections import defaultdict

statementPath = './statement'
extractedPath = './extracted'
subsectionInfoFolderPath = './subsectionsInfo'


def format(word):
    return ''.join(c if c.isalnum() else '' for c in unidecode(word)).strip().lower().replace(' ','').replace('textbf', '')

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

    # for word in wordArr:
    #     print(word)

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

        statementFound = False

        while start < len(parts):
            partMatches = re.search(pattern2, parts[start])

            if partMatches:
                break

            statementFound = True
            statement += parts[start] + '\n'
            start += 1

        if not statementFound and start + 1 < len(parts):
            statement += parts[start + 1] + '\n'
            start += 2

        for i in range(start, len(parts) - 1):
            try:
                subsectionMatches = re.search(pattern2, parts[i])
                if not subsectionMatches or re.match(pattern2, parts[i + 1]):
                    continue
                subsectionName = subsectionMatches.group(1).strip()
                formattedSubsectionName = format(subsectionName)
                subsectionContent = parts[i + 1].strip() + '\n'

                content = subsectionName + '\n' + subsectionContent

                found = False

                for keyword in statementKeywords:
                    if keyword in formattedSubsectionName:
                        statement += content
                        found = True
                        break

                if found: continue

                for keyword in outputKeywords:
                    if keyword in formattedSubsectionName:
                        output += content
                        found = True
                        break

                if found: continue

                for keyword in inputKeywords:
                    if keyword in formattedSubsectionName:
                        input += content
                        found = True
                        break

                if found: continue

                notes += content
            except Exception as e:
                print(e)
                # print(parts)

        if not (statement and input and output):
            notFound = []
            if not statement:
                notFound.append('statement')
            if not input:
                notFound.append('input')
            if not output:
                notFound.append('output')
            if not notes:
                notFound.append('notes')
            print("Couldn't find 4 parts for " + name + ". Not found: " + ', '.join(notFound))
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

        tests = extractSampleTests(notes)

        if not tests:
            print("Can't extract sample tests for " + name)
        else:
            for i in range(len(tests)):
                open(extractedProblemFolder + '/TEST' + str(i + 1) + '.INP', 'w').write(tests[i][0])
                open(extractedProblemFolder + '/TEST' + str(i + 1) + '.OUT', 'w').write(tests[i][1])

def extractSampleTests(notes):
    statementKeywords = ['debai', 'yeucau', 'hanche', 'constraints', 'constraint', 'limit', 'phanbogioihantest']
    inputKeywords = ['input', 'dulieuvao', 'dulieu', 'quycachnhapdulieu']
    outputKeywords = ['output', 'ketqua', 'dulieura', 'quycachghiketqua']
    forbiddenKeywords = ['test', 'sample']

    forbiddenKeywords += statementKeywords + inputKeywords + outputKeywords

    def caseInconsistent(s):
        haveLower = False
        haveUpper = False

        for c in s:
            if c.islower():
                haveLower = True
            else:
                haveUpper = True

            if (haveUpper and haveLower):
                return True

        return False

    def forbidden(s):
        formatted = format(s)

        for keyword in forbiddenKeywords:
            if keyword in formatted:
                return True

        return False

    notes = notes.replace('}', '}\n').replace('\\', '\n\\')
    while ('\n\n' in notes):
        notes = notes.replace('\n\n', '\n')
    lines = notes.split('\n')
    pattern = '[.0-9 a-zA-Z-]+'

    tests = []

    inputContent = ''
    outputContent = ''
    inputMode = True

    for line in lines:
        line = line.strip()

        if re.match(pattern, line) and not (caseInconsistent(line) or forbidden(line)):
            if (inputMode):
                inputContent += line + '\n'
            else:
                outputContent += line + '\n'
        elif inputContent:
            if not inputMode:
                if (inputContent and outputContent):
                    tests.append([inputContent, outputContent])
                    inputContent = ''
                    outputContent = ''
            else:
                inputMode = False

    return tests

if __name__ == '__main__':
    # analyze()
    for i in range(3, 8):
        extractNSections(i)
