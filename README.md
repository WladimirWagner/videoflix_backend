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

2. **Start with Docker**
```bash
docker-compose up -d
```

The backend server starts at http://localhost:8000

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

3. **Setup Database**
```bash
python manage.py migrate
```

4. **Create Superuser**
```bash
python manage.py createsuperuser
```

5. **Start Server**
```bash
python manage.py runserver
```

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
Supports multiple email backends:
- SMTP (Gmail, etc.)
- Console backend for development
- Custom SMTP servers

## Docker Configuration

### Services
- **Web**: Django application
- **DB**: PostgreSQL database
- **Redis**: Cache and queue backend
- **Worker**: RQ worker for background tasks

### Environment Variables
```env
SECRET_KEY=your-secret-key
DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=your-password
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
FRONTEND_URL=http://localhost:4200
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
- [ ] Configure email backend
- [ ] Set secure cookies (`secure=True`)
- [ ] Configure HTTPS
- [ ] Set up media file serving
- [ ] Configure background workers

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
