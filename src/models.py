""" flask_sqlalchemy models"""
import datetime
import hashlib
import binascii
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class User(db.Model):
    """ User model """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), unique=True)
    block_until = db.Column(db.DateTime)
    avatar = db.Column(db.String(1024))
    blogs = db.relationship('Blog', backref='users', lazy=True)

    def __init__(self, username: str, password: str, name: str, email: str):
        """ User constructor """
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def verify(self, password):
        (pwd, salt) = self.password.split(";")
        test = binascii.hexlify(hashlib.scrypt(password.encode('utf-8'), salt=salt.encode('utf-8'), n=2,
                                               r=8, p=1)).decode('utf-8')
        return pwd == test

    def serialize(self):
        """ User serialized sans password """
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'block_until': self.block_until,
            'avatar': self.avatar
        }


class BlogCategory(db.Model):
    """ Blog_Category model """
    __tablename__ = 'blog_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class Blog(db.Model):
    """ Blog model """
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    author = db.Column('author_id', db.Integer,
                       db.ForeignKey('users.id'), nullable=False)
    category = db.Column('category_id', db.Integer, db.ForeignKey(
        'blog_category.id'), nullable=False)
    published = db.Column(db.DateTime)
    blog_entries = db.relationship(
        'BlogEntry', backref='blog_entry', lazy=True)

    def __init__(self, title: str, description: str, author: int, category: int, published: datetime):
        self.title = title
        self.description = description
        self.author = author
        self.category = category
        self.published = published


follow_author = db.Table('follow_author',
                         db.Column('author_id', db.Integer, db.ForeignKey(
                             'users.id'), primary_key=True),
                         db.Column('follower_id', db.Integer, db.ForeignKey(
                             'users.id'), primary_key=True)
                         )

follow_blog = db.Table('follow_blog',
                       db.Column('blog_id', db.BigInteger, db.ForeignKey(
                           'blog.id'), primary_key=True),
                       db.Column('follower_id', db.Integer, db.ForeignKey(
                           'users.id'), primary_key=True)
                       )


class BlogEntry(db.Model):
    """ Blog Entry model """
    __tablename__ = 'blog_entry'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    entry = db.Column(db.Text, nullable=False)
    blog = db.Column('blog_id', db.BigInteger,
                     db.ForeignKey('blog.id'), nullable=False)
    published = db.Column(db.DateTime)

    def __init__(self, entry: str, blog: int, published: datetime):
        self.entry = entry
        self.blog = blog
        self.published = published


class Comment(db.Model):
    """ Comment model """
    __table_args__ = (
        db.CheckConstraint(
            '''    (blog_entry_id IS NOT NULL OR parent_id IS NOT NULL)
               AND (blog_entry_id IS NULL OR parent_id IS NULL)'''),
    )
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    entry = db.Column(db.Text, nullable=False)
    user = db.Column('user_id', db.Integer,
                     db.ForeignKey('users.id'), nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False,
                             server_default=func.current_timestamp())
    blog_entry = db.Column('blog_entry_id', db.BigInteger,
                           db.ForeignKey('blog_entry.id'))
    parent = db.Column('parent_id', db.BigInteger, db.ForeignKey('comment.id'))

    def __init__(self, entry: str, user: int, comment_date: datetime, blog_entry: int, parent: int):
        self.entry = entry
        self.user = user
        self.comment_date = comment_date
        self.blog_entry = blog_entry
        self.parent = parent


class Rating(db.Model):
    """ Rating model """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stars = db.Column(db.Integer, nullable=False)
    emoji = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(10), nullable=False)

    def __init__(self, stars: int, emoji: str, description: str):
        self.stars = stars
        self.emoji = emoji
        self.description = description


class BlogRating(db.Model):
    """ Blog Rating blog+user many to many model """
    __tablename__ = 'blog_rating'
    __table_args__ = (
        db.PrimaryKeyConstraint('blog_id', 'user_id'),
    )
    blog = db.Column('blog_id', db.BigInteger, db.ForeignKey('blog.id'))
    user = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    rating = db.Column('rating_id', db.Integer, db.ForeignKey('rating.id'))
    comment = db.Column('comment', db.String(255))

    def __init__(self, blog: int, user: int, rating: int):
        self.blog = blog
        self.user = user
        self.rating = rating


class BlogEntryRating(db.Model):
    """ Blog Entry Rating blog_entry+user many to many model """
    __tablename__ = 'blog_entry_rating'
    __table_args__ = (
        db.PrimaryKeyConstraint('blog_entry_id', 'user_id'),
    )
    blog_entry = db.Column('blog_entry_id', db.BigInteger,
                           db.ForeignKey('blog_entry.id'))
    user = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    rating = db.Column('rating_id', db.Integer, db.ForeignKey('rating.id'))

    def __init__(self, blog_entry: int, user: int, rating: int):
        self.blog_entry = blog_entry
        self.user = user
        self.rating = rating


class CommentRating(db.Model):
    """ Comment Rating model """
    __tablename__ = 'comment_rating'
    __table_args__ = (
        db.PrimaryKeyConstraint('comment_id', 'user_id'),
    )
    comment = db.Column('comment_id', db.BigInteger,
                        db.ForeignKey('comment.id'))
    user = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    rating = db.Column('rating_id', db.Integer, db.ForeignKey('rating.id'))

    def __init__(self, comment: int, user: int, rating: int):
        self.comment = comment
        self.user = user
        self.rating = rating
