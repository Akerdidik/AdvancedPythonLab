import json
import os

# md5,sha1,sha256
import hashlib

# User data class;
class User:
    def __init__(self,username,name,surname,age,password):
        self.username=username
        self.name=name
        self.surname=surname
        self.age=age
        self.hashpass=password

    # Getter functions for simplifying work in Auth class;
    def getter_username(self):
        return self.username

    def getter_name(self):
        return self.name

    def getter_surname(self):
        return self.surname

    def getter_age(self):
        return self.age

    def getter_hashpass(self):
        return self.hashpass

# Authenticate class;
class Auth:
    def login(self,User):
        keys = {User.getter_username():{"name":User.getter_name(),"surname":User.getter_surname(),"age":User.getter_age(),"password":User.getter_hashpass()}}
        with open('users.json','r') as j:
            info = json.load(j)
        flag = False
        for els in info:
            if els == next(iter(keys)):
                for k,v in info[els].items():
                    if v == keys[next(iter(keys))][k]:
                        flag = True
        if not flag:
            return "Invalid username or password!"
        else:
            return "Successfull logon!"

    def register(self,User):
        keys = {User.getter_username():{"name":User.getter_name(),"surname":User.getter_surname(),"age":User.getter_age(),"password":User.getter_hashpass()}}
        with open('users.json','r') as j:
            info = json.load(j)
            for els in info:
                if els == next(iter(keys)):
                    return "This username exist! Try again!"
            info.update(keys)
        with open('users.json','w') as j:
            json.dump(info,j,indent=4)
        return 'Registered!'

    def hash_password(self,password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()
# main function;
def main():
    a = Auth()
    choice = input("Choose options [R] = Register, [L] = Login\n")
    if choice == "R":
        u = input("Username: ")
        n = input("Name: ")
        s = input("Surname: ")
        ag = input("Age: ")
        p = input("Password: ")
        h = a.hash_password(p)
        person = User(u,n,s,ag,h)
        print(a.register(person))
    elif choice == "L":
        u = input("Username: ")
        p = input("Password: ")
        h = hashlib.md5(p.encode('utf-8')).hexdigest()
        #print(h)
        person = User(u,"","","",h)
        res = a.login(person)
        if res == "Successfull logon!":
            status = ""
            if u=="admin":
                status="'root'"
            else:
                status="'default user'"
            print("Welcome " + u + " to the system!")
            print("Your currently status is " + status + "!" )
            ins = input("Would you like to change password [Yes/No]: \n")
            if ins == "Yes":
                new_pass = input("Write new password: ")
                has = a.hash_password(new_pass)
                with open('users.json','r') as j:
                    info = json.load(j)
                for els in info:
                    if els == u:
                        info[els]['password'] = has
                        with open('users.json','w') as t:
                            json.dump(info,t,indent=4)
                        print("Succesfully changed password!")
                        break
            elif ins == "No":
                print("Bye!")
            else:
                print("Invalid option!")
        else:
            print(res)
    else:
        print("Invalid option!")

# main runner;
if __name__=="__main__":
    main()
