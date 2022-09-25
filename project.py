import sys
from PyQt5 import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialog,QApplication,QWidget,QLabel,QTableWidgetItem,QMessageBox
from PyQt5.QtGui import QPixmap,QIcon
import mysql.connector
user=passw=''
database=''

#Main Login Page
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("C:\\Users\\rocky\\Desktop\\coding\\project\\ui\\loginMain.ui",self)
        self.setWindowTitle('Inventory Management System')
        self.label_5.resize(1600, 850)
        self.loginBtn.clicked.connect(self.gotologin)
        self.pxp = QPixmap('C:\\Users\\rocky\\Desktop\\coding\\project\\warehouse-6-blog.jpg')
        self.label_5.setPixmap(QPixmap(self.pxp))
        self.label_5.setScaledContents(True)

    def gotologin(self):
        global user
        global passw
        user1 = self.lineEdit.text()
        passw1 = self.lineEdit_2.text()

        if len(user1)==0 or len(passw1)==0:
            self.redLab.setText("Please input all fields!")
        else:
            try:
                mydb = mysql.connector.connect(host="localhost",user=user1,passwd=passw1)
                user = user1
                passw = passw1
                widget.setCurrentIndex(1)
            except Exception:
                self.redLab.setText("Invalid Credentials!")
class alertbx:
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Are You want to delete the selected item?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        return retval
#functionality start
class mainOrders(QDialog):
    def __init__(self):
        super(mainOrders,self).__init__()
        loadUi("C:\\Users\\rocky\\Desktop\\coding\\project\\ui\\MainPageOrd.ui",self)
        self.frame.resize(1600, 850)
        self.refbtn.setIcon(QIcon('C:\\Users\\rocky\\Desktop\\coding\\project\\ref_icon.png'))
        self.refbtn.clicked.connect(self.init)
        self.invBtn.clicked.connect(self.gotoinv)
        self.salesBtn.clicked.connect(self.gotosls)
        self.pushButton_8.clicked.connect(self.shadcus)
        self.pushButton.clicked.connect(self.shord)
        self.addcust.clicked.connect(self.custnm)
        self.addord.clicked.connect(self.addOrd)
        self.orddet.clicked.connect(self.shodet)
        self.adttm.clicked.connect(self.adddet)
        self.delcust.clicked.connect(self.dlcus)
        self.edtordet.clicked.connect(self.edtorddet)
        self.svechng.clicked.connect(self.saveChanges)
        self.pushButton_2.clicked.connect(self.upcust)
        self.pushButton_3.hide()
        self.pushButton_3.clicked.connect(self.savecust)
        self.eidet.clicked.connect(self.updet)
        self.delord.clicked.connect(self.delords)
        self.svechng.hide()
        self.savedet.hide()
        self.savedet.clicked.connect(self.svedet)
        self.addcust_3.clicked.connect(self.deldets)
        self.backbtn.clicked.connect(self.backf)
        self.stackedWidget.setCurrentIndex(1)
        self.init()
        self.custtable()
    def shadcus(self):
        self.stackedWidget.setCurrentIndex(1)
    def shord(self):
        self.stackedWidget.setCurrentIndex(0)
    def gotoinv(self):
        widget.setCurrentIndex(4)
    def gotosls(self):
        widget.setCurrentIndex(6)
    def backf(self):
        self.qtyedit.setText('')
        self.amtedt.setText('')
        self.label_7.setText('')
        self.stackedWidget.setCurrentIndex(0)
    def deldets(self):
        try:
            r=self.itemdettbl.selectedItems()[0].row()
        except Exception:
            self.label_7.setText('select item from table')
            return
        obj = alertbx()
        val=obj.showdialog()
        if val!=1024:
            return
        oid = int(self.label_2.text()[10:])
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        iname = self.itemdettbl.item(r,0).text()
        crsr.execute("select iid from item where iname= '"+str(iname)+"'")
        iid=int(crsr.fetchall()[0][0])
        crsr.execute("delete from ord_det where ordid ="+str(oid)+" and iid ="+str(iid))
        mydb.commit()
        self.qtyedit.setText('')
        self.amtedt.setText('')
        self.loaddet()
    def updet(self):
        try:
            r=self.itemdettbl.selectedItems()[0].row()
        except Exception:
            self.label_7.setText('select item from table')
            return
        oid = int(self.label_2.text()[10:])
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        iname = self.itemdettbl.item(r,0).text()
        crsr.execute("select iid from item where iname= '"+str(iname)+"'")
        iid=int(crsr.fetchall()[0][0])
        crsr.execute("select quant,amount from ord_det where ordid="+str(oid)+" and iid="+str(iid))
        res=crsr.fetchall()
        self.qtyedit.setText(str(res[0][0]))
        self.amtedt.setText(str(res[0][1]))
        crsr.execute("select iname from item where iid = "+str(iid))
        index = self.ibox.findText((crsr.fetchall())[0][0], QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.ibox.setCurrentIndex(index)
        self.savedet.show()
        mydb.commit()
    def svedet(self):
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        if not isinstance(self.amtedt.text(),int):
            self.label_7.setText('amount should be an integer')
            return
        r=self.itemdettbl.selectedItems()[0].row()
        oid = int(self.label_2.text()[10:])
        iname = self.itemdettbl.item(r,0).text()
        crsr.execute("select iid from item where iname= '"+str(iname)+"'")
        iid=int(crsr.fetchall()[0][0])
        crsr.execute("update ord_det set quant ='"+str(self.qtyedit.text())+"' , amount ="+str(self.amtedt.text())+" where ordid = "+str(oid)+" and iid ="+str(iid))
        mydb.commit()
        self.loaddet()
        self.savedet.hide()
        self.qtyedit.setText('')
        self.amtedt.setText('')
    def shodet(self):
        try:
            r=self.ord_table.selectedItems()[0].row()
            self.redLab.setText('')
            self.loaddet()
            self.stackedWidget.setCurrentIndex(2)
        except Exception:
            self.redLab.setText('select an item from the table')
            return
            
    def loaddet(self):
        self.label_2.setText("Order ID :")
        r=self.ord_table.selectedItems()[0].row()
        oid = int(self.ord_table.item(r,0).text())
        lblid="Order ID :"+str(oid)
        self.label_2.setText(lblid)
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute("select iname from item")
        res=crsr.fetchall()
        mydb.commit()
        self.ibox.clear()
        for i in res:
            for j in i:
                self.ibox.addItem(str(j))
        sql="select * from ord_det where ordid={}".format(oid)
        crsr.execute(sql)
        res = crsr.fetchall()
        self.itemdettbl.setRowCount(len(res))
        self.itemdettbl.horizontalHeader().setVisible(True)
        self.itemdettbl.setColumnWidth(0,200)
        self.itemdettbl.setColumnWidth(1,140)
        self.itemdettbl.setColumnWidth(2,140)
        r=c=0
        for i in res:
            c=0
            for j in [1,2,3]:
                if c==0:
                    crsr.execute("select iname from item where iid="+str(i[j]))
                    self.itemdettbl.setItem(r,c,QTableWidgetItem(str(crsr.fetchall()[0][0])))
                else:
                    self.itemdettbl.setItem(r,c,QTableWidgetItem(str(i[j])))
                c+=1
            r+=1
        mydb.commit()
    def adddet(self):
        quant = self.qtyedit.text()
        if quant == '' or self.amtedt.text()=='':
            self.label_7.setText('enter all fields')
            return
        if not isinstance(int(self.amtedt.text()),int):
            self.label_7.setText('amount should be an integer')
            return
        r=self.ord_table.selectedItems()[0].row()
        oid = int(self.ord_table.item(r,0).text())
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        name = self.ibox.currentText()
        sql="select iid from item where iname = '{}'".format(name)
        crsr.execute(sql)
        iid=(crsr.fetchall())[0][0]
        sql="insert into ord_det (ordid,iid,quant,amount) values({},{},'{}',{})".format(oid,iid,quant,self.amtedt.text())
        crsr.execute(sql)
        mydb.commit()
        self.loaddet()
        self.qtyedit.setText('')
        self.amtedt.setText('')

    
    def saveChanges(self):
        if not isinstance(float(self.edt2.text()),float):
            self.label_7.setText('amount should be an integer')
            return
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        r=self.ord_table.selectedItems()[0].row()
        id=self.ord_table.item(r,0).text()
        date = self.edt1.text()
        amt=self.edt2.text()       
        cust=self.custbox.currentText()
        if self.statrad.isChecked():
            stat='true'
        else:
            stat='false'
        crsr.execute("select cid from customer where cname ='"+str(cust)+"'")
        sql="update orders set odate='{}',amount={},status={},cid={} where ordid ={}".format(date,amt,stat,(crsr.fetchall())[0][0],id)
        crsr.execute(sql)
        mydb.commit()
        self.loadData()
        self.svechng.hide()
        self.edt1.setText('')
        self.edt2.setText('')       

    def edtorddet(self):
        try:
            r=self.ord_table.selectedItems()[0].row()
            id=self.ord_table.item(r,0).text()
        except Exception:
            self.redLab.setText('select an item from the table')
            return
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        sql='select * from orders where ordid ='+str(id)
        crsr.execute(sql)
        res=crsr.fetchall()
        self.edt1.setText(str(res[0][3]))
        self.edt2.setText(str(res[0][2]))
        if res[0][1] != None:
            crsr.execute("select cname from customer where cid = "+str(res[0][1]))
            index = self.custbox.findText((crsr.fetchall())[0][0], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.custbox.setCurrentIndex(index)
        self.svechng.show()

    def delords(self):
        try:
            r=self.ord_table.selectedItems()[0].row()
            oid=self.ord_table.item(r,0).text()
        except Exception:
            self.redLab.setText('select an item from the table')
            return
        obj = alertbx()
        val=obj.showdialog()
        if val!=1024:
            return
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute("delete from orders where ordid ="+str(oid))
        mydb.commit()
        self.loadData()
    def addOrd(self):
        if self.edt1.text()=='' or self.edt2.text()==''  :
            self.redLab.setText("Fill all the fields!")
        else:
            self.redLab.setText("")
            mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
            crsr = mydb.cursor()
            stat=0
            if self.statrad.isChecked():
                stat=1
            date=self.edt1.text()
            amnt=self.edt2.text()
            cnme = self.custbox.currentText()
            crsr.execute("select cid from customer where cname = '{}'".format(cnme))
            cid=(crsr.fetchall())[0][0]        
            sql="insert into orders (cid,amount,odate,status) values({},{},'{}',{})".format(cid,amnt,date,stat)
            crsr.execute(sql)
            mydb.commit()
            self.loadData()
            self.edt1.setText('')
            self.edt2.setText('')

    
    def loadData(self):
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute("select * from orders")
        res=crsr.fetchall()
        self.ord_table.setRowCount(len(res))
        self.ord_table.horizontalHeader().setVisible(True)
        self.ord_table.setColumnWidth(0,110)
        self.ord_table.setColumnWidth(1,150)
        self.ord_table.setColumnWidth(2,140)
        self.ord_table.setColumnWidth(3,140)
        self.ord_table.setColumnWidth(4,175)
        r=c=0
        for i in res:
            c=0
            for j in i:
                if c==1:
                    sql="select cname from customer where cid={}".format(j)
                    crsr.execute(sql)
                    j=(crsr.fetchall())[0][0]
                if c==4:
                    if j==1:
                        j='Delivered'
                    else:
                        j='Delivery Pending'
                self.ord_table.setItem(r,c,QTableWidgetItem(str(j)))
                c+=1

            r+=1
        mydb.commit()
    def init(self):
        self.custbox.clear()
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute('select cname from customer')
        res = crsr.fetchall()
        mydb.commit()
        for i in res:
            self.custbox.addItem(i[0])
        self.loadData()
    def dlcus(self):
        try:
            r=self.cust_table.selectedItems()[0].row()
            id=self.cust_table.item(r,0).text()
        except Exception:
            self.label.setText('select an item from the table')
            return
        obj = alertbx()
        val=obj.showdialog()
        if val!=1024:
            return
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        sql='delete from customer where cid ='+str(id)
        crsr.execute(sql)
        mydb.commit()
        self.custtable()
    def custtable(self):
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute("select * from customer")
        res=crsr.fetchall()
        self.cust_table.setRowCount(len(res))
        self.cust_table.horizontalHeader().setVisible(True)
        self.cust_table.setColumnWidth(0,100)
        self.cust_table.setColumnWidth(1,150)
        self.cust_table.setColumnWidth(2,150)
        self.cust_table.setColumnWidth(3,300)
        self.cust_table.setColumnWidth(4,180)
        r=c=0
        for i in res:
            c=0
            for j in i:
                self.cust_table.setItem(r,c,QTableWidgetItem(str(j)))
                c+=1
            r+=1
        mydb.commit()
    def custnm(self):
        if self.lineEdit_1.text()=='' or self.lineEdit_2.text()=='' or self.lineEdit_3.text()=='' or self.lineEdit_4.toPlainText()=='':
            self.label.setText("enter all fields")
        else:
            self.label.setText("")
            name = self.lineEdit_1.text()
            print(name)
            mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
            crsr = mydb.cursor()
            crsr.execute("select cname from customer")
            nm = crsr.fetchall()
            for i in nm:
                if self.lineEdit_1.text()==i[0]:
                    self.label.setText("name already exists")
                    return
            sql="insert into customer(cname,phone,address,email) values('{}',{},'{}','{}')".format(name,self.lineEdit_2.text(),self.lineEdit_4.toPlainText(),self.lineEdit_3.text())
            crsr.execute(sql)
            mydb.commit()
            self.custtable()
            self.lineEdit_1.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.clear()
    def savecust(self):
        r=self.cust_table.selectedItems()[0].row()
        id=self.cust_table.item(r,0).text()
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        sql="update customer set cname='{}',phone={},address='{}',email='{}' where cid ={}".format(self.lineEdit_1.text(),self.lineEdit_2.text(),self.lineEdit_4.toPlainText(),self.lineEdit_3.text(),id)
        crsr.execute(sql)
        mydb.commit()
        self.custtable()
        self.lineEdit_1.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.clear()
        self.pushButton_3.hide()

    def upcust(self):
        try:
            r=self.cust_table.selectedItems()[0].row()
            id=self.cust_table.item(r,0).text()
        except Exception:
            self.label.setText("Select item from table")
            return
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        
        crsr.execute("select * from customer where cid ="+str(id))
        res=crsr.fetchall()
        self.lineEdit_1.setText(str(res[0][1]))
        self.lineEdit_2.setText(str(res[0][2]))
        self.lineEdit_3.setText(str(res[0][4]))
        self.lineEdit_4.setText(str(res[0][3]))
        self.pushButton_3.show()
class mainSales(QDialog):
    def __init__(self):
        super(mainSales,self).__init__()
        loadUi("C:\\Users\\rocky\\Desktop\\coding\\project\\ui\\MainPageSls.ui",self)
        self.pushButton_4.setIcon(QIcon('C:\\Users\\rocky\\Desktop\\coding\\project\\backbtn.png'))
        self.orderBtn.clicked.connect(self.gotoordr)
        self.invBtn.clicked.connect(self.gotoinv)
        self.pushButton.clicked.connect(self.showdet)
        self.pushButton_4.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.pushButton_5.setIcon(QIcon('C:\\Users\\rocky\\Desktop\\coding\\project\\ref_icon.png'))
        self.pushButton_5.clicked.connect(self.laodtable)
        self.laodtable()
    def showdet(self):
        try:
            r=self.tableWidget.selectedItems()[0].row()
            id=self.tableWidget.item(r,0).text()
        except Exception:
            self.label.setText("Select item from table")
            return
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute("select iname from item where iid="+str(id))
        self.nmlbl.setText("Item Name : "+str(crsr.fetchall()[0][0]))
        self.idlbl.setText("Item ID : "+str(id))
        crsr.execute("select sum(amount) from ord_det where iid="+str(id))
        self.amtlbl.setText("Total Amount Sold : "+str(crsr.fetchall()[0][0]))
        crsr.execute("select a.ordid,b.cid,b.odate,a.quant,a.amount from ord_det a,orders b where a.ordid=b.ordid and iid="+str(id))
        res=crsr.fetchall()
        self.tableWidget_2.setRowCount(len(res))
        self.tableWidget_2.setColumnWidth(0,100)
        self.tableWidget_2.setColumnWidth(1,200)
        self.tableWidget_2.setColumnWidth(2,150)
        self.tableWidget_2.setColumnWidth(2,150)
        self.tableWidget_2.setColumnWidth(2,150)
        r=c=0
        for i in res:
            c=0
            for j in i:
                if c==1:
                    crsr.execute("select cname from customer where cid="+str(j))
                    self.tableWidget_2.setItem(r,c,QTableWidgetItem(str(crsr.fetchall()[0][0])))
                    c+=1
                    continue
                self.tableWidget_2.setItem(r,c,QTableWidgetItem(str(j)))
                c+=1
            r+=1
        self.stackedWidget.setCurrentIndex(1)
    def laodtable(self):
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()

        crsr.execute("select a.iid,o.iname,sum(a.amount) from ord_det a,item o where o.iid=a.iid group by a.iid")
        res=crsr.fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnWidth(0,130)
        self.tableWidget.setColumnWidth(1,200)
        self.tableWidget.setColumnWidth(2,200)
        r=c=0
        for i in res:
            c=0
            for j in i:
                
                self.tableWidget.setItem(r,c,QTableWidgetItem(str(j)))
                c+=1
            r+=1
    def gotoordr(self):
        widget.setCurrentIndex(5)
    def gotoinv(self):
        widget.setCurrentIndex(4)


class maininv(QDialog):
    def __init__(self):
        super(maininv,self).__init__()
        loadUi("C:\\Users\\rocky\\Desktop\\coding\\project\\ui\\MainPage.ui",self)
        self.frame.resize(1600, 850)
        self.refbtn.setIcon(QIcon('C:\\Users\\rocky\\Desktop\\coding\\project\\ref_icon.png'))
        self.pushButton_4.setIcon(QIcon('C:\\Users\\rocky\\Desktop\\coding\\project\\backbtn.png'))
        self.refbtn.clicked.connect(self.typinit)
        self.orderBtn.clicked.connect(self.gotoordr)
        self.salesBtn.clicked.connect(self.gotosls)
        self.addItm.clicked.connect(self.showAdd)
        self.itmTyp.clicked.connect(self.showTyp)
        self.addbtn.clicked.connect(self.additem)
        self.addItp.clicked.connect(self.additmtyp)
        self.delbtn.clicked.connect(self.delitm)
        self.deltp.clicked.connect(self.deltyp)
        self.addbtn_3.clicked.connect(self.updtitm)
        self.save.clicked.connect(self.sve)
        self.stackedWidget.setCurrentIndex(1)
        self.pushButton_4.clicked.connect(self.goback)
        self.save.hide()
        self.loadData()
        self.typinit()
        self.typtable()
    
    def goback(self):
        global widget
        widget.setCurrentIndex(1)
    def updtitm(self):
        try:
            r=self.tableWidget.selectedItems()[0].row()
            id=self.tableWidget.item(r,0).text()
        except Exception:
            self.redLab.setText('select an item from the table')
            return
        self.redLab.setText("")
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        sql="select * from item where iid ="+str(id)
        crsr.execute(sql)
        res=crsr.fetchall()
        self.nmeEdt.setText(str(res[0][1]))
        self.quantEdt.setText(str(res[0][5]))    
        self.spEdt.setText(str(res[0][4]))
        self.cpEdt.setText(str(res[0][3]))
        crsr.execute("select typnm from itmtype where typid ="+str(res[0][2]))
        index = self.typCmb.findText((crsr.fetchall())[0][0], QtCore.Qt.MatchFixedString)
        print(index)
        if index >= 0:
            self.typCmb.setCurrentIndex(index)
        self.save.show()
        
    def sve(self):
        self.redLab.setText("")
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        r=self.tableWidget.selectedItems()[0].row()
        id=self.tableWidget.item(r,0).text()
        name = (self.nmeEdt.text()).strip().lower()
        quant=self.quantEdt.text()       
        sp=self.spEdt.text()
        cp=self.cpEdt.text()
        ityp = self.typCmb.currentText()
        crsr.execute("select typid from itmtype where typnm ='"+str(ityp)+"'")
        sql="update item set iname='{}',quantity='{}',cstprc={},selprc={},typid={} where iid ={}".format(name,quant,cp,sp,(crsr.fetchall())[0][0],id)
        crsr.execute(sql)
        mydb.commit()
        self.loadData()
        self.save.hide()
        self.nmeEdt.setText('')
        self.quantEdt.setText('')       
        self.spEdt.setText('')
        self.cpEdt.setText('')

    def delitm(self):
        try:
            r=self.tableWidget.selectedItems()[0].row()
            id=self.tableWidget.item(r,0).text()
        except Exception:
            self.redLab.setText('select an item from the table')
            return
        self.redLab.setText("")
        obj = alertbx()
        val=obj.showdialog()
        if val!=1024:
            return
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()

        sql='delete from item where iid ='+str(id)
        crsr.execute(sql)
        mydb.commit()
        self.loadData()
        
    def deltyp(self):
        try:
            r=self.type_table.selectedItems()[0].row()
            id=self.type_table.item(r,0).text()
        except Exception:
            self.label.setText('select an item from the table')
            return
        obj = alertbx()
        val=obj.showdialog()
        if val!=1024:
            return
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        sql='delete from itmtype where typid ='+str(id)
        crsr.execute(sql)
        mydb.commit()
        self.loadData()
        self.typinit()
        self.typtable()
    def additem(self):
        if self.nmeEdt.text()=='' or self.quantEdt.text()=='' or self.cpEdt.text()=='' or self.spEdt.text()=='' :
            self.redLab.setText("Fill all the fields!")
        else:
            self.redLab.setText("")
            mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
            crsr = mydb.cursor()
            name = self.nmeEdt.text().strip().lower()
            quant=self.quantEdt.text()       
            sp=self.spEdt.text()
            cp=self.cpEdt.text()
            ityp = self.typCmb.currentText() 
            sql = "select typid from itmtype where typnm ='{}'".format(ityp)
            crsr.execute(sql) 
            tid = (crsr.fetchall())[0][0]    
            sql="insert into item (iname,typid,cstprc,selprc,quantity) values('{}',{},{},{},'{}')".format(name,tid,cp,sp,quant)
            crsr.execute(sql)
            mydb.commit()
            self.nmeEdt.setText('')
            self.quantEdt.setText('')       
            self.spEdt.setText('')
            self.cpEdt.setText('')

            self.loadData()
            

    def loadData(self):
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute("select * from item")
        res=crsr.fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,170)
        self.tableWidget.setColumnWidth(2,150)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(4,100)
        self.tableWidget.setColumnWidth(5,150)
        
        r=c=0
        for i in res:
            c=0
            for j in i:
                if c == 2:
                    sql="select typnm from itmtype where typid={}".format(j)
                    crsr.execute(sql)
                    rlt=(crsr.fetchall())[0][0]
                    self.tableWidget.setItem(r,c,QTableWidgetItem(str(rlt)))
                else:
                    self.tableWidget.setItem(r,c,QTableWidgetItem(str(j)))
                c+=1
            r+=1
        mydb.commit()

    def typtable(self):
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute("select * from itmtype")
        res=crsr.fetchall()
        self.type_table.setRowCount(len(res))
        self.type_table.horizontalHeader().setVisible(True)
        self.type_table.setColumnWidth(0,200)
        self.type_table.setColumnWidth(1,220)
        r=c=0
        for i in res:
            c=0
            for j in i:
                self.type_table.setItem(r,c,QTableWidgetItem(str(j)))
                c+=1
            r+=1
        mydb.commit()

    def typinit(self):
        self.typCmb.clear()
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute('select typnm from itmtype')
        
        res = crsr.fetchall()
        mydb.commit()
        for i in res:
            self.typCmb.addItem(i[0])
        
    def gotoordr(self):
        widget.setCurrentIndex(5)
    def gotosls(self):
        widget.setCurrentIndex(6)
    def showAdd(self):
        self.stackedWidget.setCurrentIndex(0)
    def showTyp(self):
        self.stackedWidget.setCurrentIndex(1)
    def additmtyp(self):
        if self.typNme.text()=='':
            self.label.setText("enter type name")
        else:
            name = self.typNme.text()
            mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
            crsr = mydb.cursor()
            crsr.execute("select typnm from itmtype")
            nm = crsr.fetchall()
            for i in nm:
                if self.typNme.text()==i[0]:
                    self.label.setText("type already exists")
                    return
            sql="insert into itmtype(typnm) values('{}')".format(name)
            crsr.execute(sql)
            mydb.commit()
            self.typtable()
           
            self.typNme.setText('')

#functionality end

#inventory create and choose start
class chseInvn(QDialog):
    def __init__(self):
        super(chseInvn,self).__init__()
        loadUi("C:\\Users\\rocky\\Desktop\\coding\\project\\ui\\invn.ui",self)
        self.label_5.resize(1600, 850)
        self.pxp = QPixmap('C:\\Users\\rocky\\Desktop\\coding\\project\\warehouse-6-blog.jpg')
        self.label_5.setPixmap(QPixmap(self.pxp))
        self.label_5.setScaledContents(True)
        self.opbtn.clicked.connect(self.gotoop)
        self.crtbtn.clicked.connect(self.gotocrt)
    def gotoop(self):
        widget.setCurrentIndex(2)
        
    def gotocrt(self):
        widget.setCurrentIndex(3)

class Openinvn(QDialog):
    def __init__(self):
        super(Openinvn,self).__init__()
        loadUi("C:\\Users\\rocky\\Desktop\\coding\\project\\ui\\openinvn.ui",self)
        self.label_5.resize(1600, 850)
        self.pxp = QPixmap('C:\\Users\\rocky\\Desktop\\coding\\project\\warehouse-6-blog.jpg')
        self.label_5.setPixmap(QPixmap(self.pxp))
        self.label_5.setScaledContents(True)
        self.openbtn.clicked.connect(self.gotoinv)
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123')
        crsr = mydb.cursor()
        crsr.execute("show databases")
        abc = crsr.fetchall()
        for i in abc:
            lst=i[0].split('_')
            if len(lst)>2:
                if lst[0]=="root" and lst[2]=="root":
                    self.invnsel1.addItem(lst[1])
    def gotoinv(self):
        global database
        database='root_'+self.invnsel1.currentText()+'_root'
        obj = initialize()
        obj.init()
        widget.setCurrentIndex(4)
    

class creatinvn(QDialog):
    def __init__(self):
        super(creatinvn,self).__init__()
        loadUi("C:\\Users\\rocky\\Desktop\\coding\\project\\ui\\createinvn.ui",self)
        self.label_5.resize(1600, 850)
        self.pxp = QPixmap('project\\warehouse-6-blog.jpg')
        self.label_5.setPixmap(QPixmap(self.pxp))
        self.label_5.setScaledContents(True)
        self.openbtn.clicked.connect(self.gotoinv)
    
    def gotoinv(self):
        global database
        lst =[user,user]
        mydb = mysql.connector.connect(host="localhost",user=user,passwd=passw)
        crsr = mydb.cursor()
        lst.insert(1,(invnName:=self.lineEdit_5.text()))
        print(lst)
        cmd = "create database "+(dbname:=("_".join(lst)))
        usr = self.lineEdit_4.text()
        pasd = self.lineEdit_3.text()
        if len(invnName)==0:
            self.label.setText("database name cannot be empty!")
        elif usr!=user or pasd != passw:
            self.label.setText("invalid credentials")
        else:
            try:
                crsr.execute(cmd)
                database = dbname
                obj = initialize()
                self.create()
                obj.init()
                widget.setCurrentIndex(4)
            except Exception as e:
                self.label.setText("Database already exists")
    
    def create(self):
        print(database)
        mydb = mysql.connector.connect(host="localhost",user='root',passwd='abc123',db=database)
        crsr = mydb.cursor()
        crsr.execute("create table itmtype(typid int auto_increment,typnm varchar(20),primary key(typid))")
        crsr.execute('''create table item(iid int auto_increment,iname varchar(20),typid int ,
                        cstprc float,selprc float,quantity varchar(10),primary key(iid),foreign key(typid) references itmtype(typid) on delete cascade)''')
        crsr.execute("create table customer(cid int auto_increment,cname varchar(20),phone int,address varchar(50),email varchar(20), primary key(cid))")
        crsr.execute('''create table orders(ordid int auto_increment,cid int,amount float,odate date,status boolean,
                        primary key(ordid),foreign key(cid) references customer(cid) on delete cascade on update cascade)''')
        crsr.execute('''create table ord_det(ordid int,iid int,quant varchar(15),amount float,
                        foreign key(ordid) references orders(ordid) on delete cascade on update cascade,
                        foreign key(iid) references item(iid) on delete cascade on update cascade)''')
        mydb.commit()

#inventory create and choose end       

class initialize():
    def init(self):
        mp=maininv()
        mp2=mainOrders()
        mp3=mainSales()
        widget.addWidget(mp)
        widget.addWidget(mp2)
        widget.addWidget(mp3)


app = QApplication(sys.argv)
mainwindow=MainWindow()
inv = chseInvn()
opinv = Openinvn()
crinv = creatinvn()
widget = QtWidgets.QStackedWidget()
widget.setWindowTitle('Inventory Management System')
widget.addWidget(mainwindow)
widget.addWidget(inv)
widget.addWidget(opinv)
widget.addWidget(crinv)
widget.setFixedWidth(1600)
widget.setFixedHeight(850)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("exiting")