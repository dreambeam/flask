from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set file size
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Set a DB, tested in the Venv
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/bleza/Documents/flask/flask-upload/datafile.db'

# db instance
db=SQLAlchemy(app)

# db: model
class Datafile(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
	file=request.files['datafile']
	# 1 * 2
	newFile=Datafile(name=file.filename, data=file.read())
	db.session.add(newFile)
	db.session.commit()
	return file.filename
	#return redirect(url_for('index'))

@app.route('/download', methods=['GET', 'POST'])
def download():

	data_file = Datafile.query.filter_by(id=1).first()
	#return send_file(BytesIO(data_file.data), attachement_filename="", as_attachment=True)

if __name__== '__main__':
	app.run(debug=True,host='0.0.0.0', port=9000)