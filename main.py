import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import pytesseract
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os
import pandas as pd
import mysql.connector as sql
from tkinter.simpledialog import askstring


# defining the attributes that are required for number plate text
def get_number_plate_text():   
    global root, car_number, show_name_plate_label, error_msg, error_msg_label, df1, car_no

    try:
        mycon1 = sql.connect(host='localhost', user='root', password=myPass)#declare a mycon1 as a variable to connect SQL serever to the python     
        cursor1 = mycon1.cursor()
        create_database = "create database if not exists anpr;"   #create a database if database is not crated (not exists) in the system
        cursor1.execute(create_database) #execute the command to create database
        mycon1.commit()             #used to save changes in database
        mycon1.close()              # close database

# After creating a database
# Create a tables
# If already tables are exists then don't create table
        mycon2 = sql.connect(host='localhost', user='root', password=myPass, database='anpr')
        
        if mycon2.is_connected():
            create_table_theft = "create table if not exists thief(Sr_No int, Car_number varchar(30));"
            create_table_car_data = "create table if not exists car_data(Sr_No int, Car_number varchar(30));"
            cursor2 = mycon2.cursor()
            cursor3 = mycon2.cursor()
            cursor2.execute(create_table_theft)     #execute the command to create table thief  
            cursor3.execute(create_table_car_data)  #execute the command to create table car_data
            mycon2.commit()
        mycon2.close()

        mycon = sql.connect(host='localhost', user='root', password=myPass, database='anpr')
       
        if mycon.is_connected():
            df1 = pd.read_sql("select * from thief;", mycon)
            theft_list = []
            # print(df1["Car_No"])
            for i in range(0, len(df1)):
                theft_list.append(df1["Car_number"][i])
            #print(theft_list)

        image_file = tkinter.filedialog.askopenfile()
        # declare the variable as image_path
        image_path = os.path.abspath(image_file.name)       
        #image path
        img = cv2.imread(image_path)
        # convert into gray scale
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # show the image
        plt.imshow(cv2.cvtColor(gray,cv2.COLOR_BGR2RGB))   
        # plt.show()
        plt.show(block=False)
        # time delay to show the image
        plt.pause(3)
        # after execution close the tab
        plt.close()
        # Noise reduction
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
        # Edge detection
        edged = cv2.Canny(bfilter, 30, 200)
        plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))  
        # plt.show()
        plt.show(block=False)
        plt.pause(3)
        plt.close()

# using the matplotlib (library of python)
# showing the image_edges locations
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        # print(location)


# Masking of the image
# and Crop the image to apropriate size

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
        # plt.show()
        plt.show(block=False)
        plt.pause(3)
        plt.close()

        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        # plt.show()

    # pip install pytesseract

    # give the path of pytesseract
    
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        # To convert the image into text 
        image_to_text = pytesseract.image_to_string(new_image, lang='eng')
        # print(image_to_text)
        tkinter.messagebox.showinfo("Car Number Extracted", f"Number: {image_to_text}")
       # tkinter.messagebox.showerror("Car Number Extracted", f"Number: {image_to_text}")
        car_no = image_to_text.strip().lstrip()   # to remove the spaces in th output for comparing the number with the database
        car_number.set(car_no)
        if(car_no in theft_list):           # check whether the number is in thief list???
                error_msg.set("This Car Number is found in Thief Activity")     # this message show in main (front) page
                tkinter.messagebox.showerror("Error", "Thief Number Found!")        # if number plate found in the thief list show pop-up message 
        else:
            error_msg.set("")
            

        # print(car_no, type(car_no))
        df2 = pd.read_sql("select * from car_data;", mycon) # use table car_data to store 
        car_data_list = []
        for i in range(0, len(df2)):
            car_data_list.append(df2["Car_number"][i])   # new car numbers are append(insert) in the table of the database


    # compare whether the number is in the table or not
        if(car_no in car_data_list):
            #if():
                tkinter.messagebox.showinfo("Info", "Car Number Already Exists")  

        # insert into car_data Table if not prsent
        else:
            cursor = mycon.cursor()
            car_no_database_len = len(df2)
            insert_car_no = f"insert into car_data values({car_no_database_len+1}, '{car_no}');"
            cursor.execute(insert_car_no)
            mycon.commit()
        mycon.close()
    except Exception as e1:
        tkinter.messagebox.showerror("Error", "You Entered Wrong MySQL Password\nPlease Restart the Software!")  # if your password of mySQL is incorrect the restart the machine
       # tkinter.messagebox.showerror("Error", "You Entered wrong ")  # Input image is incorrect the restart the machine 



 
def add_thief_func():
    try:
        mycon3 = sql.connect(host='localhost', user='root', password=myPass, database='anpr')
        if mycon3.is_connected():
            df1_len = len(df1)
            cursor4 = mycon3.cursor()
            insert_into_thief = f"insert into thief values({df1_len+1}, '{car_no}');"
            cursor4.execute(insert_into_thief)
            mycon3.commit()
            tkinter.messagebox.showinfo("Sucess", "Thief Number Added Successfully!!")
        mycon3.close()
    except Exception as e:
        tkinter.messagebox.showerror("Error", "Please Select Number Plate Image to add as Thief!!")



# Main page interface

root = Tk()
#size of the display
root.geometry("700x500")    # size of window
root.title("Automatic Number Plate Recognition (ANPR)")  # title on the main page
root.iconbitmap('car.ico')   # icon of the ANPR
root.resizable(False, False)  # we can't maximize the window 


# backgound image 
bg = PhotoImage(file = "bg_img.png")   
label1 = Label(root, image = bg)
label1.place(x = -10, y = 0)


# the size,font, colour, and the geometry of the main title and backgound colour of the text
title_name = Label(root, text="Automatic Number Plate Recognition (ANPR)", font="comicsansms 19 bold", bg="#38015e", fg="white")
title_name.place(x=100, y=50)


# The size,font, colour, and the geometry of the  select image button
select_image_btn = Button(root, text="Select Image", font="comicsansms 12 bold", fg="blue", command=get_number_plate_text)
select_image_btn.place(x=285, y=110)


# The size,font, colour, and the geometry of the  thief button
add_thief_btn = Button(root, text="Add Thief", font="comicsansms 12 bold", fg="red", command=add_thief_func)
add_thief_btn.place(x=295, y=150)


# The size,font, colour, and the geometry of the output i.e. number of car
car_number = StringVar()
show_name_plate_label = Label(root, textvariable=car_number, font="comicsansms 19 bold", fg='green')
show_name_plate_label.place(x=270, y=300)


# The size,font, colour, and the geometry of the output i.e. number of car which is present in the thief acitivites
error_msg = StringVar()
error_msg_label = Label(root, textvariable=error_msg, font=("Berlin Sans FB", 16), fg='red')
error_msg_label.place(x=185, y=340)


myPass = askstring('Mysql Password', 'Enter Your MySQL Password')   # for entering the password of mySQL server

root.mainloop()
