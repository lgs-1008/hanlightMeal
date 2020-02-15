import requests
import datetime
from bs4 import BeautifulSoup
import re
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from crawler.models.meal import MealModel

def get_date():
    date = datetime.datetime.now().strftime('%Y%m')
    return date

def gsclear(string, i):
    gl = string #gl은 잠깐 담아놓는 그릇
    try:
        gl = gl[i]
        gl = str(gl)
        gl = gl.replace('[', '')
        gl = gl.replace(']', '')
        gl = gl.replace('<br/>', '\n')
        gl = gl.replace('<td class="textC last">', '')
        gl = gl.replace('<td class="textC">', '')
        gl = gl.replace('</td>', '')
        gl = gl.replace('(h)', '')
        gl = gl.replace('.', '')
        gl = gl.replace(',', '')
        gl = gl.replace('*', '')
        gl = gl.replace(' ', '')
        gl = re.sub(r"\d", "", gl) #정수형으로 오는 알러지기호 없애줌. 정규표현식
    except:
        gl = " "

    if(gl == ""):
        gl = "급식이 없습니다\n"

    return gl

def dayclear(string, i):
    gl = string
    try:
        gl = gl[i]
        gl = str(gl)
        gl = re.sub(r"\D", "", gl)

    except:
        gl = " "

    return gl

def get_html(D): #여기부터 D를 넣어주는 이유는 뒤에 날짜기 때문
    schYmd = get_date() + D #D는 문자열임

    URL = (
            "http://stu.sen.go.kr/sts_sci_md01_001.do?"
            "schulCode=B100000662&schulCrseScCode=4&schulKndScCode=04" # 학교코드10자리 고등학고 4, 04
            "&schMmealScCode=2&schYmd=%s" % (schYmd) #코드2는 중식, 포멧팅한건 날짜
        )# url 이쁘게 잘라줌
    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'html.parser')
    gshtml = soup.find_all("tr")
    return gshtml

def get_day(D, i): #위에 클리어 함수랑 인자 맞춰줘야함;
    day = get_html(D)
    day = day[0].find_all('th')
    return int(dayclear(day,i))

def get_meal(D, i): #위에 클리어 함수랑 인자 맞춰줘야함;
    gs = get_html(D)
    gs = gs[2].find_all('td') #gs는 급식, 소스코드 보면 3번째 tr안에 급식 내용이 있음. 0 1 2 해서 2
    return gsclear(gs,i)


if __name__ == "__main__":
    week = ["1","8","15","22","29"] #1주일 7일이니 7씩 더해진다. url에는 문자열로 합치니 문자열 형태로 저장
    Dayotw = [1,2,3,4,5] #월 화 수 목 금. 날짜를 받아올때는 1씩 더해서 사용, 식단은 그대로 사용.
    for D in week:
        for i in Dayotw:
            if int(datetime.datetime.now().strftime('%m'))==int((get_day(D,i+1)%10000)/100):
                MealModel(month = int((get_day(D,i+1)%10000)/100), date = get_day(D,i+1)%100, detail = get_meal(D,i)).save()
