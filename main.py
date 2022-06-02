import datetime
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3



#----------
#=========================Functions==================================

#----------------------------------Validations------------------------------------------------

# 1st Window

def next_page_1(frame):
    global name, sex, category, religion, nationality,handicap,handicap_percentage, dob, dob_txt, father_name, father_occ, mother_name, mother_occ, guardian_name, rel_guardian, session, reg_no, student_id, course

    name = str(ent_name.get()).title()
    sex = cmb_sex.get()
    category = cmb_category.get()
    religion = cmb_religion.get()
    nationality = cmb_nationality.get()
    handicap = ph.get().capitalize()
    handicap_percentage = ent_per_ph.get()
    dob = cal.get_date()
    dob_txt = cal.get()
    father_name = str(ent_father_name.get())
    father_occ = str(ent_father_occu.get())
    mother_name = str(ent_mother_name.get())
    mother_occ = str(ent_mother_occu.get())
    guardian_name = str(ent_guardian.get())
    rel_guardian = str(ent_guardian_rel.get())
    session = cmb_session.get()
    reg_no = str(ent_registration.get())
    student_id = str(ent_student_id.get())
    course = str(cmb_course.get())


    # Nationality
    if cmb_nationality.get() == "Indian":
        ent_country.delete(0, END)
        ent_country.insert(0, "India")
        lbl_country.configure(text="Country")
        ent_country.configure(state="readonly")
    elif cmb_nationality.get() == "Others":
        lbl_country.configure(text="Country *")
        ent_country.configure(state=NORMAL)
        ent_country.delete(0, END)


    # Validation
    if name == "" or sex == "Select" or category == "Select" or religion == "Select" or nationality == "Select" or father_name == "" or father_occ == "" or mother_name == "" or mother_occ == "" or guardian_name == "" or rel_guardian == "" or session == "Select" or reg_no == "" or  course == "Select" :
        messagebox.showerror("Error", "All Fields are Required!", parent = root)
    elif ph.get() == "yes" and ent_per_ph.get() == "":
        messagebox.showerror("Error", "Please Enter the Percentage of Disability.", parent = root)
    elif dob == tdy:
        messagebox.showerror("Date Entry Error", "Please Select Date of Birth.", parent = root)
    elif student_id == "":
        value = messagebox.askquestion("Students Id.", "Want to go to the Next Page without Student ID?", parent=root)

        if value == "yes":
            frame.tkraise()
    else:
        frame.tkraise()

    ent_phone.focus()



#-----------------------Swapping--------------------------------------




#-----------------------Enable and Disable---------------------------

# Handicap text area
def enable_ph():
    if ph.get() == "yes":
        ent_per_ph.configure(state = NORMAL)
        ent_per_ph.focus()          # Focus the entry field
    else:
        ent_per_ph.delete(0, END)
        ent_per_ph.configure(state=DISABLED)




#----------------------------- 2nd Window Functions -----------------------------------

# Transfer address
def disable_add():
    if same_add.get() == "no":
        text_prsnt_add.configure(state = NORMAL)
        text_prsnt_add.configure(bg="whitesmoke")
        ent_pincode.configure(state=NORMAL)

        lbl_prsnt_add.configure(text="Present Address *")
        lbl_pincode.configure(text="Pincode *")
    else:
        text_prsnt_add.delete("1.0", END)
        text_prsnt_add.configure(state=DISABLED)
        text_prsnt_add.configure(bg= "#2C3E50")
        ent_pincode.delete(0, END)
        ent_pincode.configure(state=DISABLED)

        lbl_prsnt_add.configure(text="Present Address")
        lbl_pincode.configure(text="Pincode")



# Validation 2nd Window

def next_page_2(frame):

    global contact, email, guardian_contact, guardian_email, aadhaar, prmnt_address, prmnt_pincode, prsnt_address, prsnt_pincode, city, district, state, country

    contact = str(ent_phone.get())
    email = str(ent_email.get())
    guardian_contact = str(ent_g_phone.get())
    guardian_email = str(ent_g_email.get())
    aadhaar = str(ent_aadhaar.get())

    prmnt_address = str(text_prmnt_add.get("1.0", END)).rstrip()
    prmnt_pincode = str(ent_pincode_p.get())

    if text_prsnt_add.cget("state") != DISABLED:
        prsnt_address = str(text_prsnt_add.get("1.0", END)).rstrip()
        prsnt_pincode = str(ent_pincode.get())
    else:
        prsnt_address = prmnt_address
        prsnt_pincode = prmnt_pincode

    city = str(ent_city.get())
    district = str(ent_district.get())
    state = str(ent_state.get())
    country = str(ent_country.get())

    ses = "s" + session[:4] + "to" + session[5:9]

    if contact == ""  or guardian_contact =="" or aadhaar =="" or prmnt_address=="" or prmnt_pincode=="" or city =="" or district=="" or state =="" or country=="" :
        messagebox.showerror("Error", "All Fields are Required!!!", parent = root)
    elif prsnt_address == '' or prsnt_pincode == "":
        messagebox.showerror("Error", "All Fields are Required!!!", parent = root)
    elif email == "":
        messagebox.showerror("Error", "Please Enter the Email Address!!!", parent = root)
        lbl_email.configure(text = "Email Address *", fg="red")
    else:
        lbl_email.configure(text="Email Address", fg="black")
        try:
            conn = sqlite3.connect("./databases_student/students.db")
            cur = conn.cursor()

            # cur.execute(f"""
            # SELECT * FROM {ses} WHERE email = (%s)
            # """, (email, ))

            cur.execute(f"""
            SELECT * FROM {ses} WHERE email = (?)
            """, (email,))

            data_email = cur.fetchone()
            conn.commit()

            if data_email != None:
                messagebox.showerror("Email Error", "Email is already in use!!!")
            else:
                frame.tkraise()

        # except pymysql.Error:
        except sqlite3.OperationalError as es:
            frame.tkraise()


#--------------------------------------------3rd Window-------------------------------------------
#-----------------------Upload Image---------------------------

def upload_image():
    global photo, image_data
    filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("jpg", "*.jpg"), ("png", "*.png")])

    if filename == "":
        pass
    else:
        try:
            selected_image = Image.open(filename)
            # Resizing image
            resized = selected_image.resize((170, 200), Image.ANTIALIAS)

            # new image
            photo = ImageTk.PhotoImage(resized)

            # Changing the image
            lbl_image.configure(image = photo)

            # Adding the filename
            lbl_image_name.configure(text = os.path.basename(filename))


            # Image
            with open(filename, "rb") as f_obj:
                image_data = f_obj.read()

            ses = "s" + session[:4] + "to" + session[5:9]
            conn = sqlite3.connect("./databases_student/student_images.db")
            cur = conn.cursor()

            cur.execute(f"CREATE TABLE IF NOT EXISTS {ses} (email TEXT, image BLOB)")
            conn.commit()

            cur.execute(f"INSERT INTO {ses} VALUES(?, ?)", (ent_email.get(), image_data))
            conn.commit()

            cur.close()
            conn.close()
        except Exception:
            messagebox.showerror("Upload Error", "Please select correct image.", parent=root)


def clear_regiser():
    # 1st window
    ent_name.delete(0, END)
    cmb_sex.current(0)
    cmb_category.current(0)
    cmb_religion.current(0)
    cmb_nationality.current(0)

    ph.set("no")
    ent_per_ph.delete(0, END)
    ent_per_ph.config(state=DISABLED)

    cal.set_date(tdy)

    ent_father_name.delete(0, END)
    ent_father_occu.delete(0, END)
    ent_mother_name.delete(0, END)
    ent_mother_occu.delete(0, END)
    ent_guardian.delete(0, END)
    ent_guardian_rel.delete(0, END)
    cmb_session.current(0)
    ent_registration.delete(0, END)
    ent_student_id.delete(0, END)
    cmb_course.current(0)

    # 2nd window
    ent_phone.delete(0, END)
    ent_email.delete(0, END)
    ent_g_phone.delete(0, END)
    ent_g_email.delete(0, END)
    ent_aadhaar.delete(0, END)

    text_prmnt_add.delete("1.0", END)
    ent_pincode_p.delete(0, END)

    same_add.set("no")
    text_prsnt_add.configure(bg="whitesmoke")
    lbl_prsnt_add.configure(text="Present Address *")
    lbl_pincode.configure(text="Pincode *")

    text_prsnt_add.config(state=NORMAL)
    text_prsnt_add.delete("1.0", END)

    ent_pincode.config(state=NORMAL)
    ent_pincode.delete(0, END)


    ent_city.delete(0, END)
    ent_district.delete(0, END)
    ent_state.delete(0, END)

    ent_country.config(state=NORMAL)
    ent_country.delete(0, END)

    # 3rd window
    ent_last_instn.delete(0, END)
    txt_last_instn_addrs.delete("1.0", END)
    txt_hobby.delete("1.0", END)

    ent_exam1.delete(0, END)
    ent_exam2.delete(0, END)
    ent_exam3.delete(0, END)
    ent_exam4.delete(0, END)

    ent_board1.delete(0, END)
    ent_board2.delete(0, END)
    ent_board3.delete(0, END)
    ent_board4.delete(0, END)

    ent_passyear1.delete(0, END)
    ent_passyear2.delete(0, END)
    ent_passyear3.delete(0, END)
    ent_passyear4.delete(0, END)

    ent_marks1.delete(0, END)
    ent_marks2.delete(0, END)
    ent_marks3.delete(0, END)
    ent_marks4.delete(0, END)

    ent_cgpa1.delete(0, END)
    ent_cgpa2.delete(0, END)
    ent_cgpa3.delete(0, END)
    ent_cgpa4.delete(0, END)

    ent_percentage1.delete(0, END)
    ent_percentage2.delete(0, END)
    ent_percentage3.delete(0, END)
    ent_percentage4.delete(0, END)


    lbl_image.config(text="Your Image", image="")
    lbl_image_name.config(text="")


def submit():
    global last_instn, last_instn_add, hobby, exam_1, exam_2, exam_3, exam_4, board_1, board_2, board_3, board_4, tm_1, tm_2, tm_3, tm_4, cgpa_1, cgpa_2, cgpa_3, cgpa_4, percnt_1, percnt_2, percnt_3, percnt_4, image_check, passyear_1, passyear_2, passyear_3, passyear_4

    last_instn = str(ent_last_instn.get())
    last_instn_add = str(txt_last_instn_addrs.get("1.0", END)).rstrip()
    hobby = str(txt_hobby.get("1.0", END)).rstrip()

    exam_1 = str(ent_exam1.get())
    exam_2 = str(ent_exam2.get())
    exam_3 = str(ent_exam3.get())
    exam_4 = str(ent_exam4.get())

    board_1 = str(ent_board1.get())
    board_2 = str(ent_board2.get())
    board_3 = str(ent_board3.get())
    board_4 = str(ent_board4.get())

    passyear_1 = str(ent_passyear1.get())
    passyear_2 = str(ent_passyear2.get())
    passyear_3 = str(ent_passyear3.get())
    passyear_4 = str(ent_passyear4.get())

    tm_1 = str(ent_marks1.get())
    tm_2 = str(ent_marks2.get())
    tm_3 = str(ent_marks3.get())
    tm_4 = str(ent_marks4.get())

    cgpa_1 = str(ent_cgpa1.get())
    cgpa_2 = str(ent_cgpa2.get())
    cgpa_3 = str(ent_cgpa3.get())
    cgpa_4 = str(ent_cgpa4.get())

    percnt_1 = str(ent_percentage1.get())
    percnt_2 = str(ent_percentage2.get())
    percnt_3 = str(ent_percentage3.get())
    percnt_4 = str(ent_percentage4.get())



    image_check = str(lbl_image_name.cget("text"))

    if last_instn == "" or last_instn_add == "" or hobby == "":
        messagebox.showerror("Error", "All Fields Are Requeired!")
    elif image_check == "":
        messagebox.showerror("Error", "Please Upload an Image!!!", parent = root)
    else :
        # Modify session text
        ses = "s" + session[:4] + "to" + session[5:9]

        conn = sqlite3.connect("./databases_student/students.db")
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {ses}(id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, sex TEXT, category TEXT, religion TEXT, nationality TEXT, handicapped TEXT, percentageHandicap TEXT,  dob TEXT, fatherName TEXT, fatherOccu TEXT, motherName TEXT, motherOccu TEXT, guardianName TEXT, relGuardian TEXT, session TEXT, regNo TEXT, studentId TEXT, course TEXT, contact TEXT, email TEXT, guardian_contact TEXT, guardian_email TEXT, aadhaar TEXT, prmnt_address TEXT, prmnt_pincode TEXT, prsnt_address TEXT, prsnt_pincode TEXT, city TEXT, district TEXT, state TEXT, country TEXT, last_instn TEXT, last_instn_add TEXT, hobby TEXT, exam_1 TEXT, exam_2 TEXT, exam_3 TEXT, exam_4 TEXT, board_1 TEXT, board_2 TEXT, board_3 TEXT, board_4 TEXT, tm_1 TEXT, tm_2 TEXT, tm_3 TEXT, tm_4 TEXT, cgpa_1 TEXT, cgpa_2 TEXT, cgpa_3 TEXT, cgpa_4 TEXT, percnt_1 TEXT, percnt_2 TEXT, percnt_3 TEXT, percnt_4 TEXT, passyear_1 TEXT,passyear_2 TEXT, passyear_3 TEXT, passyear_4 TEXT)""")

        # cur.execute(f"""CREATE TABLE IF NOT EXISTS {ses}(id INT AUTO_INCREMENT PRIMARY KEY, fullname VARCHAR(50), sex VARCHAR(50), category VARCHAR(50), religion VARCHAR(50), nationality VARCHAR(50), handicapped VARCHAR(50), percentageHandicap VARCHAR(50),  dob VARCHAR(50), fatherName VARCHAR(50), fatherOccu VARCHAR(50), motherName VARCHAR(50), motherOccu VARCHAR(50), guardianName VARCHAR(50), relGuardian VARCHAR(50), session VARCHAR(50), regNo VARCHAR(50), studentId VARCHAR(50), course VARCHAR(50), contact VARCHAR(50), email VARCHAR(50), guardian_contact VARCHAR(50), guardian_email VARCHAR(50), aadhaar VARCHAR(50), prmnt_address VARCHAR(50), prmnt_pincode VARCHAR(50), prsnt_address VARCHAR(50), prsnt_pincode VARCHAR(50), city VARCHAR(50), district VARCHAR(50), state VARCHAR(50), country VARCHAR(50), last_instn VARCHAR(50), last_instn_add VARCHAR(50), hobby VARCHAR(50), exam_1 VARCHAR(50), exam_2 VARCHAR(50), exam_3 VARCHAR(50), exam_4 VARCHAR(50), board_1 VARCHAR(50), board_2 VARCHAR(50), board_3 VARCHAR(50), board_4 VARCHAR(50), tm_1 VARCHAR(50), tm_2 VARCHAR(50), tm_3 VARCHAR(50), tm_4 VARCHAR(50), cgpa_1 VARCHAR(50), cgpa_2 VARCHAR(50), cgpa_3 VARCHAR(50), cgpa_4 VARCHAR(50), percnt_1 VARCHAR(50), percnt_2 VARCHAR(50), percnt_3 VARCHAR(50), percnt_4 VARCHAR(50), passyear_1 VARCHAR(50),passyear_2 VARCHAR(50), passyear_3 VARCHAR(50), passyear_4 VARCHAR(50))""")
        # conn.commit()
        # Inserting data into database
        # cur.execute(f"""INSERT INTO {ses}(fullname, sex, category, religion, nationality, handicapped, percentageHandicap, dob, fatherName, fatherOccu, motherName, motherOccu, guardianName, relGuardian, session, regNo, studentId, course,  contact, email, guardian_contact, guardian_email, aadhaar, prmnt_address, prmnt_pincode, prsnt_address, prsnt_pincode, city, district, state, country, last_instn, last_instn_add, hobby, exam_1, exam_2, exam_3, exam_4, board_1, board_2, board_3, board_4, tm_1, tm_2, tm_3, tm_4, cgpa_1, cgpa_2, cgpa_3, cgpa_4, percnt_1, percnt_2, percnt_3, percnt_4, passyear_1, passyear_2, passyear_3, passyear_4) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
        #     (name, sex, category, religion, nationality, handicap, handicap_percentage, dob_txt, father_name, father_occ, mother_name, mother_occ,guardian_name, rel_guardian, session, reg_no, student_id, course, contact, email, guardian_contact, guardian_email, aadhaar, prmnt_address, prmnt_pincode, prsnt_address, prsnt_pincode, city, district, state, country, last_instn, last_instn_add, hobby, exam_1, exam_2, exam_3, exam_4, board_1, board_2, board_3, board_4,tm_1, tm_2, tm_3, tm_4, cgpa_1, cgpa_2, cgpa_3, cgpa_4, percnt_1, percnt_2, percnt_3, percnt_4, passyear_1, passyear_2, passyear_3, passyear_4)
        # )
        # conn.commit()

        #---sqlite----
        cur.execute(
            f"""INSERT INTO {ses}(fullname, sex, category, religion, nationality, handicapped, percentageHandicap, dob, fatherName, fatherOccu, motherName, motherOccu, guardianName, relGuardian, session, regNo, studentId, course,  contact, email, guardian_contact, guardian_email, aadhaar, prmnt_address, prmnt_pincode, prsnt_address, prsnt_pincode, city, district, state, country, last_instn, last_instn_add, hobby, exam_1, exam_2, exam_3, exam_4, board_1, board_2, board_3, board_4, tm_1, tm_2, tm_3, tm_4, cgpa_1, cgpa_2, cgpa_3, cgpa_4, percnt_1, percnt_2, percnt_3, percnt_4, passyear_1, passyear_2, passyear_3, passyear_4) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """,
            (
            name, sex, category, religion, nationality, handicap, handicap_percentage, dob_txt, father_name, father_occ,
            mother_name, mother_occ, guardian_name, rel_guardian, session, reg_no, student_id, course, contact, email,
            guardian_contact, guardian_email, aadhaar, prmnt_address, prmnt_pincode, prsnt_address, prsnt_pincode, city,
            district, state, country, last_instn, last_instn_add, hobby, exam_1, exam_2, exam_3, exam_4, board_1,
            board_2, board_3, board_4, tm_1, tm_2, tm_3, tm_4, cgpa_1, cgpa_2, cgpa_3, cgpa_4, percnt_1, percnt_2,
            percnt_3, percnt_4, passyear_1, passyear_2, passyear_3, passyear_4)
            )
        conn.commit()



        #---sqlite----


        cur.close()
        conn.close()
        messagebox.showinfo("Success", "Registered", parent=root)
        clear_regiser()
        main_frame_homepage.tkraise()
        frame_body.tkraise()





        # print(name, sex, category, religion, nationality, dob, father_name, father_occ, mother_name, mother_occ,
        #       guardian_name, rel_guardian, session, reg_no, student_id, course,
        #       contact, email, guardian_contact, guardian_email, aadhaar, prmnt_address, prmnt_pincode, prsnt_address,
        #       prsnt_pincode, city, district, state, country,
        #       last_instn, last_instn_add, hobby, exam_1, exam_2, exam_3, exam_4, board_1, board_2, board_3, board_4,
        #       tm_1, tm_2, tm_3, tm_4, cgpa_1, cgpa_2, cgpa_3, cgpa_4, percnt_1, percnt_2, percnt_3, percnt_4, image_check
        # )
