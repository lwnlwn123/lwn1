# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import random
import math
import operator
import tkinter
import tkinter.messagebox
from tkinter import ttk 
from collections import deque
from functools import reduce
from PIL import Image,ImageTk

N=3#边块数
W=600#窗口宽
H=720#窗口高
WIDTH=200
HEIGHT=200
step=0#步数
stop=0
t=0#时间
sign=0#判断是否进入主窗口的标志
st=0#判断是否进入设置窗口的标志
k=0#图片选取判断标志
opt=""
src=r'char/a_.jpg'
path=r'picture/A3'
base=r'picture/A3/a_'#默认图片目录
mark_row=0#空白格行
mark_column=0#空白格列
sq=[] #存放图片的列表     
Pics=[]
history=deque([],10)
def splitimage(src,row,col,dstpath):#src图片文件路径,row切割行数,column切割列数,dstpath图片输出目录
    img=Image.open(src)
    w,h=img.size
    if row<=h and col<=w:
        s=os.path.split(src)
        if dstpath=='':
            dstpath=s[0]
        fn=s[1].split('.')
        basename=fn[0]
        
        num=0
        rowheight=h//row
        colwidth=w//col
        for r in range(row):
            for c in range(col):
                box=(c*colwidth, r*rowheight, (c+1)*colwidth, (r+1)*rowheight)
                img.crop(box).resize((200,200)).save(os.path.join(dstpath, basename +str(num)+ '.png'), 'png')
                num+=1
                
def pic_cmp(img1,img2):
    image1=Image.open(img1)
    image2=Image.open(img2)
    h1=image1.histogram()
    h2=image2.histogram()
    result=math.sqrt(reduce(operator.add,list(map(lambda a,b:(a-b)**2,h1,h2)))/len(h1))
    return result    

def pic_match():
    pathlist1=[]
    imglist=[]
    for root,dummy_dirs,files in os.walk(r".\cut_picture"):
            for file in files:
                pathlist1.append(root)
    pathlist2=list(set(pathlist1))
    pathlist2.sort()#文件夹名称列表
    path1=r'.\test_picture'
    for root,dirs,files in os.walk(r".\cut_picture"):
        for file in files:
            imglist.append(os.path.join(root,file))
    resultnum=[]
    for x in range(36):
        path2=pathlist2[x]
        k=0
        resultnum=[]
        for i in range(9):
            for j in range(9):
                temp=pic_cmp(os.path.join(path1,str(i)+'.png'),os.path.join(path2,str(j)+'.png'))
                resultnum.append(temp)
        resultnum.sort()        
        for y in range(8):
            k+=resultnum[y]
        if k==0:
            return path2
        else:
            continue
            
class Imageblock:#定义图片类
    def __init__(self,num):
        self.num=num
    def draw(self,canvas,pos_x,pos_y):
        img1=Pics[self.num]
        canvas.create_image(pos_x,pos_y,image=img1)
        
def initsquare():#初始化sq
    global mark_row,mark_column
    ls=random.sample(range(N*N),N*N)       
    k=random.randint(0,N*N-1)
    for row in range(N):
        sq.append([])
        for column in range(N):
            sq[row].append(ls[row*N+column])
            if(row*N+column==k):
                sq[row][column]=None
                mark_row=row
                mark_column=column
            else:
                sq[row][column]=Imageblock(ls[row*N+column])             

def draw_image(cv):#显示图片
    cv.create_polygon((0,0,W,0,W,H,0,H),width=1,outline='Black',fill='White')
    for i in range(N):
        for j in range(N):
            if(sq[i][j]!=None):
                sq[i][j].draw(cv,WIDTH*(j+0.5),HEIGHT*(i+0.5))
                
