from tkinter import *
from tkinter import ttk, filedialog, messagebox
import imagePrediction as imagePredict
from PIL import Image, ImageTk
import constan
from constan import region, buttonLabel, pesan, gender
import os
import json


global REGION, GENDER
button_dict, imgREGIONS, lbl, lbl_value = {}, {}, {}, {}
fontDecoration = f'arial 10 bold'
WIDTH, HEIGHT = 1200, 800
GENDER = gender.MALE
REGIONS = [ region.CENTRAL_INCISOR,
            region.LATERAL_INCISOR,
            region.CANINE, 
            region.FIRST_PREMOLAR,
            region.SECOND_PREMOLAR,
            region.FIRST_MOLAR,
            region.SECOND_MOLAR ]
REGION = REGIONS[0] #region.CENTRAL_INCISOR

root = Tk()
root.title(f'{pesan.TITLE}')
root.geometry(f'{WIDTH}x{HEIGHT}')
v = IntVar()
v.set(1)

#=================================================================================================================
#=================================================================================================================
#=================================================================================================================
def readJson(pathJsonFile):
    with open(pathJsonFile, 'r') as file:
        return json.load(file)

def openAndPut():
    status(message =f'{pesan.OPEN_AND_PUT}')
    global _path
    _path = path = filedialog.askopenfilename()
    for x in range(len(REGIONS)):  
        try: os.remove(f'{constan.PATH_TESTING}{REGIONS[x]}{constan.IMAGE_TYPE}')
        except: pass
    imagetRegion() 
    openImage(path)

def resetImage():
    status(message =f'{pesan.RESET_IMAGE}')
    openImage(_path)

def openImage(path):
    status(message =f'{pesan.CREATE_IMAGE}', imgaePath = path)
    global image, cropImage
    width, height = round(WIDTH * 0.75), round(HEIGHT * 0.75)
    if path:
        cropImage = Image.open(path)
        cropImage = cropImage.resize((width, height), Image.ANTIALIAS)
        image = Image.open(path)
        image = image.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        image_area.create_image(0, 0, image=image, anchor='nw')
#-----------------------------------------------------------

def buttonPress(event):
    # simpan mouse drag posisi awal
    global start_x, start_y, rect
    start_x = image_area.canvasx(event.x)
    start_y = image_area.canvasy(event.y)
    status(f'{pesan.BUTTON_PRESS}{start_x}, {start_y}')
    # buat kotak seleksi warna merah
    rect = image_area.create_rectangle(0, 0, 1, 1, outline='red')

def buttonMove(event):
    global curX, curY
    curX = image_area.canvasx(event.x)
    curY = image_area.canvasy(event.y)
    status(f'{pesan.BUTTON_MOVE}{curX}, y : {curY}')
    # buat kotak selama di drag
    image_area.coords(rect, start_x, start_y, curX, curY)    

def buttonRelease(event):
    if  Status == pesan.SELECT:
        res = messagebox.askquestion('askquestion', pesan.SIMPAN_STAGE+REGION)
        if res == 'yes':
            saveImage(REGION)        
            imagetRegion()
        elif res == 'no': pass
        else: messagebox.showwarning('error', pesan.ERR_KESALAHAN)
        image_area.delete(rect) #hapus kotak di gambar
    elif Status == pesan.CROP:
        path = saveImage(constan.CROP_FILE_NAME)  
        openImage(path)

    status(message =f'{pesan.BUTTON_RELEASE}')

def saveImage(fileName, showImage=False):
    path = f'{constan.PATH_TESTING}{fileName}{constan.IMAGE_TYPE}'
    status(message =f'{pesan.SAVE_IMAGE}', imgaePath = path)
    imageCrop = cropImage.crop((start_x, start_y, curX, curY))
    imageCrop.save(path)
    if showImage: imageCrop.show()
    return path
    
def selectArea(_status):
    global Status 
    Status = _status
    status(f'{Status} {pesan.IMAGE}')
    image_area.bind('<ButtonPress-1>', buttonPress)
    image_area.bind('<B1-Motion>', buttonMove)
    image_area.bind('<ButtonRelease-1>', buttonRelease)


