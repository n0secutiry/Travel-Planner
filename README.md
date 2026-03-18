# Travel Project Management API

A RESTful API for managing travel projects, places (fetched from the Art Institute of Chicago API), and personal notes. Built with FastAPI, SQLite, and SQLAlchemy.

## Features

- **Projects**: Create, read, update, delete travel projects. A project consists of a name, optional description and start date.
- **Places**: Add places (artworks) from the Art Institute of Chicago API to a project. Each place is validated against the external API before being stored.
- **Notes & visited status**: Attach notes to a place in a project and mark it as visited.
- **Business rules**:
  - Maximum 10 places per project.
  - Cannot delete a project if any place in it is already marked as visited.
  - Duplicate places (by external ID) cannot be added to the same project.
- **Automatic interactive API docs** at `/docs` (Swagger UI) and `/redoc`.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (database)
- Docker & Docker Compose (optional)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip
- (Optional) Docker & Docker Compose

### Installation (local)

1. Clone the repository:
   ```bash
   git clone https://github.com/n0secutiry/Travel-Planner
   cd Travel-Planner
```

2. Start project:
   ```bash
docker-compose up --build
   ```