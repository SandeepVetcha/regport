from tkinter import *
from tkinter import messagebox
import shelve

class Person:
    def __init__(self, username, password, role, subjects=None):
        if subjects is None:
            subjects = []
        self.username = username
        self.password = password
        self.role = role
        self.subjects = subjects

    def __str__(self):
        return f"{self.username}({self.role})"

    def printDetails(self):
        print(self.username, self.role, self.subjects)

class Teacher(Person):
    def __init__(self, username, password, role, department, subjects):
        super().__init__(username, password, role, subjects)
        self.department = department
        self.consecutive_wrong_attempts = 0

    def printDetails(self):
        print(self.username, self.role, self.department, self.subjects)

class UGStudent(Person):
    def __init__(self, username, password, role, department, year_of_graduation, subjects):
        super().__init__(username, password, role, subjects)
        self.department = department
        self.year_of_graduation = year_of_graduation
        self.consecutive_wrong_attempts = 0

    def printDetails(self):
        print(self.username, self.role, self.department, self.year_of_graduation, self.subjects)

class PGStudent(Person):
    def __init__(self, username, password, role, department, subjects):
        super().__init__(username, password, role, subjects)
        self.department = department
        self.consecutive_wrong_attempts = 0

    def printDetails(self):
        print(self.username, self.role, self.department, self.subjects)

def loadDetails():
    with shelve.open("user_details") as db:
        return list(db.values())

def saveDetails(details):
    with shelve.open("user_details") as db:
        db.clear()
        for user in details:
            db[user.username] = user

listOfDetails = loadDetails()
window_stack = []

def signUp():
    userSignUp()

def signIn():
    userSignIn()