def imageRegionPress(x):
    global REGION
    for y in range(len(REGIONS)):
        button_dict[REGIONS[y]].configure(highlightbackground='white', highlightthickness=2)            
        if y == x:
            status(f'{REGIONS[y]} {pesan.SELECTED}')
            REGION = REGIONS[y]
            button_dict[REGIONS[y]].configure(highlightbackground='blue', highlightthickness=2)

def boysGirls():
    global GENDER
    GENDER = gender.MALE if v.get() == 1 else gender.FEMALE
    status(message = f'{GENDER}') 

#=============================================================
#             Digunakan Untuk Prediksi
#=============================================================      
def predict():
    for region in REGIONS:
        status(StatusProcess = f'{pesan.PREDICT1} {region}')
        imagePred = imagePredict.imagePrediction(region)
        imagePredict.imageClasification(GENDER, region, imagePred) 
        resultLabelValue()
    status(StatusProcess = f'{pesan.PREDICT2}') 
    finalResult()

def finalResult():
    result = imagePredict.agePrediction()
    lblResult.configure(text=f'{round(result):.1f}')
    lblMaxResult.configure(text=f'{round(result + constan.THRESHOLD):.1f}')
    lblMinResult.configure(text=f'{round(result - constan.THRESHOLD):.1f}')
    status(StatusPredict = pesan.FINAL_RESULT.format(GENDER,result)) 

def resultLabelValue():
    dictResult = readJson(constan.RESULT_JSON_PATH)
    for x in range(len(REGIONS)):
        try: 
            sign = '' if dictResult[REGIONS[x]] < 0 else ' '
            lbl_value[x].configure(text=f': {sign}{dictResult[REGIONS[x]]:.2f}   ')
        except:pass


#=============================================================
#                   Report
#=============================================================  

def status(message=None, imgaePath=None, StatusPredict=None,StatusProcess=None):
    if message is not None: lblMessage.configure(    text=f'{pesan.LABEL_MESSAGE}{message}')
    if imgaePath is not None: lblImagePath.configure(text=f'{pesan.LABEL_IMAGE_PATH}{imgaePath}')
    if StatusPredict is not None: lblStatusPredict.configure(text=f'{pesan.LABEL_STATUS_PREDICT}{StatusPredict}')
    if StatusProcess is not None: lblStatusProcess.configure(text=f'{pesan.LABEL_STATUS_PROCESS}{StatusProcess}')


#=================================================================================================================
#=================================================================================================================
#=================================================================================================================

# import model as mdl
# mdl.executeModels(REGION)


#=============================================================
#                   Buat Frame Dan Canvas
#=============================================================
left_frame = Frame(root, width=WIDTH * 0.18, height=HEIGHT * 1, highlightbackground='white', highlightthickness=1)
left_region_frame = Frame(left_frame, width=int(WIDTH * 0.014), highlightbackground='white', highlightthickness=0.5)
left_result_frame = Frame(left_frame, width=int(WIDTH * 0.014), highlightbackground='white', highlightthickness=0.5)
left_crop_reset_frame = Frame(left_frame, width=int(WIDTH * 0.014))
left_girls_boys_frame = Frame(left_frame, width=int(WIDTH * 0.014))
right_frame = Frame(root, width=WIDTH * 0.83, height=HEIGHT * 1)
right_top_frame = Frame(right_frame, width=WIDTH * 0.83, height=HEIGHT * 0.74)
right_bottom_frame = ttk.Notebook(right_frame, width=int(WIDTH * 0.82), height=int(HEIGHT * 0.25))
frameStatus = ttk.Frame(right_bottom_frame, width=WIDTH * 0.82, height=HEIGHT * 0.25)
frameInformation = ttk.Frame(right_bottom_frame, width=WIDTH * 0.82, height=HEIGHT * 0.25)
frameProfile = ttk.Frame(right_bottom_frame, width=WIDTH * 0.82, height=HEIGHT * 0.25)
images_area = Frame(right_top_frame, width=WIDTH * 0.07, height=HEIGHT * 0.74 )
image_area = Canvas(right_top_frame, bg='white', width=WIDTH * 0.75, height=HEIGHT * 0.74, highlightbackground='white', highlightthickness=1)

