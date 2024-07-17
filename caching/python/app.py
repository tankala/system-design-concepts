from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from dotenv import load_dotenv
from redis import Redis
from functools import wraps
import json

load_dotenv()

app = Flask(__name__)

# Connect to the database using the connection string from the environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

# Connect to Redis using the connection details from the environment variables
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD')
redis_db = os.getenv('REDIS_DB')
redis = Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)

DEFAULT_ORGANISATION_ID = 1

def cache_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if the data is present in cache
        cache_key = f"cache:{func.__name__}:{args}:{kwargs}"
        cached_data = redis.get(cache_key)

        if cached_data:
            # Data is present in cache, return it
            return json.loads(cached_data)

        # Data is not present in cache, execute the function
        result = func(*args, **kwargs)

        # Set the result in cache
        redis.set(cache_key, json.dumps(result))

        return result

    return wrapper

def get_users():
    users = db.session.execute(text("SELECT * FROM users")).fetchall()
    return users

def get_organisations():
    organisations = db.session.execute(text("SELECT * FROM organisations")).fetchall()
    return organisations

@app.route("/")
def home():
    users = get_users()
    theme = get_theme()
    return render_template("index.html", users=users, theme=theme)

@app.route("/theme")
def theme():
    organisations = get_organisations()
    return render_template("theme.html", organisation_list=organisations)


@app.route("/get-theme/<organisation_id>")
@cache_decorator
def get_theme(organisation_id=DEFAULT_ORGANISATION_ID):
    theme_db = db.session.execute(text(f"SELECT * FROM themes WHERE organisation_id = {organisation_id}")).fetchone()

    theme = {}
    if theme_db:
        theme['organisation_id'] = theme_db[1]
        theme['title'] = theme_db[2]
        theme['header'] = theme_db[3]
        theme['content'] = theme_db[4]
        theme['styles'] = json.loads(theme_db[5])
    else:
        return get_theme()
    
    return theme

@app.route("/set-theme", methods=['POST'])
def set_theme():
    organisation_id = request.form['id']
    title = request.form['title']
    header = request.form['header']
    content = request.form['content']
    h1_color = request.form['h1_color']
    h2_color = request.form['h2_color']
    p_color = request.form['p_color']

    styles = json.dumps({
        "h1_color": h1_color,
        "h2_color": h2_color,
        "p_color": p_color
    })

    theme = db.session.execute(text(f"SELECT * FROM themes WHERE organisation_id = {organisation_id}")).fetchone()
    # Evict the cache for the get_theme function
    # redis.delete('"cache:get_theme:():{' + "'organisation_id':'" + str(organisation_id) + "'}" + '"')
    redis.delete(f"cache:get_theme:():{{'organisation_id': '{organisation_id}'}}")

    if theme:
        # Theme already exists, update it
        db.session.execute(text(f"UPDATE themes SET title = '{title}', header = '{header}', content = '{content}', styles = '{styles}' WHERE organisation_id = {organisation_id}"))
    else:
        # Theme doesn't exist, insert it
        db.session.execute(text(f"INSERT INTO themes (organisation_id, title, header, content, styles) VALUES ({organisation_id}, '{title}', '{header}', '{content}', '{styles}')"))

    db.session.commit()

    return "Theme set successfully"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)