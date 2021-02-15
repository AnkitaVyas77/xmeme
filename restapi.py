from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, send_from_directory
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os







ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

api=Api(app)
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    caption = db.Column(db.String(50))
    url = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "caption": self.caption,
                "url": self.url}
    
    
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')    

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc())

    return render_template("home.html",posts=posts)

@app.route('/updatepos')
def updatepos():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc())

    return render_template("updatepost.html",posts=posts)




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/memes', methods=['GET','POST'])

def addpost():
    
        
    if request.method == 'POST':
        
            
        if request.headers['Content-Type'] == 'application/json':
            json_data = request.get_json(force=True)
            name = json_data['name']
            caption = json_data['caption']
                
            url = json_data['url']
        else:
            name = request.form['name']
            caption = request.form['caption']
                
            url = request.form['url']
            
        posts=db.session.query(Blogpost)
        if name in posts and caption in posts and url in posts:
            return redirect("/"),409
             
        else:
            post = Blogpost(name=name, caption=caption, url=url,date_posted=datetime.now())

            db.session.add(post)
            db.session.commit()
            

                
            return redirect("/")
    else:
        
        return jsonify([
                {'id': post.id, 'name': post.name, 'caption': post.caption,'url':post.url,'date':post.date_posted}
                    for post in Blogpost.query.order_by(Blogpost.date_posted.desc())
                      ])

@app.route('/memes/<id>', methods=['GET'])
def get_post(id):
    #id=request.args['id']
    post=Blogpost.query.get_or_404(id)
    return jsonify([
                {'id': post.id, 'name': post.name, 'caption': post.caption,'url':post.url,'date':post.date_posted} 
                      ])
@app.route('/memes/delete', methods=['DELETE','GET'])
def deletepost():
    
    id=request.args['id']
    
    post=Blogpost.query.get_or_404(id)
    
    db.session.delete(post)
    db.session.commit()
    if request.method == 'GET':
        return redirect("/")
        
    else:
        return jsonify([
                {'id': post.id, 'name': post.name, 'caption': post.caption,'url':post.image,'date':post.date_posted}
                    for post in Blogpost.query.order_by(Blogpost.date_posted.desc())
                      ])
@app.route('/memes/update', methods=['PUT','GET'])
def updatepost():
    
    id=request.args['id']
    post=Blogpost.query.get_or_404(id)

    if request.args.get('caption'):
        post.caption = request.args['caption']
    if request.args.get('url'):    
        post.url = request.args['url']
    
    
        
    
            
    
    db.session.commit()
    if request.method == 'GET':
        return redirect('/updatepos')
        
    else:
        return jsonify([
                {'id': post.id, 'name': post.name, 'caption': post.caption,'url':post.url, 'date':post.date_posted}
                    for post in Blogpost.query.order_by(Blogpost.date_posted.desc())
                      ])

@app.route('/memes/<id>', methods=['PATCH'])

def patchpost(id):
    render_template("updatepost.html")
    #id=request.args['id']
    post=Blogpost.query.get_or_404(id)
    
    
    if request.args.get('caption'):
        post.caption = request.args['caption']
    if request.args.get('url'):    
        post.url = request.args['url']   
    
            
    
    db.session.commit()
    
    return jsonify([
                {'id': post.id, 'name': post.name, 'caption': post.caption,'url':post.url, 'date':post.date_posted}
                    for post in Blogpost.query.order_by(Blogpost.date_posted.desc())
                      ])

    

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8081)
    
