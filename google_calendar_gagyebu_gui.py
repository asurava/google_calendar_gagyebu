from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as mbox
import google_calendar_gagyebu as gcg
import datetime
from tkcalendar import *

today_time = datetime.date.today()
calendar_ext = r"*.ics"

def file_find():
    file = filedialog.askopenfilenames(filetypes=(("ical", calendar_ext), ("all file", "*.*")),
                                       initialdir=r"C:\Users")
    filepath_space.delete(0, END)
    filepath_space.insert(END, file[0])


def process():
    if len(filepath_space.get()) == 0:
        mbox.showinfo("warning", "select file, please")
        return
    else:
        gcg.main(filepath_space.get(), start_date_space.get().replace("-",""), end_date_space.get().replace("-",""))
        mbox.showinfo("Complete", "Complete")
        return


app = Tk()
app.title('google calendar gagyebu')

#창 크기 +붙은 부분은 좌상단 떨어진 위치
app.geometry("250x250+100+100")

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
bt_find.grid(row=3,column=0,padx=5,pady=10)
bt_process = Button(app, text="process", width=10, command=process)
bt_process.grid(row=3,column=1,padx=5,pady=10)

app.mainloop()
