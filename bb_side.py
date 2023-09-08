from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as msc

app = Tk()
app.geometry(f"{363}x{640}+{580}+{120}")
app.configure(bg="#8d1e1e")
app.resizable(0,0)
app.title("Blood Bank Buddy ")

#*************************************************************************************************************#

#**************************************************FUnctions**************************************************#
#signed up
def signedup():
    if len(SBBInfo_Licenseno.get()) != 13:
        messagebox.showwarning("Incorrect Licence No.", "Licence No. Should be 13 digits long",parent=SBBInfo)
        return
    
    if SBBInfo_address.get() == "" or SBBInfo_City.get() == "select" or SBBInfo_State.get() == "select" or SBBInfo_Pincode.get() == "" or SBBInfo_Licenseno.get() == "":
        messagebox.showwarning("Empty Field", "Fields Cant be Empty",parent=SBBInfo)

    else:
         try:
            conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
            cur = conn.cursor()
            cur.execute("Insert into BB_details (BB_username,BB_password,BB_name,BB_address,BB_city,BB_state,BB_pincode,BB_licence_no, `A+`, `A-`,`B+`,`B-`,`AB+`,`AB-`,`O+`,`O-`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                signup_username_entry.get(),
                signup_password_entry.get(),
                signup_name_entry.get(),
                SBBInfo_address.get(),
                SBBInfo_City.get(),
                SBBInfo_State.get(),
                int(SBBInfo_Pincode.get()),
                int(SBBInfo_Licenseno.get()),
                0,0,0,0,0,0,0,0
                )

            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sign Up SuccessFull", "Congratulations! You are signedup successfully !!")
            LoginPage.tkraise()
            signup_name_entry.delete(0,END)
            signup_username_entry.delete(0,END)
            signup_password_entry.delete(0, END)
            signup_cnfpassword_entry.delete(0, END)
            SBBInfo_address.delete(0,END)
            SBBInfo_City.set(value=cities[0])
            SBBInfo_State.set(value=states[0])
            SBBInfo_Pincode.delete(0,END)
            SBBInfo_Licenseno.delete(0,END)

         except Exception as e:
             messagebox.showerror("Error!",f"Error due to {e}")


    
        
    
         

#***************************#
#***************************#

#loged in 
def logedin():
    username = login_username_entry.get()
    password = login_password_entry.get()


    #check in database

    if len(username) == 0 or len(password) == 0:
        messagebox.showwarning("Empty Field", "Fields Cant be Empty")
        return

    try:
        conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
        cur = conn.cursor()
        cur.execute("select * from BB_details where BB_username=%s and BB_password=%s",(username,password))
        row = cur.fetchone()
        if row == None:
            messagebox.showwarning("Bad Entry", "Username or password incorrect")
            login_password_entry.delete(0,END)
            login_username_entry.delete(0,END)
        else:
            
            BBHomepg.tkraise()
            conn.close()

            try:
                conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
                cur = conn.cursor()
                cur.execute("select BB_name, BB_licence_no from BB_details where BB_username=%s and BB_password=%s",(username,password))
                name = cur.fetchone()
                welcome_message.config(text=f"BB: {str(name[0])}\nLicense: {str(name[1])}")

            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {e}",parent=BBHomepg)


    
    except Exception as e:
        messagebox.showerror("Error!",f"Error due to {e}",parent=LoginPage)


#***************************#
#***************************#

#forgot password

def get_pass():
    userid = ar_userid_entry.get()
    license_no = ar_Liscence_entry.get()

    if len(userid) == 0 or len(license_no) == 0:
        messagebox.showwarning("Empty Field", "Fields Cant be Empty")
        return
    
    try:
        conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
        cur = conn.cursor()
        cur.execute("select BB_password from BB_details where BB_username=%s and  BB_licence_no=%s",(userid,int(license_no)))
        row = cur.fetchone()
        password_message.config(text=f"Password: {row[0]}")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error!",f"Incorrect Credentials")



#***************************#
#***************************#




#logout function
def logged_out():
    login_username_entry.delete(0, END)
    login_password_entry.delete(0, END)
    LoginPage.tkraise()
#***************************#
#***************************#

