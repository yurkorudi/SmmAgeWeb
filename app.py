import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError

from extentions import db
from models import ContactRequest, ProjectExample, MainProjectExample
from telegram_notifier import notify_new_request
import os
from werkzeug.utils import secure_filename

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
DB_CONFIGURED = bool(DATABASE_URL)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me-before-production")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL or "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "AdMin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "QweAsd")

SERVICE_TEMPLATES = {
    "smm": "services/smm.html",
    "web": "services/web.html",
    "content": "services/content.html",
    "branding": "services/branding.html",
}

DEFAULT_EXAMPLES = {
    "smm": [
        {
            "title": "Coffee Room social launch",
            "category": "Instagram / TikTok",
            "description": "Оформили сторінку кав'ярні, зібрали рубрики, tone of voice і план reels на перший місяць.",
            "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=1200&q=80",
            "result": "+42% охоплення за 30 днів",
            "link": "#",
        },
        {
            "title": "Beauty Studio content rhythm",
            "category": "Content plan",
            "description": "Перепакували послуги салону в зрозумілі серії постів, сторіс і коротких відео.",
            "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=1200&q=80",
            "result": "18 заявок із контенту",
            "link": "#",
        },
    ],
    "web": [
        {
            "title": "Dental clinic landing",
            "category": "Landing page",
            "description": "Створили лендінг для клініки з блоками довіри, послугами, цінами й швидкою формою запису.",
            "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80",
            "result": "готовий запуск за 12 днів",
            "link": "#",
        },
        {
            "title": "Interior portfolio website",
            "category": "Portfolio",
            "description": "Зібрали сайт-портфоліо для дизайн-студії з галереєю, кейсами й контактною формою.",
            "image_url": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=80",
            "result": "зручна подача кейсів",
            "link": "#",
        },
    ],
    "content": [
        {
            "title": "Fitness reels pack",
            "category": "Video content",
            "description": "Підготували сценарії, тексти й структуру коротких відео для фітнес-тренера.",
            "image_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1200&q=80",
            "result": "24 готові ідеї",
            "link": "#",
        },
        {
            "title": "Restaurant visual menu",
            "category": "Photo / copy",
            "description": "Оновили подачу страв у соцмережах: фото-напрям, підписи й візуальні рубрики.",
            "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
            "result": "+31% збережень",
            "link": "#",
        },
    ],
    "branding": [
        {
            "title": "Boutique brand refresh",
            "category": "Visual identity",
            "description": "Оновили тон, кольорову логіку, базові правила візуалу й приклади постів для локального бренду.",
            "image_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=1200&q=80",
            "result": "єдина система для сайту й соцмереж",
            "link": "#",
        },
        {
            "title": "Tech startup offer pack",
            "category": "Positioning",
            "description": "Сформулювали позиціонування, меседжі й структуру першої презентації для B2B-сервісу.",
            "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80",
            "result": "готовий pitch-набір",
            "link": "#",
        },
    ],
}


def is_admin_logged_in():
    return session.get("admin_logged_in") is True


def load_examples(service_slug):
    examples = [dict(example) for example in DEFAULT_EXAMPLES.get(service_slug, [])]
    if not DB_CONFIGURED:
        return examples

    try:
        db_examples = (
            ProjectExample.query.filter_by(service_slug=service_slug, is_featured=True)
            .order_by(ProjectExample.created_at.desc())
            .all()
        )
        examples = [
            {
                "title": item.title,
                "category": item.category,
                "description": item.description,
                "image_url": item.image_url,
                "result": item.result,
                "link": item.link,
            }
            for item in db_examples
        ] + examples
    except SQLAlchemyError as exc:
        db.session.rollback()
        print("Project examples DB error:", exc)
    return examples


@app.route("/")
def home():
    main_projects = []
    try: 
        main_projects = MainProjectExample.query.filter_by(is_active=True).order_by(MainProjectExample.created_at.desc()).all()
    except SQLAlchemyError as exc:
        db.session.rollback()
        print("Main projects DB error:", exc)
    return render_template("Homepage.html", main_projects=main_projects)


@app.route("/services/smm")
def service_smm():
    return render_template("services/smm.html", examples=load_examples("smm"))


@app.route("/services/web")
def service_web():
    return render_template("services/web.html", examples=load_examples("web"))


@app.route("/services/content")
def service_content():
    return render_template("services/content.html", examples=load_examples("content"))


@app.route("/services/branding")
def service_branding():
    return render_template("services/branding.html", examples=load_examples("branding"))


@app.route("/services/<slug>")
def service_detail(slug):
    if slug in SERVICE_TEMPLATES:
        return redirect(url_for(f"service_{slug}"))
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return redirect(url_for("home", _anchor="about-us"))


@app.route("/contacts")
def contacts():
    return redirect(url_for("home", _anchor="contact-us"))


