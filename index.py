from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    email = request.form.get('email')
    phone = request.form.get('phone')
    note = request.form.get('note')
    
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded')
        
        # create a text file with the same name as the uploaded image
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)
        
        # write the note, email, and phone to the text file
        with open(txt_path, 'w') as f:
            f.write(f"Note: {note}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Phone: {phone}\n")
        
        return redirect(url_for('success'))
    
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
        
@app.route('/success')
def success():
    return "<h1>Image successfully uploaded</h1>"
 
if __name__ == "__main__":
    app.run()
