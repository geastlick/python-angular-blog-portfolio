# python-angular-blog-portfolio
Portfolio project created during NuCamp Python-SQL bootcamp

* update src/__init__.py create_app parameters, specifically the database URI
* execute "flask db upgrade".  This will apply all migrations.
* execute "python seed.py".  This will pre-populate the database tables with fake data.  There is a default user demo/demo for testing.
* execute "flask run".  This will start the API server.  By default it runs on http://localhost:5000/api/
* You must have nodejs and npm installed
* execute "cd ui; npm install; ng serve".  This will start the Angular dev server at http://localhost:4200

# Technology stack

## Back end
* [Python](http://python.org) 3.9.6
  * [Flask](https://flask.palletsprojects.com) 2.0.1:  Provides server/controller application
  * [SQLAlchemy](https://www.sqlalchemy.org) 1.4.17:  Provides database/model interface (ORM)
  * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com) 2.5.1 : Integrates the two
    * *Various other supporting libraries mentioned in requirements.txt*

## Front end
* [TypeScript](https://www.typescriptlang.org) 4.3.5
  * [Angular](http://angular.io) 12.2.9:  Provides SPA (Single Page Application) opinionated framework
  * [PrimeNG](http://primefaces.org/primeng) 12.2.0:  Component library for Angular
  * [PrimeFlex](http://primefaces.org/primeflex) 3.0.1:  Styling css for PrimeNG
    * *Various other supporting libraries mentioned in package.json*

## API
Method | URI | Description
------ | --- | -----------
POST | api/login | Payload: {username, password}.  Returns 400 if username/password not provided or username doesn't exist, otherwise, returns True if sucessful.
GET | api/logout | Deletes session data and returns True
GET | api/self | Returns 400 if no session, else returns user {id, username, name, email, block_until, avatar }
POST | api/users | Payload: {username, password, name, email}.  Returns 400 if any are not provided, username is less than 3 characters or password is less than 8 characters.  Also returns {error} 409 if username/email are already taken.  Returns created user {id, username, name, email, block_until, avatar} when successful
DELETE | api/users/<id:int> | Returns 400 if not logged in as the user to be deleted.  Logs out and returns true if successful
PUT, PATCH | api/users/<id:int> | Returns 400 if not logged in as the user to be deleted.  Will change username, name, email, or password depending on payload.  If changing password, then the old password must be provided as well.
GET | api/authors | Returns {id, name, avatar} or all authors who have published a blog order by name
GET | api/blogs | Returns {id, title, description, category} of all published blogs order by ratings