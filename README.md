AI Car Mechanic

An AI-assisted web application that helps car owners troubleshoot common vehicle problems through a conversational mechanic interface. The system asks relevant follow-up questions before providing a diagnosis, supports media uploads, and allows users to book a mechanic after receiving a service recommendation.

Internship Task: Full-Stack Developer Intern — AI Car Mechanic Chatbot

Table of Contents

Overview

Features

Architecture

Technology Stack

Project Structure

How the System Works

Diagnosis Logic

Database Design

REST API Documentation

Local Development Setup

Environment Variables

Running the Application

Deployment

Error Handling

Security and Configuration

Design Decisions

Future Improvements

Submission Checklist

Overview

AI Car Mechanic is a full-stack troubleshooting application consisting of:

A React/Vite conversational frontend.

A Django REST backend.

SQLite for application data.

Deterministic diagnostic logic for currently supported mechanical symptoms.

Media upload support for vehicle-related evidence.

A mechanic booking workflow.

The core workflow is:

Collect symptoms → ask relevant follow-up questions → diagnose when enough information is available → recommend an appropriate next step → allow mechanic booking.

The backend exposes REST APIs so the frontend and backend remain cleanly separated.

Features

Conversational Troubleshooting

Users can describe a vehicle problem in natural language.

Example:

User:
My car brakes are making a squealing noise.

AI Mechanic:
When does the noise happen — only when braking or also while driving?
Also, does the brake pedal feel soft, hard, or normal?

Follow-Up Questions

The backend maintains conversation history and uses previous messages when determining whether enough information is available.

Rule-Based Diagnosis

The current diagnostic service handles supported mechanical scenarios using deterministic backend logic.

Current supported examples include:

Brake squealing / squeaking

Brake grinding

Engine overheating

Engine overheating accompanied by steam

This keeps deterministic diagnostic behavior in the backend instead of unnecessarily relying on an external AI service.

Media Upload

Users can upload vehicle-related media associated with a conversation.

Supported media categories:

Image

Audio

Video

Mechanic Booking

Users can submit:

Customer name

Phone

Vehicle

Required service

Preferred date

Preferred time

Bookings are stored in the Django database.

Booking Status

Bookings use these statuses:

pending
confirmed
completed
cancelled

New bookings default to pending.

Architecture

                    ┌──────────────────────┐
                    │        User          │
                    │   Browser / Mobile   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    React Frontend    │
                    │        Vite          │
                    └──────────┬───────────┘
                               │
                         REST API / HTTP
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Django Backend    │
                    │   Django REST API    │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
       │ Chat Logic  │  │ Diagnosis   │  │ Booking      │
       │             │  │ Service     │  │ Workflow     │
       └─────────────┘  └─────────────┘  └──────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │       SQLite         │
                    │ Conversations       │
                    │ Messages             │
                    │ Media                │
                    │ Diagnosis            │
                    │ Bookings             │
                    └──────────────────────┘

Intended Production Architecture

                    Internet
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      ┌──────────────┐    ┌─────────────────┐
      │   Vercel     │    │    AWS EC2      │
      │ React/Vite   │───►│ Nginx           │
      └──────────────┘    │      │          │
                          │      ▼          │
                          │ Gunicorn         │
                          │      │          │
                          │      ▼          │
                          │ Django REST API  │
                          │      │          │
                          │      ▼          │
                          │ SQLite + Media   │
                          └─────────────────┘

Technology Stack

Frontend

React

Vite

JavaScript

CSS

Lucide React

Backend

Python

Django

Django REST Framework

django-cors-headers

Pillow

python-dotenv

Database

SQLite

Production

Gunicorn

Nginx

Vercel for frontend

AWS EC2 for backend

Project Structure

ai-car-mechanic/
│
├── .gitignore
├── README.md
│
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── mechanic/
│   │   ├── migrations/
│   │   ├── services/
│   │   │   ├── chatbot.py
│   │   │   └── diagnosis.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── ...
│   │
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
└── diagnosis.json

.env, venv, node_modules, db.sqlite3, media files, and generated static files are excluded from version control through .gitignore.

How the System Works

1. Start a Conversation

The user enters a vehicle-related problem.

My car brakes are making a squealing noise.

The frontend sends the message to:

POST /api/chat/

The backend creates or continues a conversation.

2. Store Conversation Data

Messages are stored using Conversation and Message.

Each message records:

sender
message
created_at
conversation

The conversation ID allows later requests to continue the same troubleshooting session.

3. Ask Follow-Up Questions

If more information is needed, the chatbot asks a relevant question.

When does the noise happen — only when braking or also while driving?

Does the brake pedal feel soft, hard, or normal?

The user's answer becomes part of the same conversation.

4. Request Diagnosis

Once enough information is available:

POST /api/diagnosis/

The backend collects the conversation history and passes it to the diagnostic service.

