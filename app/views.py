# views.py 

from flask import Flask, flash , redirect, render_template, request, session, url_for, g

from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import FTasks, User
from forms import AddTask, RegisterForm, LoginForm

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You are logged out. Bye. :(')
	return redirect(url_for('login'))

@app.route('/', methods= ['GET', 'POST'])
def login():
	error = None
	if request.method =='POST':
		u = User.query.filter_by(name= request.form['name'],
			password= request.form['password']).first()
		if u is None:
			error = 'Invalid  username or password'
		else:
			session['logged_in'] = True
			flash('You are logged in . Go fucking crazy')
			return redirect(url_for('tasks'))
	return render_template("login.html", form = LoginForm(request.form), error=error)



#@app.route('/', methods=['GET', 'POST'])
#def login():
 #   if request.method == 'POST':
  #      if request.form['username'] != app.config['USERNAME'] \
  #              or request.form['password'] != app.config['PASSWORD']:
  #          error = 'Invalid Credentials. Please try again.'
  #          return render_template('login.html', error=error)
  #      else:
  #          session['logged_in'] = True
  #          flash('Welcome!')
  #          return redirect(url_for('tasks'))
  #  return render_template('login.html')
	
@app.route('/tasks')
@login_required
def tasks():
	#g.db = connect_db()
	#cur = g.db.execute('SELECT NAME, DUE_DATE, PRIORITY, TASK_ID FROM FTASKS WHERE STATUS=1')
	#open_tasks= [dict(name=row[0], due_date=row[1],priority=row[2],task_id=row[3]) for row in cur.fetchall()]
	#cur = g.db.execute(' SELECT NAME , DUE_DATE, PRIORITY, TASK_ID FROM FTASKS WHERE STATUS=0')
	#closed_tasks = [dict(name = row[0], due_date=row[1],priority=row[2],task_id=row[3]) for row in cur.fetchall()]
	#g.db.close()
	#return render_template('tasks.html', open_tasks=open_tasks, closed_tasks=closed_tasks)
	open_tasks = db.session.query(FTasks).filter_by(status='1').order_by(FTasks.due_date.asc())

	closed_tasks = db.session.query(FTasks).filter_by(status='0').order_by(FTasks.due_date.asc())

	return render_template('tasks.html',form = AddTask(request.form), open_tasks=open_tasks, closed_tasks=closed_tasks)


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
	print ( "new_task")
	form = AddTask(request.form, csrf_enabled=False)
	if form.validate_on_submit():
		print ("Form validated")
		new_task = FTasks(
			form.name.data,
			form.due_date.data,
			form.priority.data,
			form.posted_date.data,
			'1',
			'1')
		db.session.add(new_task)
		db.session.commit()
		flash('New entry was succssfully posted. Thanks')
	else:
		print ("Addition Failed")
		flash('Error entry not added.')
	return redirect(url_for('tasks'))

@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
	#g.db = connect_db()
	#cur = g.db.execute('update ftasks set status = 0 where task_id='+str(task_id))
	#g.db.commit()
	#g.db.close()
	new_id = task_id
	db.session.query(FTasks).filter_by(task_id=new_id).update({"status":"0"})
	db.session.commit()
	flash('The task was marked as complete.')
	return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
	#g.db = connect_db()
	#cur = g.db.execute('delete from ftasks where task_id='+str(task_id))
	#g.db.commit()
	#g.db.close()
	new_id = task_id
	db.session.query(FTasks).filter_by(task_id = new_id).delete()
	db.session.commit()
	flash('Task was deleted')
	return redirect(url_for('tasks'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	error=None 
	form = RegisterForm(request.form, csrf_enabled=False)
	if form.validate_on_submit():
		new_user = User(
			form.name.data,
			form.email.data,
			form.password.data,
			)
		db.session.add(new_user)
		db.session.commit()
		flash('Thaks for registering. Please login. ')
		return redirect(url_for('login'))
	return render_template('register.html', form=form, error=error)