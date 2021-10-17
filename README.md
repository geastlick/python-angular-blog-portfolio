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
    <table>
        <tr>
            <th>Endpoint</th>
            <th>Methods</th>
            <th>Rule</th>
            <th>Request</th>
            <th>Response</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>login</td>
            <td>POST</td>
            <td>/login</td>
            <td>{username: str, password: str}</td>
            <td>
                <ul>
                    <li>HTTP Status 400 if username or password are missing</li>
                    <li>HTTP Status 404 if username does not exist</li>
                    <li>True if logon was successful, else False</li>
                </ul>
            </td>
            <td>Creates Session in Flask</td>
        </tr>


        <tr>
            <td>authors.popular_authors</td>
            <td>GET</td>
            <td>/authors/popular</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>blog-entries.blog_entry_by_id</td>
            <td>GET</td>
            <td>/blog-entries/<int:id>
            </td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>blogs.blog_by_id</td>
            <td>GET</td>
            <td>/blogs/<int:id>
            </td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>blogs.blog_entries_for_blog_id</td>
            <td>GET</td>
            <td>/blogs/<int:id>/entries</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>blogs.popular_blogs</td>
            <td>GET</td>
            <td>/blogs/popular</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>logout</td>
            <td>GET</td>
            <td>/logout</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>self</td>
            <td>GET</td>
            <td>/self</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>users.create</td>
            <td>POST</td>
            <td>/users</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>users.delete</td>
            <td>DELETE</td>
            <td>/users/<int:id>
            </td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>users.update</td>
            <td>PATCH, PUT</td>
            <td>/users/<int:id>
            </td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    </table>
