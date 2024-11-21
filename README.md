# Chat Room

A real-time chat application built with Django that allows users to create and join chat rooms, share invite links, and communicate with other users in real-time.
This is my first Django project that I built while learning web development. I had a blast making it and learned a ton along the way! Hope you find it useful or inspiring for your own learning journey.

## Overview

Chat Room is a web-based messaging platform that enables users to:
- Create private chat rooms
- Share invite links with friends
- Send and receive messages in real-time
- Manage room memberships and permissions
- Toggle between light/dark themes

The application uses Django for the backend, Bootstrap for the frontend styling, and implements real-time updates using AJAX polling.

## Features

- **User Authentication**: Secure signup and login system with email verification
- **Room Management**: Create, join and leave chat rooms
- **Real-time Messaging**: Instant message updates without page refresh
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Admin Controls**: Room creators have special privileges for managing members
- **Message History**: Preserves chat history for future reference

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chatroom.git
cd chatroom
```

<!-- 2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
``` -->

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application at `http://localhost:8000`

## Project Structure

- `home/`: Main application directory
  - `templates/`: HTML templates
  - `static/`: CSS, JavaScript, and other static files
  - `models.py`: Database models
  - `views.py`: View controllers
  - `forms.py`: Form definitions

## Technical Details

### Models
- **User**: Extended Django user model with additional fields
- **Room**: Chat room with name and invite link
- **Member**: Represents user membership in rooms
- **Message**: Stores chat messages with sender and timestamp

### Security Features
- CSRF protection
- Secure password handling
- Email verification for new accounts
- Protected room access via invite links

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)