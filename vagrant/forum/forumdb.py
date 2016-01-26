#
# Database access functions for the web forum.
# 
import psycopg2
import time
import bleach

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #connect to Database
    DB=psycopg2.connect("dbname=forum")
    #then establish a cursor
    c= DB.cursor()
    #Then exectute the query
    c.execute("SELECT time, content FROM posts ORDER BY time DESC")
    #Reformat them in way the post expects
    posts=({'content': str(row[1]),'time': str(row[0])}
            for row in c.fetchall())
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB=psycopg2.connect("dbname=forum")
    c = DB.cursor()
    bleach.clean(content)
    #Execute insert query, substituting the post content into the query string
    c.execute("INSERT INTO posts (content) VALUES (%s)",(content,))
    #c.execute("DELETE FROM posts WHERE content = 'spam'")

    DB.commit()
    DB.close()