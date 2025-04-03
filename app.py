
import rag
from flask import Flask, render_template, request,session,logging,url_for,redirect,flash ,send_from_directory  
from flask_recaptcha import ReCaptcha
import mysql.connector
import os



#import openpyxl
app = Flask(__name__)
recaptcha = ReCaptcha(app=app)
app.secret_key=os.urandom(24)
app.static_folder = 'static'




app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = "6LdbAx0aAAAAAANl04WHtDbraFMufACHccHbn09L",
    RECAPTCHA_SECRET_KEY = "6LdbAx0aAAAAAMmkgBKJ2Z9xsQjMD5YutoXC6Wee"
))




recaptcha=ReCaptcha()

recaptcha.init_app(app)


app.config['SECRET_KEY'] = 'cairocoders-ednalan'

#database connectivity
conn=mysql.connector.connect(host='localhost',port='3306',user='root',password='b@GH3r!276',database='register')
cur=conn.cursor()

#########################################

# Directory to store uploaded files
UPLOAD_FOLDER = 'test'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Admin credentials
ADMIN_USERNAME = 'reyhane.bagheri1380@gmail.com'
ADMIN_PASSWORD = '12345678'

#########################################

# Google recaptcha - site key : 6LdbAx0aAAAAAANl04WHtDbraFMufACHccHbn09L
# Google recaptcha - secret key : 6LdbAx0aAAAAAMmkgBKJ2Z9xsQjMD5YutoXC6Wee

@app.route("/index")
def home():
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')




@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template('register.html')




@app.route('/forgot')
def forgot():
    
    return render_template('forgot.html')


@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cur.fetchall()
    if len(users)>0:
        session['id']=users[0][0]
        flash('ورود شما با موفقیت انجام شد :))')
        ###############################
        if email == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for('admin'))
        else:
        ###############################
            return redirect('/index')
    else:
        flash('اطلاعات ورود نامعتبر است')
        return redirect('/')
    # return "The Email is {} and the Password is {}".format(email,password)
    # return render_template('register.html')
    


@app.route('/dashboard')
def dashboard():
    # لیست فایل‌های PDF
    pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    return render_template('admin.html', files=pdf_files)

# این مسیر برای خدمت‌رسانی به فایل‌های PDF از دایرکتوری test
@app.route('/test/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

##################################
@app.route('/admin')
def admin():
    # List all PDF files in the upload directory
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    return render_template('admin.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('admin'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('admin'))
    
    if file and file.filename.endswith('.pdf'):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        flash('فایل با موفقیت آپلود شد.')
        return redirect(url_for('admin'))

@app.route('/delete', methods=['GET', 'POST'])
def delete_files():
    if request.method == 'POST':
        selected_files = request.form.getlist('files')
        for file_name in selected_files:
            os.remove(os.path.join(UPLOAD_FOLDER, file_name))
        flash('فایل های انتخابی با موفقیت حذف شدند.')
        return redirect(url_for('admin'))

    # List all PDF files in the upload directory
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    return render_template('admin.html', files=files)

##################################

@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('name') 
    email=request.form.get('uemail')
    password=request.form.get('upassword')


    #cur.execute("UPDATE users SET password='{}'WHERE name = '{}'".format(password, name))
    cur.execute("""INSERT INTO  users(name,email,password) VALUES('{}','{}','{}')""".format(name,email,password))
    conn.commit()
    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cur.fetchall()
    flash('ثبت‌نام شما با موفقیت انجام شد :)))')
    session['id']=myuser[0][0]
    return redirect('/index')

@app.route('/suggestion',methods=['POST'])
def suggestion():
    email=request.form.get('uemail')
    suggesMess=request.form.get('message')

    cur.execute("""INSERT INTO  suggestion(email,message) VALUES('{}','{}')""".format(email,suggesMess))
    conn.commit()
    flash('پیشنهاد شما با موفقیت ارسال شد :))')
    return redirect('/index')


@app.route('/add_user',methods=['POST'])
def register():
    if recaptcha.verify():
        flash('ثبت‌نام کاربر جدید با موفقیت انجام شد')
        return redirect('/register')
    else:
        flash('لطفا مجددا تلاش کنید ') 
        return redirect('/register')


@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')  
    #print(str((userText)))
    return str(rag.query(str(userText)))
    #return(str('test'))
    #return str(chatbot.get_response(userText))

if __name__ == "__main__":
    # app.secret_key=""
    
    app.run()
    