def key_control(event):
    global mark_row,mark_column,src,step,t,history,stop,opt
    print(mark_row,mark_column)
    if(event.keysym=="w"):
        if(mark_row!=0):
            sq[mark_row][mark_column],sq[mark_row-1][mark_column]=sq[mark_row-1][mark_column],sq[mark_row][mark_column]
            mark_row-=1
            step+=1
            opt+="w"
            print(opt)
    if(event.keysym=="s"):
        if(mark_row!=N-1):
            sq[mark_row][mark_column],sq[mark_row+1][mark_column]=sq[mark_row+1][mark_column],sq[mark_row][mark_column]
            mark_row+=1
            step+=1
            opt+="s"
            print(opt)
    if(event.keysym=="a"):
        if(mark_column!=0):
            sq[mark_row][mark_column],sq[mark_row][mark_column-1]=sq[mark_row][mark_column-1],sq[mark_row][mark_column]
            mark_column-=1
            step+=1
            opt+="a"
            print(opt)
    if(event.keysym=="d"):
        if(mark_column!=N-1):
            sq[mark_row][mark_column],sq[mark_row][mark_column+1]=sq[mark_row][mark_column+1],sq[mark_row][mark_column]      
            mark_column+=1
            step+=1
            opt+="d"
            print(opt)
    steps.set(str(step))
    cv.delete("all")
    draw_image(cv)
    if iswin():
        stop=1
        tkinter.messagebox.showinfo(title="恭喜",message="挑战成功！")
        time.set(str(t))
        history.append((step,t))
        orl_jpg=Image.open(src)
        dest=orl_jpg.resize((250,250),Image.ANTIALIAS)
        orl_img=ImageTk.PhotoImage(dest)
        cv.create_image(750,270,image=orl_img)
        window.mainloop()
            
