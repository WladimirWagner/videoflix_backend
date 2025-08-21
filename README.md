# VideoFlix Backend - Django REST API

A Django REST API backend for a video streaming platform with user authentication, JWT cookie-based security, video management, HLS streaming, and email verification.

## Project Structure

```
videoflix_backend/
├── auth_app/           # Authentication app with JWT cookies
│   ├── api/           # Authentication API endpoints
│   ├── authentication.py  # Custom JWT cookie authentication
│   └── models.py      # User-related models
├── videoflix_app/     # Main video streaming app
│   ├── api/           # Video API endpoints
│   ├── models.py      # Video and Profile models
│   ├── signals.py     # Video processing signals
│   └── tasks.py       # Background video processing
├── core/              # Django project settings and URLs
├── templates/         # Email templates
│   └── emails/        # Activation and password reset emails
├── media/             # Video files and HLS segments
├── static/            # Static files
├── requirements.txt   # Python dependencies
├── manage.py          # Django management script
├── docker-compose.yml # Docker configuration
└── README.md          # This file
```

## Features

- **JWT Cookie Authentication** with HTTP-Only cookies for security
- **User Registration** with email activation
- **Password Reset** functionality with email confirmation
- **Video Management** with automatic HLS conversion
- **Video Streaming** with adaptive bitrate (480p, 720p, 1080p)
- **Background Processing** for video conversion using Redis/RQ
- **Email System** with HTML templates
- **Docker Support** for easy deployment
- **CORS Support** for frontend integration

## Quick Start

### Docker Setup (Recommended)

1. **Clone Repository**
```bash
git clone <repository-url>
cd videoflix_backend
```

2. **Email Configuration (REQUIRED)**
```bash
# Create a .env file with your SMTP data
cp .env.example .env
# Edit .env and enter your email data
```

3. **Start with Docker**
```bash
docker-compose up -d
```

The backend server starts at http://localhost:8000

**⚠️ Important**: Without proper email configuration, user registration and password reset will not work!

### Manual Setup

1. **Create Virtual Environment**
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Email Configuration (REQUIRED)**
```bash
# Create a .env file with your SMTP data
cp .env.example .env
# Edit .env and enter your email data
```

4. **Setup Database**
```bash
python manage.py migrate
```

5. **Create Superuser**
```bash
python manage.py createsuperuser
```

6. **Start Server**
```bash
python manage.py runserver
```

**⚠️ Important**: Without proper email configuration, user registration and password reset will not work!

## Data Model

### User & Profile
- Extends Django User model
- Email-based authentication
- Profile with additional user information
- Email activation required

### Video
- Video file management with metadata
- Automatic HLS conversion in multiple resolutions
- Support for 480p, 720p, and 1080p streaming
- Background processing for video conversion

## API Endpoints

### Authentication
- `POST /api/register/` - Register new user
- `GET /api/activate/<uidb64>/<token>/` - Activate user account
- `POST /api/login/` - User login (sets HTTP-Only cookies)
- `POST /api/logout/` - User logout (clears cookies)
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/password_reset/` - Request password reset
- `POST /api/password_confirm/<uidb64>/<token>/` - Confirm password reset

### Video Management
- `GET /api/video/` - List all videos (authenticated)
- `GET /api/video/<id>/<resolution>/index.m3u8` - HLS manifest file
- `GET /api/video/<id>/<resolution>/<segment>` - HLS video segments

## Security Features

### JWT Cookie Authentication
- **HTTP-Only Cookies**: Prevents XSS attacks
- **Secure Cookies**: Only sent over HTTPS in production
- **SameSite Protection**: CSRF protection
- **Token Rotation**: Automatic refresh token rotation
- **Token Blacklisting**: Secure logout functionality

### Video Security
- **Authentication Required**: All video endpoints require valid JWT
- **Direct File Protection**: Videos served through Django views
- **HLS Streaming**: Segments protected by authentication

## Background Processing

### Video Conversion
Videos are automatically converted to HLS format with multiple resolutions:
- **480p**: Standard definition
- **720p**: High definition
- **1080p**: Full HD

Processing is handled by Redis Queue (RQ) workers for scalability.

## Email System

### Templates
- **Activation Email**: HTML and text versions
- **Password Reset**: HTML and text versions
- **Responsive Design**: Mobile-friendly email templates

### Configuration
The project uses SMTP for email sending. **Each developer must configure their own SMTP data.**

#### Dynamic Frontend URL Detection
The system automatically detects the current domain and port from the request and generates appropriate frontend URLs for email links:
- **Development**: Backend on port 8000 → Frontend on port 5500
- **Production**: Backend on port 443 → Frontend on port 443 (HTTPS)
- **Fallback**: Uses `FRONTEND_URL` from settings if request context is not available

#### Email Configuration in .env File

Create a `.env` file in the project root with your SMTP data:

```env
# Email Configuration (REQUIRED - enter your own SMTP data)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@your-domain.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=VideoFlix <your-email@your-domain.com>
SERVER_EMAIL=VideoFlix <your-email@your-domain.com>
EMAIL_SUBJECT_PREFIX=[VideoFlix] 
```

#### Known SMTP Configurations

**Gmail:**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**All-Inkl/KAS-Server:**
```env
EMAIL_HOST=your-login.kasserver.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@your-domain.com
EMAIL_HOST_PASSWORD=your-password
```

**Outlook/Hotmail:**
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-password
```

