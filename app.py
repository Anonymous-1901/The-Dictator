from flask import *
import threading as t
app = Flask(__name__)
import os
import textract 
import codecs
import pdfplumber

@app.route('/')
@app.route('/index')
def index():    
    return render_template('index.html',active="active")

@app.route('/about')
def about():
    return render_template('about.html',active="active")
@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.isdir('.\\uploads'):
        os.mkdir('.\\uploads')
    if request.method == 'POST':
        if 'file' not in request.files:
            return "<h1>NO file present</h1>"
        file = request.files['file']
        if file.filename == '':
            return "no file uploaded"
        if file:
            path = '.\\uploads\\'+file.filename
            file.save(".\\uploads\\"+file.filename)
            ext = file.filename.split('.')[-1]
            if ext =='txt':
                # with open(path,'r') as f:
                #     text = f.read()
                #     text.decode('utf-8')
                with codecs.open(path,encoding='utf-8') as f:
                    text = f.read()
                return render_template('success.html',data = text,file_name=file.filename,text=text)
            elif ext == 'docx':
                with open(path,'r',encoding="utf-8") as f:
                    text = textract.process(path)
                    text = text.decode('utf-8')
                return render_template("success.html", file_name=file.filename,data=text,text=text)
            elif ext=='pdf':
                all_pages = []
                with pdfplumber.open(path) as pdf:
                    for pages in pdf.pages:
                        all_pages.append(pages.extract_text())
                        
                    text = ' '.join(all_pages)
                return render_template('success.html',data = text,file_name=file.filename,text=text) 
            else:
                return render_template('success.html',data="Invalid document format - "+ext)


if __name__ == '__main__':
    app.run(debug=True)
