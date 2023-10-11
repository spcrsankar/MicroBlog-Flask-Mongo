from flask import Flask,render_template,request, redirect, url_for
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # mongo connection
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client.MicroBlog


    @app.route('/',methods=['GET','POST'])
    def home():
        
        entries = []

         # fetch data from db
        entries = []
        
            

        if request.method == 'POST':
            entry_title = request.form.get('title')
            entry_content = request.form.get('body')
            print(entry_title)

            if(len(entry_title) < 5):
                return render_template('home.html',entries=entries, title = entry_title, content= entry_content, message="Title should have minimum length of 5")
            
            if(len(entry_content) < 10):
                return render_template('home.html',entries=entries, title = entry_title, content= entry_content, message="Description should have minimum length of 10")    

            current_date = datetime.now()
            formatted_date = current_date.strftime("%b %d")


            new_document = {
                "title": entry_title,
                "content": entry_content,
                "date": formatted_date
            }

            # insert into db
            db.entries.insert_one(new_document)
            for e in db.entries.find({}):
                entries.append({ 
                        "title": e["title"],
                        "content": e['content'],
                        "date": e['date']
                        })
            return redirect(url_for('home'))
       
        for e in db.entries.find({}):
            entries.append({ 
                    "title": e["title"],
                    "content": e['content'],
                    "date": e['date']
                    })
        return render_template('home.html',entries=entries, title = "", content= "")

    return app