The service returns:

Problem

Explanation

Severity

Recommendation

5. Recommend Service

Example:

Problem:
Brake pad or brake hardware noise

Severity:
Medium

Recommendation:
Have the brake pads, rotors, and brake hardware inspected.

6. Book a Mechanic

If the customer wants professional assistance:

POST /api/booking/

The backend validates the booking data and creates the booking.

Diagnosis Logic

The current implementation intentionally uses deterministic backend rules for supported mechanical scenarios.

Benefits:

Predictable results

Easy testing

Reproducible behavior

Lower external API dependency

Clear debugging

Brake Rules

Terms such as:

squeal
squeaking

can identify a possible brake pad or brake hardware noise condition.

The term:

grinding

can identify a possible severely worn brake pad condition.

Engine Rules

Terms such as:

overheat
overheating

identify an engine overheating condition.

If overheating is also accompanied by:

steam

the system provides a higher-severity cooling-system recommendation.

Safety

The diagnosis provides troubleshooting guidance rather than claiming a definitive physical inspection.

For serious conditions, recommendations emphasize stopping or limiting driving and having the vehicle inspected.

Database Design

Conversation

Conversation
├── id
├── created_at
└── updated_at

A conversation has multiple messages and media files.

Message

Message
├── id
├── conversation
├── sender
├── message
└── created_at

sender can be:

user
bot

Media

Media
├── id
├── conversation
├── file
├── media_type
└── created_at

Supported types:

image
audio
video

Diagnosis

Diagnosis
├── id
├── conversation
├── problem
├── explanation
├── severity
├── recommendation
└── created_at

A conversation has at most one diagnosis.

Booking

Booking
├── id
├── customer_name
├── phone
├── vehicle
├── service
├── preferred_date
├── preferred_time
├── status
└── created_at

New bookings default to:

pending

REST API Documentation

Local base URL:

http://127.0.0.1:8000

API prefix:

/api/

1. Chat

POST /api/chat/

Starts or continues a troubleshooting conversation.

Request:

{
  "conversation_id": 6,
  "message": "My car brakes are making a squealing noise"
}

For a new conversation, the conversation ID can be omitted according to the current backend implementation.

Example response:

{
  "conversation_id": 6,
  "user_message": "My car brakes are making a squealing noise",
  "response": "I can help investigate the brake issue. Before suggesting a diagnosis, I need a little more information.\n\nWhen does the noise happen — only when braking or also while driving? Also, does the brake pedal feel soft, hard, or normal?",
  "is_car_related": true,
  "needs_follow_up": true
}

Response fields:

Field

Description

conversation_id

Conversation ID

user_message

Received user message

response

Mechanic response

is_car_related

Whether the query is vehicle-related

needs_follow_up

Whether more information is required

2. Media Upload

POST /api/upload/

Content type:

multipart/form-data

Fields:

Field

Description

conversation_id

Conversation ID

media_type

image, audio, or video

file

Uploaded media

Example:

curl -X POST http://127.0.0.1:8000/api/upload/   -F "conversation_id=6"   -F "media_type=image"   -F "file=@test_car.jpg"

Example response:

{
  "message": "Media uploaded successfully.",
  "media_id": 2,
  "conversation_id": 6,
  "media_type": "image",
  "file_url": "/media/uploads/test_car.jpg"
}

3. Diagnosis

POST /api/diagnosis/

Request:

{
  "conversation_id": 6
}

Example response:

{
  "diagnosis_available": true,
  "diagnosis_id": 3,
  "conversation_id": 6,
  "problem": "Brake pad or brake hardware noise",
  "explanation": "A squealing noise during braking can be caused by worn brake pads, brake pad vibration, brake dust, or brake hardware.",
  "severity": "medium",
  "recommendation": "Have the brake pads, rotors, and brake hardware inspected. If the brake pads are significantly worn, they should be replaced."
}

Severity values:

low
medium
high
critical

4. Create Booking

POST /api/booking/

Request:

{
  "customer_name": "John Doe",
  "phone": "9876543210",
  "vehicle": "Honda City 2022",
  "service": "Brake inspection",
  "preferred_date": "2026-10-10",
  "preferred_time": "10:30:00"
}

Example response:

{
  "id": 4,
  "customer_name": "John Doe",
  "phone": "9876543210",
  "vehicle": "Honda City 2022",
  "service": "Brake inspection",
  "preferred_date": "2026-10-10",
  "preferred_time": "10:30:00",
  "status": "pending",
  "created_at": "2026-10-01T..."
}

Invalid or incomplete booking data returns HTTP 400 with validation details.

5. Get Booking

GET /api/booking/{booking_id}/

Example:

GET /api/booking/4/

Example response:

