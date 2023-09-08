from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as msc



app = Tk()
app.geometry(f"{363}x{640}+{580}+{120}")
app.configure(bg="#8d1e1e")
app.resizable(0,0)
app.title("Blood Buddy")


#*************************************************Functions**************************************************#

#goto fill user deatils
def goto_userdetails():
    if len(signup_name_entry.get()) == 0 or len(signup_username_entry.get()) == 0 or len(signup_password_entry.get()) == 0 or len(signup_cnfpassword_entry.get()) == 0 :
        messagebox.showwarning("Empty Field", "Fields Cant be Empty",parent=SignupPage)
        return
    
    if len(signup_username_entry.get()) < 8:
        messagebox.showwarning("Short Username", "Username Should Be Atleast 8 characters Long")
        return

    if len(signup_password_entry.get()) < 8:
        messagebox.showwarning("Short Password", "Password Should Be Atleast 8 characters Long")
        return
    
    if signup_password_entry.get() != signup_cnfpassword_entry.get():
        messagebox.showwarning("Missmatch Password", "Passwords Don't match",parent=SignupPage)
        signup_password_entry.delete(0, END)
        signup_cnfpassword_entry.delete(0, END)

    else:
        
        SUserInfo.tkraise()
         

#***************************#

#signedup
def signedup():
    if len(SUserInfo_aadharno.get()) != 12:
        messagebox.showwarning("Incorrect Addhar", "Addhar Number Should Be 12 digits long")
        return
    
    if SUserInfo_Age.get() == "" or SUserInfo_aadharno.get()== "" or SUserInfo_address.get()== "" or SUserInfo_Gender.get() == "" or Susr_city.get() == "" or Susr_state.get() == "" or Susrinfo_bgroup.get() == "" or SUserInfo_Pincode.get() == "":
        messagebox.showwarning("Empty Field", "Fields Cant be Empty",parent=SUserInfo)
    
    else:
        try:
            conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
            cur = conn.cursor()
            cur.execute("Insert into user_details (username,password,name,aadhar_no,user_age,user_gender,user_address,user_city,user_state,user_pincode,user_bg) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                signup_username_entry.get(),
                signup_password_entry.get(),
                signup_name_entry.get(),
                int(SUserInfo_aadharno.get()),
                int(SUserInfo_Age.get()),
                SUserInfo_Gender.get(),
                SUserInfo_address.get(),
                Susr_city.get(),
                Susr_state.get(),
                int(SUserInfo_Pincode.get()),
                Susrinfo_bgroup.get()

            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sign Up SuccessFull", "Congratulations! You are signedup successfully !!")
            LoginPage.tkraise()
            signup_name_entry.delete(0,END)
            signup_username_entry.delete(0,END)
            signup_password_entry.delete(0, END)
            signup_cnfpassword_entry.delete(0, END)
            SUserInfo_aadharno.delete(0,END)
            SUserInfo_Age.delete(0,END)
            SUserInfo_Gender.delete(0,END)
            SUserInfo_address.delete(0,END)
            Susr_city.set(value = cities[0])
            Susr_state.set(value = states[0])
            SUserInfo_Pincode.delete(0,END)
            Susrinfo_bgroup.set(value = blood_groups[0])

        except Exception as e:
             messagebox.showerror("Error!",f"Error due to {e}",parent=SUserInfo)




#***************************#
#***************************#

#loged in 
def logedin():

    username = login_username_entry.get()
    password = login_password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning("Empty Field", "Fields Cant be Empty",parent=LoginPage)
        return
    

    try:
        conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
        cur = conn.cursor()
        cur.execute("select * from user_details where username=%s and password=%s",(username,password))
        row = cur.fetchone()
        if row == None:
            messagebox.showwarning("Bad Entry", "Username or password incorrect")
            login_password_entry.delete(0,END)
            login_username_entry.delete(0,END)
        else:
            
            UserMainPage.tkraise()
            conn.close()

            try:
                conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
                cur = conn.cursor()
                cur.execute("select name from user_details where username=%s and password=%s",(username,password))
                name = cur.fetchone()
                welcome_message.config(text=f"Welcome {str(name[0])}")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {e}",parent=UserMainPage)


    
    except Exception as e:
        messagebox.showerror("Error!",f"Error due to {e}",parent=LoginPage)
        

    
        

#***************************#
#***************************#


#forgot password

def get_pass():
    userid = ar_userid_entry.get()
    addhar_no = ar_addhar_entry.get()

    if len(userid) == 0 or len(addhar_no) == 0:
        messagebox.showwarning("Empty Field", "Fields Cant be Empty")
        return
    
    try:
        conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
        cur = conn.cursor()
        cur.execute("select password from user_details where username=%s and  aadhar_no=%s",(userid,int(addhar_no)))
        row = cur.fetchone()
        password_message.config(text=f"Password: {row[0]}")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error!",f"Incorrect Credentials")
        ar_userid_entry.delete(0,END)
        ar_addhar_entry.delete(0,END)





#***************************#
#***************************#





#logout function
def logged_out():
    login_username_entry.delete(0, END)
    login_password_entry.delete(0, END)
    LoginPage.tkraise()
#***************************#
#***************************#
    
    


#cancel signup

def cancel_signup():
    LoginPage.tkraise()
    signup_name_entry.delete(0,END)
    signup_username_entry.delete(0,END)
    signup_password_entry.delete(0, END)
    signup_cnfpassword_entry.delete(0, END)
    SUserInfo_aadharno.delete(0,END)
    SUserInfo_Age.delete(0,END)
    SUserInfo_Gender.delete(0,END)
    SUserInfo_address.delete(0,END)
    Susr_city.set(value = cities[0])
    Susr_state.set(value = states[0])
    SUserInfo_Pincode.delete(0,END)
    Susrinfo_bgroup.set(value = blood_groups[0])

#***************************#
#***************************#

#cancel update
def cancel_update():
    UserMainPage.tkraise()
    UserInfo_aadharno.delete(0,END)
    UserInfo_Age.delete(0,END)
    UserInfo_Gender.delete(0,END)
    UserInfo_address.delete(0,END)
    usr_city.set(value = cities[0])
    usr_state.set(value = states[0])
    UserInfo_Pincode.delete(0,END)
    usrinfo_bgroup.set(value = blood_groups[0])

#***************************#
#***************************#

#search blood Avalibility
def search_Aval():
    if bas_state.get() == "select" or bas_city.get()== "select" or bas_bg.get()=="select" or bas_bc.get() == "select":
        messagebox.showwarning("Empty Field", "Fields Cant be Empty",parent=BloodAvbty)

    try:
        conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
        cur = conn.cursor()
        cur.execute(f"select BB_name, BB_address, BB_city , BB_pincode from Bb_details where BB_city = %s and BB_state = %s and `{bas_bg.get()}`= (select max(`{bas_bg.get()}`) from BB_details where BB_city = %s and BB_state = %s);",            
        (bas_city.get(),
        bas_state.get(),
        bas_city.get(),
        bas_state.get()
        )
        )
        name = cur.fetchone()
        Working_message.config(text=f"{name[0]}\n{name[1]}, {name[2]}, {name[3]}")
       
        conn.close()  

    except Exception as e:
            Working_message.config(text=f"Blood Group Not Avilable in selected city")
    UserMainPage.tkraise()

#***************************#
#***************************#
#***************************#

#medical history updated
def donate_blood():
    
    if medhis_bgroup.get() == "select" or diabetes.get() == "select" or tattoo.get() == "select" or recent_dnt.get() == "select" or intox.get() == "select":
        messagebox.showwarning("Empty Field", "Fields Cant be Empty",parent=MedHistory)
        return
    
    if diabetes.get() == "yes" or tattoo.get() == "yes" or recent_dnt.get() == "yes" or intox.get() == "yes":
        Working_message.config(text = f"You can't donate blood :(")
        UserMainPage.tkraise()
        return
    
    else:
        try:
            conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
            cur1 = conn.cursor()
            cur1.execute(f"SELECT user_pincode, user_city, user_bg from user_details where username = %s and password = %s", (login_username_entry.get(), login_password_entry.get()))
            user_det = cur1.fetchone()

            cur2 = conn.cursor()
            cur2.execute(f"SELECT BB_username, BB_licence_no from BB_details where BB_pincode = %s and `{user_det[2]}` = (select min(`{user_det[2]}`) from BB_details where BB_pincode = %s)",            
            (user_det[0],
             user_det[0]
            )
            )
            temp_bb_username = cur2.fetchone()

            
            cur = conn.cursor()
            cur.execute(f"select BB_name, BB_address, BB_city , BB_pincode from Bb_details where BB_username = %s and BB_licence_no = %s", (temp_bb_username[0], temp_bb_username[1]))
            name =  cur.fetchone()   
            Working_message.config(text=f"{name[0]}\n{name[1]}, {name[2]}, {name[3]}")
            conn.close()

        except Exception as e:
            try:
                conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
                cur2 = conn.cursor()
                cur2.execute(f"SELECT BB_username , BB_licence_no from BB_details where BB_city = %s and `{user_det[2]}` = (select min(`{user_det[2]}`) from BB_details where BB_city = %s)",            
                (user_det[1],
                user_det[1]
                )
                )
                temp_bb_username = cur2.fetchone()

                
                cur = conn.cursor()
                cur.execute(f"select BB_name, BB_address, BB_city , BB_pincode from Bb_details where BB_username = %s and BB_licence_no = %s ", (temp_bb_username[0], temp_bb_username[1]))
                name =  cur.fetchone()   
                Working_message.config(text=f"{name[0]}\n{name[1]}, {name[2]}, {name[3]}")
                UserMainPage.tkraise()
                conn.close()

            except Exception as e:
                Working_message.config(text=f"Could Not Find Blood Bank In Your City")
                UserMainPage.tkraise()
         


#***************************#
#***************************#

#get blood function
def get_blood():
    try:
        conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
        cur1 = conn.cursor()
        cur1.execute(f"SELECT user_pincode, user_city, user_bg from user_details where username = %s and password = %s", (login_username_entry.get(), login_password_entry.get()))
        user_det = cur1.fetchone()
        cur2 = conn.cursor()
        cur2.execute(f"SELECT BB_username, BB_licence_no from BB_details where BB_pincode = %s and `{user_det[2]}` = (select max(`{user_det[2]}`) from BB_details where BB_pincode = %s)",            
        (user_det[0],
         user_det[0]
        )
        )
        temp_bb_username = cur2.fetchone()
        
        cur = conn.cursor()
        cur.execute(f"select BB_name, BB_address, BB_city , BB_pincode from Bb_details where BB_username = %s and BB_licence_no = %s", (temp_bb_username[0], temp_bb_username[1]))
        name =  cur.fetchone()   
        Working_message.config(text=f"{name[0]}\n{name[1]}, {name[2]}, {name[3]}")
        conn.close()
    except Exception as e:
            try:
                conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
                cur2 = conn.cursor()
                cur2.execute(f"SELECT BB_username , BB_licence_no from BB_details where BB_city = %s and `{user_det[2]}` = (select max(`{user_det[2]}`) from BB_details where BB_city = %s)",            
                (user_det[1],
                user_det[1]
                )
                )
                temp_bb_username = cur2.fetchone()

                
                cur = conn.cursor()
                cur.execute(f"select BB_name, BB_address, BB_city , BB_pincode from Bb_details where BB_username = %s and BB_licence_no = %s ", (temp_bb_username[0], temp_bb_username[1]))
                name =  cur.fetchone()   
                Working_message.config(text=f"{name[0]}\n{name[1]}, {name[2]}, {name[3]}")
                conn.close()

            except Exception as e:
                Working_message.config(text=f"Could Not Find Blood Bank In Your City")


#***************************#
#***************************#           
         

# user info update
def update_user_info():

    username = login_username_entry.get()

    if len(UserInfo_aadharno.get()) != 12:
        messagebox.showwarning("Incorrect Addhar", "Addhar Number Should Be 12 digits long")
        return
    
    if UserInfo_Age.get() == "" or UserInfo_aadharno.get()== "" or UserInfo_address.get()== "" or UserInfo_Gender.get() == "" or usr_city.get() == "" or usr_state.get() == "" or usrinfo_bgroup.get() == "" or UserInfo_Pincode.get() == "":
        messagebox.showwarning("Empty Field", "Fields Cant be Empty",parent=UserInfo)
    
    else:
        try:
            conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
            cur = conn.cursor()
            cur.execute("UPDATE user_details SET aadhar_no=%s,user_age=%s,user_gender=%s,user_address=%s,user_city=%s,user_state=%s,user_pincode=%s,user_bg=%s WHERE username = %s ", (
                
                int(UserInfo_aadharno.get()),
                int(UserInfo_Age.get()),
                UserInfo_Gender.get(),
                UserInfo_address.get(),
                usr_city.get(),
                usr_state.get(),
                int(UserInfo_Pincode.get()),
                usrinfo_bgroup.get(),
                username
            ))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Update SuccessFull", "Congratulations! Your Update was successful !!")
            UserMainPage.tkraise()
            UserInfo_aadharno.delete(0,END)
            UserInfo_Age.delete(0,END)
            UserInfo_Gender.delete(0,END)
            UserInfo_address.delete(0,END)
            usr_city.set(value = cities[0])
            usr_state.set(value = states[0])
            UserInfo_Pincode.delete(0,END)
            usrinfo_bgroup.set(value = blood_groups[0])

        except Exception as e:
             messagebox.showerror("Error!",f"Error due to {e}",parent=SUserInfo)




#***************************#
#***************************#

    
    
#*************************************************************************************************************#
#*************************************************************************************************************#
#*************************************************************************************************************#













#*********************************************Define All Images*************************************************#


bg_login = PhotoImage(file="login.png")
bg_signup = PhotoImage(file="signup.png")
bg_about = PhotoImage(file="about.png")
bg_UserMainPage = PhotoImage(file="usermainpage.png")
bg_BloodAvbty=PhotoImage(file="bloodAvl.png")
bg_MedHistory=PhotoImage(file="medHistory.png")
bg_UserInfo=PhotoImage(file="userinfo.png")
bg_acc_recovery=PhotoImage(file="accrecoveryuser.png")



#button image
exit_btn = PhotoImage(file="exitBtn.png")





#*************************************************************************************************************#
#*************************************************************************************************************#






#**********************************************login Page*****************************************************#


LoginPage = Frame(app, height=640, width=360)
LoginPage.grid(row=0, column=0, sticky="nsew")


#background lable
login_bg_lbl = Label(LoginPage, image=bg_login)
login_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
login_bg_lbl.pack()

#username entry
login_username_entry = Entry(LoginPage, width=18, font="Ariel 11", bg="white",borderwidth=0)
login_username_entry.place(x=34,y=333)

#password entry
login_password_entry = Entry(LoginPage, width=18, font="Ariel 11", bg="white",borderwidth=0,show="●")
login_password_entry.place(x=34,y=412)

#forgot passoword Button
forgot_password_button =  ctk.CTkButton(LoginPage,
                                border=0,
                                width=100,
                                height=20,
                                text="Forgot Password ?",
                                text_font=("Ariel", 8),
                                text_color= "blue",
                                fg_color="white",
                                bg_color="white",
                                hover_color= "#d7ded9",
                                command = lambda: AccRecovery.tkraise()
                                )

forgot_password_button.place(x=30, y=460)

#login button
login_login_btn = ctk.CTkButton(LoginPage,
                                 border=0, 
                                 width=300,
                                 height=54 , 
                                 corner_radius= 20, 
                                 text="Login",
                                 text_font= ("Open Sans Bold",15,"bold"),
                                 text_color= "white", 
                                 fg_color= "#223239", 
                                 hover_color="#242424",
                                 bg_color="white",
                                 command=logedin)
login_login_btn.place(x=30,y=484)

#signin button 
login_signup_btn = ctk.CTkButton(LoginPage,
                                 border=0, 
                                 width=160,
                                 height=46, 
                                 corner_radius= 15, 
                                 text="Sign Up",
                                 text_font= ("Open Sans Bold",15,"bold"),
                                 text_color= "white", 
                                 fg_color= "#223239", 
                                 hover_color="#242424",
                                 bg_color="#8d1e1e",
                                 command=lambda: SignupPage.tkraise())
login_signup_btn.place(x=14,y=579)

#about button 
login_about_btn = ctk.CTkButton(LoginPage,
                                 border=0, 
                                 width=160,
                                 height=46, 
                                 corner_radius= 15, 
                                 text="About",
                                 text_font= ("Open Sans Bold",15,"bold"),
                                 text_color= "white", 
                                 fg_color= "#223239", 
                                 hover_color="#242424",
                                 bg_color="#8d1e1e",
                                 command=lambda: AboutPage.tkraise()
                                 )
login_about_btn.place(x=192,y=579)

#*************************************************************************************************************#





#**********************************************Sign Up Page***************************************************#

SignupPage = Frame(app, height=640, width=360)
SignupPage.grid(row=0, column=0, sticky="nsew")

#background lable
signup_bg_lbl = Label(SignupPage, image=bg_signup)
signup_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
signup_bg_lbl.pack()

#name entry
signup_name_entry = Entry(SignupPage, width=18, font="Ariel 11", bg="#e7ded9",borderwidth=0)
signup_name_entry.place(x=78,y=190)

#username entry
signup_username_entry = Entry(SignupPage, width=18, font="Ariel 11", bg="#e7ded9",borderwidth=0)
signup_username_entry.place(x=78,y=282)

#password entry
signup_password_entry = Entry(SignupPage, width=18, font="Ariel 11", bg="#e7ded9",borderwidth=0,show="●")
signup_password_entry.place(x=78,y=375)

#confirm password entry
signup_cnfpassword_entry = Entry(SignupPage, width=18, font="Ariel 11", bg="#e7ded9",borderwidth=0,show="●")
signup_cnfpassword_entry.place(x=82,y=469)



#letss goo button
signup_letsgo_btn = ctk.CTkButton(SignupPage,
                                 border=0, 
                                 width=300,
                                 height=54, 
                                 corner_radius= 20, 
                                 text="Let's Go!",
                                 text_font= ("Open Sans Bold",15,"bold"),
                                 text_color= "white", 
                                 fg_color= "#223239", 
                                 hover_color="#242424",
                                 bg_color="#e7ded9",
                                 command=goto_userdetails
                                 )
signup_letsgo_btn.place(x=30,y=550)


#back to Login button
back_to_login =  ctk.CTkButton(SignupPage,
                                border=0,
                                width=100,
                                height=20,
                                text="Already Have an Account ? Login",
                                text_font=("Ariel", 8),
                                text_color= "blue",
                                fg_color="#e7ded9",
                                bg_color="#e7ded9",
                                hover_color= "#d7ded9",
                                command = lambda: LoginPage.tkraise()
                                )

back_to_login.place(x=40, y=610)

#*************************************************************************************************************#


#*********************************************Signup User Info ******************************************************#


SUserInfo = Frame(app, height= 640, width=360)
SUserInfo.grid(row=0, column=0, sticky="nsew")

#page background label
SUserInfo_label= Label(SUserInfo,image=bg_UserInfo)
SUserInfo_label.place(x=0,y=0,relheight=1,relwidth=1)
SUserInfo_label.pack()

#age entrybox
SUserInfo_Age=Entry(SUserInfo,
                    width=15,
                    font=('Georgia',15),
                    borderwidth=0,
                    fg="black",
                    bg="white",
                    )
SUserInfo_Age.place(x=155,y=174)

#gender entry box
SUserInfo_Gender=Entry(SUserInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )
SUserInfo_Gender.place(x=155,y=220)

#Address entry box
SUserInfo_address=Entry(SUserInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )

SUserInfo_address.place(x=155,y=276)
#City drop box
cities = ["Select","Sangli","Satara","Kolhapur","Solapur","Surat","Mumbai","Pune"]
Susr_city = ctk.StringVar(value= cities[0])
SUserInfo_City_drop=ctk.CTkComboBox(SUserInfo, variable= Susr_city,
                                      values=cities,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9"
                                     )

SUserInfo_City_drop.place(x=155,y=330)

#State drop box
states = ["Select","Gujarat","Maharashtra","Delhi"]
Susr_state = ctk.StringVar(value=states[0])
SUserInfo_State_drop=ctk.CTkComboBox(SUserInfo, variable=Susr_state,
                                      values=states,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15,),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9",
                                      )