def userSignUp():
    if window_stack:
        window_stack[-1].withdraw()

    signupWindow = Tk()
    window_stack.append(signupWindow)
    signupWindow.geometry("500x600")
    signupWindow.title("Sign Up")
    signupWindow.configure(bg="#A4C330")

    frame1 = Frame(signupWindow, bg="#A4C330")
    frame1.pack(side=TOP, pady=10)

    frame2 = Frame(signupWindow, bg="#A4C330")
    frame2.pack(side=TOP, pady=10)

    frame3 = Frame(signupWindow, bg="#A4C330")
    frame3.pack(side=TOP, pady=10)

    label_user = Label(frame1, text="Enter your email ID:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
    label_user.pack(side=TOP)

    entry_user = Entry(frame1, font=("Helvetica", 10))
    entry_user.pack(side=TOP)

    label_pass = Label(frame2, text="Enter your password:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
    label_pass.pack(side=TOP)

    entry_pass = Entry(frame2, font=("Helvetica", 10), show="*")
    entry_pass.pack(side=TOP)

    roles = ["UG Student", "Teacher", "PG Student"]
    selected_role = StringVar()
    selected_role.set(roles[0])

    label_role = Label(frame3, text="Select your role:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
    label_role.pack(side=TOP)

    option_menu = OptionMenu(frame3, selected_role, *roles)
    option_menu.config(font=("Helvetica", 10), bg="#A4C330")
    option_menu.pack(side=TOP)

    additional_details_frame = Frame(signupWindow, bg="#A4C330")
    additional_details_frame.pack(side=TOP)

    def displayAdditionalDetails():
        role = selected_role.get()
        clearAdditionalDetailsFrame()

        label_subjects = Label(additional_details_frame, text="Enter your subjects (separated by commas):", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
        label_subjects.pack(side=TOP)

        entry_subjects = Entry(additional_details_frame, font=("Helvetica", 10))
        entry_subjects.pack(side=TOP)

        if role == "Teacher":
            label_department = Label(additional_details_frame, text="Enter your department:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
            label_department.pack(side=TOP)

            entry_department = Entry(additional_details_frame, font=("Helvetica", 10))
            entry_department.pack(side=TOP)

        elif role == "UG Student":
            label_department = Label(additional_details_frame, text="Enter your department:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
            label_department.pack(side=TOP)

            entry_department = Entry(additional_details_frame, font=("Helvetica", 10))
            entry_department.pack(side=TOP)

            label_year_of_graduation = Label(additional_details_frame, text="Enter your year of graduation:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
            label_year_of_graduation.pack(side=TOP)

            entry_year_of_graduation = Entry(additional_details_frame, font=("Helvetica", 10))
            entry_year_of_graduation.pack(side=TOP)

        elif role == "PG Student":
            label_department = Label(additional_details_frame, text="Enter your department:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
            label_department.pack(side=TOP)

            entry_department = Entry(additional_details_frame, font=("Helvetica", 10))
            entry_department.pack(side=TOP)

        submit_details = Button(additional_details_frame, text="Submit", command=lambda: submitSignUp(role, entry_user.get(), entry_pass.get(), entry_department.get(), entry_year_of_graduation.get() if role == "UG Student" else "", entry_subjects.get().split(',')), font=("Helvetica", 10))
        submit_details.pack(side=TOP)

    def clearAdditionalDetailsFrame():
        for widget in additional_details_frame.winfo_children():
            widget.destroy()

    def submitSignUp(role, username, password, department, year_of_graduation, subjects):
        def checkUserId():
            flag = 0
            for i, char in enumerate(username):
                if char == '@':
                    x = username[i:]
                    if x in ['@gmail.com', '@outlook.com', '@gmail.cc', '@kgpian.iitkgp.ac.in']:
                        print("User ID valid.")
                        flag = 1
            if flag == 0:
                messagebox.showinfo("Can't use this", "Email ID Invalid.")
                return False
            return True

        def checkPassword():
            if len(password) < 8:
                messagebox.showinfo("Password is bad", "Password is too weak.")
                return False
            elif len(password) > 12:
                messagebox.showinfo("Password is bad", "Password is too long.")
                return False
            else:
                a = b = c = 0
                for x in password:
                    if 'A' <= x <= 'Z':
                        a = 1
                    elif 'a' <= 'z':
                        b = 1
                    elif x == ' ':
                        messagebox.showinfo("Password is bad", "Password can't have spaces.")
                        return False
                    else:
                        c = 1
                if a == 0:
                    messagebox.showinfo("Password is bad", "Password needs to have at least one upper case letter.")
                    return False
                elif b == 0:
                    messagebox.showinfo("Password is bad", "Password needs to have at least one lower case letter.")
                    return False
                elif c == 0:
                    messagebox.showinfo("Password is bad", "Password needs to have at least one symbol.")
                    return False
                else:
                    print("Password accepted")
                    return True

        if not checkUserId() or not checkPassword():
            return

        if role == "Teacher":
            user_instance = Teacher(username, password, role, department, subjects)
        elif role == "UG Student":
            user_instance = UGStudent(username, password, role, department, int(year_of_graduation), subjects)
        elif role == "PG Student":
            user_instance = PGStudent(username, password, role, department, subjects)

        listOfDetails.append(user_instance)
        saveDetails(listOfDetails)
        messagebox.showinfo("Success", "Account successfully created!")

    displayAdditionalDetails()

    def back():
        signupWindow.destroy()
        window_stack.pop()
        if window_stack:
            window_stack[-1].deiconify()

    back_button = Button(signupWindow, text="Back", command=back, font=("Helvetica", 10))
    back_button.pack(side=BOTTOM, pady=10)

    signupWindow.mainloop()

def userSignIn():
    if window_stack:
        window_stack[-1].withdraw()

    signinWindow = Tk()
    window_stack.append(signinWindow)
    signinWindow.geometry("500x500")
    signinWindow.title("Sign In")
    signinWindow.configure(bg="#A4C330")

    frame1 = Frame(signinWindow, bg="#A4C330")
    frame1.pack(side=TOP, pady=10)

    frame2 = Frame(signinWindow, bg="#A4C330")
    frame2.pack(side=TOP, pady=10)

    label_user = Label(frame1, text="Enter your email ID:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
    label_user.pack(side=TOP)

    entry_user = Entry(frame1, font=("Helvetica", 10))
    entry_user.pack(side=TOP)

    label_pass = Label(frame2, text="Enter your password:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
    label_pass.pack(side=TOP)

    entry_pass = Entry(frame2, font=("Helvetica", 10), show="*")
    entry_pass.pack(side=TOP)

    def authenticateUser():
        username = entry_user.get()
        password = entry_pass.get()

        for user in listOfDetails:
            if user.username == username and user.password == password:
                messagebox.showinfo("Success", "Login successful!")
                mainPage(user)
                signinWindow.destroy()
                return
        messagebox.showerror("Error", "Invalid username or password")

    submit_button = Button(signinWindow, text="Sign In", command=authenticateUser, font=("Helvetica", 10))
    submit_button.pack(side=TOP, pady=20)

    def back():
        signinWindow.destroy()
        window_stack.pop()
        if window_stack:
            window_stack[-1].deiconify()

    back_button = Button(signinWindow, text="Back", command=back, font=("Helvetica", 10))
    back_button.pack(side=BOTTOM, pady=10)

    signinWindow.mainloop()

def mainPage(user):
    if window_stack:
        window_stack[-1].withdraw()

    mainWindow = Tk()
    window_stack.append(mainWindow)
    mainWindow.geometry("500x500")
    mainWindow.title("Main Page")
    mainWindow.configure(bg="#A4C330")

    frame1 = Frame(mainWindow, bg="#A4C330")
    frame1.pack(side=TOP, pady=10)

    label_user = Label(frame1, text=f"Welcome, {user.username}!", font=('Arial', 20, 'bold'), fg='black', bg="#A4C330")
    label_user.pack(side=TOP)

    frame2 = Frame(mainWindow, bg="#A4C330")
    frame2.pack(side=TOP, pady=10)

    def viewProfile():
        if window_stack:
            window_stack[-1].withdraw()

        profileWindow = Tk()
        window_stack.append(profileWindow)
        profileWindow.geometry("500x500")
        profileWindow.title("Profile Info")
        profileWindow.configure(bg="#A4C330")

        frame1 = Frame(profileWindow, bg="#A4C330")
        frame1.pack(side=TOP, pady=10)

        details = f"Username: {user.username}\nRole: {user.role}\nDepartment: {user.department}\nSubjects: {', '.join(user.subjects)}"
        if isinstance(user, UGStudent):
            details += f"\nYear of Graduation: {user.year_of_graduation}"

        label_details = Label(frame1, text=details, font=('Arial', 12, 'bold'), fg='black', bg="#A4C330")
        label_details.pack(side=TOP)

        def back():
            profileWindow.destroy()
            window_stack.pop()
            if window_stack:
                window_stack[-1].deiconify()

        back_button = Button(profileWindow, text="Back", command=back, font=("Helvetica", 10))
        back_button.pack(side=BOTTOM, pady=10)

        profileWindow.mainloop()

    def updateUser():
        if window_stack:
            window_stack[-1].withdraw()

        updateWindow = Tk()
        window_stack.append(updateWindow)
        updateWindow.geometry("500x600")
        updateWindow.title("Update Profile")
        updateWindow.configure(bg="#A4C330")

        frame1 = Frame(updateWindow, bg="#A4C330")
        frame1.pack(side=TOP, pady=10)

        frame2 = Frame(updateWindow, bg="#A4C330")
        frame2.pack(side=TOP, pady=10)

        frame3 = Frame(updateWindow, bg="#A4C330")
        frame3.pack(side=TOP, pady=10)

        frame4 = Frame(updateWindow, bg="#A4C330")
        frame4.pack(side=TOP, pady=10)

        frame5 = Frame(updateWindow, bg="#A4C330")
        frame5.pack(side=TOP, pady=10)

        frame6 = Frame(updateWindow, bg="#A4C330")
        frame6.pack(side=TOP, pady=10)

        label_user = Label(frame1, text="Enter new username:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
        label_user.pack(side=TOP)

        entry_user = Entry(frame1, font=("Helvetica", 10))
        entry_user.insert(0, user.username)
        entry_user.pack(side=TOP)

        label_pass = Label(frame2, text="Enter new password:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
        label_pass.pack(side=TOP)

        entry_pass = Entry(frame2, font=("Helvetica", 10), show="*")
        entry_pass.insert(0, user.password)
        entry_pass.pack(side=TOP)

        label_department = Label(frame3, text="Enter new department:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
        label_department.pack(side=TOP)

        entry_department = Entry(frame3, font=("Helvetica", 10))
        entry_department.insert(0, user.department)
        entry_department.pack(side=TOP)

        label_subjects = Label(frame4, text="Enter new subjects (separated by commas):", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
        label_subjects.pack(side=TOP)

        entry_subjects = Entry(frame4, font=("Helvetica", 10))
        entry_subjects.insert(0, ','.join(user.subjects))
        entry_subjects.pack(side=TOP)

        if isinstance(user, UGStudent):
            label_year_of_graduation = Label(frame5, text="Enter new year of graduation:", font=('Arial', 10, 'bold'), fg='black', bg="#A4C330")
            label_year_of_graduation.pack(side=TOP)

            entry_year_of_graduation = Entry(frame5, font=("Helvetica", 10))
            entry_year_of_graduation.insert(0, user.year_of_graduation)
            entry_year_of_graduation.pack(side=TOP)

        def submitUpdate():
            new_username = entry_user.get()
            new_password = entry_pass.get()
            new_department = entry_department.get()
            new_subjects = entry_subjects.get().split(',')
            new_year_of_graduation = entry_year_of_graduation.get() if isinstance(user, UGStudent) else ""

            if new_username:
                user.username = new_username
            if new_password:
                user.password = new_password
            if new_department:
                user.department = new_department
            if new_subjects:
                user.subjects = new_subjects
            if isinstance(user, UGStudent) and new_year_of_graduation:
                user.year_of_graduation = int(new_year_of_graduation)

            saveDetails(listOfDetails)
            messagebox.showinfo("Success", "Profile updated successfully!")
            updateWindow.destroy()
            if window_stack:
                window_stack.pop()
            if window_stack:
                window_stack[-1].deiconify()

        submit_button = Button(frame6, text="Submit", command=submitUpdate, font=("Helvetica", 10))
        submit_button.pack(side=TOP)

        def back():
            updateWindow.destroy()
            window_stack.pop()
            if window_stack:
                window_stack[-1].deiconify()

        back_button = Button(updateWindow, text="Back", command=back, font=("Helvetica", 10))
        back_button.pack(side=BOTTOM, pady=10)

        updateWindow.mainloop()

    def deleteUser():
        listOfDetails.remove(user)
        saveDetails(listOfDetails)
        messagebox.showinfo("Deleted", "Profile deleted successfully")
        mainWindow.destroy()
        if window_stack:
            window_stack.pop()
        if window_stack:
            window_stack[-1].deiconify()

    view_button = Button(frame2, text="View Profile", command=viewProfile, font=("Helvetica", 10))
    view_button.pack(side=LEFT, padx=10)

    update_button = Button(frame2, text="Update Profile", command=updateUser, font=("Helvetica", 10))
    update_button.pack(side=LEFT, padx=10)

    delete_button = Button(frame2, text="Delete Profile", command=deleteUser, font=("Helvetica", 10))
    delete_button.pack(side=RIGHT, padx=10)

    def back():
        mainWindow.destroy()
        window_stack.pop()
        if window_stack:
            window_stack[-1].deiconify()

    back_button = Button(mainWindow, text="Back", command=back, font=("Helvetica", 10))
    back_button.pack(side=BOTTOM, pady=10)

    mainWindow.mainloop()

mainWindow = Tk()
window_stack.append(mainWindow)
mainWindow.geometry("500x500")
mainWindow.title("Main Menu")
mainWindow.configure(bg="#A4C330")

frame = Frame(mainWindow, bg="#A4C330")
frame.pack(pady=20)

signup_button = Button(frame, text="Sign Up", command=signUp, font=("Helvetica", 12))
signup_button.pack(pady=10)

signin_button = Button(frame, text="Sign In", command=signIn, font=("Helvetica", 12))
signin_button.pack(pady=10)

mainWindow.mainloop()