{
  "id": 4,
  "customer_name": "John Doe",
  "phone": "9876543210",
  "vehicle": "Honda City 2022",
  "service": "Brake inspection",
  "preferred_date": "2026-10-10",
  "preferred_time": "10:30:00",
  "status": "pending",
  "created_at": "2026-10-01T..."
}

If the booking does not exist:

404 Not Found

{
  "error": "Booking not found."
}

Local Development Setup

Prerequisites

Python 3.12+

Node.js and npm

Git

Clone

git clone https://github.com/ThakurSiddharthsingh/ai-car-mechanic.git
cd ai-car-mechanic

Backend

cd backend

Windows:

python -m venv venv
.env\Scripts\Activate.ps1

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Install:

pip install -r requirements.txt

Migrate:

python manage.py migrate

Optional admin account:

python manage.py createsuperuser

Run:

python manage.py runserver

Backend:

http://127.0.0.1:8000/

Frontend

In another terminal:

cd frontend
npm install

Create frontend/.env:

VITE_API_URL=http://127.0.0.1:8000

Run:

npm run dev

Frontend:

http://localhost:5173/

Environment Variables

Backend

Create:

backend/.env

Example:

DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,testserver
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

For production, use a strong secret key and production host/origin values.

Never commit .env files.

Frontend

Local:

VITE_API_URL=http://127.0.0.1:8000

Production:

VITE_API_URL=https://your-backend-domain

Running the Application

Terminal 1:

cd backend
python manage.py runserver

Terminal 2:

cd frontend
npm run dev

Open:

http://localhost:5173/

Deployment

Frontend — Vercel

The frontend is a Vite React application.

Recommended Vercel settings:

Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install

Production environment variable:

VITE_API_URL=<public-backend-url>

The frontend should be redeployed after changing the production API URL.

Backend — AWS EC2

The intended Linux deployment is:

Internet
   ↓
Nginx
   ↓
Gunicorn
   ↓
Django
   ↓
SQLite

Typical setup:

git clone https://github.com/ThakurSiddharthsingh/ai-car-mechanic.git
cd ai-car-mechanic/backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --noinput

Gunicorn is used as the production WSGI server on Linux.

Nginx can forward API requests to Gunicorn and serve static/media files.

AWS deployment is a separate production step. The repository should not contain production secrets.

Error Handling

Common API responses include:

400 Bad Request

Used for invalid request data, such as incomplete booking information.

404 Not Found

Used when a requested booking does not exist.

500 Internal Server Error

Unexpected server-side errors should be handled without exposing secrets or internal configuration.

Security and Configuration

The repository excludes generated and sensitive files through .gitignore.

Examples:

.env
venv/
node_modules/
db.sqlite3
media/
staticfiles/

Production should use:

DEBUG=False

and explicitly configured:

ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS
CSRF_TRUSTED_ORIGINS

Uploaded files should be validated and treated as untrusted input in production.

Design Decisions

REST API Separation

React communicates with Django through REST endpoints rather than accessing the database directly.

Benefits:

Clear separation of concerns

Easier testing

Independent frontend/backend deployment

Reusable APIs

Deterministic Diagnosis Where Possible

The assignment emphasizes minimizing unnecessary AI usage.

For supported symptoms, deterministic backend logic provides:

Predictable behavior

Reproducible results

Easy testing

Lower external dependency

Easier debugging

AI can be introduced later for cases where broader reasoning is actually required.

Conversation Persistence

Conversation and message records are persisted so the diagnostic service can use previous user answers during multi-turn troubleshooting.

Structured Diagnosis

Diagnosis is stored separately from chat messages so the frontend can display structured:

Problem
Explanation
Severity
Recommendation

Dedicated Booking Resource

Booking is a separate REST resource so scheduling information can evolve independently from conversational messages.

Future Improvements

Gemini integration for complex diagnostic reasoning.

Image-based inspection assistance.

Audio analysis for engine/brake sounds.

Video analysis for mechanical symptoms.

More comprehensive diagnostic rules.

Vehicle make/model/year collection.

Mechanic availability management.

Real appointment scheduling.

Authentication and user accounts.

Email/SMS booking notifications.

PostgreSQL for larger deployments.

S3/object storage for uploaded media.

HTTPS and a custom domain.

Automated API tests and CI/CD.

Rate limiting and stronger upload validation.

Admin dashboard for mechanics and bookings.

Submission Checklist

React frontend

Django backend

REST API architecture

Conversational troubleshooting

Follow-up questions

Rule-based diagnosis

Media upload endpoint

Mechanic booking API

Booking retrieval API

SQLite database

Environment-based configuration

Git/GitHub repository

Vercel frontend deployment

Public AWS backend deployment

Connect Vercel to production backend

Final end-to-end production testing

Final API/architecture review

Repository

GitHub:

https://github.com/ThakurSiddharthsingh/ai-car-mechanic

License

This project was created as part of a Full-Stack Developer Intern technical assignment.
