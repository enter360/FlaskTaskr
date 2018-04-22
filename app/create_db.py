#db_create.py
from views import db
from models import FTasks
from datetime import date

db.create_all()


#db.session.add(FTasks("Finish this tutorial",10,10 ,date(2014,3,13), date(2017,4,21),1))
#db.session.add(FTasks("Finish Real Python", date(2014,3,13), 10,1,1))

db.session.commit()