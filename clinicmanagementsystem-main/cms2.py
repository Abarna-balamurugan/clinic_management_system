import pickle
import pandas as pd 
from datetime import date,timedelta

class Medicine:

    def __init__(self,*args):
        self.id = args[0]
        self.name = args[1]
        self.type = args[2]
        l = args[3].split('-')
        self.doe = date(int(l[2]),int(l[1]),int(l[0]))
        self.Total = args[4]
        self.used = args[5]
        self.stock = args[6]
        self.cost = args[7]

    def __str__(self):
        return self.name

class Med_Data:
    def __init__(self):
        self.m = []
        self.load_data()

    def load_data(self):

        df = pd.read_csv("med.csv")
        print(df)
        for i in range (len(df)):
            m1 = Medicine(df.loc[i,"ID"],df.loc[i,"Name"],df.loc[i,"Type"],df.loc[i,"DOE"],df.loc[i,"Total"],df.loc[i,"Used"],df.loc[i,"Stock"],df.loc[i,"Cost"])
            self.add_med(m1)

    def add_med(self,me:Medicine):
        self.m.append(me)

    def __str__(self):
        s = '['
        for i in self.m:
            s+=i.name
            s+=','
        s+=']'
        return s

    def med_expired(self):
        return med_iter_exp(self.m)
    
    def med_stock(self):
        return med_iter_stock(self.m)
    
    def med_no_stock(self):
        return med_iter_no_stock(self.m)
    
    def med_close_expired(self):
        return med_iter_close_exp(self.m)

class med_iter_no_stock:
    def __init__(self,l):
        self.l = [i for i in l if i.stock==0]
        self.index = 0
        self.len = len(self.l)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.len>self.index:
            a = self.l[self.index]
            self.index+=1
            return a
        else:
            raise StopIteration


class med_iter_stock:
    def __init__(self,l):
        self.l = [i for i in l if i.stock<10]
        self.index = 0
        self.len = len(self.l)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.len>self.index:
            a = self.l[self.index]
            self.index+=1
            return a
        else:
            raise StopIteration

class med_iter_close_exp:

    def __init__(self,l):
        self.l = []
        for i in l:
            if i.doe>date.today() and i.doe<date.today()+timedelta(days=30):
                self.l.append(i)
        #self.l = [i for i in l if i.doe<date.today()+timedelta(days=30) and i.doe>date.today()]
        self.index = 0
        self.len = len(self.l)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.len>self.index:
            a = self.l[self.index]
            self.index+=1
            return a
        else:
            raise StopIteration

class med_iter_exp:
    def __init__(self,l):
        self.l=[]
        for i in l:
            if i.doe<date.today():
                self.l.append(i)
        self.index = 0
        self.len = len(self.l)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.len>self.index:
            a = self.l[self.index]
            self.index+=1
            return a
        else:
            raise StopIteration



def main():
    print("\t\tWELCOME TO CLINIC MANAGEMENT SYSTEM \n")
    
    print("MENU\n")
    print("Select the key for the following")
    print("1 to add a medicine")
    print("2 to view medicines that have less stock")
    print("3 to view medicines that have no stock")
    print("4 to view medicines close to expiry")
    print("5 to view medicines that are expired")

    a = int(input("Enter choice : "))
    m = Med_Data()

    if a==1:
        i = int(input("enter medicine id :"))
        n = input("Enter Name of medicine :")
        ty = input("Enter medicine type :")
        d = input("Enter date of expiry :")
        t = int(input("Enter total number of medicines :"))
        c = int(input("Enter cost :"))
        m.add_med(Medicine(i,n,ty,d,t,0,t,c))
    if a == 2:
        print("medicines that have less stock")
        for i in m.med_stock():
            print(i.id,i.name)

    if a == 3:
        print("medicines that have no  stock")
        for i in m.med_no_stock():
            print(i.id,i.name)
    if a == 4:
        print("medicines close to expiry")
        for i in m.med_close_expired():
            print(i.id,i.name)

    if a == 5:
        print("medicines that are expired")
        for i in m.med_expired():
            print(i.id,i.name,i.doe)

    f = open("med2.csv","wb+")
    pickle.dump(m,f)
main()
