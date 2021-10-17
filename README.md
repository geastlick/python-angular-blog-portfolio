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
    [Online Documentation](https://github.com/geastlick/python-angular-blog-portfolio/README_API.html)