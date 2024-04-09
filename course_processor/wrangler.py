import json
import re


def start(unnest):
    sort(unnest)
    reformat()
    hyperlink_requisites()


# Bubble sort algorithm to sort the courses json, and disgard unnecessary nesting of objects. Input false into this method
# if the courses.json does not have courses nested in Items.
def sort(unnest):
    print('Sorting courses and course requisites')
    f = open('courses.json')
    courses = json.load(f)
    f_req = open('requisites.json')
    reqs = json.load(f_req)
    if unnest:
        courses = courses["Items"]

    if len(courses) != len(reqs):
        print(
            f"Serious issue! There are {len(courses)} courses, but there are {len(reqs)} requisites, which is a mismatch. Consider re-running the scraper.")

    for i in range(1, len(courses)):
        for j in range(len(courses) - i):

            if courses[j]["CourseCode"] > courses[j + 1]["CourseCode"]:
                temp = courses[j + 1]
                courses[j + 1] = courses[j]
                courses[j] = temp

            if reqs[j]["courseCode"] > reqs[j + 1]["courseCode"]:
                temp = reqs[j + 1]
                reqs[j + 1] = reqs[j]
                reqs[j] = temp
    print('Writing to file')
    f = open('courses.json', 'w')
    f_req = open('requisites.json', 'w')
    f_req.write(json.dumps(reqs, indent=4))
    f.write(json.dumps(courses, indent=4))
    print('Sorting courses and course requisites.')
    print('Sort finished')


# Things like remove unnecessary line breaks, removing awkward spaces before periods etc.
def reformat():
    print('Removing unnecessary linebreaks')
    reqs = json.load(open('requisites.json'))
    courses = json.load(open('courses.json'))
    for i in range(len(reqs)):
        reqs[i]["req"] = reformat_reqs(reqs[i]["req"], courses)
    print('Writing to file')
    f = open('requisites.json', 'w')
    f.write(json.dumps(reqs, indent=4))
    print('Linebreaks removed')



def reformat_reqs(requisite, courses):
    words = re.split(r'\n', requisite)
    for i in range(len(words)):
        if has_course(words[i], courses):
            requisite = requisite.replace(f"\n{words[i]}\n", f" {words[i]} ")
    requisite = requisite.replace(" .", ".")
    requisite = requisite.replace(" ,", ",")
    requisite = requisite.replace(" ;", ";")
    return requisite


#Scans through entire requisites json and replace any words that are an ANU course with a hyperlinked version.
def hyperlink_requisites():
    print('Hyperlinking course codes in requisites')
    f = open('requisites.json')
    reqs = json.load(f)
    courses = json.load(open('courses.json'))
    for i in range(len(reqs)):
        reqs[i]["req"] = hyperlink_requisite(reqs[i]["req"], courses)
    print('Writing to file')
    f = open('requisites.json', 'w')
    f.write(json.dumps(reqs, indent=4))
    print('Hyperlinking process complete')


# Hyperlinks one requisite string
def hyperlink_requisite(requisite, courses):
    words = re.split(r'\s+', requisite)
    linked_words = []
    for i in range(len(words)):
        if has_course(words[i], courses) and words[i] not in linked_words:
            requisite = requisite.replace(words[i], get_hyperlinked_course(words[i]))
            linked_words.append(words[i])
    return requisite


# Performs a binary search on courses and returns if word is in courses.
def has_course(word, courses):
    if len(word) > 12:
        return False
    l = 0
    r = len(courses) - 1
    m = r // 2
    while l < r:
        mc = courses[m]['CourseCode']
        if word == mc:
            return True
        elif word < mc:
            r = m - 1
        elif word > mc:
            l = m + 1
        m = (l + r) // 2
    if courses[m]['CourseCode'] == word:
        return True
    else:
        return False


def get_hyperlinked_course(courseCode):
    return f"[{courseCode}](https://programsandcourses.anu.edu.au/2024/course/{courseCode})"


def replace(s, keyword, replacement):
    return re.sub(r'\b%s\b' % re.escape(keyword), replacement, s)


start(False)