#----------




# import pymysql
#
# # conn = sqlite3.connect("./databases_student/students.db")
# try :
#     conn = pymysql.connect(
#         host='bvv3lahnyu5nncyxuqbl-mysql.services.clever-cloud.com',
#         user='ubnpk38tmih13jlz',
#         password='g6s41DvsZu2TSA0Jpb2R',
#         database="bvv3lahnyu5nncyxuqbl",
#     )
# except Exception as es:
#     print(es)
#
# finally:
#     conn = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database="students",
#     )

# Making cursor for the database
# cur = conn.cursor()


# Current Date
tdy = datetime.date.today()

root = Tk()
root.geometry("1200x600+50+50")
root.title("Krishnagar Government College - Physics Department")
root.resizable(False, False)
p1 = PhotoImage(file = './img/ico.png')
root.iconphoto(False, p1)






#--------------------------------------------------------------------------
#=========================Functions=====================================
#--------------------------------------------------------------------------

# -------------------------------------Global function-------------------------
def swap(frame):
    frame.tkraise()
# -------------------------------------$$$Global function$$$$$-------------------------


# -------------------------------------Student function-------------------------

def sign_in(frame):
    global ses_select, session_selected, regno_si, email_si

    session_selected = str(cmb_session_si.get())
    regno_si = str(ent_registration_si.get())
    email_si = str(ent_email_si.get())

    if session_selected == "Select" and regno_si == "" and email_si == "":
        messagebox.showerror("Error", "All Fields Required!!!", parent=root)
        lbl_session_si.configure(text="Session *", fg="red")
        lbl_registration_si.configure(text="Registration Number *", fg="red")
        lbl_email_si.configure(text="Email Address *", fg="red")

    elif session_selected == "Select":
        messagebox.showerror("Error", "All Fields Required!!!", parent=root)
        lbl_session_si.configure(text="Session *", fg="red")
    elif regno_si == "":
        messagebox.showerror("Error", "Please Enter Registration Number", parent=root)
        lbl_registration_si.configure(text="Registration Number *", fg="red")
    elif email_si == "":
        messagebox.showerror("Error", "Please Enter Email Address", parent=root)
        lbl_email_si.configure(text="Email Address *", fg="red")
    else:
        lbl_session_si.configure(text="Session", fg="black")
        lbl_registration_si.configure(text="Registration Number", fg="black")
        lbl_email_si.configure(text="Email Address", fg="black")

    # Modify session text
        ses_select = "s" + session_selected[:4] + "to" + session_selected[5:9]
        conn = sqlite3.connect('./databases_student/students.db')
        cur = conn.cursor()


        try:
            cur.execute(f"SELECT * FROM  {ses_select}  WHERE regNo = ? AND email = ?", (regno_si, email_si))
            personal_data = cur.fetchone()
            conn.commit()

            if personal_data == None:
                messagebox.showerror("Error", "User does not exist!!!", parent=root)
                lbl_session_si.configure(text="Session *", fg="red")
                lbl_registration_si.configure(text="Registration Number *", fg="red")
                lbl_email_si.configure(text="Email Address *", fg="red")
            else:

                cur.execute(f"SELECT * FROM {ses_select} where email = (?)", (ent_email_si.get(),))
                row = cur.fetchone()
                conn.commit()

                # Values
                name = row[1]
                sex = row[2]
                category = row[3]
                religion = row[4]
                nationality = row[5]
                handicap = row[6]
                handicap_percentage = row[7]
                dob_txt = row[8]
                father_name = row[9]
                father_occ = row[10]
                mother_name = row[11]
                mother_occ = row[12]
                guardian_name = row[13]
                rel_guardian = row[14]
                session = row[15]
                reg_no = row[16]
                student_id = row[17]
                course = row[18]
                contact = row[19]
                email = row[20]
                guardian_contact = row[21]
                guardian_email = row[22]
                aadhaar = row[23]
                prmnt_address = row[24]
                prmnt_pincode = row[25]
                prsnt_address = row[26]
                prsnt_pincode = row[27]
                city = row[28]
                district = row[29]
                state = row[30]
                country = row[31]
                last_instn = row[32]
                last_instn_add = row[33]
                hobby = row[34]
                exam_1 = row[35]
                exam_2 = row[36]
                exam_3 = row[37]
                exam_4 = row[38]
                board_1 = row[39]
                board_2 = row[40]
                board_3 = row[41]
                board_4 = row[42]
                tm_1 = row[43]
                tm_2 = row[44]
                tm_3 = row[45]
                tm_4 = row[46]
                cgpa_1 = row[47]
                cgpa_2 = row[48]
                cgpa_3 = row[49]
                cgpa_4 = row[50]
                percnt_1 = row[51]
                percnt_2 = row[52]
                percnt_3 = row[53]
                percnt_4 = row[54]
                passyear_1 = row[55]
                passyear_2 = row[56]
                passyear_3 = row[57]
                passyear_4 = row[58]

                ent_name_get_2.config(state=NORMAL)
                ent_name_get_2.delete(0, END)
                ent_name_get_2.insert(0, name)
                ent_name_get_2.config(state=DISABLED)

                lbl_sex_get_2.config(text=sex)
                lbl_cat_get_2.config(text=category)
                lbl_religion_get_2.config(text=religion)
                lbl_nationality_get_2.config(text=nationality)
                lbl_physical_handicap_get_2.config(text=handicap)
                lbl_percntg_hc_get_2.config(text=handicap_percentage)
                lbl_dob_get_2.config(text=dob_txt)
                lbl_country_get_2.config(text=country)

                ent_aadhaar_get_2.config(state=NORMAL)
                ent_aadhaar_get_2.delete(0, END)
                ent_aadhaar_get_2.insert(0, aadhaar)
                ent_aadhaar_get_2.config(state=DISABLED)

                ent_father_name_get_2.config(state=NORMAL)
                ent_father_name_get_2.delete(0, END)
                ent_father_name_get_2.insert(0, father_name)
                ent_father_name_get_2.config(state=DISABLED)

                ent_father_occu_get_2.config(state=NORMAL)
                ent_father_occu_get_2.delete(0, END)
                ent_father_occu_get_2.insert(0, father_occ)
                ent_father_occu_get_2.config(state=DISABLED)

                ent_mother_name_get_2.config(state=NORMAL)
                ent_mother_name_get_2.delete(0, END)
                ent_mother_name_get_2.insert(0, mother_name)
                ent_mother_name_get_2.config(state=DISABLED)

                ent_mother_occu_get_2.config(state=NORMAL)
                ent_mother_occu_get_2.delete(0, END)
                ent_mother_occu_get_2.insert(0, mother_occ)
                ent_mother_occu_get_2.config(state=DISABLED)

                ent_guardian_get_2.config(state=NORMAL)
                ent_guardian_get_2.delete(0, END)
                ent_guardian_get_2.insert(0, guardian_name)
                ent_guardian_get_2.config(state=DISABLED)

                ent_guardian_rel_get_2.config(state=NORMAL)
                ent_guardian_rel_get_2.delete(0, END)
                ent_guardian_rel_get_2.insert(0, rel_guardian)
                ent_guardian_rel_get_2.config(state=DISABLED)

                ent_g_email_get_2.config(state=NORMAL)
                ent_g_email_get_2.delete(0, END)
                ent_g_email_get_2.insert(0, guardian_email)
                ent_g_email_get_2.config(state=DISABLED)

                lbl_session_get_2.config(text=session)

                ent_registration_get_2.config(state=NORMAL)
                ent_registration_get_2.delete(0, END)
                ent_registration_get_2.insert(0, reg_no)
                ent_registration_get_2.config(state=DISABLED)

                ent_student_id_get_2.config(state=NORMAL)
                ent_student_id_get_2.delete(0, END)
                ent_student_id_get_2.insert(0, student_id)
                ent_student_id_get_2.config(state=DISABLED)

                lbl_get_course_2.config(text=course)

                ent_phone_get_2.config(state=NORMAL)
                ent_phone_get_2.delete(0, END)
                ent_phone_get_2.insert(0, contact)
                ent_phone_get_2.config(state=DISABLED)

                ent_email_get_2.config(state=NORMAL)
                ent_email_get_2.delete(0, END)
                ent_email_get_2.insert(0, email)
                ent_email_get_2.config(state=DISABLED)

                ent_g_phone_get_2.config(state=NORMAL)
                ent_g_phone_get_2.delete(0, END)
                ent_g_phone_get_2.insert(0, guardian_contact)
                ent_g_phone_get_2.config(state=DISABLED)

                text_prmnt_add_get_2.config(state=NORMAL)
                text_prmnt_add_get_2.delete("1.0", END)
                text_prmnt_add_get_2.insert("1.0", prmnt_address)
                text_prmnt_add_get_2.config(state=DISABLED)

                ent_pincode_p_get_2.config(state=NORMAL)
                ent_pincode_p_get_2.delete(0, END)
                ent_pincode_p_get_2.insert(0, prmnt_pincode)
                ent_pincode_p_get_2.config(state=DISABLED)

                text_prsnt_add_get_2.config(state=NORMAL)
                text_prsnt_add_get_2.delete("1.0", END)
                text_prsnt_add_get_2.insert("1.0", prsnt_address)
                text_prsnt_add_get_2.config(state=DISABLED)

                ent_pincode_get_2.config(state=NORMAL)
                ent_pincode_get_2.delete(0, END)
                ent_pincode_get_2.insert(0, prsnt_pincode)
                ent_pincode_get_2.config(state=DISABLED)

                ent_city_get_2.config(state=NORMAL)
                ent_city_get_2.delete(0, END)
                ent_city_get_2.insert(0, city)
                ent_city_get_2.config(state=DISABLED)

                ent_district_get_2.config(state=NORMAL)
                ent_district_get_2.delete(0, END)
                ent_district_get_2.insert(0, district)
                ent_district_get_2.config(state=DISABLED)

                ent_state_get_2.config(state=NORMAL)
                ent_state_get_2.delete(0, END)
                ent_state_get_2.insert(0, state)
                ent_state_get_2.config(state=DISABLED)

                ent_last_instn_get_2.config(state=NORMAL)
                ent_last_instn_get_2.delete(0, END)
                ent_last_instn_get_2.insert(0, last_instn)
                ent_last_instn_get_2.config(state=DISABLED)

                txt_last_instn_addrs_get_2.config(state=NORMAL)
                txt_last_instn_addrs_get_2.delete("1.0", END)
                txt_last_instn_addrs_get_2.insert("1.0", last_instn_add)
                txt_last_instn_addrs_get_2.config(state=DISABLED)

                txt_hobby_get_2.config(state=NORMAL)
                txt_hobby_get_2.delete("1.0", END)
                txt_hobby_get_2.insert("1.0", hobby)
                txt_hobby_get_2.config(state=DISABLED)

                ent_exam1_get_2.config(state=NORMAL)
                ent_exam1_get_2.delete(0, END)
                ent_exam1_get_2.insert(0, exam_1)
                ent_exam1_get_2.config(state=DISABLED)

                ent_exam2_get_2.config(state=NORMAL)
                ent_exam2_get_2.delete(0, END)
                ent_exam2_get_2.insert(0, exam_2)
                ent_exam2_get_2.config(state=DISABLED)

                ent_exam3_get_2.config(state=NORMAL)
                ent_exam3_get_2.delete(0, END)
                ent_exam3_get_2.insert(0, exam_3)
                ent_exam3_get_2.config(state=DISABLED)

                ent_exam4_get_2.config(state=NORMAL)
                ent_exam4_get_2.delete(0, END)
                ent_exam4_get_2.insert(0, exam_4)
                ent_exam4_get_2.config(state=DISABLED)

                ent_board1_get_2.config(state=NORMAL)
                ent_board1_get_2.delete(0, END)
                ent_board1_get_2.insert(0, board_1)
                ent_board1_get_2.config(state=DISABLED)

                ent_board2_get_2.config(state=NORMAL)
                ent_board2_get_2.delete(0, END)
                ent_board2_get_2.insert(0, board_2)
                ent_board2_get_2.config(state=DISABLED)

                ent_board3_get_2.config(state=NORMAL)
                ent_board3_get_2.delete(0, END)
                ent_board3_get_2.insert(0, board_3)
                ent_board3_get_2.config(state=DISABLED)

                ent_board4_get_2.config(state=NORMAL)
                ent_board4_get_2.delete(0, END)
                ent_board4_get_2.insert(0, board_4)
                ent_board4_get_2.config(state=DISABLED)

                ent_passyear1_get_2.config(state=NORMAL)
                ent_passyear1_get_2.delete(0, END)
                ent_passyear1_get_2.insert(0, passyear_1)
                ent_passyear1_get_2.config(state=DISABLED)

                ent_passyear2_get_2.config(state=NORMAL)
                ent_passyear2_get_2.delete(0, END)
                ent_passyear2_get_2.insert(0, passyear_2)
                ent_passyear2_get_2.config(state=DISABLED)

                ent_passyear3_get_2.config(state=NORMAL)
                ent_passyear3_get_2.delete(0, END)
                ent_passyear3_get_2.insert(0, passyear_3)
                ent_passyear3_get_2.config(state=DISABLED)

                ent_passyear4_get_2.config(state=NORMAL)
                ent_passyear4_get_2.delete(0, END)
                ent_passyear4_get_2.insert(0, passyear_4)
                ent_passyear4_get_2.config(state=DISABLED)

                ent_marks1_get_2.config(state=NORMAL)
                ent_marks1_get_2.delete(0, END)
                ent_marks1_get_2.insert(0, tm_1)
                ent_marks1_get_2.config(state=DISABLED)

                ent_marks2_get_2.config(state=NORMAL)
                ent_marks2_get_2.delete(0, END)
                ent_marks2_get_2.insert(0, tm_2)
                ent_marks2_get_2.config(state=DISABLED)

                ent_marks3_get_2.config(state=NORMAL)
                ent_marks3_get_2.delete(0, END)
                ent_marks3_get_2.insert(0, tm_3)
                ent_marks3_get_2.config(state=DISABLED)

                ent_marks4_get_2.config(state=NORMAL)
                ent_marks4_get_2.delete(0, END)
                ent_marks4_get_2.insert(0, tm_4)
                ent_marks4_get_2.config(state=DISABLED)

                ent_percentage1_get_2.config(state=NORMAL)
                ent_percentage1_get_2.delete(0, END)
                ent_percentage1_get_2.insert(0, percnt_1)
                ent_percentage1_get_2.config(state=DISABLED)

                ent_percentage2_get_2.config(state=NORMAL)
                ent_percentage2_get_2.delete(0, END)
                ent_percentage2_get_2.insert(0, percnt_2)
                ent_percentage2_get_2.config(state=DISABLED)

                ent_percentage3_get_2.config(state=NORMAL)
                ent_percentage3_get_2.delete(0, END)
                ent_percentage3_get_2.insert(0, percnt_3)
                ent_percentage3_get_2.config(state=DISABLED)

                ent_percentage4_get_2.config(state=NORMAL)
                ent_percentage4_get_2.delete(0, END)
                ent_percentage4_get_2.insert(0, percnt_4)
                ent_percentage4_get_2.config(state=DISABLED)

                ent_cgpa1_get_2.config(state=NORMAL)
                ent_cgpa1_get_2.delete(0, END)
                ent_cgpa1_get_2.insert(0, cgpa_1)
                ent_cgpa1_get_2.config(state=DISABLED)

                ent_cgpa2_get_2.config(state=NORMAL)
                ent_cgpa2_get_2.delete(0, END)
                ent_cgpa2_get_2.insert(0, cgpa_2)
                ent_cgpa2_get_2.config(state=DISABLED)

                ent_cgpa3_get_2.config(state=NORMAL)
                ent_cgpa3_get_2.delete(0, END)
                ent_cgpa3_get_2.insert(0, cgpa_3)
                ent_cgpa3_get_2.config(state=DISABLED)

                ent_cgpa4_get_2.config(state=NORMAL)
                ent_cgpa4_get_2.delete(0, END)
                ent_cgpa4_get_2.insert(0, cgpa_4)
                ent_cgpa4_get_2.config(state=DISABLED)

                cur.close()
                conn.close()

                # Image adding

                conn2 = sqlite3.connect("./databases_student/student_images.db")
                cur2 = conn2.cursor()

                cur2.execute(f"SELECT * FROM {ses_select} where email = (?)", (ent_email_si.get(),))
                image_dat = cur2.fetchone()[1]
                conn2.commit()

                global photo_show_2

                with open("./img/temp2.png", "wb") as f_obj:
                    f_obj.write(image_dat)

                selected_image_show = Image.open("./img/temp2.png")

                # Resizing image
                resized_show = selected_image_show.resize((130, 170), Image.ANTIALIAS)

                # new image
                photo_show_2 = ImageTk.PhotoImage(resized_show)

                # Changing the image
                lbl_image_show_2.configure(image=photo_show_2)

                cur2.close()
                conn2.close()






                lbl_session_si.configure(text="Session")
                lbl_registration_si.configure(text="Registration Number")
                lbl_email_si.configure(text="Email Address")

                cmb_session_si.current(0)
                ent_registration_si.delete(0, END)
                ent_email_si.delete(0, END)

                frame.tkraise()
        # except sqlite3.OperationalError:
        except Exception as es:
            messagebox.showerror("Error", f"Session {es} Does Not Exist!!!", parent=root)