#go to info
def goto_info():
    if len(signup_name_entry.get()) == 0 or len(signup_username_entry.get()) == 0 or len(signup_password_entry.get()) == 0 or len(signup_cnfpassword_entry.get()) == 0 :
        messagebox.showwarning("Empty Field", "Fields Cant be Empty")
        return
    
    if len(signup_username_entry.get()) < 8:
        messagebox.showwarning("Short Username", "Username Should Be Atleast 8 characters Long",parent=SBBInfo)
        return

    if len(signup_password_entry.get()) < 8:
        messagebox.showwarning("Short Password", "Password Should Be Atleast 8 characters Long",parent=SBBInfo)
        return
    
    if signup_password_entry.get() != signup_cnfpassword_entry.get():
        messagebox.showwarning("Missmatch Password", "Passwords Don't match")
        signup_password_entry.delete(0, END)
        signup_cnfpassword_entry.delete(0, END)

    else:
        #add every signup data to database
        SBBInfo.tkraise()

# cancel signup
def cancel_signup():
    LoginPage.tkraise()
    signup_name_entry.delete(0,END)
    signup_username_entry.delete(0,END)
    signup_password_entry.delete(0,END)
    signup_cnfpassword_entry.delete(0,END)
    SBBInfo_address.delete(0,END)
    SBBInfo_Pincode.delete(0,END)
    SBBInfo_Licenseno.delete(0,END)
    SBBInfo_State.set(value= "select")
    SBBInfo_City.set(value= "select")
    

#cancel update
def cancel_update():
    BBHomepg.tkraise()
    BBInfo_address.delete(0,END)
    BBInfo_Pincode.delete(0,END)
    BBInfo_Licenseno.delete(0,END)
    BBInfo_State.set(value= "select")
    BBInfo_City.set(value= "select")



