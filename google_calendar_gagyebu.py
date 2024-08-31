'''
<정규표현식 패턴>
* 대괄호([]) : 대괄호 안에 있는 문자 중에 하나라도 매치되면 추출
* 점(.) : 앞뒤 문자의 사이에 주로 사용함. 하나의 문자를 의미함
            예시) a.c의 패턴인 경우 "abc" , "adc"...
* 반복(*) : 앞의 문자가 0번 이상 반복될 때 추출
            예시) ab*c의 패턴인 경우 "ac","abc","abbc","abbbbc"...
* 반복(+) : 앞의 문자가 1번 이상 반복될 때 추출
            예시) ab+c의 패턴인 경우 "abc","abbc", "abbbbbc"...
* 반복({m,n}) : 앞의 문자가 최소 m번, 최대 n번 반복될 때 추출됨
            예시) a{2,4}의 패턴인 경우 "aa","aaa","aaaa"
* 시작(^) 끝($) : 각 문자열의 시작과 끝을 나타냄
            예시) ^abc의 패턴인 경우 "abc"로 시작하는 문자열 추출
            예시) abc$의 패턴인 경우 "abc"로 끝나는 문자열 추출
* 물음표(?) : 바로 앞의 문자가 0또는 1회 나타날 수 있음을 의미함
            예시) a?의 패턴인 경우 "a",""
* 역슬래시(\) : 이스케이프라고 읽음 특수문자를 일반 문자로 인식하게함
* 소괄호(()) : 그룹화라고 읽음 괄호 안의 패턴을 하나의 그룹으로 묶어서 처리가능
            예시) (abc)+의 패턴인 경우 "abc","abcabc","abcabcabc"...
* [0-9] : 0에서 9까지의 숫자중 하나
* [!@#$%^&*(),.?";{}|<>] : 특수 기호 중 하나
* [ㄱ-ㅎ ㅏ-ㅣ 가-힣] : 한글 중 하나
* [a-zA-Z] : 알파벳 소문자 또는 대문자 중 하나
** \d : 숫자 (숫자 하나)
* \w : 한개의 문자 or 한개의 숫자 포함
* \s : 공백(탭,스페이스,줄바꿈(\n),캐리지리턴(CR))

* \b : 단어의 경계를 나타냄(보통 문장의 처음과 끝에 제시함)
------> 위의 패턴은 조합해서 사용 가능
'''

import datetime
import re

class calendar_day_obj:
    def __init__(self, dtstart, dtend, category, money):
        self.DTSTART = dtstart
        self.DTEND = dtend
        self.CATEGORY = category
        self.MONEY = money
    def __str__(self):
        return self.DTSTART + " " + self.DTEND + " " + self.CATEGORY + " " + self.MONEY

def read_ics_file(filename):

    f = open("./"+filename+".ics", 'r', encoding='UTF-8')
    #print(line)
    file_content = f.readlines()
    f.close()

    return file_content

