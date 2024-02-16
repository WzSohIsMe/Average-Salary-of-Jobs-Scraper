import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options

jobTitleList = [
"Systems Analyst",
"IT Executive",
"IT Consultant",
"Information Systems Analyst",
"Chief Technology Officer (CTO)",
"Technical Support Manager",
"IT Sales Manager",
"IT Application Developer",
"IT Auditor",
"IT Project Manager",
"IT Helpdesk Manager",
"System Administrator",
"Systems Consultant",
"Chief Technology Officer (CTO)",
"Server Developer",
"Cloud Solution Consultant",
"Technical Support Manager",
"IT Cloud Test Engineer",
"Cloud Platform Developer",
"IT Solution Manager",
"Cloud Solution Development Engineer",
"IT Cloud Application Developer",
"Application Platform Services Specialist",
"Cloud Architect",
"Cloud Software Engineer",
"Cloud Network Engineer",
"Cloud Product Manager",
"Cloud Consultant",
"Mobile Application Developer",
"Mobile iOS Developer",
"Android Mobile Developer",
"M-Commerce Consultant",
"Mobile Programmer",
"Telecommunications Solutions Consultant",
"Application Engineer",
"Chief Technology Officer (CTO)",
"Mobile Application Specialist",
"Technical Support Manager",
"Mobile Solutions Consultant",
"Mobile Application Designer",
"Business IT Analyst",
"Digital Engineer",
"Digital Lead",
"Entrepreneur",
"Innovation Architect",
"Business Strategies",
"Digital Transformation Officer",
"Digital Strategist",
"Chief Innovation Officer ",
"Digital Designer",
"Business Transformation Analyst",
"Customer Experience Transformation Lead",
"Enterprise Digital Transformation Specialist",
"HR Digital Transformation Lead",
"Strategic IT Consultant",
"Digital Finance Transformation Leader",
"IT Business Systems Developer",
"IT Systems Analyst",
"E-Commerce Consultant",
"Chief Technology Officer",
"Management Information System Manager",
"Global Business Solution Specialist",
"Global Business Solution Consultant",
"IT Business Development Manager",
"IT Quality Assurance (QA) Analyst",
"IT Business Engagement Manager",
"SAP Business Analyst",
"Technical Business Analyst",
"Business Systems Analyst",
"System Analyst",
"Business Intelligence Manager",
"CRM Business Analyst",
"Computer Engineer",
"Systems Engineer",
"Software Developer",
"Programmer",
"Chief Technology Officer",
"IT Technical Manager",
"Technical Architect",
"Technical Support Manager",
"IT Service Desk Manager",
"Application Engineer",
"Mainframe Developer",
"Software Architect",
"Software Quality Assurance",
"Data Warehouse Manager",
"Applications Development Manager",
"Applications Architect",
"Digital Forensics Investigator",
"Forensic Compliance Investigator",
"Computer Forensics Analyst",
"Cyber Defense Forensics Analyst",
"Cyber Defense Incident Response Analyst",
"Ethical Hacker",
"Penetration Tester",
"Intrusion Detection Analyst",
"Forensic Analytics Specialist",
"Secure Applications Engineer",
"Information Security Analyst",
"Information Security Engineer",
"Information Security Technical Specialist",
"Software Developer",
"Chief Technology Officer",
"Chief Information Security Officer"

]

scrapedData = []
# Acess to the URL and Get the HTML
def getDom(jobTitle):
    # Change the url if you want
    driver.get(f"https://malaysia.indeed.com/career/{jobTitle}/salaries")
    pageContent = driver.page_source
    pageSoup = BeautifulSoup(pageContent,'html.parser')
    try:
        appendScrapedDataList(jobTitle,pageSoup)
    except:
        pass
    driver.quit()
    return pageSoup

# Extract Average Salary from soup
def getAverageSalary(soup):
    # Change the class name if you want to scrape other countries' jobs
    results = soup.find("div",class_="css-12k8m2u eu4oa1w0")

    # Remove $ and , and Convert to Integer
    averageSalary = int(((results.text).replace("RM","")).replace(",",""))
    return averageSalary

def appendScrapedDataList(jobTitle,pageSoup):
    scrapedData.append([jobTitle,getAverageSalary(pageSoup)])

# Write List to CSV File
def writetoCSV():
    fields = ["Job Title", "Average Salary Per Month (MYR)"]
    with open("E:\Pycharm Project\JobsSalaryScraper\JobSalary.csv",'w',newline="") as file:
        write = csv.writer(file)

        write.writerow(fields)
        write.writerows(scrapedData)
        print("CSV has been exported.")



numberJobTitle = 1
for title in jobTitleList:

    print(f"{numberJobTitle}/{len(jobTitleList)}")

    # Hide the browser
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    try:
        print(f"Fetching {title} data...")
        getDom(title)
        print(f"Fecthing {title} completed.")

        print("-"*100)
        numberJobTitle += 1

    except:
        print(f"Fetching {title} failed.")

        print("-"*100)
        numberJobTitle += 1

writetoCSV()