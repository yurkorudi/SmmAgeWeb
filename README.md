# SmmAgeWeb

**SMMAge — Professional Digital Services Portfolio**

**Project Overview**
SMMAge is a clean, responsive portfolio website showcasing the services and past work of a digital services studio (SMM, content creation, web development, and web applications). The project is implemented with a Python Flask backend and modern frontend technologies, and includes tooling for development and Docker-based deployment.

**Key Features**
- **Portfolio Showcase**: Curated case studies and project galleries.
- **Service Pages**: Clear descriptions for SMM, content creation, and web development offerings.
- **Pricing Section**: Example packages and transparent pricing information.
- **Contact Form**: Email-capable contact form with server-side handling and SMTP integration.
- **Responsive Design**: Mobile-first layouts and accessible UI.
- **Admin Panel**: Simple content management for adding or editing portfolio items.

**Tech Stack**
- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development) — PostgreSQL recommended for production
- **Email**: SMTP integration for contact submissions
- **Deployment**: Docker / Docker Compose supported

**Requirements**
- **Python**: 3.8+ recommended
- **Dependencies**: See `requirements.txt`
- **Optional**: Docker and Docker Compose for containerized runs

**Quick Start (Development)**
1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` from the example and update values (SMTP, SECRET_KEY, etc.):

```powershell
copy .env.example .env
# then edit .env with your preferred editor
```

4. Run the app:

```powershell
python app.py
```

The site will be available at `http://127.0.0.1:5000` by default.

**Quick Start (Docker)**
1. Build and run with Docker Compose:

```powershell
docker-compose up --build
```

2. Stop and remove containers:

```powershell
docker-compose down
```

**Project Structure (Overview)**
- `app.py`: Flask application entrypoint
- `requirements.txt`: Python dependency list
- `static/`: CSS, JavaScript, and image assets
- `templates/`: Jinja2 HTML templates
- `instance/`: (optional) runtime files such as the SQLite DB
- `docker-compose.yml` and `Dockerfile`: containerization files

**Contribution**
- **Bug reports / feature requests**: Please open an issue describing the problem or proposal.
- **Code contributions**: Fork the repo, create a feature branch, and submit a pull request.

**License & Contact**
- Add a `LICENSE` file to define project licensing.
- For questions or commercial inquiries, contact the project owner or add contact details here.



