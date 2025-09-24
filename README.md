# HackMate 🚀

**Find Your Perfect Team for Hackathons and Tech Events**

HackMate is a comprehensive web application that connects students, professionals, and organizations to form teams for hackathons, workshops, and tech events. Built with Django and modern web technologies, it provides an intuitive platform for team formation, event management, and collaboration.

## ✨ Features

### 🔐 Authentication & Profiles
- **User Registration & Login**: Email/password authentication with social login support (Google, GitHub)
- **Rich User Profiles**: Skills, experience levels, interests, availability status
- **Portfolio Integration**: LinkedIn, GitHub, and portfolio URL support
- **Profile Customization**: Bio, university/organization, avatar uploads

### 🔍 Smart Team Matching
- **Skill-Based Search**: Find teammates by skills, experience, and interests
- **Advanced Filtering**: Filter by university, organization, availability, and status
- **AI-Powered Matching**: Intelligent algorithm for team compatibility
- **Status Management**: "Looking for Team", "Looking for Members", or "Not Looking"

### 👥 Team Management
- **Team Creation**: Create teams with custom descriptions and required skills
- **Member Roles**: Team Leader, Member, and Mentor roles
- **Invitation System**: Send and manage team invitations
- **Join Requests**: Request to join teams with custom messages
- **Team Settings**: Public/private teams, member limits, skill requirements

### 📅 Event Management
- **Hackathon Posting**: Universities/organizations can post events
- **Event Details**: Comprehensive event information, rules, prizes, themes
- **Registration System**: Easy event registration with capacity management
- **Admin Approval**: Moderation system for event publishing
- **Event Categories**: Organized by type and tags

### 💬 Communication System
- **Real-time Messaging**: Built-in chat system for team collaboration
- **Notifications**: Instant updates for invites, approvals, and events
- **Conversation Management**: Organized chat threads and message history
- **Read Status**: Track message delivery and read receipts

## 🛠️ Tech Stack

### Backend
- **Django 4.2.7**: Robust web framework with built-in admin
- **Django REST Framework**: Powerful API development
- **Django Allauth**: Comprehensive authentication system
- **SQLite/PostgreSQL**: Flexible database support

### Frontend
- **Bootstrap 5.3**: Modern, responsive CSS framework
- **Font Awesome 6.4**: Beautiful icon library
- **Vanilla JavaScript**: Lightweight, performant client-side code
- **CSS3**: Modern styling with CSS variables and animations

### Authentication
- **Email/Password**: Traditional authentication
- **Google OAuth**: Social login integration
- **GitHub OAuth**: Developer-friendly authentication
- **Session Management**: Secure session handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hackmate.git](https://github.com/Ayesha-Rimione/Hackathon-Team-Matching-Portal..git
   cd hackmate
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   Navigate to `http://localhost:8000`

## 📁 Project Structure

```
hackmate/
├── hackmate/                 # Main Django project
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── users/                   # User management app
│   ├── models.py            # User and profile models
│   ├── views.py             # User API views
│   ├── serializers.py       # User data serializers
│   └── admin.py             # Admin interface
├── teams/                   # Team management app
│   ├── models.py            # Team and membership models
│   ├── views.py             # Team API views
│   ├── serializers.py       # Team data serializers
│   └── admin.py             # Admin interface
├── events/                  # Event management app
│   ├── models.py            # Event and participant models
│   ├── views.py             # Event API views
│   ├── serializers.py       # Event data serializers
│   └── admin.py             # Admin interface
├── messaging/               # Communication app
│   ├── models.py            # Message and notification models
│   ├── views.py             # Messaging API views
│   ├── serializers.py       # Message data serializers
│   └── admin.py             # Admin interface
├── core/                    # Main frontend app
│   ├── views.py             # Page views
│   └── urls.py              # Frontend routing
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── core/                # Page-specific templates
├── static/                  # Static files
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Database Configuration
The default configuration uses SQLite for development. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hackmate_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Social Authentication
Configure OAuth providers in Django admin:

1. Go to `/admin/socialaccount/socialapp/`
2. Add Google and GitHub applications
3. Configure client IDs and secrets

## 📱 API Endpoints

### Authentication
- `POST /accounts/login/` - User login
- `POST /accounts/signup/` - User registration
- `POST /accounts/logout/` - User logout

### Users
- `GET /api/users/me/` - Current user profile
- `GET /api/users/search/` - Search users by skills
- `PUT /api/profiles/{id}/` - Update user profile

### Teams
- `GET /api/teams/` - List teams
- `POST /api/teams/` - Create team
- `POST /api/teams/{id}/join/` - Join team
- `POST /api/invitations/` - Send team invitation

### Events
- `GET /api/events/` - List events
- `POST /api/events/` - Create event
- `POST /api/events/{id}/register/` - Register for event
- `GET /api/events/upcoming/` - Upcoming events

### Messaging
- `GET /api/conversations/` - User conversations
- `POST /api/messages/` - Send message
- `GET /api/notifications/` - User notifications

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styles
- Update CSS variables in `:root` for theme colors
- Add custom animations and transitions

### JavaScript
- Extend `static/js/main.js` for additional functionality
- Use the `HackMate` global object for API access
- Add custom event handlers and UI components

### Templates
- Customize HTML templates in `templates/` directory
- Extend `base.html` for consistent layout
- Add new page templates as needed

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in environment variables
2. Configure production database (PostgreSQL recommended)
3. Set up static file serving with WhiteNoise or CDN
4. Configure email backend for production
5. Set secure `SECRET_KEY`

### Deployment Options
- **Heroku**: Easy deployment with PostgreSQL addon
- **DigitalOcean**: App Platform or Droplet deployment
- **AWS**: Elastic Beanstalk or EC2 with RDS
- **Docker**: Containerized deployment

### Environment Setup
```bash
# Install production dependencies
pip install gunicorn whitenoise psycopg2-binary

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn hackmate.wsgi:application
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure responsive design for mobile devices



## 🙏 Acknowledgments

- Django community for the excellent web framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the beautiful icon library



**Built with ❤️ for the University students who don't find their perfect match for Hackathon team!**

*HackMate - Where great teams are born*
