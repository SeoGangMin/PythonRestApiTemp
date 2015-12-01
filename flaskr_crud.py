from database import init_db
from database import db_session
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from models import User
import json

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.before_request
def before_request():
  print 'before_request'

@app.teardown_request
def teardown_request(exception):
	print 'teardown_request'

@app.route('/')
def show_entries():
	users_query = db_session.query(User)
	entries = [dict(name=user.name, email=user.email, description=user.description) for user in users_query]

	print len(entries)

	return json.dumps(entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)

	u = User(request.form['name'], request.form['email'])
	db_session.add(u)
	db_session.commit()

	flash('New User was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/update', methods=['POST'])
def update_entry():
	u = db_session.query(User).filter(User.name==request.form['name']).first()
	u.description = 'my description'

	db_session.commit()

	print '##########'
	print u.description

	return redirect(url_for('show_entries'))

@app.route('/delete', methods=['POST'])
def delete_entry():
	u = User(request.form['name'], request.form['email'])

	db_session.query(User).filter(User.name==u.name).delete()
	db_session.commit()

	flash('Selected User was successfully deleted')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    init_db()
    app.run()