#***************************#
#info updated
def info_updated():
    if len(SBBInfo_Licenseno.get()) != 13:
        messagebox.showwarning("Incorrect Licence No.", "Licence No. Should be 13 digits long",parent=SBBInfo)
        return
    
    if BBInfo_address.get() == "" or BBInfo_City.get() == "select" or BBInfo_State.get() == "select" or BBInfo_Pincode.get() == "" or BBInfo_Licenseno.get() == 0:
        messagebox.showwarning("Empty Field", "Fields Cant be Empty",parent=BBInfo)

    else:
        try:
            conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
            cur = conn.cursor()
            cur.execute("UPDATE BB_details SET BB_address=%s,BB_city=%s,BB_state=%s,BB_pincode=%s,BB_licence_no=%s WHERE BB_username = %s ", (
                
                BBInfo_address.get(),
                BBInfo_City.get(),
                BBInfo_State.get(),
                int(BBInfo_Pincode.get()),
                int(BBInfo_Licenseno.get()),
                login_username_entry.get()
                )


            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Update SuccessFull", "Values have been updated successfully !!")
            BBHomepg.tkraise()
            BBInfo_address.delete(0,END)
            BBInfo_City.set(value=cities[0])
            BBInfo_State.set(value=states[0])
            BBInfo_Pincode.delete(0,END)
            BBInfo_Licenseno.delete(0,END)

        except Exception as e:
             messagebox.showerror("Error!",f"Error due to {e}")


#*******************#
#update blood stock
def bs_updated():
    if update_bg.get() == "select" or BB_updatebs_qty_entry.get() == "":
        messagebox.showwarning("Empty Field", "Fields Cant be Empty")
    
    else:
        try:
            conn = msc.connect(host = "127.0.0.1", password="chocolate", username= "gmmr", database= "blood_buddy")
            cur = conn.cursor()
            cur.execute(f"UPDATE BB_details SET `{update_bg.get()}`=%s WHERE BB_username = %s ", (
                
                int(BB_updatebs_qty_entry.get()),
                login_username_entry.get()
                )


            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Update SuccessFull", "Values have been updated successfully !!")
            BBHomepg.tkraise()
            update_bg.set( value=blood_groups[0])
            BB_updatebs_qty_entry.delete(0,END)
            
        except Exception as e:
             messagebox.showerror("Error!",f"Error due to {e}") 


#*************************************************************************************************************#
#*************************************************************************************************************#
#*************************************************************************************************************#








#*********************************************Define All Images*************************************************#

bg_login = PhotoImage(file="login.png")
bg_signup = PhotoImage(file="signup.png")
bg_about = PhotoImage(file="about.png")
bg_BBMainPage = PhotoImage(file="bbmainpage.png")
bg_BBInfo = PhotoImage(file="bbinfo.png")
bg_BB_updatebs=PhotoImage(file="updatebgqty.png")
bg_BB_setcamp=PhotoImage(file="BBsetupcamp.png")
bg_acc_recovery=PhotoImage(file="accrecoverybb.png")


#exit btn
BB_exit_btn = PhotoImage(file="bbexitBtn.png")




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
                                 command= goto_info
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


#*************************************************BB Info @ Signup********************************************#

SBBInfo = Frame(app, height= 640, width=360)
SBBInfo.grid(row=0, column=0, sticky="nsew")


#bbinfo background
SBBInfo_label= Label(SBBInfo,image=bg_BBInfo)
SBBInfo_label.place(x=0,y=0,relheight=1,relwidth=1)
SBBInfo_label.pack()

#Address entry box
SBBInfo_address=Entry(SBBInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )

SBBInfo_address.place(x=150,y=230)
#City drop box
cities = ["Select","Sangli","Satara","Kolhapur","Solapur","Surat","Mumbai","Pune"]
SBBInfo_City = ctk.StringVar(value = cities[0])
SBBInfo_City_drop=ctk.CTkComboBox(SBBInfo,
                                      values=cities, variable= SBBInfo_City,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9",
                                      dropdown_color="lightgrey")

SBBInfo_City_drop.place(x=150,y=280)

#State drop box

states = ["select","Gujarat","Maharashtra","Delhi"]
SBBInfo_State = ctk.StringVar(value= states[0])
SBBInfo_State_drop=ctk.CTkComboBox(SBBInfo,
                                      values=states, variable=SBBInfo_State,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15,),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9",
                                      dropdown_color="lightgrey")

SBBInfo_State_drop.place(x=150,y=330)


#Pincode entry box
SBBInfo_Pincode=Entry(SBBInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )

SBBInfo_Pincode.place(x=150,y=378)

#Licenseno entry box
SBBInfo_Licenseno=Entry(SBBInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
)
SBBInfo_Licenseno.place(x=150,y=429)

#Signup button

SBBInfo_signup_btn=ctk.CTkButton(SBBInfo,
                                   width=300,
                                   height=50,
                                   corner_radius=18,
                                   text = "Sign Up!",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#223239",
                                   hover_color="black",
                                   command =  signedup)
SBBInfo_signup_btn.place(x=30,y=500)

SBBInfo_cancel_btn=ctk.CTkButton(SBBInfo,
                                   width=300,
                                   height=50,
                                   corner_radius=18,
                                   text = "Cancel",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command =  cancel_signup)
SBBInfo_cancel_btn.place(x=30,y=582)



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
ar_Liscence_entry = Entry(AccRecovery, width=15, font="Ariel 14", bg="#CBEFFF",borderwidth=0)
ar_Liscence_entry.place(x=167,y=370)


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

#***************************************** BB Main Page******************************************************#
BBHomepg = Frame(app, height= 640, width=360)
BBHomepg.grid(row=0, column=0, sticky="nsew")





BBHomepg_label= Label(BBHomepg,image=bg_BBMainPage)
BBHomepg_label.place(x=0,y=0,relheight=1,relwidth=1)
BBHomepg_label.pack()


#creating update blood stock button
BBHomepg_updatebst_btn=ctk.CTkButton(BBHomepg,
                                    height=45,
                                    width=275,
                                    fg_color="#223239",
                                    text_color="white",
                                    text_font= ("Open Sans Bold",15,"bold"),
                                    text="Update Blood Stock",
                                    bg_color="white",
                                    hover_color="black",
                                    corner_radius=15,
                                    command=lambda: BB_updatebs.tkraise())
BBHomepg_updatebst_btn.place(x=46,y=345)
                       
#creating setup blood camp button
BBHomepg_bldcamp_btn=ctk.CTkButton(BBHomepg,
                                    height=48,
                                    width=275,
                                    fg_color="#223239",
                                    text="Setup Blood Camp",
                                    text_color="white",
                                    text_font= ("Open Sans Bold",15,"bold"),
                                    bg_color="white",
                                    hover_color="black",
                                    corner_radius=15,
                                    command=lambda: BB_setcamp.tkraise())
BBHomepg_bldcamp_btn.place(x=46,y=429)

#Update BloodBank details button
BBHomepg_bbdetails_btn=ctk.CTkButton(BBHomepg,
                                     height=49,
                                     width=262,
                                     fg_color="#223239",
                                     text_color= "white",
                                     text_font=("Open Sans Bold",12,"bold"),
                                     text="Update Blood Bank Details",
                                     bg_color="#e7ded9",
                                     hover_color="black",
                                     corner_radius=15,
                                     command= lambda: BBInfo.tkraise())
BBHomepg_bbdetails_btn.place(x=15,y=554)

#bb home page exit button
Mainpage_exit_btn=Button(BBHomepg,
                         width=68,
                         height=65,
                         image=BB_exit_btn,
                         border=0,
                         command=logged_out)
Mainpage_exit_btn.place(x=287,y=550)

welcome_message = Message(BBHomepg,
                          font=('Bahnschrift',14, "bold"),
                          aspect=500,
                          bg="#e7ded9")
welcome_message.place(x=75,y=170)

Working_message = Message(BBHomepg,
                          font=('Georgia',10),
                          aspect=325,
                          bg="#e7ded9")
Working_message.place(x=70,y=180)


#*************************************************************************************************************#


#*************************************************BB Info Update********************************************#

BBInfo = Frame(app, height= 640, width=360)
BBInfo.grid(row=0, column=0, sticky="nsew")


#bbinfo background
BBInfo_label= Label(BBInfo,image=bg_BBInfo)
BBInfo_label.place(x=0,y=0,relheight=1,relwidth=1)
BBInfo_label.pack()

#Address entry box
BBInfo_address=Entry(BBInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )

BBInfo_address.place(x=150,y=230)
#City drop box
cities = ["Select","Sangli","Satara","Kolhapur","Solapur","Surat","Mumbai","Pune"]
BBInfo_City = ctk.StringVar(value = cities[0])
BBInfo_City_drop=ctk.CTkComboBox(BBInfo,
                                      values=cities, variable= BBInfo_City,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9",
                                      dropdown_color="lightgrey")

BBInfo_City_drop.place(x=150,y=280)

#State drop box

states = ["select","Gujarat","Maharashtra","Delhi"]
BBInfo_State = ctk.StringVar(value= states[0])
BBInfo_State_drop=ctk.CTkComboBox(BBInfo,
                                      values=states, variable=BBInfo_State,
                                      width=180,
                                      height=25,
                                      text_font=('Georgia',15,),
                                      border_width=0,
                                      fg_color="white",
                                      bg_color="#e7ded9",
                                      dropdown_color="lightgrey")

BBInfo_State_drop.place(x=150,y=330)


#Pincode entry box
BBInfo_Pincode=Entry(BBInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
                            )

BBInfo_Pincode.place(x=150,y=378)

#Licenseno entry box
BBInfo_Licenseno=Entry(BBInfo,
                            width=15,
                            font=('Georgia',15),
                            borderwidth=0,
                            fg="black",
                            bg="white",
)
BBInfo_Licenseno.place(x=150,y=429)

#update button

BBInfo_update_btn=ctk.CTkButton(BBInfo,
                                   width=300,
                                   height=50,
                                   corner_radius=18,
                                   text = "Update",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#223239",
                                   hover_color="black",
                                   command =  info_updated)
BBInfo_update_btn.place(x=30,y=500)

#cancel button
BBInfo_cancel_btn=ctk.CTkButton(BBInfo,
                                   width=300,
                                   height=50,
                                   corner_radius=18,
                                   text = "Cancel",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command = cancel_update)
BBInfo_cancel_btn.place(x=30,y=582)



#*************************************************************************************************************#


#*******************************************Update Blood Stock************************************************#

BB_updatebs = Frame(app, height= 640, width=360)
BB_updatebs.grid(row=0, column=0, sticky="nsew")

BB_updatebs_label= Label(BB_updatebs,image=bg_BB_updatebs)
BB_updatebs.place(x=0,y=0,relheight=1,relwidth=1)
BB_updatebs_label.pack()

 #creating update blood stockbutton
BB_updatebs_updbldstck_btn=ctk.CTkButton(BB_updatebs,
                                        height=49,
                                        width=290,
                                        text_font= ("Open Sans Bold",15,"bold"),
                                        text_color="white",
                                        fg_color="#223239",
                                        text="Update",
                                        bg_color="white",
                                        hover_color="black",
                                        corner_radius=15,
                                        command= bs_updated)
BB_updatebs_updbldstck_btn.place(x=43,y=434)

blood_groups = ["select","A+","A-","B+","B-","AB+","AB-","O+","O-"]
update_bg = ctk.StringVar(value=blood_groups[0])
BB_updatebs_bgroup_drop=ctk.CTkComboBox(BB_updatebs, variable=update_bg,
                                      values= blood_groups,
                                      width=150,
                                      height=25,
                                      text_font=('Georgia',15),
                                      border_width=0,
                                      fg_color="#CBEFFF",
                                      bg_color="#e7ded9",
                                      dropdown_color="white")
BB_updatebs_bgroup_drop.pack()
BB_updatebs_bgroup_drop.place(x=165,y=290)

#creating quantity button
BB_updatebs_qty_entry = Entry(BB_updatebs, width=11, font="Ariel 14", bg="#CBEFFF",borderwidth=0)
BB_updatebs_qty_entry.place(x=165,y=365)


#cancel updatebs button
BB_updatebs_cancel_btn=ctk.CTkButton(BB_updatebs,
                                   width=20,
                                   height=20,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "X",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command= lambda: BBHomepg.tkraise())
BB_updatebs_cancel_btn.place(x=280,y=530)

#*************************************************************************************************************#

#************************************************Set Blood Camp***********************************************#

BB_setcamp = Frame(app, height= 640, width=360)
BB_setcamp.grid(row=0, column=0, sticky="nsew")

BB_setcamp_label= Label(BB_setcamp,image=bg_BB_setcamp)
BB_setcamp.place(x=0,y=0,relheight=1,relwidth=1)
BB_setcamp_label.pack()

#  #creating update setupcamp
BB_setcamp_updatebtn=ctk.CTkButton(BB_setcamp,
                                        height=50,
                                        width=310,
                                        text_font= ("Open Sans Bold",15,"bold"),
                                        text_color="white",
                                        fg_color="#223239",
                                        text="Update",
                                        bg_color="#e7ded9",
                                        hover_color="black",
                                        corner_radius=15)
BB_setcamp_updatebtn.place(x=30,y=558)


            

# #creating blood bank name button
BB_setcamp_bcname_entry = Entry(BB_setcamp, width=18, font="Ariel 11", bg="#e7ded9",borderwidth=0)
BB_setcamp_bcname_entry.place(x=175,y=274)

#creating blood bank address button
BB_setcamp_bcadd_entry = Entry(BB_setcamp, width=18, font="Ariel 11", bg="#e7ded9",borderwidth=0)
BB_setcamp_bcadd_entry.place(x=175,y=347)

#creating blood bank pincode button
BB_setcamp_bcpin_entry = Entry(BB_setcamp, width=18, font="Ariel 11", bg="#e7ded9",borderwidth=0)
BB_setcamp_bcpin_entry.place(x=175,y=430)

#cancel updatebs button
BB_updatebs_cancel_btn=ctk.CTkButton(BB_setcamp,
                                   width=20,
                                   height=20,
                                   corner_radius=18,
                                   text_font= ("Open Sans Bold",15,"bold"),
                                   text = "X",
                                   text_color= "white",
                                   bg_color= "#e7ded9",
                                   fg_color="#ff585a",
                                   hover_color="#cf2e38",
                                   command= lambda: BBHomepg.tkraise())
BB_updatebs_cancel_btn.place(x=280,y=520)

#*************************************************************************************************************#


LoginPage.tkraise()
app.mainloop()