def register(frame):
    ent_name.focus()
    frame.tkraise()



# -------------------------------------$$$Student function$$$-------------------------







#----------------Admin Panel Functions----------------------------------------

def check_pass(frame):
    global password
    password = str(ent_admin_password.get())
    if password != "kgc1820":
        messagebox.showerror("Log In Error", "Invalid Password", parent=root)
        ent_admin_password.delete(0, END)
    else:
        frame.tkraise()
        student_table.delete(*student_table.get_children())
        ent_admin_password.delete(0, END)


def take_focus():
    if len(student_table.selection()) > 0:
        student_table.selection_remove(student_table.selection()[0])

    ent_selected_name.config(state=NORMAL)
    ent_selected_email.config(state=NORMAL)

    ent_selected_name.delete(0, END)
    ent_selected_email.delete(0, END)

    ent_selected_name.config(state=DISABLED)
    ent_selected_email.config(state=DISABLED)

    btn_delete_student.config(state=DISABLED)
    btn_show_student.config(state=DISABLED)


def show_table():
    session_selected = cmb_select_session.get()
    # Modify session text
    ses_select = "s" + session_selected[:4] + "to" + session_selected[5:9]
    if session_selected != "Select":
        student_table.delete(*student_table.get_children())
        try:
            conn = sqlite3.connect("./databases_student/students.db")
            cur = conn.cursor()

            cur.execute(f"""
            SELECT * FROM {ses_select} 
            """)
            rows = cur.fetchall()

            if len(rows) != 0:
                # btn_delete_student.config(state=NORMAL)
                # btn_show_student.config(state=NORMAL)
                student_table.delete(*student_table.get_children())

                for row in rows:
                    student_table.insert('', END, values=row)
                conn.commit()

            else:
                btn_delete_student.config(state=DISABLED)
                btn_show_student.config(state=DISABLED)

                ent_selected_name.config(state=NORMAL)
                ent_selected_email.config(state=NORMAL)

                ent_selected_name.delete(0, END)
                ent_selected_email.delete(0, END)

                ent_selected_name.config(state=DISABLED)
                ent_selected_email.config(state=DISABLED)

                student_table.delete(*student_table.get_children())

                messagebox.showerror("Error", "No Data", parent = root)



        except sqlite3.OperationalError as es:
            btn_delete_student.config(state=DISABLED)
            btn_show_student.config(state=DISABLED)

            ent_selected_name.config(state=NORMAL)
            ent_selected_email.config(state=NORMAL)

            ent_selected_name.delete(0, END)
            ent_selected_email.delete(0, END)

            ent_selected_name.config(state=DISABLED)
            ent_selected_email.config(state=DISABLED)

            messagebox.showerror("Error", f"No data in this session", parent = root)


    else:
        student_table.delete(*student_table.get_children())

        ent_selected_name.config(state=NORMAL)
        ent_selected_email.config(state=NORMAL)

        ent_selected_name.delete(0, END)
        ent_selected_email.delete(0, END)

        ent_selected_name.config(state=DISABLED)
        ent_selected_email.config(state=DISABLED)

        btn_delete_student.config(state=DISABLED)
        btn_show_student.config(state=DISABLED)
        messagebox.showerror("Error", "Please Select the Session!!!", parent=root)



def get_cursor(ev):
    cursor = student_table.focus()
    contents = student_table.item(cursor)
    row = contents['values']

    real_row = student_table.identify_row(student_table.winfo_pointerxy()[1] - student_table.winfo_rooty())
    if row != '':
        btn_delete_student.config(state=NORMAL)
        btn_show_student.config(state=NORMAL)

        ent_selected_name.config(state=NORMAL)
        ent_selected_email.config(state=NORMAL)

        ent_selected_name.delete(0, END)
        ent_selected_email.delete(0, END)

        ent_selected_name.insert(0, row[1])
        ent_selected_email.insert(0, row[20])

        ent_selected_name.config(state=DISABLED)
        ent_selected_email.config(state=DISABLED)
    else:
        ent_selected_name.config(state=NORMAL)
        ent_selected_email.config(state=NORMAL)

        ent_selected_name.delete(0, END)
        ent_selected_email.delete(0, END)

        ent_selected_name.config(state=DISABLED)
        ent_selected_email.config(state=DISABLED)

        if len(student_table.selection()) > 0:
            student_table.selection_remove(student_table.selection()[0])

    if real_row == '':
        take_focus()



def delete_data_from_database():
    session_selected = cmb_select_session.get()
    # Modify session text
    ses_select = "s" + session_selected[:4] + "to" + session_selected[5:9]

    # Making connection to the database
    conn = sqlite3.connect("./databases_student/students.db")
    cur = conn.cursor()

    ent_selected_email.config(state=NORMAL)
    email_selected = ent_selected_email.get()
    ent_selected_email.config(state=DISABLED)

    if email_selected == "":
        btn_delete_student.config(state=DISABLED)
        btn_show_student.config(state=DISABLED)
        messagebox.showerror("Error", "Please select a student from table!!!", parent=root)
    else:
        q = messagebox.askquestion("Delete", f"Do you want to delete the student {ent_selected_name.get()}?", parent=root)
        if q == "yes":
            cur.execute(f"DELETE FROM {ses_select} WHERE email = (?)", (email_selected,))
            conn.commit()

            show_table()

            ent_selected_name.config(state=NORMAL)
            ent_selected_email.config(state=NORMAL)

            ent_selected_name.delete(0, END)
            ent_selected_email.delete(0, END)

            ent_selected_name.config(state=DISABLED)
            ent_selected_email.config(state=DISABLED)
        else :
            pass




    # Closing the connection
    cur.close()
    conn.close()

def gotohome(frame):
    frame.tkraise()
    frame_admin_password_window.tkraise()
    cmb_select_session.current(0)
    student_table.delete(*student_table.get_children())
    btn_delete_student.config(state=DISABLED)
    btn_show_student.config(state=DISABLED)


