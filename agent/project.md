# Trading Assistant

A platform for defining and managing trading information, strategies, actions, and related data.

The platform allows the user to enter, view, and manage the information required for the trading system.

The project is developed incrementally in phases.

<br> <br>

## Project Structure

The project consists of:

- **Backend** — manages application data and functionality.
- **Frontend** — provides the user interface for entering, viewing, and managing information.

This document defines **what the application should do** and what should be delivered in each phase.

It does not define how the application should be implemented.

<br> <br>

## Development

### Backend

- Language: Python
- API: FastAPI
- ORM: SQLAlchemy
- Database: SQLite
- Database Migration: Standard Python migration framework
- Python Version: Latest stable version available when development starts

### Frontend

A Frontend is required for interacting with the application and managing its information.

The Frontend technology and framework will be defined separately.

### General

- Authentication is not required.
- Automated tests are not required.

<br> <br>

# Phase 1 — Data Entry and Management

The goal of Phase 1 is to create a working Backend and Frontend for entering and managing the application's trading information.

The user should be able to:

- Add information.
- View information in lists.
- View individual items.
- Edit and update items.
- Delete items.
- Enable or disable items through their status.

Phase 1 is limited to data entry and data management.

It does not include MetaTrader integration, trade execution, or reporting.

## Models

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