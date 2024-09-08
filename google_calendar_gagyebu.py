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

def day_Validation_check(day, start_date, end_date):
    datetime_format = datetime.date.fromisoformat(day)
    if (datetime_format < start_date or datetime_format > end_date):
        return False # 기간 내에 들어오지 않으면 False 반환
    return True

def read_ics_file(filename):

    f = open("./"+filename+".ics", 'r', encoding='UTF-8')
    #print(line)
    file_content = f.readlines()
    f.close()

    return file_content

def write_ics_line(filestream, start_date, end_date_day_after, string):
    filestream.writelines(["DTSTART;VALUE=DATE:", start_date, "\n"])
    filestream.writelines(["DTEND;VALUE=DATE:", end_date_day_after, "\n"])
    filestream.writelines( ["SUMMARY:", string] )

class calendar_day_obj:
    def __init__(self, dtstart, dtend, category, money, is_fixed):
        self.DTSTART = dtstart
        self.DTEND = dtend
        self.CATEGORY = category
        self.MONEY = int(money)
        self.IS_FIXED = bool(is_fixed)

    def __str__(self):
        return self.DTSTART + " " + self.DTEND + " " + self.CATEGORY + " " + str(self.MONEY) + " " + str(self.IS_FIXED)

    # DTSTART, DTEND, CATEGORY, IS_FIXED가 같으면 동일 객체로 인식
    def __eq__(self, other):
        return (self.CATEGORY == other.CATEGORY
                and self.IS_FIXED == other.IS_FIXED
                and self.DTSTART == other.DTSTART
                and self.DTEND == other.DTEND)

    # DTSTART, DTEND, CATEGORY, IS_FIXED가 같으면 동일 객체로 인식
    def __ne__(self, other):
        return not(self.CATEGORY == other.CATEGORY
                and self.IS_FIXED == other.IS_FIXED
                and self.DTSTART == other.DTSTART
                and self.DTEND == other.DTEND)

    def __add__(self, other):
        self.MONEY = self.MONEY + other.MONEY
        return self

def make_calendar_day_obj(content, start_date, end_date):
    DTSTART = ""
    DTEND = ""
    CATEGORY = ""
    MONEY = ""
    IS_FIXED = ""

    calendar_list = []

    for line in content:
        if("DTSTART;") in line:
            DTSTART = line[-9:].replace("\n","") # 줄바꿈 문자 제거
        elif("DTEND;") in line:
            DTEND = line[-9:].replace("\n","") # 줄바꿈 문자 제거
        elif("SUMMARY:") in line:
            # summary 전처리 start
            SUMMARY = line.replace("\n","") # 줄바꿈 문자 제거
            SUMMARY = SUMMARY.replace("\\","") # calendar에서 메타문자(특수문자) [ , ] 를 일반 문자로 인식하려고 앞에 붙이는 \ 제거
            SUMMARY = SUMMARY.replace(",", "") # 입출금액에 있는 , 제거
            # summary 전처리 end

            is_fixed_pattern = re.compile('\{[^]]+\}') # 고정입출(fixed), 변동입출(variable) pattern { }

            category_pattern = re.compile('\[[^]]+\]') # 입출 카테고리 pattern [ ]
            '''
            \{ \} 메타문자 중괄호를 일반문자로 인식
            \[ \] 메타문자 대괄호를 일반문자로 인식
            
            대괄호 [] : 대괄호 안에 있는 문자 중에 하나라도 매치되면 추출
            시작(^) 끝($) : 각 문자열의 시작과 끝을 나타냄
                예시) ^abc의 패턴인 경우 "abc"로 시작하는 문자열 추출
                예시) abc$의 패턴인 경우 "abc"로 끝나는 문자열 추출
            반복(+) : 앞의 문자가 1번 이상 반복될 때 추출
                예시) ab+c의 패턴인 경우 "abc","abbc", "abbbbbc"...
            '''

            money_pattern = re.compile('([+-][^]]+)원') # 금액 pattern +-N원
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

            try:
                IS_FIXED = is_fixed_pattern.findall(SUMMARY)[0]
                if "고정" in IS_FIXED:
                    IS_FIXED = True
                else:
                    IS_FIXED = False
            except:
                IS_FIXED = False # 라벨링 안했으면 변동으로 간주
            CATEGORY = category_pattern.findall(SUMMARY)[0]
            MONEY = money_pattern.findall(SUMMARY)[0]

        if("END:VEVENT") in line:
            if(day_Validation_check(DTSTART, start_date, end_date)): # 집계기간에 들어오는 것만 객체 생성
                calendar_list.append(calendar_day_obj(DTSTART, DTEND, CATEGORY, MONEY, IS_FIXED))

    #for obj in calendar_list:
    #    print(obj)

    return calendar_list