def mouseclick(pos):#鼠标控制图片
    global step,t,stop,history
    r=int(pos.y//HEIGHT)
    c=int(pos.x//WIDTH)
    if r<3 and c<3:
        if sq[r][c] is None:
            return
        else:
            cur_sq=sq[r][c]
            if r-1>=0 and sq[r-1][c] is None:
                sq[r][c]=None
                sq[r-1][c]=cur_sq
                step+=1
            elif c+1<=2 and sq[r][c+1] is None:
                sq[r][c]=None
                sq[r][c+1]=cur_sq
                step+=1
            elif r+1<=2 and sq[r+1][c] is None:
                sq[r][c]=None
                sq[r+1][c]=cur_sq
                step+=1
            elif c-1>=0 and sq[r][c-1] is None:
                sq[r][c]=None
                sq[r][c-1]=cur_sq
                step+=1
            # label1["text"]=str(step)
            steps.set(str(step))
            cv.delete('all')
            draw_image(cv)
        if(iswin()):
            stop=1
            tkinter.messagebox.showinfo(title="恭喜",message="挑战成功！")
            history.append((step,t))
            orl_jpg=Image.open(src)
            dest=orl_jpg.resize((250,250),Image.ANTIALIAS)
            orl_img=ImageTk.PhotoImage(dest)
            cv.create_image(750,270,image=orl_img)
            window.mainloop()  
            
def iswin():#成功判断
    for row in range(N):
        for column in range(N):
           if sq[row][column]!=None and sq[row][column].num!=row*N+column:
                return False
    return True

def update_time():
    global t,stop
    if(stop%2==0):
        t=t+1
        time.set(str(t))
        window.after(1000,update_time) 
    else:
        window.after(1000,update_time)
    
def stop_time():
    global t,stop
    stop+=1
    if(stop%2):
        time.set(str(t))
         
def enter_game():#进入游戏主窗口
     global root,sign
     root.destroy()
     window=tkinter.Tk('图片华容道') 
     window.destroy()
     sign=1
     
def game_begining():
    global step,stop,t
    step=0
    stop=0
    t=0
    steps.set(str(step))
    time.set(str(t))
    initsquare()
    
def game_ending():
    game_begining()
    cv.delete('all')
    draw_image(cv)
   
def print_selection2():#选择图片(有bug) 
    global src,path,k
    if(photo.get()=='a'):
        src=r'char/a_.jpg'
        if(N==3):
            path=r'picture/A3'
    if(photo.get()=='b'):
        src=r'char/b_ (2).jpg'
        if(N==3):
            path=r'picture/B'
    if(photo.get()=='c'):
        src=r'char/c_.jpg'
        if(N==3):
            path=r'picture/C3'
        k=1
        
def history_record():
    global history
    wind=tkinter.Tk()
    wind.title('排行榜')
    wind.geometry('400x450+0+0')
    wind.resizable(False,False)
    tree=ttk.Treeview(wind,height=450,columns=("步数","用时"))
    tree.column("步数",width=100)
    tree.column("用时",width=100)
    tree.heading("#0",text="名次",anchor="center")
    tree.heading("#1",text="步数",anchor="center")
    tree.heading('#2',text="用时",anchor="center")
    sorted(history)
    l=list(history)
    sorted(l)
    print(l[0])
    for i in range(len(history)):   
        tree.insert("",index=tkinter.END,text=str(i+1), values=(l[i][0],l[i][1]))
    tree.pack()
    wind.mainloop()
    tree.destroy()
     
def set_model():#进入设置窗口
    global root,st
    st=1
    window=tkinter.Toplevel(root)
    window.title('设 置')
    window.geometry('500x500+0+0')
    window.resizable(False, False)
    window.destroy()
def callback():
    global window_modselect,root
    window_modselect.destroy()
    root.mainloop()
#主函数
root=tkinter.Tk()
root.title('华容道')
root.geometry('600x720')
root.maxsize(600,720)
root.resizable(False, False)

background_jpg=Image.open(r'picture/1.jpg')
dest0=background_jpg.resize((1200,1440),Image.ANTIALIAS)
background_img=ImageTk.PhotoImage(dest0)

but1_png=Image.open(r'picture/pic/but (1).png')
w1,h1=but1_png.size
dest1=but1_png.resize((w1//8,h1//8),Image.ANTIALIAS)
but1_img=ImageTk.PhotoImage(dest1)

but2_png=Image.open(r'picture/button.png')
w2,h2=but2_png.size
dest2=but2_png.resize((w2//8,h2//8),Image.ANTIALIAS)
but2_img=ImageTk.PhotoImage(dest2)

root_c=tkinter.Canvas(root,bg='white',width=W,height=H)
root_c.create_image(0,0,image=background_img)
root_c.grid()
root_c.create_text(300,130,text='图 片 华 容 道',font=('方正粗黑宋简体',28),fill='blue')

tkinter.Button(root,text="开始游戏",image=but2_img,font=('方正粗黑宋简体',12),fg='white',compound='center',cursor='circle',highlightbackground='lightyellow',command=enter_game,width=100,height=20).place(x=245,y=400) 
tkinter.Button(root,text="设 置",image=but2_img,font=('方正粗黑宋简体',12),fg='white',compound='center',cursor='circle',command=set_model,width=100,height=20).place(x=245,y=480)
root.mainloop()
if(st):
    window_modselect=tkinter.Tk()
    window_modselect.geometry('340x450+0+0')
    window_modselect.resizable(False, False)
    window_modselect.title('设 置')
    
    but2_png=Image.open(r'picture/button.png')
    w2,h2=but2_png.size
    dest2=but2_png.resize((w2//8,h2//8),Image.ANTIALIAS)
    but2_img=ImageTk.PhotoImage(dest2)
    
    window_modselect_c=tkinter.Canvas(window_modselect,bg='lightblue',width=340,height=450).grid()
    tkinter.Label(window_modselect,bg='lightblue',width=20,text='挑战图片：',font=('方正粗黑宋简体',14),fg='yellow').place(x=50,y=30)
    photo=tkinter.StringVar()
    tkinter.Radiobutton(window_modselect,text='a',image=but2_img,font=('方正粗黑宋简体',12),fg='white',variable=photo,value='a',indicatoron=0,compound='center',cursor='circle',highlightbackground='lightyellow',width=120,height=20,command=print_selection2).place(x=100,y=120)
    tkinter.Radiobutton(window_modselect,text='b',image=but2_img,font=('方正粗黑宋简体',12),fg='white',variable=photo,value='b',indicatoron=0,compound='center',cursor='circle',highlightbackground='lightyellow',width=120,height=20,command=print_selection2).place(x=100,y=160)
    tkinter.Radiobutton(window_modselect,text='c',image=but2_img,font=('方正粗黑宋简体',12),fg='white',variable=photo,value='c',indicatoron=0, compound='center',cursor='circle',highlightbackground='lightyellow',width=120,height=20,command=print_selection2).place(x=100,y=200)
    confirm=tkinter.Button(window_modselect,text="确定",image=but2_img,font=('方正粗黑宋简体',12),fg='white',compound='center',cursor='circle',highlightbackground='lightyellow',width=80,height=20,command=callback).place(x=120,y=300)
    window_modselect.mainloop()
    
root.mainloop()
if(sign):
    window=tkinter.Tk('图片华容道')  
    window.title('华容道')
    window.geometry('900x710+0+0')
    window.resizable(False, False)
    splitimage(src,N,N,path)
    frame1=tkinter.Frame(window,bg='lightblue',width=900,height=120).grid()
    frame2=tkinter.Frame(window,bg='lightblue',width=900,height=410)
    cv=tkinter.Canvas(frame2,bg='lightblue',width=900,height=610)
    c1=tkinter.Canvas(frame1,bg='lightblue',width=690,height=90)

    but2_png=Image.open(r'picture/button.png')
    w2,h2=but2_png.size
    dest2=but2_png.resize((w2//8,h2//8),Image.ANTIALIAS)
    but2_img=ImageTk.PhotoImage(dest2)

    tkinter.Button(window,text="退 出",image=but2_img,font=('方正粗黑宋简体',12),fg='white',bg='lightblue',compound='center',cursor='circle',highlightbackground='lightyellow',command=window.destroy,width=80,height=20).place(x=20,y=40)
    tkinter.Button(window,text="排行榜",image=but2_img,font=('方正粗黑宋简体',12),fg='white',bg='lightblue',compound='center',cursor='circle',highlightbackground='lightyellow',command=history_record,width=80,height=20).place(x=540,y=40)
    tkinter.Button(window,text="暂 停",image=but2_img,font=('方正粗黑宋简体',12),fg='white',bg='lightblue',compound='center',cursor='circle',highlightbackground='lightyellow',command=stop_time,width=80,height=20).place(x=660,y=40) 
    tkinter.Button(window,text="再玩一次",image=but2_img,font=('方正粗黑宋简体',12),fg='white',bg='lightblue',compound='center',cursor='circle',highlightbackground='lightyellow',command=game_ending,width=80,height=20).place(x=780,y=40)
    splitimage(src,N,N,path)
    if k==1:
        base=r'C3\c_'
    for i in range(N*N):
        filename=Image.open(base+str(i)+'.png')
        picture=ImageTk.PhotoImage(filename)
        Pics.append(picture)
        
    tkinter.Label(frame1,text=" 步数：",font=('楷体',15),bg='lightblue',width=0,height=0).place(x=180,y=50)
    steps=tkinter.IntVar()
    tkinter.Label(frame1,text="0",textvariable=steps,fg="red",bg='lightblue',font=('Arial',15),width=0,height=0).place(x=250,y=50)
    
    tkinter.Label(frame1,text="   用时：",font=('楷体',15),bg='lightblue',width=0).place(x=340,y=50)
    time=tkinter.IntVar()
    tkinter.Label(frame1,text="0",textvariable=time,fg="red",bg='lightblue',font=('Arial',15),width=0).place(x=430,y=49)
    tkinter.Label(frame1,text="s",fg="red",font=('Arial',15),bg='lightblue',width=0).place(x=472,y=49)
    window.after(1000,update_time)
    cv.bind("<Button-1>",mouseclick)
    cv.bind_all("<KeyPress-w>",key_control)
    cv.bind_all("<KeyPress-a>",key_control)
    cv.bind_all("<KeyPress-s>",key_control)
    cv.bind_all("<KeyPress-d>",key_control)
    cv.grid()
    game_begining()
    draw_image(cv)
    frame2.grid(sticky=tkinter.SW)
    window.mainloop()


