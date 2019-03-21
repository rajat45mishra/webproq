
from flask import Flask, request , render_template , url_for , flash , redirect 
from forms import AddAsset ,  ProjectDetail , WarrentyDetail , ReferanceDoc , LegalDocu , InvestmentInfo , AddProjectDocument , AddTechDocument , AssetSpecification , AssetCorrespondance , Investment , Installment
from sa import db ,addasset_data_model,User
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField , SubmitField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = '4546757868697970'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rajat@localhost/test5'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
    
@app.route('/AddAsset' , methods = ['GET' , 'POST'])
def AddAssetForm():
        form = AddAsset() 
        if request.method == 'POST':
            dataAssettype = request.form['Assettype']
            dataAssetname = request.form['Assetname']
            dataAssetnumber = request.form['Assetnumber']
            dataDateofPurchase = request.form['DateofPurchase']
            dataAssestWarrentyUpto = request.form['AssestWarrentyUpto']
            entry = addasset_data_model(dataAssettype, dataAssetname , dataAssetnumber , dataDateofPurchase , dataAssestWarrentyUpto)
            db.session.add(entry)
            db.session.commit()
            return 'form submitted'
        return render_template('AddAsset.html' , form= form)

@app.route('/ProjectDetails' , methods = ['GET' , 'POST'])
def ProjectDetailForm():
    ProjectDetailForm = ProjectDetail()
    if ProjectDetailForm.validate_on_submit():
        return  'Form Sucessfully Submitted!'
    return render_template('Project_Detail.html' , form=ProjectDetailForm)

@app.route("/AddProDoc" , methods = ['GET' , 'POST'])
def AddProDocForm():
    AddProDocForm = AddProjectDocument()
    if AddProDocForm.validate_on_submit():
        return 'Form Sucessfully Submitted!'
    return render_template('Add_Project_Document.html' , form=AddProDocForm)

@app.route('/AddTechDocument' , methods = ['GET' , 'POST'])
def AddTechDocumentForm():
    AddTechDocumentForm = AddTechDocument()
    if AddTechDocumentForm.validate_on_submit():
        return 'Form Sucessfully Submitted !'
    return render_template('Add_Technical_Document.html' , form=AddTechDocumentForm)

@app.route('/AssetSpecification' , methods = ['GET' , 'POST'])
def AssetSpecificationForm():
    AssetSpecificationForm = AssetSpecification()
    if AssetSpecificationForm.validate_on_submit():
        return 'Form Sucessfully Submitted !'
    return render_template('Asset_Specification.html' , form=AssetSpecificationForm)

@app.route('/AssetCorrespondance' , methods = ['GET' , 'POST'])
def AssetCorrespondanceForm():
    AssetCorrespondanceForm = AssetCorrespondance()
    if AssetCorrespondanceForm.validate_on_submit():
        return 'Form Sucessfully Submitted !'
    return render_template('Assets_Correspondance.html' , form=AssetCorrespondanceForm)

@app.route('/Investment' , methods = ['GET' , 'POST'])
def InvestmentForm():
    InvestmentForm = Investment()
    if InvestmentForm.validate_on_submit():
        return 'Form Sucessfully Submitted !'
    return render_template('Investment.html', form=InvestmentForm)

@app.route('/Installment', methods = ['GET' , 'POST'])
def InstallmentForm():
    InstallmentForm = Installment()
    if InstallmentForm.validate_on_submit():
        return 'Form Sucessfully Submitted !'
    return render_template('Installments.html' , form=InstallmentForm)

@app.route('/InvestmentInfo' , methods = ['GET' , 'POST'])
def InvestmentInfoForm():
    InvestmentInfoForm = InvestmentInfo()
    if InvestmentInfoForm.validate_on_submit():
        return 'Form Sucessfully Submitted !'
    return render_template('Investment_Info.html' , form=InvestmentInfoForm)

@app.route('/LegalDocument')
def LegalDocumentForm():
    LegalDocumentForm = LegalDocu()
    if LegalDocumentForm.validate_on_submit():
        return 'Form Sucessfully Submitted !'
    return render_template('Legal_Document.html' , form=LegalDocumentForm)

@app.route('/ReferanceDocument' , methods = ['GET' , 'POST'])
def ReferanceDocumentForm():
    ReferanceDocumentForm = ReferanceDoc()
    if ReferanceDocumentForm.validate_on_submit():
        return 'Form Sucessfully Submitted !'
    return render_template('Referance_Document.html' , form=ReferanceDocumentForm)

@app.route('/WarrentyDetail' , methods = ['GET' , 'POST'])
def WarrentyDetailForm():
    WarrentyDetailForm = WarrentyDetail()
    if WarrentyDetailForm.validate_on_submit():
        return 'Form  Sucessfully Submitted!'
    return render_template('Warrenty_Detail.html' , form=WarrentyDetailForm)

@app.route('/')
def TDM_Home():
    return render_template('first.html')
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Sign Up')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for('login'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080
    app.run(HOST, PORT)