left_frame.grid(row=0, column=0, sticky='nsew')
left_crop_reset_frame.grid(row=1, column=0, sticky='nsew',padx=(10,10), pady=5)
left_girls_boys_frame.grid(row=3, column=0, sticky='nsew',padx=(10,10), pady=5)
left_region_frame.grid(row=5, column=0, sticky='nsew',padx=(10,10), pady=20)
left_result_frame.grid(row=6, column=0, sticky='nsew',padx=(10,10))
right_frame.grid(row=0, column=1, sticky='nsew')
right_top_frame.grid(row=0, column=0, sticky='nsew')
right_bottom_frame.grid(row=1, column=0, sticky='nsew')
images_area.grid(row=0, column=0, sticky='nsew')
image_area.grid(row=0, column=1)

left_frame.grid_propagate(False)
right_frame.grid_propagate(False)
right_top_frame.grid_propagate(False)
right_bottom_frame.grid_propagate(False)
images_area.grid_propagate(False)
image_area.grid_propagate(False)

frameStatus.pack(fill='both', expand=True)
frameInformation.pack(fill='both', expand=True)
frameProfile.pack(fill='both', expand=True)

right_bottom_frame.add(frameStatus, text=f'{pesan.FRAME_STATUS}')
right_bottom_frame.add(frameInformation, text=f'{pesan.FRAME_INFORMATION}')
right_bottom_frame.add(frameProfile, text=f'{pesan.FRAME_PROFILE}')

#=============================================================
#                   Buat Text BOX
#=============================================================
text_box = Text(frameInformation, bg=right_frame['background'],font='arial 8',borderwidth=0,width=int(WIDTH * 0.82))
text_box.grid(row=0, column=0, sticky=W)
text_box.insert('end', f'{pesan.TOOTH}')
text_box.config(state='disabled')

text_box = Text(frameProfile, bg=right_frame['background'],font='arial 10',borderwidth=0,width=int(WIDTH * 0.82))
text_box.grid(row=0, column=0,sticky=W)
text_box.insert('end', f'{pesan.PROFILE}')
text_box.config(state='disabled')

lblMessage = Label(frameStatus,       text=f'{pesan.LABEL_MESSAGE}', font=fontDecoration,highlightthickness=2)
lblMessage.grid(row=0, column=0, sticky=W, pady=(20,5),padx=20)
lblImagePath = Label(frameStatus,     text=f'{pesan.LABEL_IMAGE_PATH}', font=fontDecoration,highlightthickness=2)
lblImagePath.grid(row=1, column=0, sticky=W, padx=(20),pady=(5))
lblStatusProcess = Label(frameStatus, text=f'{pesan.LABEL_STATUS_PROCESS}', font=fontDecoration,highlightthickness=2)
lblStatusProcess.grid(row=2, column=0, sticky=W, padx=20,pady=(5))
lblStatusPredict = Label(frameStatus, text=f'{pesan.LABEL_STATUS_PREDICT}', font=fontDecoration,highlightthickness=2)
lblStatusPredict.grid(row=3, column=0, sticky=W, padx=20,pady=(5))

lblResult = Label(left_result_frame, text=f'0.0', font=f'arial 40 bold',highlightthickness=2)
lblResult.grid(row=0, column=0, sticky=W)
lblTahun = Label(left_result_frame, text=f'{pesan.UMUR}', font=fontDecoration,highlightthickness=2)
lblTahun.grid(row=0, column=1, sticky=W)
lblTareshold = Label(left_result_frame, text=f'{pesan.THRESHOLD}{constan.THRESHOLD}', font=fontDecoration,highlightthickness=2)
lblTareshold.grid(row=1, column=0, sticky=W)
lblMaxResult = Label(left_result_frame, text=f'{pesan.MAX_THRESHOLD}0.0', font=fontDecoration,highlightthickness=2)
lblMaxResult.grid(row=2, column=0, sticky=W)
lblMinResult = Label(left_result_frame, text=f'{pesan.MIN_THRESHOLD}0.0', font=fontDecoration,highlightthickness=2)
lblMinResult.grid(row=3, column=0, sticky=W,pady=(0,10))

#======================================================================
#                       Show/Hide TabMenu
#======================================================================

