from flask import Flask,request,jsonify
import os,io,re,glob,base64
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image

date_list=[]
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\adars\Desktop\internship\rest\date_scanner.json'
client=vision.ImageAnnotatorClient()
app = Flask(__name__)
@app.route('/jason_example',methods=['POST'])
def jason_example():
    req_data=request.get_json()
    base_64_image_content=req_data['imgcnt']
    image = base64.b64decode(base_64_image_content)
    padding = len(image) % 4
    if padding > 0:
        image += '='* (4 - padding)
    #image=Image.open(io.BytesIO(image))
    image=vision.types.Image(content=image)
    response=client.text_detection(image=image)
    texts=response.text_annotations
    maintext=""
    for text in texts:
        maintext=maintext+text.description
    maintext=maintext.replace("\n","")
    maintext=maintext.replace(" ","#")
    text=maintext.lower()
    print(text)
    dateformat="\d{1,2}[-/](\d{1,2}|\D{3})[-/](\d{2}|\d{4})"
    usdate1="\d{1,2}(jan|feb|mar|apr|may|june|july|aug|sept|oct|nov|dec)[',](\d{4}|\d{2})"
    usdate2="(jan|feb|mar|apr|may|june|july|aug|sept|oct|nov|dec)\d{1,2}[',](\d{4}|\d{2})"
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
        dateformat="\d{1,2}[-/](\d{1,2}|\D{3})[-/](\d{4})"
        r11=re.search(dateformat,text)
        if r11:
            for i in range(r11.start(),r11.end()):
                s=s+text[i]   
            date_list.append(s)
            
        else:
            for i in range(r1.start(),r1.end()):
                s=s+text[i]   
            date_list.append(s)
                
    elif r2:
        usdate1="\d{1,2}\w{3}[',]\d{4}"
        r21=re.search(usdate1,text)
        if r21:
            for i in range(r21.start(),r21.end()):
                s=s+text[i]
            date_list.append(s)
            
        else:
            for i in range(r2.start(),r2.end()):
                s=s+text[i]
            date_list.append(s)
            
    elif r3:
        usdate2="(january|february|march|april|may|june|july|august|september|october|november|december)\d{1,2}[',](\d{4}|\d{2})"
        r31=re.search(usdate2,text)
        if r31:
            for i in range(r31.start(),r31.end()):
                 s=s+text[i]
            date_list.append(s)
            
        else:
            for i in range(r3.start(),r3.end()):
                s=s+text[i]   
            date_list.append(s)
            
    elif r4:
        for i in range(r4.start(),r4.end()):
             s=s+text[i]   
        date_list.append(s)
        
    elif r5:
        for i in range(r5.start(),r5.end()):
            s=s+text[i]   
        date_list.append(s)
        
            
            
    else:
        
        date_list.append(invi)
             
            # print("invalid")
    return jsonify({"date":date_list})


'''
finish that google billing or this serice wont run
'''
