import subprocess
from time import strftime
from bs4 import BeautifulSoup
import requests
from fpdf import FPDF 
import datetime;

global city, username
username=input("Enter Username: ")
cityinp=input("Enter City: ")
city = cityinp+" weather"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
 
def weather(city):
    global location, weatherf
    city = city.replace(" ", "+")
    res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    weatherf=weather+"°C, "+info
weather(city)



def makepdf(x,y,resultfromtxt):
    class PDF(FPDF):
        def header(self):
            self.image('pdfbgi.png', 0, 0, 210)
            self.set_font('Arial', 'B', 30)
            self.cell(80)
            self.cell(30, 30, 'Mal-Or-Not', 0, 1, 'C')
            self.set_font('Arial', 'U', 25)
            if(y=='ip' or y=='url'):
                self.cell(190, 10, y.upper()+' Report', 0, 1, 'C')
            else:
                self.cell(190, 10, y.capitalize()+' Report', 0, 1, 'C')
            self.ln(20)

        def footer(self):
            self.set_y(-20)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 5, "Report generated at: "+txs, 0, 1, 'L')
            self.cell(0, 5, "Report generated by: "+username, 0, 1, 'L')
            self.cell(0, 5, "Location: "+location, 0, 0, 'L')
            self.cell(0, 5, 'Page ' + str(self.page_no()) + '/{nb}', 0, 1, 'R')
            self.set_text_color(127, 127, 127)
            self.cell(0, 5, "© 2022 Mal-Or-Not, All rights reserved.", 0, 0, 'C')

    pdf = PDF()
    pdf.alias_nb_pages()
    name="reports/"+y+"/"+x+".pdf"

    ct=datetime.datetime.now().isoformat(' ', 'seconds')
    txs=str(ct)

    pdf.add_page()
    pdf.set_font("Arial", 'B', size = 15) 
    file = open("output/"+y+"/"+x+"."+y+".report", "r") 
    for g in file:
            pdf.multi_cell(0, 10, txt = g, border=1, align = 'L') 

    pdf.output(name)

def IP():
    global typeid
    typeid='ip'
    global inp
    inp= input("Enter IP: ")
    subprocess.check_output(["./ipintel.sh", "-i", inp])
    with open("output/ip/"+inp+".ip.report","r") as f:
        data=f.read()
    print ('RESULT BEGINS HERE'.center(100,'-'))
    print (data)
    print ('RESULT ENDS HERE'.center(100,'-'))
    makepdf(inp,typeid,data)

def Domain():
    with open("usernamelocation.txt","w") as n:
        n.write(username+'\n'+location)
    subprocess.call(['python3','WhoIsInfo.py'])

def Email():
    global typeid
    typeid='email'
    global inp
    inp= input("Enter E-MAIL: ")
    subprocess.check_output(["./email.sh",inp])
    with open("output/email/"+inp.split("@")[0]+".email.report","r") as f:      # I changed
        data=f.read()
    print ('RESULT BEGINS HERE'.center(100,'-'))
    print (data)
    print ('RESULT ENDS HERE'.center(100,'-'))    
    newinp=inp.split("@")[0]
    makepdf(newinp,typeid,data)

def phno():
    global typeid
    typeid='number'
    global inp
    inp= input("Enter phone number: ")
    subprocess.check_output(["sh","./number.sh", inp])
    with open("output/number/"+inp+".number.report","r") as f:
        data=f.read()
    print ('RESULT BEGINS HERE'.center(100,'-'))
    print (data)
    print ('RESULT ENDS HERE'.center(100,'-'))
    makepdf(inp,typeid,data)

def link():
    global typeid
    typeid='url'
    global inp
    inp= input("Enter the URL: ")
    subprocess.check_output(["./urlreport.sh", inp])
    with open("output/url/"+inp.split("/")[2]+".url.report","r") as f:
        data=f.read()
    print ('RESULT BEGINS HERE'.center(100,'-'))
    print (data)
    print ('RESULT ENDS HERE'.center(100,'-'))
    newinp=inp.split("/")[2]
    makepdf(newinp,typeid,data)

def files():
    global typeid
    typeid='file'
    global inp
    inp = input("Enter file path: ")
    subprocess.check_output(["./file.sh", inp])
    with open("output/file/"+inp.split("/")[-1].split(".")[0]+".file.report","r") as f:
        data=f.read()
    print ('RESULT BEGINS HERE'.center(100,'-'))
    print (data)
    print ('RESULT ENDS HERE'.center(100,'-'))
    newinp=inp.split("/")[-1].split(".")[0]
    makepdf(newinp,typeid,data)

while True:
    choice = int(input("1) FILE\n2) URL\n3) IP\n4) E-MAIL\n5) Domain\n6) Phone Number\n7) Exit\nWhich entity do you wish to test?: "))
    if choice==1:
            files()
    elif choice==2:
            link()
    elif choice==3:
            IP()
    elif choice==4:
            Email()
    elif choice==5:
            Domain()
    elif choice==6:
            phno()
    elif choice==7:
            break
    else:
            print ("Incorrect Option")