if(constan.hideFrame.hideFrameStatus): frameStatus.destroy()      # Tab Status
if(constan.hideFrame.hideFrameInformation): frameInformation.destroy() # Tab Infnforamtion
if(constan.hideFrame.hideFrameProfile): frameProfile.destroy()     # Tab Profile


#=============================================================
#                   Load Image Pertama kali
#=============================================================
_path = f'{constan.PATH_TESTING}{constan.NO_IMAGES_FILE_NAME}{constan.IMAGE_TYPE}'
imgs = Image.open(_path)
imgs = ImageTk.PhotoImage(imgs)
image_area.create_image(WIDTH * 0.75/2,HEIGHT * 0.74/2,anchor=CENTER, image=imgs)

#=============================================================
#                   Buat Button
#=============================================================
size = int(WIDTH * 0.014)
_padx, _pady = (10,10), 5
load_image = Button(left_frame,  width=size, text=buttonLabel.LOAD_IMAGE, font=fontDecoration,command=openAndPut)
load_image.grid(row=0, column=0, sticky='nsew', padx=_padx, pady=(20,_pady))

crop_image = Button(left_crop_reset_frame,  width=int(size-6), text=buttonLabel.CROP_IMAGE, font=fontDecoration, command = lambda s=f'{pesan.CROP}': selectArea(s))
crop_image.grid(row=0, column=0, sticky='nsew')
reset_image = Button(left_crop_reset_frame,  width=int(size-6), text=buttonLabel.RESET_IMAGE, font=fontDecoration, command = resetImage)
reset_image.grid(row=0, column=1, sticky='nsew' )

select_region = Button(left_frame, width=size, text=buttonLabel.SELECT_REGION, font=fontDecoration, command = lambda s=f'{pesan.SELECT}': selectArea(s))
select_region.grid(row=2, column=0, sticky='nsew', padx=_padx, pady=_pady)
singlePredict = Button(left_frame,  width=size, text=buttonLabel.PREDICT, font=fontDecoration, command = predict)
singlePredict.grid(row=4, column=0, sticky='nsew', padx=_padx, pady=_pady)

boys = Radiobutton(left_girls_boys_frame, width=int(size-3), height=2, text=gender.MALE,command = boysGirls, indicatoron=0, variable=v, value=1,font=fontDecoration)
girls = Radiobutton(left_girls_boys_frame, width=int(size-3), height=2, text=gender.FEMALE,command = boysGirls, indicatoron=0, variable=v, value=2,font=fontDecoration)
boys.grid(row=0, column=0,sticky='nsew')
girls.grid(row=0, column=1,sticky='nsew')

#=============================================================
#                   Buat Label Region
#=============================================================
for x in range(len(REGIONS)):  
    lbl[x] = Label(left_region_frame, text=f'{REGIONS[x]}', font=fontDecoration,highlightthickness=2)
    lbl[x].grid(row=x, column=0, sticky=W, pady=5)
    lbl_value[x] = Label(left_region_frame, text=f':         ', font=fontDecoration,highlightthickness=2)
    lbl_value[x].grid(row=x, column=1,  sticky=W, pady=5)

#=============================================================
#                   Buat Image Region
#=============================================================
def imagetRegion():
    for x in range(len(REGIONS)):
        size = WIDTH * 0.065
        fileName = REGIONS[x] if os.path.isfile(f'{constan.PATH_TESTING}{REGIONS[x]}{constan.IMAGE_TYPE}') else constan.NO_IMAGE_FILE_NAME 
        path = f'{constan.PATH_TESTING}{fileName}{constan.IMAGE_TYPE}'
        img = Image.open(path)
        imgRegion = img.resize((int(size), int(size)), Image.ANTIALIAS)
        imgREGIONS[x] = ImageTk.PhotoImage(imgRegion)
        button_dict[REGIONS[x]] = Button(images_area, width=size, height=size, image=imgREGIONS[x],
        borderwidth=0, command=lambda m=x: imageRegionPress(m), highlightthickness=2)
        button_dict[REGIONS[x]].grid(row=x, column=0,sticky='nsew')
        button_dict[REGION].configure(highlightbackground='blue', highlightthickness=2)
imagetRegion()




#=============================================================
#                   Tampilkan Seluruh komponen
#=============================================================
root.eval('tk::PlaceWindow . center')
root.resizable(False, False) 
root.mainloop()