#### Important Notes

- **App Passwords**: For Gmail, you need to create an app password
- **Enable 2FA**: 2-factor authentication is required for Gmail
- **Firewall**: Make sure SMTP ports (587/465) are not blocked
- **Docker**: Docker containers must be restarted after .env changes

## Docker Configuration

### Services
- **Web**: Django application
- **DB**: PostgreSQL database
- **Redis**: Cache and queue backend
- **Worker**: RQ worker for background tasks

### Environment Variables

Copy `env.template` to `.env` and configure:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_LOCATION=redis://redis:6379/1

# Frontend
FRONTEND_URL=http://localhost:5500

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:4200

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
CORS_ALLOW_ALL_ORIGINS=True

# Email (REQUIRED - enter your own SMTP data)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@your-domain.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=VideoFlix <your-email@your-domain.com>
SERVER_EMAIL=VideoFlix <your-email@your-domain.com>
EMAIL_SUBJECT_PREFIX=[VideoFlix]
```

## Development

### Local Development
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver

# Start RQ worker (separate terminal)
python manage.py rqworker
```

### Video Processing
Videos are processed automatically when uploaded through the admin interface. Processing includes:
1. Format validation
2. HLS conversion
3. Multiple resolution generation
4. Thumbnail creation

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure secure database (PostgreSQL)
- [ ] Set up Redis for production
- [ ] **Configure SMTP email backend** (REQUIRED)
- [ ] Set secure cookies (`secure=True`)
- [ ] Configure HTTPS
- [ ] Set up media file serving
- [ ] Configure background workers
- [ ] Test email functionality (registration & password reset)

### Docker Production
```bash
# Production build
docker-compose -f docker-compose.prod.yml up -d
```

## Technologies

- **Django 5.2** - Web framework
- **Django REST Framework** - API framework
- **SimpleJWT** - JWT authentication
- **PostgreSQL** - Production database
- **Redis** - Cache and queue backend
- **RQ (Redis Queue)** - Background job processing
- **FFmpeg** - Video processing
- **Gunicorn** - WSGI server
- **Docker** - Containerization

## Testing

### Test User Accounts
After running migrations, test users are available:
- **Admin**: admin / admin
- **Test User**: test@example.com / testpassword

### API Testing
Use tools like:
- **Postman** - API testing
- **curl** - Command line testing
- **Django Admin** - Video upload and management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is part of the Developer Academy training program.

## Support

For questions or issues:
- Create issues on GitHub
- Check Django logs: `docker-compose logs web`
- Check worker logs: `docker-compose logs worker`
- Monitor Redis: `docker-compose logs redis`

## Performance Notes

- Videos are served through Django views for security but consider CDN for production
- HLS segments are cached for better performance
- Use Redis for session storage in production
- Consider using a reverse proxy (Nginx) for static file serving
