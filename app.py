from flask import Flask, jsonify ,request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'aacd1234'
app.config['MYSQL_DATABASE_DB'] = 'flask_book'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
conn = mysql.connect()
cur = conn.cursor()

@app.route('/')
def all_data_get():
    
    cur.execute('''select * from tbl_books''')
   
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    resp = jsonify({
        'code':200,
        'result' : r
        })
    resp.status_code = 200
    return resp

@app.route('/book/<id>')
def one_data_get(id):
    
    cur.execute("select * from tbl_books WHERE id_book="+id+"")
    r  = cur.fetchone()
    resp_data = dict(zip([c[0] for c in cur.description], r))
    resp = jsonify({
        'code':200,
        'result' : resp_data
        })
    resp.status_code = 200
    return resp

@app.route('/insert_book', methods=['POST'])
def data_post():
    
    json_data = request.json
    json_data = list(json_data.values())
    
    excec = cur.execute('''INSERT INTO tbl_books(title,description,author,date_book,price,book_status) 
                VALUES(%s,%s,%s,%s,%s,%s)''',json_data)
            
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
def data_update(id):
    
    json_data = request.json
    json_data = list(json_data.values())
    
    excec = cur.execute('''UPDATE tbl_books SET title=%s,description=%s,
                    author=%s,date_book=%s,price=%s,book_status=%s 
                WHERE id_book='''+id+'''''',json_data)
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
def data_delete(id):
    
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