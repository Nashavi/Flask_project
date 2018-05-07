import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mssql+pyodbc://(LocalDb)\MSSQLLocalDB/Migratedb?driver=SQL+Server+Native+Client+11.0')
db = scoped_session(sessionmaker(bind=engine))


result = db.execute("SELECT * from HR1.JOBS")
for r in result:
    print(" %s has a minimum salary of %i and a maximum salary of %i"%(r.JOB_TITLE, r.MIN_SALARY,r.MAX_SALARY))