def make_money_summary(calendar_obj_list, start_date, end_date):

    calendar_obj_summary_dict = {}
    key1, key2, key3 = '[★입출계]'+str(False), '[★고정입출계]'+str(True), '[★변동입출계]'+str(False)
    calendar_obj_summary_dict[key1] = calendar_day_obj(start_date, end_date, '[★입출계]', 0, False)
    calendar_obj_summary_dict[key2] = calendar_day_obj(start_date, end_date, '[★고정입출계]', 0, True)
    calendar_obj_summary_dict[key3] = calendar_day_obj(start_date, end_date, '[★변동입출계]', 0, False)

    for cal_obj in calendar_obj_list:
        # 카테고리별 집계
        cal_obj_key = cal_obj.CATEGORY+str(cal_obj.IS_FIXED)
        if(cal_obj_key in calendar_obj_summary_dict):
            calendar_obj_summary_dict[cal_obj_key] = calendar_obj_summary_dict[cal_obj_key] + cal_obj # cal_obj 날짜가 다른 상태긴 한데, add 메소드는 정상작동함
        else:
            calendar_obj_summary_dict[cal_obj_key] = cal_obj
            calendar_obj_summary_dict[cal_obj_key].DTSTART = start_date # 집계할거니까 집계기간으로 속성값 조정
            calendar_obj_summary_dict[cal_obj_key].DTEND = end_date # 집계할거니까 집계기간으로 속성값 조정

        # 고정입출별, 변동입출별 집계
        if(cal_obj.IS_FIXED):
            calendar_obj_summary_dict[key2] = calendar_obj_summary_dict[key2] + cal_obj
            #print(cal_obj)
            #print("고정")
        else:
            calendar_obj_summary_dict[key3] = calendar_obj_summary_dict[key3] + cal_obj
            #print(cal_obj)
            #print("변동")

        # 총집계
        calendar_obj_summary_dict[key1] = calendar_obj_summary_dict[key1] + cal_obj

    #print(calendar_obj_summary_dict)
    return calendar_obj_summary_dict

def make_ical_file(filename, calendar_obj_summary_dict, start_date, end_date):
    f = open("./" + filename + ".ics", 'w', encoding='UTF-8')

    end_date_day_after = str(datetime.date.fromisoformat(end_date) + datetime.timedelta(days=1)).replace("-","") # 구글 캘린더에 저장할 때 마지막 날짜까지 이벤트가 표시되도록 하기 위함

    f.write("BEGIN:VCALENDAR\n")
    for calendar_obj in calendar_obj_summary_dict.values():
        #print(calendar_obj)
        f.write("BEGIN:VEVENT\n")

        write_ics_line(f, start_date, end_date_day_after
                       , "(금융-가계부-집계) (" + start_date[-6:] + "~" + end_date[-6:] + ") " + calendar_obj.CATEGORY + " " + ("+" if calendar_obj.MONEY >= 0 else "") + str(format(calendar_obj.MONEY, ",")) + "원")

        if "입출계" not in calendar_obj.CATEGORY:
            f.write(" {▶고정}\n" if calendar_obj.IS_FIXED else " {▷변동}\n")
        else:
            f.write("\n") # 입출계 라인에는 IS_FIXED 출력하지 않음

        f.write("END:VEVENT\n")

    f.write("BEGIN:VEVENT\n")
    write_ics_line(f, start_date, end_date_day_after
                   , "(금융-가계부-집계) (" + start_date[-6:] + "~" + end_date[-6:] + ") " + "[☆-------------------------------]\n") # 입출계 라인을 분리하기 위함 / 구글 캘린더에서 가나다 순으로 정렬해서 예쁘게 정렬됨
    f.write("END:VEVENT\n")

    f.write("END:VCALENDAR")

    f.close()


file_name = input("집계대상 ical 파일명 (확장자 제외하고 입력해주세요) : ")
start_date = input("집계 시작일 (YYYYMMDD) : ")
end_date = input("집계 종료일 (YYYYMMDD) : ")

calendar_obj_list = sorted(make_calendar_day_obj(read_ics_file(file_name),
                                                 datetime.date.fromisoformat(start_date),
                                                 datetime.date.fromisoformat(end_date)),
                               key=lambda calendar_obj: calendar_obj.DTSTART) # 시작일 순으로 정렬, 지금 시점에서는 불필요하긴 함

calendar_obj_summary_dict = make_money_summary(calendar_obj_list, start_date, end_date)

make_ical_file("result", calendar_obj_summary_dict, start_date, end_date)
print("수행되었습니다.")
