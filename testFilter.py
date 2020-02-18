import os

testFolder = './tests'

problems = list(filter(lambda folder: not '.' in folder, os.listdir(testFolder)))

for problem in problems:
    inputs = sorted(filter(lambda problem: '.in' in problem, os.listdir(testFolder + '/' + problem)), key=lambda item: int(item.replace('.in', '')))
    status = open(testFolder + '/' + problem + '/status.txt').read().strip().split(',')
    removed = [False] * len(inputs)
    filteredStatus = []

    for i in range(len(inputs)):
        if removed[i]:
            continue

        filteredStatus.append(status[i])

        for j in range(i + 1, len(inputs)):
            if removed[j]:
                break

            if (open(testFolder + '/' + problem + '/' + inputs[i]).read().strip() == open(testFolder + '/' + problem + '/' + inputs[j]).read().strip()):
                os.remove(testFolder + '/' + problem + '/' + inputs[j])
                print('Removed ' + problem + '/' + inputs[j] + ' because it\'s the same as ' + inputs[i])
                removed[j] = True

    open(testFolder + '/' + problem + '/status.txt', 'w').write(','.join(filteredStatus))

for problem in problems:
    tests = os.listdir(testFolder + '/' + problem)
    inputs = list(filter(lambda problem: '.in' in problem, tests))
    outputs = list(filter(lambda problem: '.out' in problem, tests))

    for output in outputs:
        if not output.replace('.out', '.in') in inputs:
            os.remove(testFolder + '/' + problem + '/' + output)
            print('Removed ' + problem + '/' + output + ' because input was removed')