SUserInfo_State_drop.place(x=155,y=390)


#Pincode entry box
SUserInfo_Pincode=Entry(SUserInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )

SUserInfo_Pincode.place(x=155,y=442)

#Addharno entry box
SUserInfo_aadharno=Entry(SUserInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )

SUserInfo_aadharno.place(x=155,y=489)

blood_groups = ["Select","A+","A-","B+","B-","AB+","AB-","O+","O-"]
Susrinfo_bgroup = ctk.StringVar(value=blood_groups[0])
SUserInfo_bgroup_drop= ctk.CTkComboBox(SUserInfo, variable= Susrinfo_bgroup,
                                      values=blood_groups,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9")

SUserInfo_bgroup_drop.place(x=155,y=535)

#signup button
SUserInfo_signup_btn=ctk.CTkButton(SUserInfo,
                                   width=300,
                                   height=50,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "Signup",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#223239",
                                   hover_color="black",
                                   command= signedup)
SUserInfo_signup_btn.place(x=30,y=582)

#cancel signup button
SUserInfo_cancel_btn=ctk.CTkButton(SUserInfo,
                                   width=20,
                                   height=20,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "X",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command= cancel_signup)
SUserInfo_cancel_btn.place(x=300,y=20)

#*************************************************************************************************************#


#***********************************************Forgot Password***********************************************#
AccRecovery = Frame(app, height=640, width=360)
AccRecovery.grid(row=0, column=0, sticky="nsew")

# account recovery page background label
about_bg_label = Label(AccRecovery, image=bg_acc_recovery)
about_bg_label.place(x=0,y=0,relwidth=1,relheight=1)



 #creating update blood stockbutton
ar_getpass_btn=ctk.CTkButton(AccRecovery,
                                        height=49,
                                        width=290,
                                        text_font= ("Open Sans Bold",15,"bold"),
                                        text_color="white",
                                        fg_color="#223239",
                                        text="Get My Password",
                                        bg_color="white",
                                        hover_color="black",
                                        corner_radius=15,
                                        command= get_pass,
                                       )
ar_getpass_btn.place(x=40,y=423)

password_message = Message(AccRecovery,
                          font=('Segoe UI',12, "bold"),
                          aspect=325,
                          bg="#e7ded9")
password_message.place(x=40,y=480)

#creating userid  field
ar_userid_entry = Entry(AccRecovery, width=15, font="Ariel 14", bg="#CBEFFF",borderwidth=0)
ar_userid_entry.place(x=167,y=325)

#creating Liscence No field
ar_addhar_entry = Entry(AccRecovery, width=15, font="Ariel 14", bg="#CBEFFF",borderwidth=0)
ar_addhar_entry.place(x=167,y=370)


#cancel updatebs button
ar_cancel_btn=ctk.CTkButton(AccRecovery,
                                   width=20,
                                   height=20,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "X",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command= lambda: LoginPage.tkraise()
                                   )
ar_cancel_btn.place(x=270,y=530)



#*************************************************************************************************************#









#***********************************************About Page****************************************************#


AboutPage = Frame(app, height=640, width=360)
AboutPage.grid(row=0, column=0, sticky="nsew")

# about page background label
about_bg_label = Label(AboutPage, image=bg_about)
about_bg_label.place(x=0,y=0,relwidth=1,relheight=1)

# vision message message
Vision_message = Message(AboutPage,text="◆ Our vision is to cater to your medical needs ,ensuring that while we adhere to proper regulations and standards, we provide you with best accessible options in blood donation and blood obtainment.We will connect you to multiple blood banks through which you will be able to get or donate blood at a button's click.",font=('Georgia',10),aspect=150,bg="#e7ded9")
Vision_message.pack(padx=10,pady=10)
Vision_message.place(x=52,y=120)

# working message
Working_message = Message(AboutPage,text="Working/n ◆ 1.Create account/n ◆ 2.Login/n ◆ 3.Fill Medical History/n ◆ 4.Get/Donate Blood/n ◆ 5.Search",font=('Georgia',10),aspect=150,bg="#e7ded9")
Working_message.place(x=50,y=280)

# rules message
Rules_message = Message(AboutPage,text="◆ Please update your medical history before making any transactions to get pertinent results. In case of any inconveniences please feel free to contact number given below/n 6844654891",font=('Georgia',10),aspect=170,bg="#e7ded9")
Rules_message.place(x=50,y=410)

# ok button
ok_AboutPage_btn = ctk.CTkButton(AboutPage, 
                                 width=100,
                                 height=50, 
                                 corner_radius= 20, 
                                 text="OK!",
                                 text_color= "white", 
                                 fg_color= "#8d1e1e", 
                                 hover_color="#242424",
                                 bg_color="#231f20",
                                 command=lambda: LoginPage.tkraise()
                                 )

ok_AboutPage_btn.place(x=248,y=575)
#*************************************************************************************************************#




#*********************************************User Main Page**************************************************#

UserMainPage = Frame(app, height= 640, width=360)
UserMainPage.grid(row=0, column=0, sticky="nsew")



MainPage_label= Label(UserMainPage,image=bg_UserMainPage)
MainPage_label.place(x=0,y=0,relheight=1,relwidth=1)
MainPage_label.pack()

Mainpage_getblood_btn=ctk.CTkButton( UserMainPage,
                            width=273,
                            height=50 , 
                            border=0,
                            text_font= ("Open Sans Bold",15,"bold"),
                            corner_radius= 15, 
                            text="Get Blood",
                            text_color= "white", 
                            fg_color= "#223239", 
                            hover_color="#242424",
                            bg_color="White",
                            command= get_blood)
Mainpage_getblood_btn.place(x=47,y=270)

Mainpage_donateblood_btn=ctk.CTkButton(UserMainPage,
                                width=274,
                                height=50 , 
                                border=0,
                                text_font= ("Open Sans Bold",15,"bold"),
                                corner_radius= 15, 
                                text="Donate Blood",
                                text_color= "white", 
                                fg_color= "#223239", 
                                hover_color="#242424",
                                bg_color="White",
                                command= lambda: MedHistory.tkraise())
Mainpage_donateblood_btn.place(x=47,y=336)

Mainpage_availsearch_btn=ctk.CTkButton(UserMainPage,
                                    width=274,
                                    height=50 , 
                                    corner_radius= 15, 
                                    border=0,
                                    text_font= ("Open Sans Bold",15,"bold"),
                                    text="Blood Availability Search",
                                    text_color= "black", 
                                    fg_color= "#ff585a",
                                    hover_color="#ff3030",
                                    bg_color="White",
                                    command = lambda: BloodAvbty.tkraise())
Mainpage_availsearch_btn.place(x=46,y=408)

Mainpage_updateprof_btn=ctk.CTkButton(UserMainPage,
                                    width=235,
                                    height=60 , 
                                    corner_radius= 15, 
                                    border=0,
                                    text_font= ("Open Sans Bold",15,"bold"),
                                    text="Update Profile",
                                    text_color= "white", 
                                    fg_color= "#223239",
                                    hover_color="#ff3030",
                                    bg_color="#acdcff",
                                    command=lambda: UserInfo.tkraise())
Mainpage_updateprof_btn.place(x=25,y=555)


Mainpage_exit_btn=Button(UserMainPage,
                         width=68,
                         height=65,
                         image=exit_btn,
                         border=0,
                         command= logged_out)
Mainpage_exit_btn.place(x=287,y=550)

welcome_message = Message(UserMainPage,
                          font=('Euphoria Script',16, "bold"),
                          aspect=500,
                          bg="white")
welcome_message.place(x=90,y=110)

Working_message = Message(UserMainPage,
                          font=('Segoe UI',12, "bold"),
                          aspect=325,
                          bg="#e7ded9")
Working_message.place(x=70,y=180)


 
#*************************************************************************************************************#





#*********************************************Blood Availability Search*****************************************#


BloodAvbty = Frame(app, height= 640, width=360)
BloodAvbty.grid(row=0, column=0, sticky="nsew")



BloodAvbty_label= Label(BloodAvbty,image=bg_BloodAvbty)
BloodAvbty_label.place(x=0,y=0,relheight=1,relwidth=1)
BloodAvbty_label.pack()

bas_state = ctk.StringVar(value=states[0])
BloodAvbty_state_drop=ctk.CTkComboBox(BloodAvbty, variable=bas_state,
                                      values=states,
                                      width=150,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9"
                                      
                                      )
BloodAvbty_state_drop.pack()
BloodAvbty_state_drop.place(x=76,y=185)

bas_city = ctk.StringVar(value=cities[0])
BloodAvbty_district_drop=ctk.CTkComboBox(BloodAvbty,variable=bas_city,
                                      values=cities,
                                      width=150,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9"
                                     
                                      )
BloodAvbty_district_drop.pack()
BloodAvbty_district_drop.place(x=76,y=278)


bas_bg = ctk.StringVar(value=blood_groups[0])
BloodAvbty_group_drop=ctk.CTkComboBox(BloodAvbty, variable=bas_bg,
                                      values=blood_groups,
                                      width=150,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9"
                                     
                                      )
BloodAvbty_group_drop.pack()
BloodAvbty_group_drop.place(x=76,y=370)

blood_components = ["select","Plasma","Whole Blood","Platelets"]
bas_bc = ctk.StringVar(value= blood_components[0])
BloodAvbty_comp_drop=ctk.CTkComboBox(BloodAvbty, variable= bas_bc,
                                      values= blood_components,
                                      width=150,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9"
                                      )
BloodAvbty_comp_drop.pack()
BloodAvbty_comp_drop.place(x=82,y=465)

BloodAvbty_srch_btn=ctk.CTkButton(BloodAvbty,
                                   width=280,
                                   height=50,
                                   corner_radius=5,
                                   text = "Search",
                                   border =0,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#223239",
                                   hover_color="black",
                                   command = search_Aval)
BloodAvbty_srch_btn.place(x=45,y=552)

BloodAvbty_cancel_btn=ctk.CTkButton(BloodAvbty,
                                   width=20,
                                   height=20,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "X",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command= lambda: UserMainPage.tkraise())
BloodAvbty_cancel_btn.place(x=300,y=20)



#*************************************************************************************************************#




#*********************************************User Info ******************************************************#


UserInfo = Frame(app, height= 640, width=360)
UserInfo.grid(row=0, column=0, sticky="nsew")

#page background label
UserInfo_label= Label(UserInfo,image=bg_UserInfo)
UserInfo_label.place(x=0,y=0,relheight=1,relwidth=1)
UserInfo_label.pack()

#age entrybox
UserInfo_Age=Entry(UserInfo,
                    width=15,
                    font=('Georgia',15),
                    borderwidth=0,
                    fg="black",
                    bg="white",
                    )
UserInfo_Age.pack()
UserInfo_Age.place(x=155,y=174)

#gender entry box
UserInfo_Gender=Entry(UserInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )
UserInfo_Gender.pack()
UserInfo_Gender.place(x=155,y=220)

#Address entry box
UserInfo_address=Entry(UserInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )
UserInfo_address.pack()
UserInfo_address.place(x=155,y=276)
#City drop box
cities = ["select","Sangli","Satara","Kolhapur","Solapur","Surat","Mumbai","Pune"]
usr_city = ctk.StringVar(value=cities[0])
UserInfo_City_drop=ctk.CTkComboBox(UserInfo, variable= usr_city,
                                      values=cities,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9"
                                     )
UserInfo_City_drop.pack()
UserInfo_City_drop.place(x=155,y=330)

#State drop box
states = ["select","Gujarat","Maharashtra","Delhi"]
usr_state = ctk.StringVar(value=states[0])
UserInfo_State_drop=ctk.CTkComboBox(UserInfo, variable=usr_state,
                                      values=states,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15,),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9",
                                      )
