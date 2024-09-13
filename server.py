from flask import Flask, request, render_template, redirect, url_for, session
import os
from datetime import timedelta
from PIL import Image

app = Flask(__name__, static_folder="public")

# Secretul aplicatiei, utilizat pentru securitate, este preluat din variabilele de mediu
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

# Utilizatori si parole permise
ALLOWED_USERS = {
    "admin": "admin",
    "user": "user",
    "test": "test",
}

# Caile pentru incarcarea imaginilor si miniaturilor
UPLOAD_FOLDER = './public/uploads'
THUMBNAIL_FOLDER = 'thumbnails'
CATEGORIES = ['honda', 'toyota', 'mercedes', 'dacia']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Seteaza durata de viata a sesiunii la 1 ora
app.permanent_session_lifetime = timedelta(hours=1)

# Creeaza directoarele necesare pentru fiecare categorie si miniaturi
for category in CATEGORIES:
    os.makedirs(os.path.join(UPLOAD_FOLDER, category), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, category, THUMBNAIL_FOLDER), exist_ok=True)

# Functie pentru crearea unei miniaturi de 200x200 pixeli
def create_thumbnail(image_path, thumbnail_path):
    with Image.open(image_path) as img:
        img.thumbnail((200, 200))
        img.save(thumbnail_path)

# Verifica daca fisierul are o extensie permisa
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    # Redirectioneaza utilizatorii autentificati la pagina de autentificare
    if session.get("user_authenticated"):
        return redirect(url_for("auth"))
    
    gallery = {}
    # Creeaza galeria de imagini pentru fiecare categorie
    for category in CATEGORIES:
        thumbnail_path = os.path.join(UPLOAD_FOLDER, category, THUMBNAIL_FOLDER)
        if os.path.exists(thumbnail_path):
            images = os.listdir(thumbnail_path)
            gallery[category] = images
    return render_template("index.html", gallery=gallery)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Redirectioneaza utilizatorii autentificati
    if session.get("user_authenticated"):
        return redirect(url_for("auth"))
    
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        # Verifica daca numele de utilizator si parola sunt corecte
        if username in ALLOWED_USERS and password == ALLOWED_USERS[username]:
            session.permanent = True  # Seteaza sesiunea ca permanenta
            session["user_authenticated"] = True
            session["username"] = username
            return redirect(url_for("auth"))
        else:
            error_msg = "Nume de utilizator sau parola incorecta"
    
    return render_template("login.html", error_msg=error_msg)

@app.route("/auth")
def auth():
    # Verifica daca utilizatorul este autentificat
    if not session.get("user_authenticated"):
        return redirect(url_for("login"))
    
    gallery = {}
    # Creeaza galeria de imagini pentru fiecare categorie
    for category in CATEGORIES:
        thumbnail_path = os.path.join(UPLOAD_FOLDER, category, THUMBNAIL_FOLDER)
        if os.path.exists(thumbnail_path):
            images = os.listdir(thumbnail_path)
            gallery[category] = images
    return render_template("index2.html", gallery=gallery)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    # Verifica daca utilizatorul este autentificat
    if not session.get("user_authenticated"):
        return redirect(url_for("login"))
    if request.method == "POST":
        file = request.files.get("file")
        new_name = request.form.get("new_name")
        category = request.form.get("category", "uncategorized").lower()

        # Verifica daca fisierul este valid si are o extensie permisa
        if file and allowed_file(file.filename):
            filename = new_name if new_name else file.filename
            category_path = os.path.join(UPLOAD_FOLDER, category)
            file_path = os.path.join(category_path, filename)
            thumbnail_path = os.path.join(category_path, THUMBNAIL_FOLDER, filename)
            
            file.save(file_path)
            create_thumbnail(file_path, thumbnail_path)
            
            return f"Fisierul {filename} a fost incarcat cu succes in categoria {category}!"
    
    return render_template("upload.html", categories=CATEGORIES)

@app.route("/logout")
def logout():
    # Sterge sesiunea utilizatorului
    session.pop("user_authenticated", None)
    session.pop("username", None)
    return redirect(url_for("index"))

# Dezactiveaza cache-ul pentru paginile sensibile (cum ar fi login)
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Ruta pentru pagina "about" pentru utilizatorii neautentificati
@app.route("/about")
def about():
    if session.get("user_authenticated"):
        return redirect(url_for("about_authenticated"))
    return render_template("about.html")

# Ruta pentru pagina "about" pentru utilizatorii autentificati
@app.route("/about_authenticated")
def about_authenticated():
    if not session.get("user_authenticated"):
        return redirect(url_for("about"))
    return render_template("about_authenticated.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
