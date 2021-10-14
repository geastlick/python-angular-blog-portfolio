# python-angular-blog-portfolio
Portfolio project created during NuCamp Python-SQL bootcamp

update src/__init__.py create_app parameters, specifically the database URI

execute "flask db upgrade".  This will apply all migrations.

execute "python seed.py".  This will pre-populate the database tables with fake data.  There is a default user demo/demo for testing.

execute "flask run".  This will start the API server.  By default it runs on http://localhost:5000/api/

execute "cd ui; ng serve".  This will start the Angular dev server at http://localhost:4200

POST:api/login {username, password}.  Returns 404 if username/password not provided or username doesn't exist, otherwise, returns True if sucessful.
GET:api/logout.  Deletes session data and returns True