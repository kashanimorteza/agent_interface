# Trading Assistant

Defines what the project is and the main parts that make up the system.

**Name:** Trading Assistant  
**Description:**  A platform for defining and managing trading information, strategies, actions, and related data.  

<br><br>

## Structure

- **Backend** — manages application data and functionality.
- **Frontend** — provides the user interface for interacting with the application.

<br><br>

## Development

Defines the technologies, tools, and development settings used to build the project.

### General

- HTTPS: false
- Error Handling: false
- Logging: false
- Testing: false
- Authentication: false

### Backend

#### Technology

- Language: Python
- API: FastAPI
- ORM: SQLAlchemy
- Database: SQLite
- Database Migration: Standard Python migration framework

#### API

- API Key: true
- API Documentation: true
- API Documentation Type: Docs
- ReDoc: false

### Frontend

#### Technology

- Language: TypeScript
- Library: React
- Framework: Next.js
- Package Manager: npm

<br><br>

## Models

Defines the core entities of the project and the data fields that belong to each entity.

### Account

Fields: ID, Name, Username, Password, Status, Description

### Asset

Fields: ID, Name, Status, Description

### Strategy

Fields: ID, Name, Risk Parameter, Status, Description

### Action Group

Fields: ID, Name, Status, Description

### Action

Fields: ID, Name, Asset ID, Strategy ID, Group ID, Status, Description

### Execute

Fields: ID, Name, Action ID, Profit, State, Status, Description

<br><br>

## Phases

Defines the project's implementation phases. Phases are executed step by step in their defined order, with each phase representing the next intended stage of project development.

### Phase 1

**Title:** Backend API  
**Target:** Backend

**Goal:** Create and run the API for all defined project models.
