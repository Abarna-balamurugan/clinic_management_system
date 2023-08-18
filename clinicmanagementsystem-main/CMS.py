import pandas as pd 
from datetime import datetime 
from datetime import date 
from datetime import timedelta
class Med_Data(): #parent class 
    ''''Managing the main table'''

    def __init__(self,path):
        '''Constructor'''
        self.df = pd.read_csv(path).dropna()             #the dataframe 
        self.data = self.df.values.tolist()              #obtaining all the rows in the form of a list to do list based operations 
        self.size = len(self.data)
        self.columns = ["ID","Name","Type","DOE","Total","Used","Stock","Cost"]   #columns in the table 
        self.path = path
        #self.links = dict(zip(self.df.index,self.df["DOE"]))
        self.pq = pq(self.df)
        #self.meds = sorted(list(self.df["Name"]))  #storing the path of the csv file to make it easily accessible through other methods 

    def __len__(self):
        return self.size  
    
    def __save__(self):
        '''Saving the csv file'''
        self.df.to_csv(path,encoding = 'utf-8',index = False)     
    
    def __str__(self):
        '''Printing the table'''
        return self.df

    def __read__(self):
        '''Reading the csv file. this is mainly done so that the table changes gets constantly updated in the dataframe'''
        read_df = pd.read_csv(self.path).dropna()
        self.df = read_df 

    def __write__(self):
        '''Writing into the csv file'''
        new_df = pd.DataFrame(self.data,columns=self.columns)
        new_df.to_csv(self.path,index=False)

    def add(self,id,name,type,doe,used,stock,cost):
        '''Adding to the csv file'''
        for i in self.data:
            if id == i[0]:
                return "ID present"

    
           
        row = [id,name,type,doe,used+stock,used,stock,cost]
        self.data.append(row)
        print("sucess")
        self.__write__()
        self.__read__()
        self.pq.add_link(max(self.df.index)+1,doe)
        self.pq.pqueue_add(doe,max(self.df.index)+1)
        return "Addition complete"

    def table_list(self):
        return self.data

    def order(self,column):
        '''Ordering the table according to the column specified'''
        if column in self.columns:
            index = self.columns.index(column)    #this index value in the nested list is what is supposed to be changed 
            self.data.sort(key = lambda x: x[index]) 
            self.__write__()
            self.__read__()
            return self.__str__()

        else:
            return "Column does not exist"

    def update(self,med_id,column,new_value):
        '''Updating a particular value in the csv file based on ID'''
        count = 0   #kept to raise error if invalid id is entered 
        if column in ["ID","Name","Type","DOE","Used","Stock","Cost"]:
            index = self.columns.index(column)

            for i in self.data:
                if med_id in i and i[0] == med_id:
                    i[index] = new_value 

                    if column == "Used":
                        if new_value > i[4]:
                            return "Used Invalid"

                        else:
                            i[6] = i[4] - new_value 

                    elif column == "Stock":
                        if new_value > i[4]:
                            return "Stock Invalid"
                        else:
                            i[5] = i[4] - new_value  #amount used gets updated 

                    count += 1 
                    self.__write__()
                    self.__read__()
        
            if count == 1:
                return "Updation complete"
            else:
                return "Invalid ID"

        else:
            return "Column does not exist"

    def update_multi(self,med_id,total,used):
        '''Updating a particular value's total, used and stock amount'''
        counter = 0 
        for i in self.data:
            if med_id in i and i[0] == med_id:
                counter += 1 
                if used > total:
                    return "Used Invalid"

                else:
                    i[4] = total 
                    i[5] = used 
                    i[6] = total - used 
                    self.__write__()
                    self.__read__()

        if counter == 1:
            return "Updation complete"

        else:
            return "Invalid ID"

        
    def delete(self,med_id):
        '''Deleting a field based on Medicine ID'''
        count = 0 
        for i in self.data:
            if med_id in i and i.index(med_id) == 0:
                self.data.remove(i)
                self.__write__()
                self.__read__()
                count += 1 

        if count == 1:
            return "Deleted successfully"
        else:
            return "Invalid ID"

    def retrieve(self,row_num):
        '''Retrieving the row details based on the row_num specified'''
        if row_num < self.size:
            return self.data[row_num]

        else:
            return "Invalid row number"

    def low_stock(self):
        '''Prints rows that have dangerously low stock left'''
        low_stock_table = []
        index = self.columns.index("Stock")
        for i in self.data:
            if i[index] < 10 and i[index]!=0:   #stock is lesser than 10, warning 
                low_stock_table.append(i)

        low_stock_df = pd.DataFrame(low_stock_table,columns=self.columns)
        return low_stock_df,low_stock_table

    def empty_stock(self):
        '''Prints rows that have no stock left'''
        no_stock = []
        index = self.columns.index("Stock")
        for i in self.data:
            if i[index] == 0:
                no_stock.append(i)

        no_stock_df = pd.DataFrame(no_stock,columns=self.columns)
        return no_stock_df,no_stock

    def reach_expiry(self):
        reach_expired_ind = self.pq.near_expired
        reach_expired_df = self.df.loc[reach_expired_ind]
        reach_expired = reach_expired_df.values.tolist()
        return reach_expired_df,reach_expired 

    def expired(self):
        
        expired_ind = self.pq.expired
        expired_df = self.df.loc[expired_ind]
        expired = expired_df.values.tolist()

        
        return expired_df,expired

        
    def clear(self):
        '''Clearing the entire table - csv file'''
        self.table.clear()
    #def print_link(self):
     #   print(self.pq)
      #  print(self.links)

class pq:
    def __init__(self,df):
        self.links = dict(zip(df.index,df["DOE"]))
        self.pq = list(self.links.values())
        self.pq.sort(key = lambda date: datetime.strptime(date, '%d-%m-%Y'))
        self.valind = [0]*len(self.pq)
        self.val_ind()
        self.expiry = datetime.now().strftime("%d-%m-%Y")
        self.close_expiry = (datetime.now()+timedelta(30)).strftime("%d-%m-%Y")
        self.expired,self.near_expired = self.exp_near_ind()

    def add_link(self,link,l):
        self.links[link] = l 
    
    def val_ind(self):
        for i in range (len(self.pq)):
            a = self.rlu(self.pq[i])
            for j in a:
                if j not in self.valind:
                    self.valind[i] = j
        return self.valind

    def exp_near_ind(self):
        i = 0
        expired = []
        near_expired =[]
        while datetime.strptime(self.pq[i],"%d-%m-%Y")<datetime.strptime(self.expiry,"%d-%m-%Y"):
            expired.append(int(self.valind[i]))
            i+=1
        while datetime.strptime(self.pq[i],"%d-%m-%Y")<datetime.strptime(self.close_expiry,"%d-%m-%Y"):
            near_expired.append(int(self.valind[i]))
            i+=1 
        return expired,near_expired 

    def rlu(self,v):
        l = []
        for i in self.links:
            if self.links[i]==v:
                l.append(i)
        return l

    def pqueue_add(self,val,ind):
        i = 0
        while val>self.pq[i]:
            i+=1
            print(i)
        self.pq.insert(i,val)
        self.valind.insert(i,ind)
             
path = "C:/Users/Lenovo/Desktop/endsem_project/med.csv"

test2 = Med_Data(path)
print(test2.data)
t3 = pq(test2.df)
#print(test2.add(19,"DOLO 900","FEVER","20-05-2022",50,10,200))
#test2.print_link()
print(t3.links,t3.pq,t3.valind,sep = "\n")

















