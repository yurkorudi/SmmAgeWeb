import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError

from extentions import db
from models import ContactRequest, ProjectExample

app = Flask(__name__)
DATABASE_URL = "mysql+pymysql://superuser:yolkipalki220@146.190.65.79/data?charset=utf8mb4"
DB_CONFIGURED = bool(DATABASE_URL)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me-before-production")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://superuser:yolkipalki220@146.190.65.79/data?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "smmageofficialpage@gmail.com"
APP_PASSWORD = "dlrz aipj hrxa tsmq"

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "AdMin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "QweAsd")

SERVICE_TEMPLATES = {
    "smm": "services/smm.html",
    "web": "services/web.html",
    "content": "services/content.html",
    "ads": "services/ads.html",
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
            "result": "найшвидший результат",
            "link": "https://www.flowersbars.com/",
        },
        {
            "title": "Interior portfolio website",
            "category": "Portfolio",
            "description": "Зібрали сайт-портфоліо для дизайн-студії з галереєю, кейсами й контактною формою.",
            "image_url": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=80",
            "result": "готовий запуск за 12 днів",
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
            "description": "Оновили подачу страв у соцмережах: фото-напрям, підписи й рекламні креативи.",
            "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
            "result": "+31% збережень",
            "link": "#",
        },
    ],
    "ads": [
        {
            "title": "Online course launch",
            "category": "Meta Ads",
            "description": "Запустили тести аудиторій і креативів для освітнього продукту перед основним продажем.",
            "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
            "result": "CPA знижено на 27%",
            "link": "#",
        },
        {
            "title": "Local service lead campaign",
            "category": "Lead generation",
            "description": "Побудували кампанію для локального сервісу з простим офером і швидкою формою заявки.",
            "image_url": "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?auto=format&fit=crop&w=1200&q=80",
            "result": "63 ліди за 3 тижні",
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
    return render_template("Homepage.html")


@app.route("/services/smm")
def service_smm():
    return render_template("services/smm.html", examples=load_examples("smm"))


@app.route("/services/web")
def service_web():
    return render_template("services/web.html", examples=load_examples("web"))


@app.route("/services/content")
def service_content():
    return render_template("services/content.html", examples=load_examples("content"))


@app.route("/services/ads")
def service_ads():
    return render_template("services/ads.html", examples=load_examples("ads"))


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
    name = request.form.get("name", "—")
    phone = request.form.get("phone", "—")
    business = request.form.get("business", "—")
    category = request.form.get("category", "")
    budget = request.form.get("budget", "")
    timeline = request.form.get("timeline", "")
    channels = ", ".join(request.form.getlist("channels"))
    message = request.form.get("message", "—")

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

    text = f"""Нова заявка з сайту

Ім'я:      {name}
Телефон:   {phone}
Бізнес:    {business}
Категорія: {category or "—"}
Бюджет:    {budget or "—"}
Старт:     {timeline or "—"}
Канали:    {channels or "—"}

Повідомлення:
{message}
"""

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = SENDER_EMAIL
    msg["Subject"] = "Нова заявка з сайту"
    msg.attach(MIMEText(text, "plain", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("Лист успішно відправлено!")
        return redirect(url_for("home", _anchor="contact-us"))

    except Exception as e:
        print("Помилка при відправці пошти:", str(e))
        return f"""
        <h2>Щось пішло не так</h2>
        <p>Не вдалося надіслати заявку. Спробуйте пізніше або напишіть нам напряму.</p>
        <p style="color: #e74c3c; font-family: monospace;">Помилка: {str(e)}</p>
        <a href="/">На головну</a>
        """, 500


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
    db_error = None
    if DB_CONFIGURED:
        try:
            requests = ContactRequest.query.order_by(ContactRequest.created_at.desc()).all()
            examples = ProjectExample.query.order_by(ProjectExample.created_at.desc()).all()
        except SQLAlchemyError as exc:
            db.session.rollback()
            db_error = str(exc)
    else:
        db_error = "DATABASE_URL не налаштовано. Вкажіть MySQL URI, щоб адмінка зберігала заявки та приклади."

    return render_template(
        "admin/dashboard.html",
        requests=requests,
        examples=examples,
        db_error=db_error,
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
