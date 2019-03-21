from flask import Flask, jsonify ,request
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
import os,jwt,datetime
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
mysql = MySQL()

UPLOAD_FOLDER = './image_source/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'aacd1234'
app.config['MYSQL_DATABASE_DB'] = 'flask_book'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#jwt
app.config['SECRET_KEY'] = 'thisissecretkey'


mysql.init_app(app)
bcrypt = Bcrypt(app)

conn = mysql.connect()
cur = conn.cursor()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']
        
        if not token:
            return jsonify({'message':'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            cur.execute("select * from tbl_user WHERE id_user="+str(data['id_user'])+"")
            r  = cur.fetchone()
            resp_data = dict(zip([c[0] for c in cur.description], r))
            current_user = resp_data['username']
         
        except:
            return jsonify({'message':'Token is invalid!'}),401

        return f(current_user,*args,**kwargs)
    
    return decorated

@app.route('/')
@token_required
def all_data_get(current_user):
    print(current_user)
    cur.execute('''select * from tbl_books''')
   
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    resp = jsonify({
        'code':200,
        'result' : r
        })
    resp.status_code = 200
    return resp

@app.route('/book/<id>')
@token_required
def one_data_get(current_user,id):
    
    cur.execute("select * from tbl_books WHERE id_book="+id+"")
    r  = cur.fetchone()
    
    if r != None:
        resp_data = dict(zip([c[0] for c in cur.description], r))
        resp = jsonify({
            'code':200,
            'result' : resp_data
            })
        resp.status_code = 200
    else:
        return jsonify({'code':401,'message':'Data Not Found'}),401
    return resp

@app.route('/login', methods=['POST'])
def login_post():
    
    json_data = request.json

    password = bcrypt.generate_password_hash(json_data['password']).decode('utf-8')
    sql = "SELECT * FROM tbl_user WHERE username=\'"+json_data['username']+"\'"

    cur.execute(sql)
    r = cur.fetchone()
    conn.commit()
    if bcrypt.check_password_hash(r[2],json_data['password']):
        print('Match Password')
        token = jwt.encode({
            'id_user':r[0],
            'full_name':r[3],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        print(jwt.decode(token,app.config['SECRET_KEY']))
        resp = jsonify({
            'code':200,
            'message' : 'Successfull to login',
            'token':token.decode('UTF-8')
        })
        resp.status_code = 200
    else:
        print('Password didn\'t match')
        resp = jsonify({
            'code':401,
            'message' : 'Login failed'
        })
        resp.status_code = 401
    
    return resp

@app.route('/register', methods=['POST'])
def register_post():
    
    json_data = request.json
    
    password = bcrypt.generate_password_hash(json_data['password']).decode('utf-8')
    excec = cur.execute('''INSERT INTO tbl_user(username,password,full_name) 
                VALUES(%s,%s,%s)''',(
                json_data['username'],
                password,
                json_data['full_name']))
            
    conn.commit()
    if excec:
        resp = jsonify({
        'code':200,
        'message' : 'Successfull to register'
        })
        resp.status_code = 200
    else:
        resp = jsonify({
        'code':401,
        'message' : 'register failed'
        })
        resp.status_code = 401
    
    return resp

@app.route('/insert_book', methods=['POST'])
@token_required
def data_post(current_user):
    
    # json_data = request.json
  
    form_data = request.form
    json_data = dict(form_data)

    if not list(request.files):
        json_data['cover'] = ''
    else:
        cover = request.files['cover']
        
        if cover and allowed_file(cover.filename):
            filename = secure_filename(cover.filename)
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            json_data['cover'] = filename
 
    excec = cur.execute('''INSERT INTO tbl_books(title,description,author,date_book,price,cover,book_status) 
                VALUES(%s,%s,%s,%s,%s,%s,%s)''',(
                json_data['title'],
                json_data['description'],
                json_data['author'],
                json_data['date_book'],
                json_data['price'],
                json_data['cover'],
                json_data['book_status']))
            
    conn.commit()
    if excec:
        resp = jsonify({
        'code':200,
        'message' : 'data was added into table'
        })
        resp.status_code = 200
    else:
        resp = jsonify({
        'code':401,
        'message' : 'data failed add into table'
        })
        resp.status_code = 401
    
    return resp

@app.route('/update_book/<id>', methods=['PUT'])
@token_required
def data_update(current_user,id):
    
    # json_data = request.json
    # json_data = list(json_data.values())
    form_data = request.form
    json_data = dict(form_data)

    print(json_data)
  
    if not list(request.files):
        excec = cur.execute('''UPDATE tbl_books SET title=%s,description=%s,
                    author=%s,date_book=%s,price=%s,book_status=%s 
                WHERE id_book='''+id+'''''',(
                json_data['title'],
                json_data['description'],
                json_data['author'],
                json_data['date_book'],
                json_data['price'],
                json_data['book_status']))
    else:
        cover = request.files['cover']
        
        if cover and allowed_file(cover.filename):
            filename = secure_filename(cover.filename)
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            json_data['cover'] = filename

        excec = cur.execute('''UPDATE tbl_books SET title=%s,description=%s,
                    author=%s,date_book=%s,price=%s,cover=%s,book_status=%s 
                WHERE id_book='''+id+'''''',(
                json_data['title'],
                json_data['description'],
                json_data['author'],
                json_data['date_book'],
                json_data['price'],
                json_data['cover'],
                json_data['book_status']))
    
    
    conn.commit()
    if excec:
        resp = jsonify({
        'code':200,
        'message' : 'data was updated'
        })
        resp.status_code = 200
    else:
        resp = jsonify({
        'code':401,
        'message' : 'data failed update into table'
        })
        resp.status_code = 401
    

    return resp

@app.route('/delete_book/<id>', methods=['DELETE'])
@token_required
def data_delete(current_user,id):

    cur.execute("select * from tbl_books WHERE id_book="+id+"")
    r  = cur.fetchone()
    # resp_data = dict(zip([c[0] for c in cur.description], r))
    if r != None:
        resp_data = dict(zip([c[0] for c in cur.description], r))
        cover = resp_data['cover']

    # path = os.path.dirname(os.path.realpath(__file__))+'/image_source'

    
    if os.path.exists('image_source/'+cover):
        os.remove('image_source/'+cover)
        print('file was deleted!')
    else:
        print("The file does not exist")
    excec = cur.execute('''DELETE FROM tbl_books 
                WHERE id_book='''+id+'''''')
    
    conn.commit()
    if excec:
        
        
        resp = jsonify({
        'code':200,
        'message' : 'data was Deleted'
        })
        resp.status_code = 200
    else:
        resp = jsonify({
        'code':401,
        'message' : 'data failed to delete'
        })
        resp.status_code = 401
    

    return resp

if __name__ == '__main__':
    app.run(debug=True)