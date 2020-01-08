import requests, threading, os, zipfile, time
from bs4 import BeautifulSoup

# For debugging, please comment out 2 lines below when you are running (in case I forget)
# s.proxies = {'https': 'http://localhost:8080'}
# s.verify = False

BASE_URL = 'https://www.spoj.com/'

def login(username, password):
    return s.post(BASE_URL + 'login/', data={
        'login_user': username,
        'password': password
    }, allow_redirects=False)

def getTestsDataInfo(problemId):
    while 1:
        try:
            html = s.get(BASE_URL + 'problems/'+ problemId +'/edit/').text

            soup = BeautifulSoup(html, features='html.parser')

            testDataElem = soup.find_all('tr', {'class': 'problemrow_'})

            enabled = list(map(lambda elem: 'checked' in elem.find_all('td')[-1].find('input').attrs, testDataElem))

            return enabled
        except Exception as e:
            print(e)

def downloadTestAsText(problemId, path, i):
    while 1:
        try:
            i = str(i)
            baseUrl = BASE_URL + 'problems/' + problemId

            input = s.get(baseUrl + '/' + i + '.in').text

            output = s.get(baseUrl + '/' + i + '.out').text

            if not (input and output):
                return

            if (input and output):
                print('Downloaded test ' + i + ' for problem ' + problemId)
                open(path + '/' + i + '.in', 'w').write(input)
                open(path + '/' + i + '.out', 'w').write(output)
        except Exception as e:
            print(e)

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

        if not len(list(filter(lambda enabled: enabled, enabledInfo))):
            return

        zipPath = tempFolder + '/' + problemId + '.zip'
        extractedProblemPath = tempFolder + '/' + problemId
        problemTestsFolder = testsFolder + '/' + problemId

        open(zipPath, 'wb').write(s.post(BASE_URL + 'problems/' + problemId + '/edit2/', data={'form_action': 'export'}).content)

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

def getEditableProblems(start = 0, sort = 5):
    html = s.get(BASE_URL + 'problems/editable/', params={
        'start': start,
        'sort': sort
    }).text

    # print(html)

    soup = BeautifulSoup(html, features='html.parser')

    # print(soup.text)

    problemElem = soup.find_all('tr', {'class': 'problemrow_'})

    codes = list(map(lambda elem: elem.find_all('td')[-1].text.strip(), problemElem))

    return codes

if __name__ == '__main__':
    crawledTests = set(os.listdir('./tests'))

    s = requests.session()

    accounts = open('accounts.csv').read().strip().split('\n')

    for account in accounts:
        s = requests.session()

        t = time.time()

        [username, password] = account.split(',')

        username = username.strip()
        password = password.strip()

        print('Crawling tests for account ' + username)

        login(username, password)

        start = 0

        while 1:
            codes = getEditableProblems(start)

            if not codes:
                break

            threads = []

            for code in codes:
                if code in crawledTests:
                    print('Crawled ' + code + ' already, skipping')
                    continue

                print('Crawling tests for ' + code)
                crawledTests.add(code)

                t = threading.Thread(target=downloadAllTestsAsText, args=(code,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            start += len(codes)