UserInfo_State_drop.pack()
UserInfo_State_drop.place(x=155,y=390)


#Pincode entry box
UserInfo_Pincode=Entry(UserInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )
UserInfo_Pincode.pack()
UserInfo_Pincode.place(x=155,y=442)

#Addharno entry box
UserInfo_aadharno=Entry(UserInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )
UserInfo_aadharno.pack()
UserInfo_aadharno.place(x=155,y=489)

blood_groups = ["select","A+","A-","B+","B-","AB+","AB-","O+","O-"]
usrinfo_bgroup = ctk.StringVar(value = blood_groups[0])
UserInfo_bgroup_drop= ctk.CTkComboBox(UserInfo, variable= usrinfo_bgroup,
                                      values=blood_groups,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9")
UserInfo_bgroup_drop.pack()
UserInfo_bgroup_drop.place(x=155,y=535)

#Update button
UserInfo_update_btn=ctk.CTkButton(UserInfo,
                                   width=300,
                                   height=50,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "Update",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#223239",
                                   hover_color="black",
                                   command= update_user_info)
UserInfo_update_btn.place(x=30,y=582)

#cancel Update button
UserInfo_cancel_btn=ctk.CTkButton(UserInfo,
                                   width=20,
                                   height=20,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "X",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command= cancel_update)
UserInfo_cancel_btn.place(x=300,y=20)


#*************************************************************************************************************#








#*******************************************User Medical History**********************************************#



MedHistory = Frame(app, height= 640, width=360)
MedHistory.grid(row=0, column=0, sticky="nsew")


# medical history background label
MedHistory_label= Label(MedHistory,image=bg_MedHistory)
MedHistory_label.place(x=0,y=0,relheight=1,relwidth=1)
MedHistory_label.pack()

#blood group drop down
 
medhis_bgroup = ctk.StringVar(value = blood_groups[0])
MedHistory_bgroup_drop=ctk.CTkComboBox(MedHistory, variable= medhis_bgroup,
                                      values=blood_groups,
                                      width=120,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9")
MedHistory_bgroup_drop.pack()
MedHistory_bgroup_drop.place(x=197,y=222)


options = ["select","yes","no"]
# recent blood donation drop down
recent_dnt = ctk.StringVar(value = options[0])
MedHistory_recdnt_drop = ctk.CTkComboBox(MedHistory, variable=recent_dnt,
                                      values= options,
                                      width=120,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9"
                                      )
MedHistory_recdnt_drop.pack()
MedHistory_recdnt_drop.place(x=197,y=290)

recent_blood_donation = Label(MedHistory,text="(Less than 3 months)",font= ('Georgia', 6,"bold"), bg="#e7ded9")
recent_blood_donation.place(x=40,y=325)




#diabetes drop down
diabetes = ctk.StringVar(value = options[0])
MedHistory_diabetes_drop=ctk.CTkComboBox(MedHistory, variable= diabetes,
                                      values=options,
                                      width=120,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9")

MedHistory_diabetes_drop.place(x=197,y=352)

#intoxication drop down
intox = ctk.StringVar(value = options[0])
MedHistory_intox_drop=ctk.CTkComboBox(MedHistory, variable= intox,
                                      values=options,
                                      width=120,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9",
                                     )


MedHistory_intox_drop.place(x=197,y=413)
intox_duration = Label(MedHistory,text="(less than 24 hrs)",font= ('Georgia', 6,"bold"), bg="#e7ded9")
intox_duration.place(x=40,y=433)

#tatoo drop down
tattoo = ctk.StringVar(value = options[0])
MedHistory_tattoo_drop=ctk.CTkComboBox(MedHistory, variable= tattoo,
                                      values=options,
                                      width=120,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9")
MedHistory_tattoo_drop.place(x=197, y=470)
tatoo_duration = Label(MedHistory,text="(less than 6 months)",font= ('Georgia', 6,"bold"), bg="#e7ded9")
tatoo_duration.place(x=40,y=490)


#update button
MedHistory_update_btn=ctk.CTkButton(MedHistory,
                                    height=45,
                                    width=286,
                                    fg_color="#223239",
                                    text="Update",
                                    text_color="white",
                                    bg_color="#e7ded9",
                                    border =0,
                                    text_font= ("Open Sans Bold",15,"bold"),
                                    hover_color="black",
                                    corner_radius=15,
                                    command= donate_blood)
MedHistory_update_btn.place(x=35,y=549)

#cancel Update button
blood_dnt_cancel_btn=ctk.CTkButton(MedHistory,
                                   width=20,
                                   height=20,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "X",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command= lambda: UserMainPage.tkraise())
blood_dnt_cancel_btn.place(x=300,y=20)


#*************************************************************************************************************#


LoginPage.tkraise()
app.mainloop()



