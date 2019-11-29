import os,io,re,glob
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'date_scanner.json'
image_list=[]
images=glob.glob("*.jpeg")
count=0
for im in images:
    count=count+1
    image_list.append(im)


date_list=[]
c=0
found=0
ntfound=0
year=""
client=vision.ImageAnnotatorClient()
path="4.jpeg"
for path in image_list:
    with io.open(path,'rb') as image_file:
        content=image_file.read()
    image=vision.types.Image(content=content)
    response=client.text_detection(image=image)
    texts=response.text_annotations
    maintext=""
    for text in texts:
        maintext=maintext+text.description
    maintext=maintext.replace("\n","")
    maintext=maintext.replace(" ","#")
    text=maintext.lower()
    dateformat="\d{1,2}[-/](\d{1,2}|\D{3})[-/](\d{2}|\d{4})"
    usdate1="\d{1,2}(jan|feb|mar|apr|may|june|july|aug|sept|oct|nov|dec)[',](\d{2}|\d{4})"
    usdate2="(jan|feb|mar|apr|may|june|july|aug|sept|oct|nov|dec)\d{1,2}[',](\d{2}|\d{4})"
    oladate="\w{3}(jan|feb|mar|apr|may|june|july|aug|sept|oct|nov|dec)[',]\d{1,2}"
    noyeardate="[0-3][0-9][/][0-3][0-9]"
    r1=re.search(dateformat,text)
    r2=re.search(usdate1,text)
    r3=re.search(usdate2,text)
    r4=re.search(oladate,text)
    r5=re.search(noyeardate,text)
    s=""
    invi="invalid"
    if r1:
        dateformat="\d{1,2}[-/](\d{1,2}|\D{3})[-/][2][0][0-1][0-9]"
        r11=re.search(dateformat,text)
        if r11:
            for i in range(r11.start(),r11.end()):
                s=s+text[i]
            
            date_list.append(s)
            found=found+1
        else:
            for i in range(r1.start(),r1.end()):
                s=s+text[i]
            
            date_list.append(s)
            found=found+1    
    elif r2:
        usdate1="\d{1,2}\w{3}[',]\d{4}"
        r21=re.search(usdate1,text)
        if r21:
            for i in range(r21.start(),r21.end()):
                s=s+text[i]
            
            date_list.append(s)
            found=found+1
        else:
            for i in range(r2.start(),r2.end()):
                s=s+text[i]
            date_list.append(s)
            found=found+1
    elif r3:
        usdate2="(january|february|march|april|may|june|july|august|september|october|november|december)\d{1,2}[',](\d{4}|\d{2})"
        r31=re.search(usdate2,text)
        if r31:
            for i in range(r31.start(),r31.end()):
                 s=s+text[i]
            
            date_list.append(s)
            found=found+1
        else:
            for i in range(r3.start(),r3.end()):
                s=s+text[i]   
            date_list.append(s)
            found=found+1
    elif r4:
        for i in range(r4.start(),r4.end()):
             s=s+text[i]   
        date_list.append(s)
        found=found+1
    elif r5:
        for i in range(r5.start(),r5.end()):
            s=s+text[i]   
        date_list.append(s)
        found=found+1
            
            
    else:
        ntfound=ntfound+1
        date_list.append(invi)
             

print(found,date_list,ntfound)
acc=0
acc=(595-ntfound)/595
print("Accuracy=",acc*100)

'''
finish that google billing or this serice wont run
'''
