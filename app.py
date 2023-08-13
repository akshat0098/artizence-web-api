# an object of WSGI application
from flask import Flask, jsonify , request , redirect , render_template
import json
import os 
import db
from serializers import AlchemyEncoder
from db import db as Database
import requests
# app init

app = Flask(__name__)   # Flask constructor

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Database.init_app(app)

app.app_context().push()
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/',methods=['GET','POST'])      
def hello():
    
    if request.method == 'POST':
        title = request.form.get('heading')
        file = request.files['banner_image']
        file_name= file.filename
        
        article = db.Article(title,file_name)
        Database.session.add(article)
        Database.session.commit()

        return redirect(f"/section/{article.id}")
        
    return render_template('dashboard.html')


@app.route('/section/<int:id>',methods=['GET', 'POST'])
def section(id):
    
    article = db.Article.query.filter_by(id=id).first()

    if request.method == "POST":
        heading = request.form.get('section_heading')
        text = request.form.get('section_article')
        image_path = request.files['image']
        
        if image_path.filename=='':
            filename=''
        else:
            filename =  image_path.filename
            
        section = db.Section(heading=heading,text=text,image_path=filename,article=id)
        Database.session.add(section)
        Database.session.commit()

        #Section

    # we will search for sections also
    section = db.Section.query.filter_by(article=id).all()

    for x in section:
        print(x)

    return render_template('section.html',heading=article.title,sections=section)

@app.route('/api')
def api():
    
    found_users = db.Author.query.all()
    
    for x in found_users:
        Database.session.delete(x)
        Database.session.commit()

    return jsonify("This is the api Homepage")


@app.route('/api/author',methods=['GET', 'POST'])
def author():
    if request.method == "POST":
        name =  request.form.get('name')
        role = request.form.get('role')
        compose = f'{name}-{role}' 

        #if True:
        try:
            author = db.Author(name,role,compose)
            Database.session.add(author)
            Database.session.commit()

            return jsonify({
                'message':"Author Profile Successfully Created :)" ,   
                'status':"201"
            })

        
        except:
            return jsonify({
                'message':"Author Already Exists! Explore an alternative pen name, like Neha Gupta, N. Gupta. Additionally, review your role and confirm precise name spelling. Modify accordingly. " ,   
                'status':"403"
            })
        
@app.route('/api/blog/',methods=['GET'])
def blog():
    """
    return all blogs and 
    """

    articles = db.Article.query.all()
    
    
    #print(json.dumps(articles,cls=AlchemyEncoder))

    return json.dumps(articles,cls=AlchemyEncoder)

@app.route('/api/blog/article/<int:id>',methods=['GET','POST'])
def article(id):
    
    sections = db.Section.query.filter_by(article=id).all()
    print(sections)
    return json.dumps(sections,cls=AlchemyEncoder)



if __name__=='__main__':
   Database.create_all()
   app.run(debug=True)