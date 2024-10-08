from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as mbox
import google_calendar_gagyebu as gcg
import datetime
from tkcalendar import *

today_time = datetime.date.today()
calendar_ext = r"*.ics"

def help_popup():
    mbox.showinfo("help", "0. 구글 캘린더에 개별 입출을 관리할 캘린더와 집계 데이터를 저장할 캘린더 2개를 만듭니다.\n\n"
                  "1. 개별 입출을 관리하는 구글 캘린더에 '[카테고리] +-N원 {고정/변동}' 양식으로 가계부를 작성해주세요.\n\n"
                  "2. 캘린더 내보내기 기능으로 개별 입출 캘린더를 *.ics 파일로 내보냅니다.\n\n"
                  "3. 해당 파일을 Find 버튼으로 지정하고, 집계할 기간을 지정하고 Process 버튼을 눌러주세요.\n\n"
                  "4. 생성된 result.ics 파일을 집계 데이터를 저장하는 캘린더에 캘린더 가져오기 기능으로 저장합니다.")

def file_find():
    file = filedialog.askopenfilenames(filetypes=(("ical", calendar_ext), ("all file", "*.*")),
                                       initialdir=r"C:\Users")
    filepath_space.delete(0, END)
    filepath_space.insert(END, file[0])


def process():
    if len(filepath_space.get()) == 0:
        mbox.showinfo("Warning", "파일을 선택해주세요.")
        return
    elif len(start_date_space.get()) != 10:
        mbox.showinfo("Warning", "집계시작일을 다시 지정해주세요.")
        return
    elif len(end_date_space.get()) != 10:
        mbox.showinfo("Warning", "집계종료일을 다시 지정해주세요.")
        return
    else:
        try:
            gcg.main(filepath_space.get(), start_date_space.get().replace("-",""), end_date_space.get().replace("-",""))
            mbox.showinfo("Complete", "Complete")
        except:
            mbox.showinfo("Error", "Error occurred")
        return


app = Tk()
app.title('google calendar gagyebu')

#창 크기 +붙은 부분은 좌상단 떨어진 위치
app.geometry("250x300+100+100")

#------------------------------------------------------------------------------

lab11=Label(app,
    text="파일 경로",
    width=8,
    height=1,
    font=('맑은 고딕',16,'bold'),
    bg='#2F5597',
    fg='white')
lab11.grid(row=0,column=0,padx=5,pady=10)

filepath_space = Entry(font=('맑은 고딕',16,'bold'),bg='white',width=8)
filepath_space.grid(row=0,column=1,padx=5,pady=10)

#------------------------------------------------------------------------------

lab21=Label(app,
    text="집계시작일",
    width=8,
    height=1,
    font=('맑은 고딕',16,'bold'),
    bg='#2F5597',
    fg='white')

lab21.grid(row=1,column=0,padx=5,pady=10)

start_date_space = DateEntry(app,selectmode="day",date_pattern="yyyy-mm-dd")
start_date_space.grid(row=1,column=1,padx=5,pady=10)

#------------------------------------------------------------------------------

lab31=Label(app,
    text="집계종료일",
    width=8,
    height=1,
    font=('맑은 고딕',16,'bold'),
    bg='#2F5597',
    fg='white')
lab31.grid(row=2,column=0,padx=5,pady=10)

end_date_space = DateEntry(app,selectmode="day",date_pattern="yyyy-mm-dd")
end_date_space.grid(row=2,column=1,padx=5,pady=10)

#------------------------------------------------------------------------------

bt_find = Button(app, text="Find", width=10, command=file_find)
bt_find.grid(row=3,column=0,padx=5,pady=5)
bt_process = Button(app, text="Process", width=10, command=process)
bt_process.grid(row=3,column=1,padx=5,pady=5)
bt_help = Button(app, text="Help", width=10, command=help_popup)
bt_help.grid(row=4,column=0,padx=5,pady=5)

app.mainloop()