@app.route("/send-request", methods=["POST"])
def send_request():
    name = request.form.get("name", "—").strip() or "—"
    phone = request.form.get("phone", "—").strip() or "—"
    business = request.form.get("business", "—").strip() or "—"
    category = request.form.get("category", "").strip()
    budget = request.form.get("budget", "").strip()
    timeline = request.form.get("timeline", "").strip()
    channels = ", ".join(request.form.getlist("channels"))
    message = request.form.get("message", "—").strip() or "—"

    contact_request = ContactRequest(
        name=name,
        phone=phone,
        business=business,
        category=category,
        budget=budget,
        timeline=timeline,
        channels=channels,
        message=message,
    )

    if DB_CONFIGURED:
        try:
            db.session.add(contact_request)
            db.session.commit()
        except SQLAlchemyError as exc:
            db.session.rollback()
            print("Contact request DB error:", exc)

    notify_new_request(
        {
            "name": name,
            "phone": phone,
            "business": business,
            "category": category,
            "budget": budget,
            "timeline": timeline,
            "message": message,
        }
    )

    return redirect(url_for("home", _anchor="contact-us"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Невірний логін або пароль.")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
def admin_dashboard():
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))

    requests = []
    examples = []
    main_projects = []
    db_error = None
    if DB_CONFIGURED:
        try:
            requests = ContactRequest.query.order_by(ContactRequest.created_at.desc()).all()
            examples = ProjectExample.query.order_by(ProjectExample.created_at.desc()).all()
            main_projects = MainProjectExample.query.order_by(MainProjectExample.created_at.desc()).all()
        except SQLAlchemyError as exc:
            db.session.rollback()
            db_error = str(exc)
    else:
        db_error = "DATABASE_URL не налаштовано. Вкажіть URI в .env, щоб адмінка зберігала заявки та приклади."

    return render_template(
        "admin/dashboard.html",
        requests=requests,
        examples=examples,
        db_error=db_error,
        main_projects=main_projects,
        service_slugs=SERVICE_TEMPLATES.keys(),
    )


@app.route("/admin/projects/add", methods=["POST"])
def admin_add_project():
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))
    if not DB_CONFIGURED:
        flash("DATABASE_URL не налаштовано, тому приклад не збережено.")
        return redirect(url_for("admin_dashboard"))

    example = ProjectExample(
        service_slug=request.form.get("service_slug", "smm"),
        title=request.form.get("title", ""),
        category=request.form.get("category", ""),
        description=request.form.get("description", ""),
        image_url=request.form.get("image_url", ""),
        result=request.form.get("result", ""),
        link=request.form.get("link", ""),
        is_featured=request.form.get("is_featured") == "on",
    )

    try:
        db.session.add(example)
        db.session.commit()
        flash("Приклад додано.")
    except SQLAlchemyError as exc:
        db.session.rollback()
        flash(f"Не вдалося додати приклад: {exc}")

    return redirect(url_for("admin_dashboard"))



@app.route("/admin/main-project/add", methods=["POST"])
def admin_add_main_project():
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))
    if not DB_CONFIGURED:
        flash("DATABASE_URL не налаштовано.")
        return redirect(url_for("admin_dashboard"))


    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            image_path = f"uploads/projects/{unique_filename}"

    new_project = MainProjectExample(
        title=request.form.get("title", ""),
        project_type=request.form.get("project_type", ""),
        description=request.form.get("description", ""),
        duration=request.form.get("duration", ""),
        budget=request.form.get("budget", ""),
        link=request.form.get("link", ""),
        image=image_path,
        is_active=request.form.get("is_active") == "on"
    )

    try:
        db.session.add(new_project)
        db.session.commit()
        flash("Головний проєкт успішно додано!")
    except SQLAlchemyError as exc:
        db.session.rollback()
        flash(f"Помилка: {exc}")

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/main-project/delete/<int:project_id>", methods=["POST"])
def admin_delete_main_project(project_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))
    if not DB_CONFIGURED:
        flash("DATABASE_URL не налаштовано.")
        return redirect(url_for("admin_dashboard"))

    project = MainProjectExample.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash("Проєкт видалено.")
    except SQLAlchemyError as exc:
        db.session.rollback()
        flash(f"Помилка при видаленні: {exc}")

    return redirect(url_for("admin_dashboard"))



# app.py

@app.route("/admin/main-project/edit/<int:project_id>", methods=["GET", "POST"])
def admin_edit_main_project(project_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))
    
    project = MainProjectExample.query.get_or_404(project_id)

    if request.method == "POST":
        project.title = request.form.get("title", "")
        project.project_type = request.form.get("project_type", "")
        project.description = request.form.get("description", "")
        project.duration = request.form.get("duration", "")
        project.budget = request.form.get("budget", "")
        project.link = request.form.get("link", "")
        project.is_active = request.form.get("is_active") == "on"


        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):

                if project.image:
                    old_path = os.path.join('static', project.image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                project.image = f"uploads/projects/{unique_filename}"

        try:
            db.session.commit()
            flash("Проєкт оновлено!")
            return redirect(url_for("admin_dashboard"))
        except SQLAlchemyError as exc:
            db.session.rollback()
            flash(f"Помилка: {exc}")

    return render_template("admin/edit_main_project.html", project=project)





@app.route("/admin/main-project/delete/<int:project_id>", methods=["POST"])
def admin_delete_main_project(project_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))
    
    project = MainProjectExample.query.get_or_404(project_id)
    

    if project.image:
        file_path = os.path.join('static', project.image)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    try:
        db.session.delete(project)
        db.session.commit()
        flash("Проєкт видалено.")
    except SQLAlchemyError as exc:
        db.session.rollback()
        flash(f"Помилка: {exc}")

    return redirect(url_for("admin_dashboard"))






@app.cli.command("init-db")
@with_appcontext
def init_db_command():
    if not DB_CONFIGURED:
        print("Set DATABASE_URL to a MySQL URI before running init-db.")
        return
    db.create_all()
    print("Database tables created.")


if __name__ == "__main__":
    app.run(debug=True)
