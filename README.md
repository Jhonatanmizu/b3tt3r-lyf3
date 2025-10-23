# Django Template - Mizu

A production-ready Django template with Docker support, modern Python tooling, and best practices.

## Features

- 🐍 Python 3.11+ with UV package manager
- 🐳 Docker & Docker Compose setup
- 🔧 Environment-based configuration
- 📦 Modern dependency management with UV
- 🎨 Static files handling
- 🔒 Security best practices
- 📝 Pre-configured logging
- 🧪 Testing setup ready
- 🚀 Production-ready deployment

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- UV package manager

### Local Development

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd template_mizu_django
   ```

2. **Set up environment**

   ```bash
   cp dotenv_files/.env.example .env
   # Edit .env with your configuration
   ```

3. **Install dependencies**

   ```bash
   uv sync
   ```

4. **Run migrations**

   ```bash
   uv run python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   uv run python manage.py runserver
   ```

### Docker Development

1. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

2. **Run migrations in container**

   ```bash
   docker compose exec web python manage.py migrate
   ```

3. **Create superuser in container**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

## Project Structure

```
template_mizu_django/
├── core/                   # Django project settings
│   ├── __init__.py
│   ├── settings.py        # Main settings
│   ├── urls.py           # URL configuration
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
├── static/               # Static files
│   └── css/
├── dotenv_files/         # Environment files
│   └── .env.example
├── docker-compose.yml    # Docker Compose configuration
├── dockerfile           # Docker configuration
├── manage.py            # Django management script
├── pyproject.toml       # Python project configuration
└── README.md           # This file
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: postgresql://user:password@localhost:5432/dbname

# Security
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper `SECRET_KEY`
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure static files serving
- [ ] Set up proper logging
- [ ] Configure HTTPS
- [ ] Set security headers

### Docker Production

```bash
# Build production image
docker build -t template-mizu-django .

# Run with production settings
docker run -p 8000:8000 --env-file .env.prod template-mizu-django
```

## Development

### Running Tests

```bash
uv run python manage.py test
```

### Code Quality

```bash
# Format code
uv run black .

# Lint code
uv run flake8 .

# Type checking
uv run mypy .
```

### Database Operations

```bash
# Create migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.
