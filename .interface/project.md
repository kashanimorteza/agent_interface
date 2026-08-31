# Trading Assistant

A platform for defining and managing trading information, strategies, actions, and related data.

The platform allows the user to enter, view, and manage the information required for the trading system.

The project is developed incrementally in phases.

<br> <br>

## Project Structure

### Structure

- **Backend** — manages application data and functionality.
- **Frontend** — provides the user interface for entering, viewing, and managing information.

### Models

#### Account

Fields: ID, Name, Username, Password, Status, Description

#### Asset

Fields: ID, Name, Status, Description

#### Strategy

Fields: ID, Name, Risk Parameter, Status, Description

#### Action Group

Fields: ID, Name, Status, Description

#### Action

Fields: ID, Name, Asset ID, Strategy ID, Group ID, Status, Description

#### Execute

Fields: ID, Name, Action ID, Profit, State, Status, Description


<br> <br>

## Development

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

#### General

- HTTPS: false
- Error Handling: false
- Logging: false
- Testing: false
- Authentication: false


### Frontend

#### Technology

- Language: TypeScript
- Library: React
- Framework: Next.js
- Package Manager: npm

#### General

- HTTPS: false
- Error Handling: false
- Logging: false
- Testing: false
- Authentication: false

<br> <br>

## Phase 1

**Title:** Backend API  
**Target:** Backend

The goal of Phase 1 is to create a working Backend and Frontend for entering and managing the application's trading information.

The user should be able to:

Add information.
View information in lists.
View individual items.
Edit and update items.
Delete items.
Enable or disable items through their status.
Phase 1 is limited to data entry and data management.

It does not include MetaTrader integration, trade execution, or reportin