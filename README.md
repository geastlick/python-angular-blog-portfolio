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

   | <table>
        <tbody>
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
                </td>
                <td>Creates Session in Flask</td>
            </tr>
            <tr>
                <td>logout</td>
                <td>GET</td>
                <td>/logout</td>
                <td></td>
                <td>True</td>
                <td>Deletes Session in Flask</td>
            </tr>
            <tr>
                <td>self</td>
                <td>GET</td>
                <td>/self</td>
                <td></td>
                <td>
                   <ul>
                    <li>HTTP Status 400 if session does not exist</li>
                    <li>HTTP Status 400 if User does not exist for the configured session</li>
                    <li>Valid session returns {id: int, username: str, name: str, email: str, block_until: datetime, avatar: str}</li>
                 </ul>
             </td>
                <td>Returns User information for currently logged in user</td>
            </tr>
            <tr>
                <td>users.create</td>
                <td>POST</td>
                <td>/users</td>
                <td>{username: str, pasword: str, name: str, email: str}</td>
                <td>
                 <ul>
                  <li>HTTP Status 400 if username, password, name, or email are not present</li>
                  <li>Http Status 400 if username is less than 3 characters or password is less than 8 characters</li>
                  <li>{error: "Duplicate username"} if username is already used</li>
                  <li>{error: "Duplicate email"} if email is already used</li>
                  <li>{success: {id: int, username: str, name: str, email: str, block_until: datetime, avatar: str} if User creation is successful</li>
                 </ul>
             </td>
                <td>aka Register</td>
            </tr>
            <tr>
                <td>users.delete</td>
                <td>DELETE</td>
                <td>/users/<int:id></td>
                <td></td>
                <td>
             <ul>
              <li>Http Status 404 if User does not exist</li>
              <li>Http Status 400 if id does not correspond to the currently logged in user</li>
              <li>True if User is successfully deleted, else False</li>
                 </ul>
             </td>
                <td>Deletes session in flask if User deletion is successful</td>
            </tr>
            <tr>
                <td>users.update</td>
                <td>PATCH, PUT</td>
                <td>/users/<int:id></td>
                <td>{username: str, pasword: str, old_password: str, name: str, email: str} -- All are optional.  If password is present, then old_password must also be present for verification</td>
                <td><ul>
              <li>Http Status 404 if User does not exist</li>
              <li>Http Status 400 if id does not correspond to the currently logged in user</li>
                 <li>Http Status 400 if username is present (and modified) and either less than 3 characters or already exists in the database</li>
                 <li>Http Status 400 if email is present (and modified) and already exists in the database</li>
                 <li>Http Status 400 if password is present and less than 8 characters or old_password is not also provided or password verification of old_password fails</li>
              <li>True if User is successfully updated, else False</li>
              </ul>  </td>
                <td>PUT should technically replace the entire record, but it will instead behave as a PATCH</td>
            </tr>
            <tr>
                <td>authors.popular_authors</td>
                <td>GET</td>
                <td>/authors/popular</td>
                <td>Supports request params page_size and page, e.g. /authors/popular?page_size=10&page=3.  Page will be ignored unless page_size is also present</td>
                <td>{count_all_authors: int, authors: [{id: int, name: str, avatar: str, stars_avg: decimal, blogs: [{id: int, title: str, blog_stars_avg: decimal}] }] }</td>
                <td>ordered by the ranking of the Authors published blogs.  Only includes authors with at least one published blog and only returns published blogs.  count_all_authors is used for paginating, i.e. (3 {page} - 1) * 10 {page_size} of (80 {count_all_authors} / 10 {page_size})</td>
            </tr>
            <tr>
                <td>blog-entries.blog_entry_by_id</td>
                <td>GET</td>
                <td>/blog-entries/<int:id></td>
                <td></td>
                <td>{id: int, entry: str, published: datetime, stars_avg: decimal, stars_1: int, stars_2: int, stars_3: int, stars_4: int, stars_5: int}</td>
                <td>stars_n are the counts of ratings for that value.  stars_avg is the average of all the ratings.</td>
            </tr>
            <tr>
                <td>blogs.blog_by_id</td>
                <td>GET</td>
                <td>/blogs/<int:id>
                </td>
                <td></td>
                <td>{id: int, title: str, descriptino: str, category: str, published: datetime, author: str, avatar: str, stars_avg: decimal, stars_1: int, stars_2: int, stars_3: int, stars_4: int, stars_5: int}</td>
                <td>stars_n are the counts of ratings for that value.  stars_avg is the average of all the ratings.</td>
            </tr>
            <tr>
                <td>blogs.blog_entries_for_blog_id</td>
                <td>GET</td>
                <td>/blogs/<int:id>/entries</td>
                <td>Supports request params page_size and page, e.g. /blogs/<int:id>/entries?page_size=10&page=3.  Page will be ignored unless page_size is also present</td>
                <td>{count_all_entries: int, blog_entries: [{id: int, entry: str, published: datetime, stars_avg: decimal, stars_1: int, stars_2: int, stars_3: int, stars_4: int, stars_5: int}] }</td>
                <td>stars_n are the counts of ratings for that value.  stars_avg is the average of all the ratings.  count_all_entries is used for paginating, i.e. (3 {page} - 1) * 10 {page_size} of (80 {count_all_entries} / 10 {page_size})</td>
            </tr>
            <tr>
                <td>blogs.popular_blogs</td>
                <td>GET</td>
                <td>/blogs/popular</td>
                <td>Supports request params page_size and page, e.g. /blogs/<int:id>/entries?page_size=10&page=3.  Page will be ignored unless page_size is also present</td>
                <td>{count_all_blogs: int, blogs: [{id: int, title: str, description: str, category: str, published: datetime, author: str, avatar: str, stars_avg: decimal, stars_1: int, stars_2: int, stars_3: int, stars_4: int, stars_5: int}] }</td>
                <td>stars_n are the counts of ratings for that value.  stars_avg is the average of all the ratings.  Only includes published blogs in order of their ranking.  count_all_blogs is used for paginating, i.e. (3 {page} - 1) * 10 {page_size} of (80 {count_all_blogs} / 10 {page_size})</td>
            </tr>
        </tbody>
    </table>