def make_calendar_day_obj(content):
    DTSTART = ""
    DTEND = ""
    CATEGORY = ""
    MONEY = ""

    calendar_list = []

    for line in content:

        if("DTSTART;") in line:
            DTSTART = line[-9:].replace("\n","")
        elif("DTEND;") in line:
            DTEND = line[-9:].replace("\n","")
        elif("SUMMARY:") in line:
            SUMMARY = line.replace("\n","") # 줄바꿈 문자 제거
            SUMMARY = SUMMARY.replace("\\","") # calendar에서 메타문자(특수문자) [ , ] 를 일반 문자로 인식하려고 앞에 붙이는 \ 제거
            SUMMARY = SUMMARY.replace(",", "") # 입출금액에 있는 , 제거

            category_pattern = re.compile('\[[^]]+\]')
            '''
            \[ \] 메타문자 대괄호를 일반문자로 인식
            
            대괄호 [] : 대괄호 안에 있는 문자 중에 하나라도 매치되면 추출
            시작(^) 끝($) : 각 문자열의 시작과 끝을 나타냄
                예시) ^abc의 패턴인 경우 "abc"로 시작하는 문자열 추출
                예시) abc$의 패턴인 경우 "abc"로 끝나는 문자열 추출
            반복(+) : 앞의 문자가 1번 이상 반복될 때 추출
                예시) ab+c의 패턴인 경우 "abc","abbc", "abbbbbc"...
            '''

            money_pattern = re.compile('([+-][^]]+)원')
            '''
            소괄호 () : 그룹화라고 읽음 괄호 안의 패턴을 하나의 그룹으로 묶어서 처리가능
                → 매치되는 패턴에서 소괄호 안에 있는 내용만 추출하는 역할 수행
            대괄호 [] : 대괄호 안에 있는 문자 중에 하나라도 매치되면 추출
            시작(^) 끝($) : 각 문자열의 시작과 끝을 나타냄
                예시) ^abc의 패턴인 경우 "abc"로 시작하는 문자열 추출
                예시) abc$의 패턴인 경우 "abc"로 끝나는 문자열 추출
            반복(+) : 앞의 문자가 1번 이상 반복될 때 추출
                예시) ab+c의 패턴인 경우 "abc","abbc", "abbbbbc"...
            '''

            CATEGORY = category_pattern.findall(SUMMARY)[0]
            MONEY = money_pattern.findall(SUMMARY)[0]

        if("END:VEVENT") in line:
            calendar_list.append(calendar_day_obj(DTSTART, DTEND, CATEGORY, MONEY))

    #for obj in calendar_list:
    #    print(obj)

    return calendar_list

def make_money_summary(calendar_obj_list, start_date, end_date):

    summary_dict = {}
    summary_dict['[입출합계]'] = 0

    for cal_obj in calendar_obj_list:
        obj_day = datetime.date.fromisoformat(cal_obj.DTSTART)
        if(obj_day < start_date or obj_day > end_date): # 집계기간에 들어오는 것만 계산
            continue

        # 카테고리별 집계
        if(cal_obj.CATEGORY in summary_dict):
            summary_dict[cal_obj.CATEGORY] = summary_dict[cal_obj.CATEGORY] + int(cal_obj.MONEY)
        else:
            summary_dict[cal_obj.CATEGORY] = int(cal_obj.MONEY)

        # 총집계
        summary_dict['[입출합계]'] = summary_dict['[입출합계]'] + int(cal_obj.MONEY)

    #print(summary_dict)
    return summary_dict

def make_ical_file(filename, summary_dict, start_date, end_date):
    f = open("./" + filename + ".ics", 'w', encoding='UTF-8')

    f.write("BEGIN:VCALENDAR\n")
    for summary in summary_dict:
        f.write("BEGIN:VEVENT\n")
        f.writelines(["DTSTART;VALUE=DATE:", start_date, "\n"])
        f.writelines(["DTEND;VALUE=DATE:", end_date, "\n"])
        f.writelines(["SUMMARY:", summary, " ", str(format(summary_dict[summary], ",")), "원\n"]) # 숫자 타입 좀 더 예쁘게 다듬고@@@@@
        f.write("END:VEVENT\n")
    f.write("END:VCALENDAR")

    f.close()


file_name = input("집계대상 ical 파일명 (확장자 제외하고 입력해주세요) : ")
start_date = input("집계 시작일 (YYYYMMDD) : ")
end_date = input("집계 종료일 (YYYYMMDD) : ")

calendar_obj_list = sorted(make_calendar_day_obj(read_ics_file(file_name)),
                               key=lambda calendar_obj: calendar_obj.DTSTART) # 시작일 순으로 정렬

summary_dict = make_money_summary(calendar_obj_list,
                                  datetime.date.fromisoformat(start_date),
                                  datetime.date.fromisoformat(end_date))

make_ical_file("result", summary_dict, start_date, end_date)
print("수행되었습니다.")