def show_details(frame):
    session_selected = cmb_select_session.get()
    # Modify session text
    ses_select = "s" + session_selected[:4] + "to" + session_selected[5:9]



    btn_show_student.config(state=DISABLED)
    btn_delete_student.config(state=DISABLED)

    ent_selected_email.config(state=NORMAL)
    email_selected = ent_selected_email.get()
    ent_selected_email.config(state=DISABLED)
    if email_selected == "":
        messagebox.showerror("Error", "Please select a student!", parent=root)
    else:

        conn = sqlite3.connect('./databases_student/students.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {ses_select} where email = (?)", (ent_selected_email.get(),))

        row = cur.fetchone()
        conn.commit()



        # Values

        name = row[1]
        sex = row[2]
        category = row[3]
        religion = row[4]
        nationality = row[5]
        handicap = row[6]
        handicap_percentage = row[7]
        dob_txt = row[8]
        father_name = row[9]
        father_occ = row[10]
        mother_name = row[11]
        mother_occ = row[12]
        guardian_name = row[13]
        rel_guardian = row[14]
        session = row[15]
        reg_no = row[16]
        student_id = row[17]
        course = row[18]
        contact = row[19]
        email = row[20]
        guardian_contact = row[21]
        guardian_email = row[22]
        aadhaar = row[23]
        prmnt_address = row[24]
        prmnt_pincode = row[25]
        prsnt_address = row[26]
        prsnt_pincode = row[27]
        city = row[28]
        district = row[29]
        state = row[30]
        country = row[31]
        last_instn = row[32]
        last_instn_add = row[33]
        hobby = row[34]
        exam_1 = row[35]
        exam_2 = row[36]
        exam_3 = row[37]
        exam_4 = row[38]
        board_1 = row[39]
        board_2 = row[40]
        board_3 = row[41]
        board_4 = row[42]
        tm_1 = row[43]
        tm_2 = row[44]
        tm_3 = row[45]
        tm_4 = row[46]
        cgpa_1 = row[47]
        cgpa_2 = row[48]
        cgpa_3 = row[49]
        cgpa_4 = row[50]
        percnt_1 = row[51]
        percnt_2 = row[52]
        percnt_3 = row[53]
        percnt_4 = row[54]
        passyear_1 = row[55]
        passyear_2 = row[56]
        passyear_3 = row[57]
        passyear_4 = row[58]

        ent_name_get.config(state=NORMAL)
        ent_name_get.delete(0, END)
        ent_name_get.insert(0, name)

        lbl_sex_get.config(text=sex)
        lbl_cat_get.config(text=category)
        lbl_religion_get.config(text=religion)
        lbl_nationality_get.config(text=nationality)
        lbl_physical_handicap_get.config(text=handicap)
        lbl_percntg_hc_get.config(text=handicap_percentage)
        lbl_dob_get.config(text=dob_txt)
        lbl_country_get.config(text=country)

        ent_aadhaar_get.config(state=NORMAL)
        ent_aadhaar_get.delete(0, END)
        ent_aadhaar_get.insert(0, aadhaar)

        ent_father_name_get.config(state=NORMAL)
        ent_father_name_get.delete(0, END)
        ent_father_name_get.insert(0, father_name)


        ent_father_occu_get.config(state=NORMAL)
        ent_father_occu_get.delete(0, END)
        ent_father_occu_get.insert(0, father_occ)


        ent_mother_name_get.config(state=NORMAL)
        ent_mother_name_get.delete(0, END)
        ent_mother_name_get.insert(0, mother_name)


        ent_mother_occu_get.config(state=NORMAL)
        ent_mother_occu_get.delete(0, END)
        ent_mother_occu_get.insert(0, mother_occ)


        ent_guardian_get.config(state=NORMAL)
        ent_guardian_get.delete(0, END)
        ent_guardian_get.insert(0, guardian_name)


        ent_guardian_rel_get.config(state=NORMAL)
        ent_guardian_rel_get.delete(0, END)
        ent_guardian_rel_get.insert(0, rel_guardian)


        ent_g_email_get.config(state=NORMAL)
        ent_g_email_get.delete(0, END)
        ent_g_email_get.insert(0, guardian_email)


        lbl_session_get.config(text=session)

        ent_registration_get.config(state=NORMAL)
        ent_registration_get.delete(0, END)
        ent_registration_get.insert(0, reg_no)


        ent_student_id_get.config(state=NORMAL)
        ent_student_id_get.delete(0, END)
        ent_student_id_get.insert(0, student_id)


        lbl_get_course.config(text=course)

        ent_phone_get.config(state=NORMAL)
        ent_phone_get.delete(0, END)
        ent_phone_get.insert(0, contact)


        ent_email_get.config(state=NORMAL)
        ent_email_get.delete(0, END)
        ent_email_get.insert(0, email)


        ent_g_phone_get.config(state=NORMAL)
        ent_g_phone_get.delete(0, END)
        ent_g_phone_get.insert(0, guardian_contact)


        text_prmnt_add_get.config(state=NORMAL)
        text_prmnt_add_get.delete("1.0", END)
        text_prmnt_add_get.insert("1.0", prmnt_address)
        # text_prmnt_add_get.config(state=DISABLED)

        ent_pincode_p_get.config(state=NORMAL)
        ent_pincode_p_get.delete(0, END)
        ent_pincode_p_get.insert(0, prmnt_pincode)
        # ent_pincode_p_get.config(state=DISABLED)

        text_prsnt_add_get.config(state=NORMAL)
        text_prsnt_add_get.delete("1.0", END)
        text_prsnt_add_get.insert("1.0", prsnt_address)
        # text_prsnt_add_get.config(state=DISABLED)

        ent_pincode_get.config(state=NORMAL)
        ent_pincode_get.delete(0, END)
        ent_pincode_get.insert(0, prsnt_pincode)
        # ent_pincode_get.config(state=DISABLED)

        ent_city_get.config(state=NORMAL)
        ent_city_get.delete(0, END)
        ent_city_get.insert(0, city)
        # ent_city_get.config(state=DISABLED)

        ent_district_get.config(state=NORMAL)
        ent_district_get.delete(0, END)
        ent_district_get.insert(0, district)
        # ent_district_get.config(state=DISABLED)

        ent_state_get.config(state=NORMAL)
        ent_state_get.delete(0, END)
        ent_state_get.insert(0, state)
        # ent_state_get.config(state=DISABLED)

        ent_last_instn_get.config(state=NORMAL)
        ent_last_instn_get.delete(0, END)
        ent_last_instn_get.insert(0, last_instn)
        # ent_last_instn_get.config(state=DISABLED)

        txt_last_instn_addrs_get.config(state=NORMAL)
        txt_last_instn_addrs_get.delete("1.0", END)
        txt_last_instn_addrs_get.insert("1.0", last_instn_add)
        # txt_last_instn_addrs_get.config(state=DISABLED)

        txt_hobby_get.config(state=NORMAL)
        txt_hobby_get.delete("1.0", END)
        txt_hobby_get.insert("1.0", hobby)
        # txt_hobby_get.config(state=DISABLED)

        ent_exam1_get.config(state=NORMAL)
        ent_exam1_get.delete(0, END)
        ent_exam1_get.insert(0, exam_1)
        # ent_exam1_get.config(state=DISABLED)

        ent_exam2_get.config(state=NORMAL)
        ent_exam2_get.delete(0, END)
        ent_exam2_get.insert(0, exam_2)
        # ent_exam2_get.config(state=DISABLED)

        ent_exam3_get.config(state=NORMAL)
        ent_exam3_get.delete(0, END)
        ent_exam3_get.insert(0, exam_3)
        # ent_exam3_get.config(state=DISABLED)

        ent_exam4_get.config(state=NORMAL)
        ent_exam4_get.delete(0, END)
        ent_exam4_get.insert(0, exam_4)
        # ent_exam4_get.config(state=DISABLED)

        ent_board1_get.config(state=NORMAL)
        ent_board1_get.delete(0, END)
        ent_board1_get.insert(0, board_1)
        # ent_board1_get.config(state=DISABLED)

        ent_board2_get.config(state=NORMAL)
        ent_board2_get.delete(0, END)
        ent_board2_get.insert(0, board_2)
        # ent_board2_get.config(state=DISABLED)

        ent_board3_get.config(state=NORMAL)
        ent_board3_get.delete(0, END)
        ent_board3_get.insert(0, board_3)
        # ent_board3_get.config(state=DISABLED)

        ent_board4_get.config(state=NORMAL)
        ent_board4_get.delete(0, END)
        ent_board4_get.insert(0, board_4)
        # ent_board4_get.config(state=DISABLED)

        ent_passyear1_get.config(state=NORMAL)
        ent_passyear1_get.delete(0, END)
        ent_passyear1_get.insert(0, passyear_1)
        # ent_passyear1_get.config(state=DISABLED)

        ent_passyear2_get.config(state=NORMAL)
        ent_passyear2_get.delete(0, END)
        ent_passyear2_get.insert(0, passyear_2)
        # ent_passyear2_get.config(state=DISABLED)

        ent_passyear3_get.config(state=NORMAL)
        ent_passyear3_get.delete(0, END)
        ent_passyear3_get.insert(0, passyear_3)
        # ent_passyear3_get.config(state=DISABLED)

        ent_passyear4_get.config(state=NORMAL)
        ent_passyear4_get.delete(0, END)
        ent_passyear4_get.insert(0, passyear_4)
        # ent_passyear4_get.config(state=DISABLED)

        ent_marks1_get.config(state=NORMAL)
        ent_marks1_get.delete(0, END)
        ent_marks1_get.insert(0, tm_1)
        # ent_marks1_get.config(state=DISABLED)

        ent_marks2_get.config(state=NORMAL)
        ent_marks2_get.delete(0, END)
        ent_marks2_get.insert(0, tm_2)
        # ent_marks2_get.config(state=DISABLED)

        ent_marks3_get.config(state=NORMAL)
        ent_marks3_get.delete(0, END)
        ent_marks3_get.insert(0, tm_3)
        # ent_marks3_get.config(state=DISABLED)

        ent_marks4_get.config(state=NORMAL)
        ent_marks4_get.delete(0, END)
        ent_marks4_get.insert(0, tm_4)
        # ent_marks4_get.config(state=DISABLED)

        ent_percentage1_get.config(state=NORMAL)
        ent_percentage1_get.delete(0, END)
        ent_percentage1_get.insert(0, percnt_1)
        # ent_percentage1_get.config(state=DISABLED)

        ent_percentage2_get.config(state=NORMAL)
        ent_percentage2_get.delete(0, END)
        ent_percentage2_get.insert(0, percnt_2)
        # ent_percentage2_get.config(state=DISABLED)

        ent_percentage3_get.config(state=NORMAL)
        ent_percentage3_get.delete(0, END)
        ent_percentage3_get.insert(0, percnt_3)
        # ent_percentage3_get.config(state=DISABLED)

        ent_percentage4_get.config(state=NORMAL)
        ent_percentage4_get.delete(0, END)
        ent_percentage4_get.insert(0, percnt_4)
        # ent_percentage4_get.config(state=DISABLED)

        ent_cgpa1_get.config(state=NORMAL)
        ent_cgpa1_get.delete(0, END)
        ent_cgpa1_get.insert(0, cgpa_1)
        # ent_cgpa1_get.config(state=DISABLED)

        ent_cgpa2_get.config(state=NORMAL)
        ent_cgpa2_get.delete(0, END)
        ent_cgpa2_get.insert(0, cgpa_2)
        # ent_cgpa2_get.config(state=DISABLED)

        ent_cgpa3_get.config(state=NORMAL)
        ent_cgpa3_get.delete(0, END)
        ent_cgpa3_get.insert(0, cgpa_3)
        # ent_cgpa3_get.config(state=DISABLED)

        ent_cgpa4_get.config(state=NORMAL)
        ent_cgpa4_get.delete(0, END)
        ent_cgpa4_get.insert(0, cgpa_4)
        # ent_cgpa4_get.config(state=DISABLED)


        cur.close()
        conn.close()

        # Image adding

        conn2 = sqlite3.connect("./databases_student/student_images.db")
        cur2 = conn2.cursor()

        cur2.execute(f"SELECT * FROM {ses_select} where email = (?)", (ent_selected_email.get(),))
        image_dat = cur2.fetchone()[1]
        conn2.commit()



        global photo_show

        with open("./img/temp.png", "wb") as f_obj:
            f_obj.write(image_dat)

        selected_image_show = Image.open("./img/temp.png")

        # Resizing image
        resized_show = selected_image_show.resize((130, 170), Image.ANTIALIAS)

        # new image
        photo_show = ImageTk.PhotoImage(resized_show)

        # Changing the image
        lbl_image_show.configure(image=photo_show)

        cur2.close()
        conn2.close()

        ent_selected_name.config(state=NORMAL)
        ent_selected_email.config(state=NORMAL)

        ent_selected_name.delete(0, END)
        ent_selected_email.delete(0, END)

        ent_selected_name.config(state=DISABLED)
        ent_selected_email.config(state=DISABLED)


        frame.tkraise()













#--------------------------------------------------------------------------
#---------Main Frame----------------------------------------------------
#--------------------------------------------------------------------------

frame_homepage_main = Frame(root, bg="white")
frame_homepage_main.place(x=0, y=0, relwidth=1, relheight = 1)


main_frame_homepage = Frame(frame_homepage_main, bg="black")
main_frame_homepage.place(x=0, y=0, relwidth =1 , relheight=1)

#-------Setting the background image in the window---------------------------------


bg_homepage = PhotoImage(file="./img/background_1.png")

lbl_background_image_homepage = Label(main_frame_homepage, image = bg_homepage)
lbl_background_image_homepage.place(x=0, y=0, relwidth =1 , relheight=1)

#--------------------Header-------------------------------------

# header frame
frame_header_homepage = Frame(main_frame_homepage, bg="#F0FFFF")
frame_header_homepage.place(x=0, y=0, height=100, relwidth=1)


lbl_college_details_name = Label(frame_header_homepage, text = "Krishnagar Government College", font = ("times", 25, "bold"), bg= "#F0FFFF")
lbl_college_details_name.place(x=50, y=10,)

lbl_college_details = Label(frame_header_homepage, text = "Krishnagar, Nadia.", font = ("times", 15, "bold"), bg= "#F0FFFF")
lbl_college_details.place(x=50, y=50)

#------------------------------Menu frame-----------------------------------

frame_black_homeapage = Frame(main_frame_homepage, bg="#262626")
frame_black_homeapage.place(x=0, y=100, height=30, relwidth=1)

# Button for admin login
btn_admin_login = Button(frame_black_homeapage, text = "Admin Login", bg="black", fg="white", font = ("meera", 11), bd=2, relief=RIDGE, command= lambda : swap(frame_admin_homepage))
btn_admin_login.pack(side = LEFT)

# Button for home
btn_admin_home = Button(frame_black_homeapage, text = "Home", bg="black", fg="white", font = ("meera", 11), bd=2, relief=RIDGE, command=lambda : swap(frame_department))
btn_admin_home.pack(side = LEFT, padx=5)



#----------------------------- Adding the college image-----------------------------

# Adding the frame
frame_college_img = Frame(main_frame_homepage, bg = "#B4CEFF")
frame_college_img.place(x=20, y=150, width=526, height=355)


clg_img = PhotoImage(file = "./img/college_image.png", master=main_frame_homepage)

lbl_clg_image = Label(frame_college_img, image = clg_img)
lbl_clg_image.place(x=5, y=5, width= 516, height=345)


# ---------------------------------------Homeapge 2nd Frame---------------------------------------

frame_department = Frame(main_frame_homepage, bg="#F0F8FF")
frame_department.place(x=600, y=150, height=400, width=500)


lbl_greeting = Label(frame_department, text = "Welcome to Krishnagar Govt. College", fg="#3B444B", bg="#F0F8FF", font=("times new roman", 20))
lbl_greeting.pack(pady=20)

lbl_department_name_homepage = Label(frame_department, text = "Physics Department", fg="#3B444B", bg="#F0F8FF", font=("times new roman", 18))
lbl_department_name_homepage.pack()

btn_students_zone = Button(frame_department, text = "Students' Zone",font=("Veranda", 18), bg="#36454F", fg="white", bd=1, relief=RAISED, activebackground= "#36454F", activeforeground="white", command= lambda : swap(frame_student_zone))
btn_students_zone.place(x=125, y=190, width=250)



# ============================2nd Window===============================================

frame_student_zone = Frame(main_frame_homepage, bg="#F0F8FF")
frame_student_zone.place(x=600, y=150, height=400, width=500)


lbl_student_homepage = Label(frame_student_zone, text = "Physics Department", fg="#3B444B", bg="#F0F8FF", font=("times new roman", 23))
lbl_student_homepage.pack(pady=20)



#Register button
btn_students_zone = Button(frame_student_zone, text = "Register",font=("meera", 12), bg="#301934", fg="white", bd=1, relief=RAISED, activebackground= "#301934", activeforeground="white",command = lambda : register(frame_register))
btn_students_zone.place(x=145, y=150, width=100, height=50)


#log in button
btn_students_zone = Button(frame_student_zone, text = "Log In",font=("meera", 12), bg="#301934", fg="white", bd=1, relief=RAISED, activebackground= "#301934", activeforeground="white", command= lambda : swap(frame_login_screen))
btn_students_zone.place(x=255, y=150, width=100, height=50)


#Previous page
btn_students_zone = Button(frame_student_zone, text = "Go Back",font=("meera", 12), bg="green", fg="white", bd=1, relief=RAISED, activebackground= "green", activeforeground="white", command= lambda : swap(frame_department))
btn_students_zone.pack(side=BOTTOM, pady=25)




#==========================3rd Window=====================================
frame_login_screen = Frame(main_frame_homepage, bg="#F0F8FF")
frame_login_screen.place(x=600, y=150, height=400, width=500)

#==========================Sign In Frame=======================================
# Label sign in
label_sign_in = Label(frame_login_screen, text="Log In", bg="#F0F8FF", font=("meera", 22))
label_sign_in.pack(pady=20)


# selecting session
lbl_session_si = Label(master=frame_login_screen, text="Session", font=("times", 13), bg="#F0F8FF")
lbl_session_si.place(x=75, y=100)

cmb_session_si = ttk.Combobox(
    master=frame_login_screen,
    values=(
        "Select",
        "2018-2019", "2019-2020", "2020-2021", "2022-2023", "2023-2024", "2024-2025", "2025-2026", "2026-2027",
        "2027-2028", "2028-2029", "2029-2030", "2030-2031", "2031-2032", "2032-2033", "2033-2034", "2034-2035",
        "2035-2024", "2036-2036", "2037-2038", "2038-2039", "2039-2040", "2040-2041", "2041-2042", "2042-2043",
    ),
    font=("times", 13),
    state="readonly",
    justify=CENTER,
    exportselection=0,
    # postcommand=select_session
)
cmb_session_si.place(x=175, y=100, width=150)
cmb_session_si.current(0)

# Sign In registration number
lbl_registration_si = Label(frame_login_screen, text="Registration Number", bg="#F0F8FF", font=("times", 13))
lbl_registration_si.place(x=75, y=150)

ent_registration_si = Entry(frame_login_screen, font=("times", 15), bg="whitesmoke", relief=SOLID, bd=1)
ent_registration_si.place(x=75, y=180, height=30, width=350)


# Sign In email
lbl_email_si = Label(frame_login_screen, text="Email Address", bg="#F0F8FF", font=("times", 13))
lbl_email_si.place(x=75, y=220)

ent_email_si = Entry(frame_login_screen, font=("times", 15), bg="whitesmoke", relief=SOLID, bd=1)
ent_email_si.place(x=75, y=250, height=30, width=350)

# sign in button
btn_sign_in = Button(frame_login_screen, text="Sign In", font=("times new roman", 14), anchor=CENTER, bg="#34495E",
                     fg="white", activebackground="#34495E", activeforeground="white", relief=FLAT, command= lambda : sign_in(student_personal_homepage_2))
btn_sign_in.place(x=75, y=300, height=40, width=350)

#------------------------------------------------------------------------------------------
#--------------------------------------------- showing the details---------------------------------------------
#------------------------------------------------------------------------------------------
student_personal_homepage_2 = Frame(frame_homepage_main, bg="white")
student_personal_homepage_2.place(x=0, y=0, relwidth =1 , relheight=1)


# print(ide,name, sex, category, religion, nationality, handicap, handicap_percentage, dob_txt, father_name, father_occ,
#             mother_name, mother_occ, guardian_name, rel_guardian, session, reg_no, student_id, course, contact, email,
#             guardian_contact, guardian_email, aadhaar, prmnt_address, prmnt_pincode, prsnt_address, prsnt_pincode, city,
#             district, state, country, last_instn, last_instn_add, hobby, exam_1, exam_2, exam_3, exam_4, board_1,
#             board_2, board_3, board_4, tm_1, tm_2, tm_3, tm_4, cgpa_1, cgpa_2, cgpa_3, cgpa_4, percnt_1, percnt_2,
#             percnt_3, percnt_4, passyear_1, passyear_2, passyear_3, passyear_4)


#----------------------------Tab----------------------------


tabControl_2 = ttk.Notebook(student_personal_homepage_2)

tab1_2 = Frame(tabControl_2, bg="#90caf9")
tabControl_2.add(tab1_2, text="Page-1")
tab2_2 = Frame(tabControl_2, bg="#90caf9")
tabControl_2.add(tab2_2, text="Page-2")



tabControl_2.place(x=20, y=20, width=1160, height=560)

# Adding details
#---------------------------tab1-----------------------------
#------------------------------------------1st Column----------------------------------------------
bg_bdy = "#90caf9"
# Name
Label(master=tab1_2, text="Full Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=10)
ent_name_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, state=DISABLED, disabledbackground="white", disabledforeground="black", cursor="arrow")
ent_name_get_2.place(x=10, y=40, height=30, width=350)

# Sex
Label(master=tab1_2, text="Sex", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=80, height=30)
lbl_sex_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_sex_get_2.place(x=210, y=80, height=30, width=150)

# Category
Label(master=tab1_2, text="Category", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=120)
lbl_cat_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_cat_get_2.place(x=210, y=120, height=30, width=150)


# Religion
Label(master=tab1_2, text="Religion", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=160)
lbl_religion_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_religion_get_2.place(x=210, y=160, height=30, width=150)


# Nationality
Label(master=tab1_2, text="Nationality", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=200)
lbl_nationality_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_nationality_get_2.place(x=210, y=200, height=30, width=150)

# Physically Handicapped
Label(master=tab1_2, text="Physically Handicapped?", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=240)
lbl_physical_handicap_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_physical_handicap_get_2.place(x=210, y=240, height=30, width=150)


# % of Disability
Label(master=tab1_2, text="% of Disability", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=280)
lbl_percntg_hc_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_percntg_hc_get_2.place(x=210, y=280, height=30, width=150)


# 	Date of Birth
Label(master=tab1_2, text="Date of Birth", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=320)
lbl_dob_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_dob_get_2.place(x=210, y=320, height=30, width=150)

# Country Name
Label(master=tab1_2, text="Country", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=360)
lbl_country_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_country_get_2.place(x=150, y=360, height=30, width=210)

# Aadhaar No.
Label(master=tab1_2, text="Aadhaar Number", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=400)

ent_aadhaar_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, state=DISABLED, disabledbackground="white", disabledforeground="black", cursor="arrow")
ent_aadhaar_get_2.place(x=10, y=430, height=30, width=350)


