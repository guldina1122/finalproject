from flask import flash, redirect, render_template, url_for, request, send_file
from app.forms import LoginForm, RegistrationForm, UpdateForm
from app.models import User
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import json
import requests


payload = {
    "search_terms": "python programmer",
    "location": "30301",
    "page": "1"
}



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/faqs')
def faqs():
    return render_template('FAQs.html', title='About')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/announcements')
def announcements():
    return render_template('announcements.html', title='Announcements')


@app.route('/events')
def events():
    return render_template('events.html', title='Events')


@app.route('/science')
def science():
    return render_template('science.html', title='Science')


@app.route('/sport')
def sport():
    return render_template('sport.html', title='Sport')


@app.route('/academic-mobility')
def academicmobility():
    return render_template('academic-mobility.html', title='Academic-mobility')


@app.route('/clubs')
def clubs():
    return render_template('clubs.html', title='Clubs')


@app.route('/schedule')
def schedule():
    return render_template('schedule.html', title='Schedule')


@app.route('/today')
def today():
    return render_template('today.html', title='News of the day')


@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful! Please check the email and password!', 'danger')
    return render_template('sign-in.html', title='Sign-in', form=form)


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        data = {
            "username": form.username.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "group": form.group.data,
            "email": form.email.data,
            "password": hashed_password
        }

        response = requests.post("http://127.0.0.1:8000/create_user", json=data)

        user = User(username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    group=form.group.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('sign_in'))

    return render_template('sign-up.html', title='Sign-up', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)


@app.route("/account-update", methods=['POST', 'GET'])
@login_required
def account_update():
    form = UpdateForm()
    image_file = url_for('static', filename='img/' + current_user.image_file)
    if request.method == "GET":
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.group.data = current_user.group
        form.email.data = current_user.email
        return render_template('account-update.html', title='Account', image_file=image_file, form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.group = form.group.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Your account has been updated!", 'success')
            return redirect(url_for('account'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{error}", 'danger')

    return render_template('account-update.html', title='Account', image_file=image_file, form=form)

@app.route('/download')
def download():
    path = 'static/files/Bachelor1.pdf'
    return send_file(path, as_attachment=True)

@app.route('/download2')
def download2():
    path = 'static/files/Bachelor2.pdf'
    return send_file(path, as_attachment=True)

@app.route('/download3')
def download3():
    path = 'static/files/Bachelor3.pdf'
    return send_file(path, as_attachment=True)

@app.route('/download4')
def download4():
    path = 'static/files/Exam2.pdf'
    return send_file(path, as_attachment=True)


