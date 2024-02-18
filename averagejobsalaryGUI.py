from PyQt5 import QtCore, QtGui, QtWidgets
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time

class MyThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(int)
    def run(self):
        cnt = 0
        while cnt < 100:
            cnt+=1
            time.sleep(0.3)
            self.change_value.emit(cnt)

class Ui_frmAverageSalaryScraper(object):
    jobTitleList = []
    scrapedData = []

    # Return Combo Box Choice
    def returnLocation(self):
        return self.cmbLocation.currentText()

    # Write List to CSV File
    def writetoCSV(self):
        print("Exporting CSV...")
        location = self.returnLocation()
        if location=="Singapore":
            fields = ["Job Title", "Average Salary Per Month (SGD)"]
        elif location == "Malaysia":
            fields = ["Job Title", "Average Salary Per Month (MYR)"]


        with open("JobSalary.csv",'w',newline="") as file:
            write = csv.writer(file)

            write.writerow(fields)
            write.writerows(self.scrapedData)
            print("CSV has been exported.")
            print("-"*100)

    # Extract Average Salary from soup
    def getAverageSalary(self,soup):
        location = self.returnLocation()
        # Change the class name if you want to scrape other countries' jobs
        results = soup.find("div",class_="css-12k8m2u eu4oa1w0")
        if location=="Singapore":
            # Remove $ and , and Convert to Integer
            averageSalary = int(((results.text).replace("$","")).replace(",",""))
        elif location == "Malaysia":
            # Remove RM and , and Convert to Integer
            averageSalary = int(((results.text).replace("RM","")).replace(",",""))

        return averageSalary

    def appendScrapedDataList(self,jobTitle,pageSoup):
        self.scrapedData.append([jobTitle,self.getAverageSalary(pageSoup)])


    def getDom(self,jobTitle,driver):
        # Change the url if you want
        location = self.returnLocation()
        if location=="Singapore":
            driver.get(f"https://sg.indeed.com/career/{jobTitle.replace(' ', '-')}/salaries")

        elif location=="Malaysia":
            driver.get(f"https://malaysia.indeed.com/career/{jobTitle.replace(' ', '-')}/salaries")
        pageContent = driver.page_source
        print("Get Page Source Succesfully.")
        pageSoup = BeautifulSoup(pageContent,'html.parser')
        try:
            self.appendScrapedDataList(jobTitle,pageSoup)
        except:
            pass

        return pageSoup

    def btnClear_clicked(self):
        self.txtJobTitle.setText("")
        self.progressBar.setValue(0)
        print("Job Titles have been cleared.")

    def startCrawl(self,jobTitleList):
        numberJobTitle = 1
        # Hide the browser
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        for title in jobTitleList:
            self.startProgressBar()
            print(f"{numberJobTitle}/{len(jobTitleList)}")

            try:
                print(f"Fetching {title} data...")
                self.getDom(title,driver)
            #     # Change the url if you want
            #     location = self.returnLocation()
            #     if location=="Singapore":
            #         driver.get(f"https://sg.indeed.com/career/{title.replace(' ', '-')}/salaries")
            #
            #     elif location=="Malaysia":
            #         driver.get(f"https://malaysia.indeed.com/career/{title.replace(' ', '-')}/salaries")
            #     pageContent = driver.page_source
            #     print("Get Page Source Succesfully.")
            #     pageSoup = BeautifulSoup(pageContent,'html.parser')
            #     try:
            #         self.appendScrapedDataList(title,pageSoup)
            #     except:
            #         pass
                print(f"Fecthing {title} completed.")
                print(f"{self.scrapedData}")
                print("-"*100)
                numberJobTitle += 1


            except:
                print(f"Fetching {title} failed.")

                print("-"*100)
                numberJobTitle += 1

            estimatedSecondLeft = (len(jobTitleList)*5)-((numberJobTitle-1)*5)
            estimatedMinuteLeft = round(estimatedSecondLeft/60,2)
            print(f"Estimated Time Left: {estimatedSecondLeft} seconds.")
            print(f"Estimated Time Left: {estimatedMinuteLeft} minutes.")
            print("-"*100)

            self.setProgressVal(int((numberJobTitle/len(jobTitleList)*100)))

        driver.quit()

    def startProgressBar(self):
        self.thread=MyThread()
        self.thread.change_value.connect(self.setProgressVal)

    def setProgressVal(self,val):
        self.progressBar.setValue(val)

    def btnStart_clicked(self):

        # Get Value From Text Field
        jobTitlesString = self.txtJobTitle.toPlainText()

        # Split Values by new lines and Add to jobTitleList
        jobTitleList = jobTitlesString.splitlines()
        self.startCrawl(jobTitleList)
        self.writetoCSV()





    def setupUi(self, frmAverageSalaryScraper):
        frmAverageSalaryScraper.setObjectName("frmAverageSalaryScraper")

        frmAverageSalaryScraper.setFixedSize(801, 450)
        self.centralwidget = QtWidgets.QWidget(frmAverageSalaryScraper)
        self.centralwidget.setObjectName("centralwidget")
        self.lblAverageSalaryScraper = QtWidgets.QLabel(self.centralwidget)
        self.lblAverageSalaryScraper.setGeometry(QtCore.QRect(230, 20, 311, 51))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI Semilight")
        font.setPointSize(24)

        self.lblAverageSalaryScraper.setFont(font)
        self.lblAverageSalaryScraper.setAutoFillBackground(False)
        self.lblAverageSalaryScraper.setObjectName("lblAverageSalaryScraper")

        self.txtJobTitle = QtWidgets.QTextEdit(self.centralwidget)
        self.txtJobTitle.setGeometry(QtCore.QRect(30, 110, 731, 171))
        self.txtJobTitle.setObjectName("txtJobTitle")

        self.lblInsertJobTitle = QtWidgets.QLabel(self.centralwidget)
        self.lblInsertJobTitle.setGeometry(QtCore.QRect(30, 90, 71, 16))

        self.lblInsertJobTitle.setObjectName("lblInsertJobTitle")
        self.cmbLocation = QtWidgets.QComboBox(self.centralwidget)
        self.cmbLocation.setGeometry(QtCore.QRect(30, 310, 111, 22))

        self.cmbLocation.setObjectName("cmbLocation")
        self.cmbLocation.addItem("")
        self.cmbLocation.addItem("")
        self.lblLocation = QtWidgets.QLabel(self.centralwidget)
        self.lblLocation.setGeometry(QtCore.QRect(30, 290, 47, 13))
        self.lblLocation.setObjectName("lblLocation")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 0, 801, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(690, 310, 75, 23))
        self.btnStart.setObjectName("btnStart")
        self.btnStart.clicked.connect(self.btnStart_clicked)
        # self.txtDetails = QtWidgets.QPlainTextEdit(self.centralwidget)
        # self.txtDetails.setGeometry(QtCore.QRect(30, 360, 731, 161))
        # self.txtDetails.setUndoRedoEnabled(False)
        # self.txtDetails.setReadOnly(True)
        # self.txtDetails.setPlainText("")
        # self.txtDetails.setBackgroundVisible(False)
        # self.txtDetails.setCenterOnScroll(False)
        # self.txtDetails.setObjectName("txtDetails")
        # self.lblDetails = QtWidgets.QLabel(self.centralwidget)
        # self.lblDetails.setGeometry(QtCore.QRect(30, 340, 47, 13))
        # self.lblDetails.setObjectName("lblDetails")
        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setGeometry(QtCore.QRect(600, 310, 75, 23))
        self.btnClear.setObjectName("btnClear")
        self.btnClear.clicked.connect(self.btnClear_clicked)
        frmAverageSalaryScraper.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(frmAverageSalaryScraper)
        self.statusbar.setObjectName("statusbar")
        frmAverageSalaryScraper.setStatusBar(self.statusbar)

        self.retranslateUi(frmAverageSalaryScraper)
        QtCore.QMetaObject.connectSlotsByName(frmAverageSalaryScraper)

    def retranslateUi(self, frmAverageSalaryScraper):
        _translate = QtCore.QCoreApplication.translate
        frmAverageSalaryScraper.setWindowTitle(_translate("frmAverageSalaryScraper", "Average Salary Scraper"))
        self.lblAverageSalaryScraper.setText(_translate("frmAverageSalaryScraper", "Average Salary Scraper"))
        self.txtJobTitle.setHtml(_translate("frmAverageSalaryScraper", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">DO NOT ADD ANY SYMBOLS SUCH AS: ,./()!#$%^</p>\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">CLICK CLEAR BUTTON TO CLEAR</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Designer</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Programmer</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Singer</p></body></html>"))
        self.lblInsertJobTitle.setText(_translate("frmAverageSalaryScraper", "Insert Job Title"))
        self.cmbLocation.setItemText(0, _translate("frmAverageSalaryScraper", "Malaysia"))
        self.cmbLocation.setItemText(1, _translate("frmAverageSalaryScraper", "Singapore"))
        self.lblLocation.setText(_translate("frmAverageSalaryScraper", "Location"))
        self.btnStart.setText(_translate("frmAverageSalaryScraper", "Start"))
        # self.lblDetails.setText(_translate("frmAverageSalaryScraper", "Details"))
        self.btnClear.setText(_translate("frmAverageSalaryScraper", "Clear"))





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frmAverageSalaryScraper = QtWidgets.QMainWindow()
    ui = Ui_frmAverageSalaryScraper()
    ui.setupUi(frmAverageSalaryScraper)
    frmAverageSalaryScraper.show()
    sys.exit(app.exec_())
