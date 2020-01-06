import requests, threading, os, zipfile
from bs4 import BeautifulSoup

s = requests.session()

def login(username, password):
    return s.post('http://www.spoj.com/login/', data={
        'login_user': username,
        'password': password
    })

def getTestsDataInfo(problemId):
    html = s.get('http://www.spoj.com/problems/'+ problemId +'/edit/').text

    soup = BeautifulSoup(html, features='html.parser')

    testDataElem = soup.find_all('tr', {'class': 'problemrow_'})

    enabled = list(map(lambda elem: 'checked' in elem.find_all('td')[-1].find('input').attrs, testDataElem))

    return enabled

def downloadTestAsText(problemId, path, i):
    i = str(i)
    baseUrl = 'http://www.spoj.com/problems/' + problemId

    input = s.get(baseUrl + '/' + i + '.in').text

    output = s.get(baseUrl + '/' + i + '.out').text

    if not (input and output):
        return

    if (input and output):
        print('Downloaded test ' + i + ' for problem ' + problemId)
        open(path + '/' + i + '.in', 'w').write(input)
        open(path + '/' + i + '.out', 'w').write(output)

def downloadAllTestsAsText(problemId, path ='./tests'):
    enabledInfo = getTestsDataInfo(problemId)

    path = path + '/' + problemId

    os.makedirs(path, exist_ok=True)

    for i in range(len(enabledInfo)):
        if not enabledInfo[i]:
            continue

        try:
            t = threading.Thread(downloadTestAsText(problemId, path, i))
            t.start()
        except Exception as e:
            print(e)

def downloadAllTestsFromZip(problemId, tempFolder = './temp', testsFolder = './tests'):
    try:
        enabledInfo = getTestsDataInfo(problemId)

        zipPath = tempFolder + '/' + problemId + '.zip'
        extractedProblemPath = tempFolder + '/' + problemId
        problemTestsFolder = testsFolder + '/' + problemId

        open(zipPath, 'wb').write(s.post('http://www.spoj.com/problems/' + problemId + '/edit2/', data={'form_action': 'export'}).content)

        zipfile.ZipFile(zipPath, "r").extractall(extractedProblemPath)

        os.remove(zipPath)

        os.makedirs(problemTestsFolder, exist_ok=True)

        for i in range(len(enabledInfo)):
            if not enabledInfo[i]:
                continue

            ii = str(i)
            os.replace(extractedProblemPath + '/' + ii + '.in', problemTestsFolder + '/' + ii + '.in')
            os.replace(extractedProblemPath + '/' + ii + '.out', problemTestsFolder + '/' + ii + '.out')

            os.removedirs(extractedProblemPath)

        print('Downloaded tests for ' + problemId)
    except Exception as e:
        print('Error while downloading tests for ' + problemId + ': ' + str(e))

def getAuthoredProblems(start = 0, sort = 5):
    html = s.get('http://www.spoj.com/problems/my/', params={
        'start': start,
        'sort': sort
    }).text

    # print(html)

    soup = BeautifulSoup(html, features='html.parser')

    # print(soup.text)

    problemElem = soup.find_all('tr', {'class': 'problemrow_'})

    codes = list(map(lambda elem: elem.find_all('td')[-1].text.strip(), problemElem))

    return codes

accounts = open('accounts.csv').read().strip().split('\n')

for account in accounts:
    [username, password] = account.split(',')

    login(username, password)

    start = 0

    while 1:
        codes = getAuthoredProblems(start)

        if not codes:
            break

        for code in codes:
            print('Crawling tests for ' + code)

            t = threading.Thread(target=downloadAllTestsAsText, args=(code,))
            t.start()

        start += len(codes)