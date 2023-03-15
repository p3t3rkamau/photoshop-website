from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret key"

# Define correct username and password
correct_username = "peter"
correct_password = "1234"

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username != correct_username or password != correct_password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/index')
def index():
    # get a list of image filenames in the uploads folder
    image_filenames = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.JPG') or f.endswith('.JPEG') or f.endswith('.png') or f.endswith('.PNG') or f.endswith('.gif') or f.endswith('.GIF')]

    # create a list of dictionaries containing image and text file data
    image_data = []
    for filename in image_filenames:
        # get the image file path
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # get the text file path
        text_filename = os.path.splitext(filename)[0] + '.txt'
        text_path = os.path.join(app.config['UPLOAD_FOLDER'], text_filename)
        
        # read the text file data
        with open(text_path, 'r') as f:
            text_data = f.read()
        
        # add the image and text data to the list
        image_data.append({
            'filename': filename,
            'image_path': image_path,
            'text_data': text_data
        })

    # render the template with the image data
    return render_template('server.html', image_data=image_data)

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    email = request.form.get('email')
    phone = request.form.get('phone')
    note = request.form.get('note')

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded')

        # create a text file with the same name as the uploaded image
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)

        # write the note, email, and phone to the text file

        # write the note, email, and phone to the text file
        with open(txt_path, 'w') as f:
            f.write(f"Note: {note}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Phone: {phone}\n")

        return redirect(url_for('index'))

    else:
        flash('Allowed file types are png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], os.path.splitext(filename)[0] + '.txt'))
        flash('File successfully deleted')
    except:
        flash('Error deleting file')
    return redirect(url_for('index'))

 
if __name__ == "__main__":
    app.run()
