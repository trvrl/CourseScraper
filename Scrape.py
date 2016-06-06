from lxml import html
import requests

BASE_URL = "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=1&dept=CPSC"
URL = "https://courses.students.ubc.ca/"

def grab_html(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def grab_courses(tree):
    course_code = tree.xpath('//tr[@class="section1"]/td/a/text() | //tr[@class="section2"]/td/a/text()')
    course_title = tree.xpath('//tr[@class="section1"]/td/text() | //tr[@class="section2"]/td/text()')
    course_url = tree.xpath('//tr[@class="section1"]/td/a/@href | //tr[@class="section2"]/td/a/@href')
    course_list = {}
    for i in range(0, len(course_title)):
        course_list[course_code[i]] = {"title": course_title[i], "url": URL + course_url[i], "prereqs" : "", "pr-plain" : ""}
    return course_list

tree = grab_html(BASE_URL)

course_dict = grab_courses(tree)


def grab_prereq(course):
    course_page = html.fromstring(requests.get(course['url']).content)
    # text = course_page.xpath('//div[@role="main"]/p/[1]')
    div = course_page.xpath('//div[@role="main"]/p/a/text()')
    course["prereqs"] = div
    # course["pr-plain"] = text

for key in course_dict:
    grab_prereq(course_dict[key])

for key in course_dict:
    print (key + " : \t\t" + course_dict[key]["title"] + "\t\t" + course_dict[key]["url"] + "\t\t")
    print (course_dict[key]["pr-plain"])
