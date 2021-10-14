"""
Populate portfolio database with fake data using the SQLAlchemy ORM.
"""
import datetime
import random
import string
import hashlib
import binascii
import secrets
from faker import Faker
from faker.providers import internet
from src.models import User, Blog, BlogCategory, follow_author, follow_blog, BlogEntry, \
    Comment, Rating, CommentRating, BlogEntryRating, BlogRating, db
from src import create_app

USER_COUNT = 50
BLOG_COUNT = 75


def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    ).encode('utf-8')

    salt = secrets.token_hex(16).encode('utf-8')
    password = binascii.hexlify(hashlib.scrypt(raw, salt=salt, n=2,
                                               r=8, p=1)).decode('utf-8') + ";" + salt.decode('utf-8')

    return password


def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(follow_author.delete())
    db.session.execute(follow_blog.delete())
    BlogRating.query.delete()
    BlogEntryRating.query.delete()
    CommentRating.query.delete()
    Rating.query.delete()
    Comment.query.delete()
    BlogEntry.query.delete()
    Blog.query.delete()
    BlogCategory.query.delete()
    User.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()
    fake.add_provider(internet)

    # Create DEMO user
    salt = secrets.token_hex(16).encode('utf-8')
    password = binascii.hexlify(hashlib.scrypt(b'demo', salt=salt, n=2,
                                               r=8, p=1)).decode('utf-8') + ";" + salt.decode('utf-8')
    last_user = User(
        username="demo",
        password=password,
        name="Demo User",
        email="demo@example.com"
    )
    db.session.add(last_user)

    last_user = None  # save last user
    user_list = ['demo']
    for _ in range(USER_COUNT):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = (first_name[0] + last_name).lower()
        tempuser = username
        while tempuser in user_list:
            n = str(random.randint(1, 150))
            tempuser = username + n
        username = tempuser
        user_list.append(username)

        last_user = User(
            username=username,
            password=random_passhash(),
            name=first_name + " " + last_name,
            email=username + "@" + fake.domain_name()
        )
        db.session.add(last_user)

    # insert users
    db.session.commit()

    CATEGORY_COUNT = 6
    db.session.add(BlogCategory(name="Clean Comedy",
                   description="Funny, suitable for all audiences"))
    db.session.add(BlogCategory(
        name="Comedy", description="Funny, might be a little edgy"))
    db.session.add(BlogCategory(name="Shopping",
                   description="Malls, Products, and everything in between"))
    db.session.add(BlogCategory(
        name="Technical", description="If it is about technology, you will find it here"))
    db.session.add(BlogCategory(name="Politics",
                   description="Viewer beware, but keep it clean and polite"))
    # Creating the last entry differently so we can obtain the id
    last_blog_category = BlogCategory(
        name="Religion", description="Viewer beware, but keep it clean and polite")
    db.session.add(last_blog_category)
    # Insert blog categories
    db.session.commit()

    last_blog = None  # save last blog
    for _ in range(BLOG_COUNT):
        published = None
        if random.randint(0, 10) <= 8:
            published = fake.date_this_year()

        last_blog = Blog(
            title=fake.sentence(nb_words=10, variable_nb_words=True),
            description=fake.paragraph(
                nb_sentences=5, variable_nb_sentences=True),
            author=random.randint(last_user.id - USER_COUNT + 1, last_user.id),
            category=random.randint(
                last_blog_category.id - CATEGORY_COUNT + 1, last_blog_category.id),
            published=published
        )
        db.session.add(last_blog)

    # insert blogs
    db.session.commit()

    published_blogs = []
    published_authors = []
    for blog in Blog.query.all():
        # Save published blogs for later use
        if blog.published is not None:
            published_blogs.append(blog.id)
            if blog.author not in published_authors:
                published_authors.append(blog.author)

    follow_author_set = set()
    while len(follow_author_set) < len(published_authors) * 2:

        candidate = (
            published_authors[random.randint(0, len(published_authors)-1)],
            random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        )

        if candidate in follow_author_set or candidate[0] == candidate[1]:
            continue  # pairs must be unique and an author may not follow their own account

        follow_author_set.add(candidate)

    new_follows = [{"author_id": pair[0], "follower_id": pair[1]}
                   for pair in list(follow_author_set)]
    insert_follows_query = follow_author.insert().values(new_follows)
    db.session.execute(insert_follows_query)

    # insert follow_author
    db.session.commit()

    follow_blog_set = set()
    while len(follow_blog_set) < len(published_blogs) * 2:

        candidate = (
            published_blogs[random.randint(0, len(published_blogs)-1)],
            random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        )

        if candidate in follow_blog_set:
            continue  # pairs must be unique

        follow_blog_set.add(candidate)

    new_follows = [{"blog_id": pair[0], "follower_id": pair[1]}
                   for pair in list(follow_blog_set)]
    insert_follows_query = follow_blog.insert().values(new_follows)
    db.session.execute(insert_follows_query)

    # insert follow_blog
    db.session.commit()

    def blog_entries(published: bool):
        """ We want some with no entries and some with more than 5, but the majority should have less than equal to 5
            Only published blogs may have entries
        """
        entries = random.randint(0, 10)
        if entries < 2 or not published:
            return 0
        elif entries <= 8:
            return random.randint(1, 5)
        else:
            return random.randint(1, 10)

    for b in range(BLOG_COUNT):
        blog = last_blog.id - BLOG_COUNT + b + 1
        # Each Blog will have between 0 and 10 entries
        entries = blog_entries(blog in published_blogs)
        for i in range(entries):
            # All entries will be published except possibly the last
            published = None
            if i + 1 != entries or random.randint(0, 3) != 0:
                published = fake.date_this_year()

            last_entry = BlogEntry(
                entry=fake.paragraph(
                    nb_sentences=5, variable_nb_sentences=True),
                blog=published_blogs[random.randint(
                    0, len(published_blogs)-1)],
                published=published
            )
            db.session.add(last_entry)

    # insert blog entries
    db.session.commit()

    published_entries = []
    entry_dates = {}
    for e in BlogEntry.query.all():
        if e.published is not None:
            published_entries.append(e.id)
            entry_dates[e.id] = e.published

    RATING_COUNT = 5
    db.session.add(Rating(stars=1, emoji="hate.jpg", description="Hate"))
    db.session.add(
        Rating(stars=2, emoji="thumbdown.jpg", description="Dislike"))
    db.session.add(Rating(stars=3, emoji="meh.jpg", description="Neutral"))
    db.session.add(Rating(stars=4, emoji="thumbup.jpg", description="Like"))
    # Creating the last entry differently so we can obtain the id
    last_rating = Rating(stars=5, emoji="heart.jpg", description="Love")
    db.session.add(last_rating)
    # Insert blog categories
    db.session.commit()

    """
        Loop in a loop ... Author can comment on their own BlogEntry or even on their own comments
            First level are comments on BlogEntry
            Second level are comments on the First level comments
            Third level are comments on Second level comments
    """
    num = random.randint(len(published_entries)//5, len(published_entries))
    COMMENT_COUNT = num
    for _ in range(num):
        # entry: str, user: int, blog_entry: int, parent: int
        blog_entry = published_entries[random.randint(
            0, len(published_entries)-1)]
        comment_date = fake.date_between(
            start_date=entry_dates[blog_entry], end_date=entry_dates[blog_entry] + datetime.timedelta(hours=10))
        entry_dates[blog_entry] = comment_date
        db.session.add(
            Comment(
                entry=fake.paragraph(
                    nb_sentences=5, variable_nb_sentences=True),
                user=random.randint(
                    last_user.id - USER_COUNT + 1, last_user.id),
                blog_entry=blog_entry,
                comment_date=comment_date,
                parent=None
            )
        )
    # insert blog comments
    db.session.commit()

    for _ in range(3):
        comments = []
        comment_dates = {}
        for c in Comment.query.all():
            comments.append(c.id)
            comment_dates[c.id] = c.comment_date
        num = random.randint(len(comments)//5, len(comments))
        COMMENT_COUNT = COMMENT_COUNT + num
        for _ in range(num):
            parent = comments[random.randint(0, len(comments)-1)]
            comment_date = fake.date_between(
                start_date=comment_dates[parent], end_date=comment_dates[parent] + datetime.timedelta(hours=10))
            comment_dates[parent] = comment_date
            last_comment = Comment(
                entry=fake.paragraph(
                    nb_sentences=5, variable_nb_sentences=True),
                user=random.randint(
                    last_user.id - USER_COUNT + 1, last_user.id),
                comment_date=comment_date,
                blog_entry=None,
                parent=parent
            )
            db.session.add(last_comment)
        # insert nested comments
        db.session.commit()

    ratings = set()
    for _ in range(BLOG_COUNT//4):
        blog = published_blogs[random.randint(0, len(published_blogs)-1)]
        user = random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        candidate = (blog, user)
        if candidate in ratings:
            continue  # pairs must be unique
        ratings.add(candidate)

        db.session.add(
            BlogRating(
                blog=blog,
                user=user,
                rating=random.randint(
                    last_rating.id - RATING_COUNT + 1, last_rating.id)
            )
        )
    db.session.commit()

    ratings = set()
    for _ in range(len(published_entries)//4):
        blog_entry = published_entries[random.randint(
            0, len(published_entries)-1)]
        user = random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        candidate = (blog_entry, user)
        if candidate in ratings:
            continue  # pairs must be unique
        ratings.add(candidate)

        db.session.add(
            BlogEntryRating(
                blog_entry=blog_entry,
                user=user,
                rating=random.randint(
                    last_rating.id - RATING_COUNT + 1, last_rating.id)
            )
        )
    db.session.commit()

    ratings = set()
    for _ in range(COMMENT_COUNT//4):
        comment = random.randint(
            last_comment.id - COMMENT_COUNT + 1, last_comment.id)
        user = random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        candidate = (comment, user)
        if candidate in ratings:
            continue  # pairs must be unique
        ratings.add(candidate)

        db.session.add(
            CommentRating(
                comment=comment,
                user=user,
                rating=random.randint(
                    last_rating.id - RATING_COUNT + 1, last_rating.id)
            )
        )
    db.session.commit()


# run script
main()