#----------------------1st tab 2nd column---------------------------------------------
# Father's Name
Label(master=tab1_2, text="Father's Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=10)

ent_father_name_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_father_name_get_2.place(x=400, y=40, height=30, width=320)


# 	Father's Occupation
Label(master=tab1_2, text="Father's Occupation", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=80)

ent_father_occu_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_father_occu_get_2.place(x=400, y=110, height=30, width=320)


# Mother's Name
Label(master=tab1_2, text="Mother's Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=150)

ent_mother_name_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_mother_name_get_2.place(x=400, y=180, height=30, width=320)

# 	Mother's Occupation
Label(master=tab1_2, text="Mother's Occupation", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=220)

ent_mother_occu_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_mother_occu_get_2.place(x=400, y=250, height=30, width=320)



# Guardian Name
Label(master=tab1_2, text="Guardian Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=290)

ent_guardian_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_guardian_get_2.place(x=400, y=320, height=30, width=320)



# Guardian Relation
Label(master=tab1_2, text="Relation with Guardian", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=360)

ent_guardian_rel_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_guardian_rel_get_2.place(x=400, y=390, height=30, width=320)


# Guardian Email Address
Label(master=tab1_2, text="Guardian's Email Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 400, y=430)

ent_g_email_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_g_email_get_2.place(x=400, y=460, height=30, width=320)


#---------------1st tab 3rd column----------------------
#Image frame
frame_student_image = Frame(tab1_2, bg="white", bd=1, relief=SOLID)
frame_student_image.place(x=1000, y=10, height=170, width=130)

# Adding Image
photo_show_2 = ImageTk.PhotoImage(file = "./img/ico.png")
lbl_image_show_2 = Label(frame_student_image, image = photo_show_2)
lbl_image_show_2.place(x=0, y=0, relwidth=1, relheight=1)



# Session
Label(master=tab1_2, text="Session", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=760, y=10)
lbl_session_get_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_session_get_2.place(x=860, y=10, height=30, width=120)

# Registration number
Label(master=tab1_2, text="Reg. No.", font=("Comic Sans MS", 13), bg=bg_bdy).place(x=760, y=50)

ent_registration_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_registration_get_2.place(x=760, y=80, width=220, height=30)


# Student Id
Label(master=tab1_2, text="Student Id", font=("Comic Sans MS", 13), bg=bg_bdy).place(x=760, y=120)

ent_student_id_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_student_id_get_2.place(x=760, y=150, width=220, height=30)


# Course
Label(master=tab1_2, text="Course", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=760, y=190)
lbl_get_course_2 = Label(tab1_2, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_get_course_2.place(x=860, y=190, height=30, width=120)

# Phone Number
Label(master=tab1_2, text="Contact Number", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 760, y=230)

ent_phone_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_phone_get_2.place(x=760, y=260, height=30, width=300)



# Email Address
Label(master=tab1_2, text="Email Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=760, y=300)

ent_email_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_email_get_2.place(x=760, y=330, height=30, width=300)


# Guardian Phone Number
Label(master=tab1_2, text="Guardian's Contact Number", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 760, y=370)

ent_g_phone_get_2 = Entry(master=tab1_2, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_g_phone_get_2.place(x=760, y=400, height=30, width=300)


# Button to datatable
btn_home_tab1_2 = Button(tab1_2, text="Back to Sign In", font=("times", 15), fg="white", bg="green", activebackground="green", activeforeground="white", command= lambda : swap(main_frame_homepage))
btn_home_tab1_2.place(x=760, y=460, height=50, width=300)


#----------------------------Tab2-------------------------------------------------

#---------------------------2nd tab 1st column
#Permanent Address
Label(master=tab2_2, text="Permanent Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=10)

text_prmnt_add_get_2 = Text(master=tab2_2, bg="white", font=("times", 12), bd=1, relief=SOLID, state=DISABLED, cursor="arrow")
text_prmnt_add_get_2.place(x=10, y=40, width=330, height=100)


# Pin Code
Label(master=tab2_2, text="Pincode", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=150)

ent_pincode_p_get_2 = Entry(master=tab2_2, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_pincode_p_get_2.place(x=10, y=180, height=30, width=230)


#Present Address
Label(master=tab2_2, text="Present Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=220)

text_prsnt_add_get_2 = Text(master=tab2_2, bg="white", font=("times", 12), bd=1, relief=SOLID, state=DISABLED, cursor="arrow")
text_prsnt_add_get_2.place(x=10, y=250, width=330, height=100)


# Pin Code
Label(master=tab2_2, text="Pincode", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=360)

ent_pincode_get_2 = Entry(master=tab2_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_pincode_get_2.place(x=10, y=390, height=30, width=230)



#--------------------2nd Tab 2nd column---------------------------
# City name
Label(master=tab2_2, text="City", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=360, y=10)

ent_city_get_2 = Entry(master=tab2_2, bg="white", font=("times", 13), bd=1, relief = SOLID,  disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_city_get_2.place(x=360, y=40, height=30, width=300)



# District Name
Label(master=tab2_2, text="District", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=360, y=80)

ent_district_get_2 = Entry(master=tab2_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_district_get_2.place(x=360, y=110, height=30, width=300)


# State Name
Label(master=tab2_2, text="State", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=360, y=150)

ent_state_get_2 = Entry(master=tab2_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_state_get_2.place(x=360, y=180, height=30, width=300)



#--------------------tab2 3rd column------------------------

# Last Institution
Label(master=tab2_2, text="Last Institution Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 700, y=10)

ent_last_instn_get_2 = Entry(master=tab2_2, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_last_instn_get_2.place(x=700, y=40, height=30, width=360)


# Last Institution Address
Label(master=tab2_2, text="Last Institution Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 700, y=80)

txt_last_instn_addrs_get_2 = Text(master=tab2_2, bg="white", font=("times", 12), bd=1, relief=SOLID, cursor="arrow")
txt_last_instn_addrs_get_2.place(x=700, y=110, width=360, height=60)


# Hobbies
Label(master=tab2_2, text="Hobbies", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 700, y=180)

txt_hobby_get_2 = Text(master=tab2_2,font=("times", 13), bg="white", bd=1, relief=SOLID, cursor="arrow")
txt_hobby_get_2.place(x=700, y=210, width=360, height=60)


# Frame for marks
frame_marks_get_2 = Frame(tab2_2, bg = "lightgray", bd=1, relief=SOLID, )
frame_marks_get_2.place(x=360, y=280, height=167, width=720)

# Titles

# Serial Number
Label(frame_marks_get_2, text="Sl.\nNo.", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=0, y=0, width=40, height=50)

# Exam name
Label(frame_marks_get_2, text="Exam Name", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=40, y=0, width=170, height=50)

# Board name
Label(frame_marks_get_2, text="Board Name", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=210, y=0, width=200, height=50)

# passing year
Label(frame_marks_get_2, text="Passing\nyear", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=410, y=0, width=70, height=50)

# Marks
Label(frame_marks_get_2, text="Total\nMarks", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=480, y=0, width=70, height=50)

# Percentage
Label(frame_marks_get_2, text="%", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=550, y=0, width=70, height=50)

# CGPA
Label(frame_marks_get_2, text="CGPA", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=620, y=0, width=99, height=50)

#-----------------------------------Data--------------------------------------------

# Serial Numbers
Label(frame_marks_get_2, text="1", font=("times", 13, "bold"),bd=1, relief=SOLID).place(x=-1, y=49, height=30, width=41)
Label(frame_marks_get_2, text="2", font=("times", 13, "bold"),bd=1, relief=SOLID).place(x=-1, y=78, height=30, width=41)
Label(frame_marks_get_2, text="3", font=("times", 13, "bold"),bd=1, relief=SOLID).place(x=-1, y=107, height=30, width=41)
Label(frame_marks_get_2, text="4", font=("times", 13, "bold"),bd=1, relief=SOLID).place(x=-1, y=136, height=30, width=41)



# Exam Names

ent_exam1_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_exam1_get_2.place(x=39, y=49, height=30, width=171)

ent_exam2_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_exam2_get_2.place(x=39, y=78, height=30, width=171)

ent_exam3_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_exam3_get_2.place(x=39, y=107, height=30, width=171)

ent_exam4_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_exam4_get_2.place(x=39, y=136, height=30, width=171)


# Board Names
ent_board1_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_board1_get_2.place(x=209, y=49, height=30, width=201)

ent_board2_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_board2_get_2.place(x=209, y=78, height=30, width=201)

ent_board3_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_board3_get_2.place(x=209, y=107, height=30, width=201)

ent_board4_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_board4_get_2.place(x=209, y=136, height=30, width=201)

# Passing Years
ent_passyear1_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_passyear1_get_2.place(x=409, y=49, height=30, width=71)

ent_passyear2_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_passyear2_get_2.place(x=409, y=78, height=30, width=71)

ent_passyear3_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_passyear3_get_2.place(x=409, y=107, height=30, width=71)

ent_passyear4_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_passyear4_get_2.place(x=409, y=136, height=30, width=71)


# Total Marks
ent_marks1_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_marks1_get_2.place(x=479, y=49, height=30, width=71)

ent_marks2_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_marks2_get_2.place(x=479, y=78, height=30, width=71)

ent_marks3_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_marks3_get_2.place(x=479, y=107, height=30, width=71)

ent_marks4_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_marks4_get_2.place(x=479, y=136, height=30, width=71)

# Percentage
ent_percentage1_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_percentage1_get_2.place(x=549, y=49, height=30, width=71)

ent_percentage2_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_percentage2_get_2.place(x=549, y=78, height=30, width=71)

ent_percentage3_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_percentage3_get_2.place(x=549, y=107, height=30, width=71)

ent_percentage4_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_percentage4_get_2.place(x=549, y=136, height=30, width=71)



# Cgpa
ent_cgpa1_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_cgpa1_get_2.place(x=619, y=49, height=30, width=100)

ent_cgpa2_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_cgpa2_get_2.place(x=619, y=78, height=30, width=100)

ent_cgpa3_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_cgpa3_get_2.place(x=619, y=107, height=30, width=100)

ent_cgpa4_get_2 = Entry(frame_marks_get_2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_cgpa4_get_2.place(x=619, y=136, height=30, width=100)


# Button
btn_home_tab2_2 = Button(tab2_2, text="Back to Sign In", font=("times", 15), fg="white", bg="green", activebackground="green", activeforeground="white", command= lambda : swap(main_frame_homepage))
btn_home_tab2_2.place(x=760, y=460, height=50, width=300)


main_frame_homepage.tkraise()
#------------------------------------------------------------------------------------------
#--------------------------------------------- showing ends---------------------------------------------
#------------------------------------------------------------------------------------------




# sign up button
lbl_sign_up = Label(frame_login_screen, text="Not a member?", font=("times new roman", 10), bg="#F0F8FF", fg="black")
lbl_sign_up.place(x=180, y=370, width=90, height=20)

btn_sign_up = Button(frame_login_screen, text="Sign Up", font=("times new roman", 10), anchor=CENTER, bg="#34495E",
                     fg="white", activebackground="#34495E", activeforeground="white", relief=FLAT, command= lambda : register(frame_register))
btn_sign_up.place(x=270, y=370, width=50, height=20)
frame_department.tkraise()

#---------------------------------------Register Window--------------------------------------------
frame_register = Frame(frame_homepage_main, bg="white")


#=========================Header======================================

# Adding a frame
frame_header = Frame(frame_register, bg="blue")
frame_header.place(x=0, y=0, relwidth=1, height=90)

# Adding contents in the header
lbl_college_name = Label(frame_header, text="Krishnagar Government College", font=("times new roman", 30, "bold"), bg="blue", fg="white")
lbl_college_name.pack()

lbl_department_name = Label(frame_header, text="Physics Department", font=("times new roman", 25, "bold"), bg="blue", fg="white")
lbl_department_name.pack()


#=========================Body========================================
bg_bdy = "white"
# Adding the frame
frame_body = LabelFrame(frame_register, bg=bg_bdy, text="1/3")
frame_body.place(x=0, y=90, relwidth=1, height=485)

# Adding contents in the body
lbl_title = Label(master=frame_body, text="Register as a New Student", bg=bg_bdy, fg="red", font=("Verdana", 19, "bold"))
lbl_title.place(x=400, y=10, width=400)


#------------------------------------------1st Column----------------------------------------------
# Name
lbl_name = Label(master=frame_body, text="Full Name", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_name.place(x=50, y=70)

ent_name = Entry(master=frame_body, bg="whitesmoke", font=("times", 13), bd=1, relief = SOLID)
ent_name.place(x=50, y=100, height=30, width=350)

# Sex
lbl_sex = Label(master=frame_body, text="Sex", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_sex.place(x=50, y=145)

cmb_sex = ttk.Combobox(master=frame_body, values=("Select", "Male", "Female", "TG"), font=("times", 13), state="readonly", justify=CENTER)
cmb_sex.place(x=250, y=145, width=150)
cmb_sex.current(0)

# Category
lbl_category = Label(master=frame_body, text="Category", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_category.place(x=50, y=190)

cmb_category = ttk.Combobox(master=frame_body, values=("Select", "GENERAL", "SC", "ST", "OBC-A", "OBC-B"), font=("times", 13), state="readonly", justify=CENTER)
cmb_category.place(x=250, y=190, width=150)
cmb_category.current(0)

# Religion
lbl_religion = Label(master=frame_body, text="Religion", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_religion.place(x=50, y=235)

cmb_religion = ttk.Combobox(master=frame_body, values=("Select", "Christianity", "Hinduism", "Islam","Humanity", "Others"), font=("times", 13), state="readonly", justify=CENTER)
cmb_religion.place(x=250, y=235, width=150)
cmb_religion.current(0)

# Nationality
lbl_nationality = Label(master=frame_body, text="Nationality", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_nationality.place(x=50, y=280)

cmb_nationality = ttk.Combobox(master=frame_body, values=("Select", "Indian", "Others"), font=("times", 13), state="readonly", justify=CENTER)
cmb_nationality.place(x=250, y=280, width=150)
cmb_nationality.current(0)

# Physically Handicapped
lbl_ph = Label(master=frame_body, text="Physically Handicapped", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_ph.place(x=50, y=325)

ph = StringVar()

radio_ph_yes = Radiobutton(master=frame_body,text="Yes", value="yes", variable = ph, font=("times", 13), bg= bg_bdy, command = enable_ph)
radio_ph_yes.place(x=250, y=325,width=75)

radio_ph_no = Radiobutton(master=frame_body,text="No", value="no", variable = ph, font=("times", 13), bg= bg_bdy, command = enable_ph)
radio_ph_no.place(x=325, y=325, width=75)

ph.set("no")

# 	% of Disability
lbl_per_ph = Label(master=frame_body, text="% of Disability", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_per_ph.place(x=50, y=370)

ent_per_ph = Entry(master=frame_body, bg="whitesmoke", font=("times", 13), bd=1, relief = SOLID, state=DISABLED, disabledbackground = "#2C3E50")
ent_per_ph.place(x=250, y=370, width=150, height=30)




#------------------------------------1sr Column Ends Here--------------------------------------------------


#------------------------------------2nd Column-------------------------------------------------------

# 	Date of Birth
lbl_dob = Label(master=frame_body, text="Date of Birth", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_dob.place(x=450, y=70)

cal = DateEntry(frame_body, background='darkblue',foreground='white', borderwidth=2, font=("", 13), state="readonly")
cal.place(x=570, y=70, width=200, height=30)

# Father's Name
lbl_father_name = Label(master=frame_body, text="Father's Name", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_father_name.place(x=450, y=115)

ent_father_name = Entry(master=frame_body, bg="whitesmoke", font=("times", 13), bd=1, relief = SOLID)
ent_father_name.place(x=450, y=145, height=30, width=320)

# 	Father's Occupation
lbl_father_occu = Label(master=frame_body, text="Father's Occupation", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_father_occu.place(x=450, y=190)

ent_father_occu = Entry(master=frame_body, bg="whitesmoke", font=("times", 13), bd=1, relief = SOLID)
ent_father_occu.place(x=450, y=220, height=30, width=320)

# Mother's Name
lbl_mother_name = Label(master=frame_body, text="Mother's Name", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_mother_name.place(x=450, y=265)

ent_mother_name = Entry(master=frame_body, bg="whitesmoke", font=("times", 13), bd=1, relief = SOLID)
ent_mother_name.place(x=450, y=295, height=30, width=320)

# 	Mother's Occupation
lbl_mother_occu = Label(master=frame_body, text="Mother's Occupation", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_mother_occu.place(x=450, y=340)

ent_mother_occu = Entry(master=frame_body, bg="whitesmoke", font=("times", 13), bd=1, relief = SOLID)
ent_mother_occu.place(x=450, y=370, height=30, width=320)

#-------------------------------------3rd Column-----------------------------------------

# Guardian Name
lbl_guardian = Label(master=frame_body, text="Guardian Name", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_guardian.place(x=820, y=70)

ent_guardian = Entry(master=frame_body, font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_guardian.place(x=820, y=100, height=30, width=330)


# Guardian Relation
lbl_guardian_rel = Label(master=frame_body, text="Relation with Guardian", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_guardian_rel.place(x=820, y=145)

ent_guardian_rel = Entry(master=frame_body, font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_guardian_rel.place(x=820, y=175, height=30, width=330)


# Session
lbl_session = Label(master=frame_body, text="Session", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_session.place(x=820, y=220)

cmb_session = ttk.Combobox(
    master=frame_body,
    values=(
        "Select",
        "2018-2019","2019-2020","2020-2021","2022-2023", "2023-2024", "2024-2025", "2025-2026", "2026-2027", "2027-2028", "2028-2029", "2029-2030", "2030-2031","2031-2032", "2032-2033", "2033-2034", "2034-2035", "2035-2024", "2036-2036", "2037-2038", "2038-2039", "2039-2040", "2040-2041", "2041-2042", "2042-2043",
    ),
    font=("times", 13),
    state="readonly",
    justify=CENTER,
)
cmb_session.place(x=1000, y=220, width=150)
cmb_session.current(0)

# Registration Number
lbl_registrarion = Label(master=frame_body, text="Reg. No.", font=("Comic Sans MS", 13), bg=bg_bdy)
lbl_registrarion.place(x=820, y=265)

ent_registration = Entry(master=frame_body, font=("times", 13), bg=bg_bdy, bd=1, relief=SOLID)
ent_registration.place(x=950, y=265, width=200, height=30)


# Student Id
lbl_student_id = Label(master=frame_body, text="Student Id", font=("Comic Sans MS", 13), bg=bg_bdy)
lbl_student_id.place(x=820, y=310)

ent_student_id = Entry(master=frame_body, font=("times", 13), bg=bg_bdy, bd=1, relief=SOLID)
ent_student_id.place(x=950, y=310, width=200, height=30)

# Course
lbl_course = Label(master=frame_body, text="Course", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_course.place(x=820, y=355)

cmb_course = ttk.Combobox(master=frame_body, values=("Select", "HONOURS", "GENERAL"), font=("times", 13), state="readonly", justify=CENTER)
cmb_course.place(x=1000, y=355, width=150)
cmb_course.current(0)



#homebutton
btn_register_to_home =  Button(master=frame_body, text = "Back", font = ("Comic Sans MS", 13), bg="green", fg="white", command= lambda : swap(main_frame_homepage))
btn_register_to_home.place(x=940, y=400, height=40, width=100)
# Next page button
btn_next_1 = Button(master=frame_body, text = "Next Page", font = ("Comic Sans MS", 13), bg="green", fg="white", command= lambda : next_page_1(frame2_body) )
btn_next_1.place(x = 1050, y = 400, height=40, width=100)

#=========================================2nd Frame===============================================
# Adding the frame
frame2_body = LabelFrame(frame_register, bg=bg_bdy, text="2/3")
frame2_body.place(x=0, y=90, relwidth=1, height=485)


# Adding contents

#-------------------------------------1st Column-------------------------------------------------

# Phone Number
lbl_phone = Label(master=frame2_body, text="Contact Number *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_phone.place(x = 50, y=30)

ent_phone = Entry(master=frame2_body,font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_phone.place(x=50, y=60, height=30, width=300)

# Email Address
lbl_email = Label(master=frame2_body, text="Email Address *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_email.place(x = 50, y=105)

ent_email = Entry(master=frame2_body,font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_email.place(x=50, y=135, height=30, width=300)

# Guardian Phone Number
lbl_g_phone = Label(master=frame2_body, text="Guardian's Contact Number *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_g_phone.place(x = 50, y=180)

ent_g_phone = Entry(master=frame2_body,font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_g_phone.place(x=50, y=210, height=30, width=300)

# Email Address
lbl_g_email = Label(master=frame2_body, text="Guardian's Email Address", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_g_email.place(x = 50, y=255)

ent_g_email = Entry(master=frame2_body,font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_g_email.place(x=50, y=285, height=30, width=300)

# Aadhaar No.
lbl_aadhaar = Label(master=frame2_body, text="Aadhaar Number *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_aadhaar.place(x=50, y=330)

ent_aadhaar = Entry(master=frame2_body, font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_aadhaar.place(x=50, y=360, height=30, width=300)

#----------------------------------2nd Column----------------------------------------------------------

# Permanent Address
lbl_prmnt_add = Label(master=frame2_body, text="Permanent Address *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_prmnt_add.place(x=400, y=30)

text_prmnt_add = Text(master=frame2_body, bg="whitesmoke", font=("times", 12), bd=1, relief=SOLID)
text_prmnt_add.place(x=400, y=60, width=330, height=60)

# Pin Code
lbl_pincode_p = Label(master=frame2_body, text="Pincode *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_pincode_p.place(x=400, y=140)

ent_pincode_p = Entry(master=frame2_body, bg="whitesmoke", font=("times", 13), bd=1, relief = SOLID)
ent_pincode_p.place(x=500, y=140, height=30, width=230)


# Checking if the two address are same
lbl_same_address = Label(master=frame2_body, text="Is your Present Address same as Permanent Address?", font=("times", 12), bg=bg_bdy, fg="blue")
lbl_same_address.place(x=400, y=185)


same_add = StringVar()

radio_same_yes = Radiobutton(master=frame2_body,text="Yes", value="yes", variable = same_add, font=("times", 13), bg= bg_bdy, command = disable_add)
radio_same_yes.place(x=400, y=215,width=75)

radio_same_no = Radiobutton(master=frame2_body,text="No", value="no", variable = same_add, font=("times", 13), bg= bg_bdy, command = disable_add)
radio_same_no.place(x=500, y=215, width=75)

same_add.set("no")


# Present Address
lbl_prsnt_add = Label(master=frame2_body, text="Present Address *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_prsnt_add.place(x=400, y=250)

text_prsnt_add = Text(master=frame2_body, bg="whitesmoke", font=("times", 12), bd=1, relief=SOLID)
text_prsnt_add.place(x=400, y=280, width=330, height=60)

# Pin Code
lbl_pincode = Label(master=frame2_body, text="Pincode *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_pincode.place(x=400, y=360)

ent_pincode = Entry(master=frame2_body, bg="whitesmoke", font=("times", 13), bd=1, relief = SOLID, disabledbackground = "#2C3E50")
ent_pincode.place(x=500, y=360, height=30, width=230)



#----------------------------------------3rd Column-----------------------------------------------
# City name
lbl_city = Label(master=frame2_body, text="City *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_city.place(x=780, y=30)

ent_city = Entry(master=frame2_body, font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_city.place(x=780, y=60, height=30, width=300)


# District Name
lbl_district = Label(master=frame2_body, text="District *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_district.place(x=780, y=105)

ent_district = Entry(master=frame2_body, font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_district.place(x=780, y=135, height=30, width=300)

# State Name
lbl_state = Label(master=frame2_body, text="State *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_state.place(x=780, y=180)

ent_state = Entry(master=frame2_body, font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_state.place(x=780, y=210, height=30, width=300)

# Country Name
lbl_country = Label(master=frame2_body, text="Country", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_country.place(x=780, y=255)

ent_country = Entry(master=frame2_body, font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_country.place(x=780, y=285, height=30, width=300)




# Previous page button
btn_previous_1 = Button(master=frame2_body, text = "Previous Page", font = ("Comic Sans MS", 13), bg="green", fg="white", command= lambda : swap(frame_body))
btn_previous_1.place(x = 920, y = 400, height=40, width=120)


# Next page button
btn_next_2 = Button(master=frame2_body, text = "Next Page", font = ("Comic Sans MS", 13), bg="green", fg="white", command= lambda : next_page_2(frame3_body))
btn_next_2.place(x = 1050, y = 400, height=40, width=100)


#=========================================3rd Frame===============================================
# Adding the frame
frame3_body = LabelFrame(frame_register, bg=bg_bdy, text="3/3")
frame3_body.place(x=0, y=90, relwidth=1, height=485)

# Adding Contents

#------------------------------------------1st Column--------------------------------------------

# Last Institution
lbl_last_instn = Label(master=frame3_body, text="Last Institution Name *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_last_instn.place(x = 50, y=30)

ent_last_instn = Entry(master=frame3_body,font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
ent_last_instn.place(x=50, y=60, height=30, width=330)

# Last Institution Address
lbl_last_instn_addrs = Label(master=frame3_body, text="Last Institution Address *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_last_instn_addrs.place(x = 50, y=105)

txt_last_instn_addrs = Text(master=frame3_body, bg="whitesmoke", font=("times", 12), bd=1, relief=SOLID)
txt_last_instn_addrs.place(x=50, y=135, width=330, height=60)

# Hobbies
lbl_hobby = Label(master=frame3_body, text="Hobbies *", font=("Comic Sans MS", 13), bg= bg_bdy)
lbl_hobby.place(x = 50, y=210)

txt_hobby = Text(master=frame3_body,font=("times", 13), bg="whitesmoke", bd=1, relief=SOLID)
txt_hobby.place(x=50, y=240, width=330, height=60)




#----------------------------- Another Frame for creating the table----------------------------------------

frame_marks = Frame(frame3_body, bg = "lightgray", bd=1, relief=SOLID, )
frame_marks.place(x=410, y=30, height=167, width=720)

# Adding widgets into this frame


# Titles

# Serial Number
lbl_slno = Label(frame_marks, text="Sl.\nNo.", font=("times", 13, "bold"), bd=1, relief=RAISED)
lbl_slno.place(x=0, y=0, width=40, height=50)



# Exam name
lbl_exam_name = Label(frame_marks, text="Exam Name", font=("times", 13, "bold"), bd=1, relief=RAISED)
lbl_exam_name.place(x=40, y=0, width=170, height=50)

# Board name
lbl_board_name = Label(frame_marks, text="Board Name", font=("times", 13, "bold"), bd=1, relief=RAISED)
lbl_board_name.place(x=210, y=0, width=200, height=50)

# passing year
lbl_passing_year = Label(frame_marks, text="Passing\nyear", font=("times", 13, "bold"), bd=1, relief=RAISED)
lbl_passing_year.place(x=410, y=0, width=70, height=50)

# Marks
lbl_marks = Label(frame_marks, text="Total\nMarks", font=("times", 13, "bold"), bd=1, relief=RAISED)
lbl_marks.place(x=480, y=0, width=70, height=50)


# Percentage
lbl_percentage = Label(frame_marks, text="%", font=("times", 13, "bold"), bd=1, relief=RAISED)
lbl_percentage.place(x=550, y=0, width=70, height=50)


# CGPA
lbl_cgpa = Label(frame_marks, text="CGPA", font=("times", 13, "bold"), bd=1, relief=RAISED)
lbl_cgpa.place(x=620, y=0, width=99, height=50)

#-----------------------------------Data--------------------------------------------

# Serial Numbers
lbl_slno1 = Label(frame_marks, text="1", font=("times", 13, "bold"),bd=1, relief=SOLID)
lbl_slno1.place(x=-1, y=49, height=30, width=41)




lbl_slno2 = Label(frame_marks, text="2", font=("times", 13, "bold"),bd=1, relief=SOLID)
lbl_slno2.place(x=-1, y=78, height=30, width=41)

lbl_slno3 = Label(frame_marks, text="3", font=("times", 13, "bold"),bd=1, relief=SOLID)
lbl_slno3.place(x=-1, y=107, height=30, width=41)

lbl_slno4 = Label(frame_marks, text="4", font=("times", 13, "bold"),bd=1, relief=SOLID)
lbl_slno4.place(x=-1, y=136, height=30, width=41)




# 1st row
ent_exam1 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_exam1.place(x=39, y=49, height=30, width=171)

ent_board1 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_board1.place(x=209, y=49, height=30, width=201)

ent_passyear1 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_passyear1.place(x=409, y=49, height=30, width=71)

ent_marks1 = Entry(frame_marks, font=("times", 13), bd=1, relief=SOLID)
ent_marks1.place(x=479, y=49, height=30, width=71)

ent_percentage1 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_percentage1.place(x=549, y=49, height=30, width=71)

ent_cgpa1 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_cgpa1.place(x=619, y=49, height=30, width=100)




# 2nd Row
ent_exam2 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_exam2.place(x=39, y=78, height=30, width=171)

ent_board2 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_board2.place(x=209, y=78, height=30, width=201)

ent_passyear2 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_passyear2.place(x=409, y=78, height=30, width=71)

ent_marks2 = Entry(frame_marks, font=("times", 13), bd=1, relief=SOLID)
ent_marks2.place(x=479, y=78, height=30, width=71)

ent_percentage2 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_percentage2.place(x=549, y=78, height=30, width=71)

ent_cgpa2 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_cgpa2.place(x=619, y=78, height=30, width=100)


# 3rd Row
ent_exam3 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_exam3.place(x=39, y=107, height=30, width=171)

ent_board3 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_board3.place(x=209, y=107, height=30, width=201)

ent_passyear3 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_passyear3.place(x=409, y=107, height=30, width=71)

ent_marks3 = Entry(frame_marks, font=("times", 13), bd=1, relief=SOLID)
ent_marks3.place(x=479, y=107, height=30, width=71)

ent_percentage3 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_percentage3.place(x=549, y=107, height=30, width=71)

ent_cgpa3 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_cgpa3.place(x=619, y=107, height=30, width=100)



# 4th Row
ent_exam4 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_exam4.place(x=39, y=136, height=30, width=171)

ent_board4 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_board4.place(x=209, y=136, height=30, width=201)

ent_passyear4 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_passyear4.place(x=409, y=136, height=30, width=71)

ent_marks4 = Entry(frame_marks, font=("times", 13), bd=1, relief=SOLID)
ent_marks4.place(x=479, y=136, height=30, width=71)

ent_percentage4 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_percentage4.place(x=549, y=136, height=30, width=71)

ent_cgpa4 = Entry(frame_marks, font=("times",13),bd=1, relief=SOLID)
ent_cgpa4.place(x=619, y=136, height=30, width=100)



#----------------------------------Image Frame-------------------------------------

frame_image = Frame(frame3_body, bg="gray", bd=3, relief=RAISED)
frame_image.place(x=410, y=230, height=200, width=170)

# Adding Image
lbl_image = Label(frame_image, text="Your Image")
lbl_image.place(x=0, y=0, relwidth=1, relheight=1)



# Choose Photo Button
btn_image = Button(frame3_body, text="Upload Image",font=("times", 15), bg="black", fg="white", command=upload_image)
btn_image.place(x=650, y=230, height=40, width=200)

#Image file name
lbl_image_name = Label(frame3_body,text="", bg=bg_bdy, fg="red", font=("meera", 11) ,bd=1, relief = FLAT, anchor=W)
lbl_image_name.place(x=650, y=295, width=480, height=20)


# Previous page button
btn_previous_2 = Button(master=frame3_body, text = "Previous Page", font = ("Comic Sans MS", 13), bg="green", fg="white", command= lambda : swap(frame2_body))
btn_previous_2.place(x = 920, y = 400, height=40, width=120)

# Submit page button
btn_next_3 = Button(master=frame3_body, text = "Submit", font = ("Comic Sans MS", 13), bg="green", fg="white", command= submit)
btn_next_3.place(x = 1050, y = 400, height=40, width=100)

#=========================Status Bar========================================

# Adding the frame
frame_status_bar = Frame(frame_register, bd=2, relief=SUNKEN, bg="whitesmoke")
frame_status_bar.place(x=0, y=575, relwidth=1, height=25)

# Adding contents in the status bar

#----------------------------1st Column--------------------------------------------------



Label(frame_status_bar, text=f"{tdy}", fg="black", bg="whitesmoke",).pack(side=LEFT)
Label(frame_status_bar, text="Developed by Subhranil Sarkar", fg="black", bg="whitesmoke", ).pack(side=RIGHT)



#========================================================================================
#==================================REGISTRATION WINDOW============================================
#========================================================================================



# Showing the first frame at the first time
frame_department.tkraise()
main_frame_homepage.tkraise()
frame_register.place(x=0, y=0, relwidth=1, relheight=1)
frame_body.tkraise()





#---------------------------------------Ends Register Window--------------------------------------------


# Adding the status frame
frame_status_bar_homepage = Frame(main_frame_homepage, bd=2, relief=SUNKEN, bg="whitesmoke")
frame_status_bar_homepage.place(x=0, y=575, relwidth=1, height=25)

# Adding contents in the status bar

Label(frame_status_bar_homepage, text=f"{tdy}", fg="black", bg="whitesmoke", ).pack(side=LEFT)
Label(frame_status_bar_homepage, text="Developed by Subhranil Sarkar", fg="black", bg="whitesmoke", ).pack(side=RIGHT)






# showing the first frame when opened


#----------------------------------------------------------------------------------------------------------------








#-------------------------------Admin Window------------------------------------------------

frame_admin_homepage = Frame(frame_homepage_main, bg="white")
frame_admin_homepage.place(x=0, y=0, relwidth =1 , relheight=1)


#------------------------------ Password Frame ----------------------------
frame_admin_password_window = Frame(frame_admin_homepage, bg="lightblue")
frame_admin_password_window.place(x=0, y=0, relwidth =1 , relheight=1)

# contents
frame_admin_password = Frame(frame_admin_password_window, bg = "white")
frame_admin_password.place(x=405, y=100, height=400, width=390)

label_password_admin = Label(frame_admin_password, text= "Password", bg="white", font=("meera", 25))
label_password_admin.pack(pady=50)

ent_admin_password = Entry(frame_admin_password, font = ("meera", 18), bg="whitesmoke", show="*")
ent_admin_password.place(x=70, y=130, width=250, height=30)

btn_admin_pass_login = Button(frame_admin_password, text= "Log In", bg="#CC0000", fg="white", font=("meera", 17), activebackground="#CC0000", activeforeground="white", command = lambda : check_pass(frame_admin_panel))
btn_admin_pass_login.place(x=195, y=200, width=100, height=50)

btn_back_homepage = Button(frame_admin_password, text= "Back", bg="#CC0000", fg="white", font=("meera", 17), activebackground="#CC0000", activeforeground="white", command = lambda : swap(main_frame_homepage))
btn_back_homepage.place(x=95, y=200, width=100, height=50)


#=========================Administrator Panel=====================================
frame_admin_panel = Frame(frame_admin_homepage, bg="crimson")
frame_admin_panel.place(x=0, y=0, relheight=1, relwidth=1)

# Session
lbl_select_session = Label(frame_admin_panel, text = "Select Session", font=("times", 15), bg="crimson", fg="white")
lbl_select_session.place(x=20, y=10, height=30, width=150)

cmb_select_session = ttk.Combobox(
    master=frame_admin_panel,
    values=(
        "Select",
        "2018-2019", "2019-2020", "2020-2021", "2022-2023", "2023-2024", "2024-2025", "2025-2026",
        "2026-2027",
        "2027-2028", "2028-2029", "2029-2030", "2030-2031", "2031-2032", "2032-2033", "2033-2034",
        "2034-2035",
        "2035-2024", "2036-2036", "2037-2038", "2038-2039", "2039-2040", "2040-2041", "2041-2042",
        "2042-2043",
    ),
    font=("times", 13),
    state="readonly",
    justify=CENTER,
    exportselection=0,
    # postcommand=select_session
)
cmb_select_session.place(x=170, y=10, width=150, height=30)
cmb_select_session.current(0)

btn_show_data_table = Button(frame_admin_panel, text="Show Students", font=("times", 15), fg="white", bg="black", command=show_table)
btn_show_data_table.place(x=340, y=10, height=30, width=150)

btn_backtohome = Button(frame_admin_panel, text="Home", font=("times", 15), fg="white", bg="black", command=lambda : gotohome(main_frame_homepage))
btn_backtohome.place(x=1090, y=10, height=30, width=90)

# --------------------- Datatable Frame---------------------
frame_data_table = Frame(frame_admin_panel, bg="white")
frame_data_table.place(x=20, y=50, width=1160, height=350)

# Adding the table
scroll_x = Scrollbar(frame_data_table, orient=HORIZONTAL)
scroll_y = Scrollbar(frame_data_table, orient=VERTICAL)

student_table = ttk.Treeview(
    master=frame_data_table,
    columns = ("id", "fullname", "sex", "category", "religion", "nationality", "handicapped",
               "percentageHandicap", "dob", "fatherName", "fatherOccu", "motherName", "motherOccu",
               "guardianName", "relGuardian", "session", "regNo", "studentId", "course",  "contact",
               "email", "guardian_contact", "guardian_email", "aadhaar", "prmnt_address",
               "prmnt_pincode", "prsnt_address", "prsnt_pincode", "city", "district", "state",
               "country", "last_instn", "last_instn_add", "hobby", "exam_1", "exam_2", "exam_3",
               "exam_4", "board_1", "board_2", "board_3", "board_4", "tm_1", "tm_2", "tm_3", "tm_4",
               "cgpa_1", "cgpa_2", "cgpa_3", "cgpa_4", "percnt_1", "percnt_2", "percnt_3",
               "percnt_4", "passyear_1", "passyear_2", "passyear_3", "passyear_4"
               ),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set,
    selectmode = "browse"

)

# Adding the scrollbar
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)

# Table headings
student_table.heading("id", text="Id")                                  # id
student_table.heading("fullname", text="Full Name")                     # name
student_table.heading("sex", text="Sex")                                # sex
student_table.heading("category", text="Category")                      # category
student_table.heading("religion", text="Religion")                      # religion
student_table.heading("nationality", text="Nationality")                # nationality
student_table.heading("handicapped", text="Handicapped")                # handicapped
student_table.heading("percentageHandicap", text="PercentageHandicap")  # % handicap
student_table.heading("dob", text="D.O.B")                              # dob
student_table.heading("fatherName", text="Father's Name")               # father's name
student_table.heading("fatherOccu", text="Father's Occupation")         # Father's occupation
student_table.heading("motherName", text="Mother's Name")               # mother's name
student_table.heading("motherOccu", text="Mother's Occupation")         # mother's occupation
student_table.heading("guardianName", text="Guardian Name")             # guardian name
student_table.heading("relGuardian", text="Relation with Guardian")     # rel guardian
student_table.heading("session",text="Session")                         # session
student_table.heading("regNo", text="Registration Number")              # registration numbe
student_table.heading("studentId",text="Student Id")                    # student id
student_table.heading("course",text="Course")                           # course
student_table.heading("contact",text="Contact Number")                  # contact no.
student_table.heading("email",text="Email")                             # email
student_table.heading("guardian_contact", text="Guardian Contact Number")   # guardian no.
student_table.heading("guardian_email", text="Guardian Email")              # guardian email
student_table.heading("aadhaar", text="Aadhaar Number")                     # aadhaar number
student_table.heading("prmnt_address",text="Permanent Address")             # prmnt address
student_table.heading("prmnt_pincode", text="Permanent Pincode")            # prmnt pincode
student_table.heading("prsnt_address", text="Present Address")              # prsnt address
student_table.heading("prsnt_pincode", text="Present Pincode")              # prstn pincode
student_table.heading("city", text="City")                                  # city
student_table.heading("district", text="District")                          # district
student_table.heading("state",text="State")                                 # state
student_table.heading("country", text="Country")                            # country
student_table.heading("last_instn",text="Last Institution")                 # last instn
student_table.heading("last_instn_add",text="Last Institution Address")     # last instn address
student_table.heading("hobby",text="Hobbies")                               # hobbies
student_table.heading("exam_1",text="Exam 1")
student_table.heading("exam_2",text="Exam 2")
student_table.heading("exam_3",text="Exam 3")
student_table.heading("exam_4",text="Exam 4")
student_table.heading("board_1",text="Board 1")
student_table.heading("board_2",text="Board 2")
student_table.heading("board_3",text="Board 3")
student_table.heading("board_4",text="Board 4")
student_table.heading("tm_1",text="Total Marks 1")
student_table.heading("tm_2",text="Total Marks 2")
student_table.heading("tm_3",text="Total Marks 3")
student_table.heading("tm_4",text="Total Marks 4")
student_table.heading("cgpa_1",text="CGPA 1")
student_table.heading("cgpa_2",text="CGPA 2")
student_table.heading("cgpa_3",text="CGPA 3")
student_table.heading("cgpa_4",text="CGPA 4")
student_table.heading("percnt_1",text="Percentage 1")
student_table.heading("percnt_2",text="Percentage 2")
student_table.heading("percnt_3",text="Percentage 3")
student_table.heading("percnt_4",text="Percentage 4")
student_table.heading("passyear_1",text="Pass Year 1")
student_table.heading("passyear_2",text="Pass Year 2")
student_table.heading("passyear_3",text="Pass Year 3")
student_table.heading("passyear_4",text="Pass Year 4")
# student_table.heading("image", text="Image Binary")


# for not showing the index
student_table["show"] = "headings"

# size
student_table.column("id", width=15)
student_table.column("sex", width=60)

student_table.pack(fill=BOTH, expand=1)
student_table.bind("<ButtonRelease-1>", get_cursor)







#----------------------------- Admin control buttons frame---------------------------------------
frame_admin_control = Frame(frame_admin_panel, bg="white")
frame_admin_control.place(x=20, y=420, width=1160, height=160)


# title
Label(frame_admin_control, text = "Selected Student", font=("times", 20), bg="white").place(x=10, y=10, height=40)

# Entry field
lbl_selected_name = Label(frame_admin_control, text = "Name", bg="white")
lbl_selected_name.place(x=10, y=50, width=50)

ent_selected_name = Entry(frame_admin_control, bg="lightgray", state = DISABLED, disabledforeground="red")
ent_selected_name.place(x=70, y=50, height=30, width=300)

lbl_selected_email = Label(frame_admin_control, text = "Email", bg="white")
lbl_selected_email.place(x=10, y=90, width=50)

ent_selected_email = Entry(frame_admin_control, bg="lightgray", state = DISABLED, disabledforeground="red")
ent_selected_email.place(x=70, y=90, height=30, width=300)



# delete button
btn_delete_student = Button(frame_admin_control, text="Delete", font=("times", 15), fg="white", bg="black", state=DISABLED, command = delete_data_from_database)
btn_delete_student.place(x=500, y=100, width=60, height=30)

# show button
btn_show_student = Button(frame_admin_control, text="Show Details", font=("times", 15), fg="white", bg="black",state=DISABLED, command= lambda : show_details(student_personal_homepage))
btn_show_student.place(x=580, y=100, width=140, height=30)



#------------------------------------------------------------------------------------------
#--------------------------------------------- showing the details---------------------------------------------
#------------------------------------------------------------------------------------------
student_personal_homepage = Frame(frame_admin_homepage, bg="white")
student_personal_homepage.place(x=0, y=0, relwidth =1 , relheight=1)


# print(ide,name, sex, category, religion, nationality, handicap, handicap_percentage, dob_txt, father_name, father_occ,
#             mother_name, mother_occ, guardian_name, rel_guardian, session, reg_no, student_id, course, contact, email,
#             guardian_contact, guardian_email, aadhaar, prmnt_address, prmnt_pincode, prsnt_address, prsnt_pincode, city,
#             district, state, country, last_instn, last_instn_add, hobby, exam_1, exam_2, exam_3, exam_4, board_1,
#             board_2, board_3, board_4, tm_1, tm_2, tm_3, tm_4, cgpa_1, cgpa_2, cgpa_3, cgpa_4, percnt_1, percnt_2,
#             percnt_3, percnt_4, passyear_1, passyear_2, passyear_3, passyear_4)


#----------------------------Tab----------------------------


tabControl = ttk.Notebook(student_personal_homepage)

tab1 = Frame(tabControl, bg="#90caf9")
tabControl.add(tab1, text="Page-1")
tab2 = Frame(tabControl, bg="#90caf9")
tabControl.add(tab2, text="Page-2")



tabControl.place(x=20, y=20, width=1160, height=560)

# Adding details
#---------------------------tab1-----------------------------
#------------------------------------------1st Column----------------------------------------------
bg_bdy = "#90caf9"
# Name
Label(master=tab1, text="Full Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=10)
ent_name_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, state=DISABLED, disabledbackground="white", disabledforeground="black", cursor="arrow")
ent_name_get.place(x=10, y=40, height=30, width=350)

# Sex
Label(master=tab1, text="Sex", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=80, height=30)
lbl_sex_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_sex_get.place(x=210, y=80, height=30, width=150)

# Category
Label(master=tab1, text="Category", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=120)
lbl_cat_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_cat_get.place(x=210, y=120, height=30, width=150)


# Religion
Label(master=tab1, text="Religion", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=160)
lbl_religion_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_religion_get.place(x=210, y=160, height=30, width=150)


# Nationality
Label(master=tab1, text="Nationality", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=200)
lbl_nationality_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_nationality_get.place(x=210, y=200, height=30, width=150)

# Physically Handicapped
Label(master=tab1, text="Physically Handicapped?", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=240)
lbl_physical_handicap_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_physical_handicap_get.place(x=210, y=240, height=30, width=150)


# % of Disability
Label(master=tab1, text="% of Disability", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=280)
lbl_percntg_hc_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_percntg_hc_get.place(x=210, y=280, height=30, width=150)


# 	Date of Birth
Label(master=tab1, text="Date of Birth", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=320)
lbl_dob_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_dob_get.place(x=210, y=320, height=30, width=150)

# Country Name
Label(master=tab1, text="Country", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=360)
lbl_country_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_country_get.place(x=150, y=360, height=30, width=210)

# Aadhaar No.
Label(master=tab1, text="Aadhaar Number", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=400)

ent_aadhaar_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, state=DISABLED, disabledbackground="white", disabledforeground="black", cursor="arrow")
ent_aadhaar_get.place(x=10, y=430, height=30, width=350)


#----------------------1st tab 2nd column---------------------------------------------
# Father's Name
Label(master=tab1, text="Father's Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=10)

ent_father_name_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_father_name_get.place(x=400, y=40, height=30, width=320)


# 	Father's Occupation
Label(master=tab1, text="Father's Occupation", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=80)

ent_father_occu_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_father_occu_get.place(x=400, y=110, height=30, width=320)


# Mother's Name
Label(master=tab1, text="Mother's Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=150)

ent_mother_name_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_mother_name_get.place(x=400, y=180, height=30, width=320)

# 	Mother's Occupation
Label(master=tab1, text="Mother's Occupation", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=220)

ent_mother_occu_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_mother_occu_get.place(x=400, y=250, height=30, width=320)



# Guardian Name
Label(master=tab1, text="Guardian Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=290)

ent_guardian_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_guardian_get.place(x=400, y=320, height=30, width=320)



# Guardian Relation
Label(master=tab1, text="Relation with Guardian", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=400, y=360)

ent_guardian_rel_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_guardian_rel_get.place(x=400, y=390, height=30, width=320)


# Guardian Email Address
Label(master=tab1, text="Guardian's Email Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 400, y=430)

ent_g_email_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_g_email_get.place(x=400, y=460, height=30, width=320)


#---------------1st tab 3rd column----------------------
#Image frame
frame_student_image = Frame(tab1, bg="white", bd=1, relief=SOLID)
frame_student_image.place(x=1000, y=10, height=170, width=130)

# Adding Image
photo_show = ImageTk.PhotoImage(file = "./img/ico.png")
lbl_image_show = Label(frame_student_image, image = photo_show)
lbl_image_show.place(x=0, y=0, relwidth=1, relheight=1)



# Session
Label(master=tab1, text="Session", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=760, y=10)
lbl_session_get = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_session_get.place(x=860, y=10, height=30, width=120)

# Registration number
Label(master=tab1, text="Reg. No.", font=("Comic Sans MS", 13), bg=bg_bdy).place(x=760, y=50)

ent_registration_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_registration_get.place(x=760, y=80, width=220, height=30)


# Student Id
Label(master=tab1, text="Student Id", font=("Comic Sans MS", 13), bg=bg_bdy).place(x=760, y=120)

ent_student_id_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_student_id_get.place(x=760, y=150, width=220, height=30)


# Course
Label(master=tab1, text="Course", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=760, y=190)
lbl_get_course = Label(tab1, text="", font=("times", 13), bg= "white", bd=1, relief = SOLID)
lbl_get_course.place(x=860, y=190, height=30, width=120)

# Phone Number
Label(master=tab1, text="Contact Number", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 760, y=230)

ent_phone_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_phone_get.place(x=760, y=260, height=30, width=300)



# Email Address
Label(master=tab1, text="Email Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=760, y=300)

ent_email_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_email_get.place(x=760, y=330, height=30, width=300)


# Guardian Phone Number
Label(master=tab1, text="Guardian's Contact Number", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 760, y=370)

ent_g_phone_get = Entry(master=tab1, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_g_phone_get.place(x=760, y=400, height=30, width=300)


# Button to datatable
btn_home_tab1 = Button(tab1, text="Back to Select Student", font=("times", 15), fg="white", bg="green", activebackground="green", activeforeground="white", command= lambda : swap(frame_admin_panel))
btn_home_tab1.place(x=760, y=460, height=50, width=300)


#----------------------------Tab2-------------------------------------------------

#---------------------------2nd tab 1st column
#Permanent Address
Label(master=tab2, text="Permanent Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=10)

text_prmnt_add_get = Text(master=tab2, bg="white", font=("times", 12), bd=1, relief=SOLID, state=DISABLED, cursor="arrow")
text_prmnt_add_get.place(x=10, y=40, width=330, height=100)


# Pin Code
Label(master=tab2, text="Pincode", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=150)

ent_pincode_p_get = Entry(master=tab2, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_pincode_p_get.place(x=10, y=180, height=30, width=230)


#Present Address
Label(master=tab2, text="Present Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=220)

text_prsnt_add_get = Text(master=tab2, bg="white", font=("times", 12), bd=1, relief=SOLID, state=DISABLED, cursor="arrow")
text_prsnt_add_get.place(x=10, y=250, width=330, height=100)


# Pin Code
Label(master=tab2, text="Pincode", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=10, y=360)

ent_pincode_get = Entry(master=tab2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_pincode_get.place(x=10, y=390, height=30, width=230)



#--------------------2nd Tab 2nd column---------------------------
# City name
Label(master=tab2, text="City", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=360, y=10)

ent_city_get = Entry(master=tab2, bg="white", font=("times", 13), bd=1, relief = SOLID,  disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_city_get.place(x=360, y=40, height=30, width=300)



# District Name
Label(master=tab2, text="District", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=360, y=80)

ent_district_get = Entry(master=tab2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_district_get.place(x=360, y=110, height=30, width=300)


# State Name
Label(master=tab2, text="State", font=("Comic Sans MS", 13), bg= bg_bdy).place(x=360, y=150)

ent_state_get = Entry(master=tab2, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_state_get.place(x=360, y=180, height=30, width=300)



#--------------------tab2 3rd column------------------------

# Last Institution
Label(master=tab2, text="Last Institution Name", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 700, y=10)

ent_last_instn_get = Entry(master=tab2, bg="white", font=("times", 13), bd=1, relief = SOLID,
                      disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_last_instn_get.place(x=700, y=40, height=30, width=360)


# Last Institution Address
Label(master=tab2, text="Last Institution Address", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 700, y=80)

txt_last_instn_addrs_get = Text(master=tab2, bg="white", font=("times", 12), bd=1, relief=SOLID, cursor="arrow")
txt_last_instn_addrs_get.place(x=700, y=110, width=360, height=60)


# Hobbies
Label(master=tab2, text="Hobbies *", font=("Comic Sans MS", 13), bg= bg_bdy).place(x = 700, y=180)

txt_hobby_get = Text(master=tab2,font=("times", 13), bg="white", bd=1, relief=SOLID, cursor="arrow")
txt_hobby_get.place(x=700, y=210, width=360, height=60)


# Frame for marks
frame_marks_get = Frame(tab2, bg = "lightgray", bd=1, relief=SOLID, )
frame_marks_get.place(x=360, y=280, height=167, width=720)

# Titles

# Serial Number
Label(frame_marks_get, text="Sl.\nNo.", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=0, y=0, width=40, height=50)

# Exam name
Label(frame_marks_get, text="Exam Name", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=40, y=0, width=170, height=50)

# Board name
Label(frame_marks_get, text="Board Name", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=210, y=0, width=200, height=50)

# passing year
Label(frame_marks_get, text="Passing\nyear", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=410, y=0, width=70, height=50)

# Marks
Label(frame_marks_get, text="Total\nMarks", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=480, y=0, width=70, height=50)

# Percentage
Label(frame_marks_get, text="%", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=550, y=0, width=70, height=50)

# CGPA
Label(frame_marks_get, text="CGPA", font=("times", 13, "bold"), bd=1, relief=RAISED).place(x=620, y=0, width=99, height=50)

#-----------------------------------Data--------------------------------------------

# Serial Numbers
Label(frame_marks_get, text="1", font=("times", 13, "bold"),bd=1, relief=SOLID).place(x=-1, y=49, height=30, width=41)
Label(frame_marks_get, text="2", font=("times", 13, "bold"),bd=1, relief=SOLID).place(x=-1, y=78, height=30, width=41)
Label(frame_marks_get, text="3", font=("times", 13, "bold"),bd=1, relief=SOLID).place(x=-1, y=107, height=30, width=41)
Label(frame_marks_get, text="4", font=("times", 13, "bold"),bd=1, relief=SOLID).place(x=-1, y=136, height=30, width=41)



# Exam Names

ent_exam1_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_exam1_get.place(x=39, y=49, height=30, width=171)

ent_exam2_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_exam2_get.place(x=39, y=78, height=30, width=171)

ent_exam3_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_exam3_get.place(x=39, y=107, height=30, width=171)

ent_exam4_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_exam4_get.place(x=39, y=136, height=30, width=171)


# Board Names
ent_board1_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_board1_get.place(x=209, y=49, height=30, width=201)

ent_board2_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_board2_get.place(x=209, y=78, height=30, width=201)

ent_board3_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_board3_get.place(x=209, y=107, height=30, width=201)

ent_board4_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_board4_get.place(x=209, y=136, height=30, width=201)

# Passing Years
ent_passyear1_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_passyear1_get.place(x=409, y=49, height=30, width=71)

ent_passyear2_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_passyear2_get.place(x=409, y=78, height=30, width=71)

ent_passyear3_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_passyear3_get.place(x=409, y=107, height=30, width=71)

ent_passyear4_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_passyear4_get.place(x=409, y=136, height=30, width=71)


# Total Marks
ent_marks1_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_marks1_get.place(x=479, y=49, height=30, width=71)

ent_marks2_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_marks2_get.place(x=479, y=78, height=30, width=71)

ent_marks3_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_marks3_get.place(x=479, y=107, height=30, width=71)

ent_marks4_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_marks4_get.place(x=479, y=136, height=30, width=71)

# Percentage
ent_percentage1_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_percentage1_get.place(x=549, y=49, height=30, width=71)

ent_percentage2_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_percentage2_get.place(x=549, y=78, height=30, width=71)

ent_percentage3_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_percentage3_get.place(x=549, y=107, height=30, width=71)

ent_percentage4_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_percentage4_get.place(x=549, y=136, height=30, width=71)



# Cgpa
ent_cgpa1_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_cgpa1_get.place(x=619, y=49, height=30, width=100)

ent_cgpa2_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_cgpa2_get.place(x=619, y=78, height=30, width=100)

ent_cgpa3_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_cgpa3_get.place(x=619, y=107, height=30, width=100)

ent_cgpa4_get = Entry(frame_marks_get, bg="white", font=("times", 13), bd=1, relief = SOLID, disabledbackground="white", disabledforeground="black", state=DISABLED, cursor="arrow")
ent_cgpa4_get.place(x=619, y=136, height=30, width=100)


# Button
btn_home_tab2 = Button(tab2, text="Back to Select Student", font=("times", 15), fg="white", bg="green", activebackground="green", activeforeground="white", command= lambda : swap(frame_admin_panel))
btn_home_tab2.place(x=760, y=460, height=50, width=300)


#------------------------------------------------------------------------------------------
#--------------------------------------------- showing ends---------------------------------------------
#------------------------------------------------------------------------------------------






frame_admin_password_window.tkraise()
main_frame_homepage.tkraise()


root.mainloop()