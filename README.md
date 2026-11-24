# Payment Processing and Transaction Management System

## Fintech Wallet Platform

A full-stack fintech wallet application demonstrating reliable and secure money transfer processing using **Django, React, PostgreSQL, Redis, and Celery**.

The platform focuses on transaction reliability, asynchronous processing, automatic retries, idempotency protection, and audit logging.

---

## Architecture and Project Structure

```text
fintech-wallet-platform/
│
├── README.md
├── docker-compose.yml
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   │
│   ├── fintech/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   │
│   ├── apps/
│   │   ├── accounts/
│   │   │   └── models.py
│   │   │
│   │   ├── wallets/
│   │   │   └── models.py
│   │   │
│   │   ├── transactions/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── tasks.py
│   │   │   ├── services.py
│   │   │   └── provider.py
│   │   │
│   │   └── audit/
│   │       └── models.py
│   │
│   └── tests/
│       ├── test_auth.py
│       ├── test_wallets.py
│       ├── test_provider.py
│       ├── test_services.py
│       ├── test_tasks.py
│       ├── test_transactions_api.py
│       └── test_idempotency.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   │
│   ├── public/
│   │
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   │
│   │   ├── api/
│   │   │   └── axios.ts
│   │   │
│   │   ├── services/
│   │   │   ├── authService.ts
│   │   │   ├── walletService.ts
│   │   │   └── transactionService.ts
│   │   │
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   └── TransferPage.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── WalletCard.tsx
│   │   │   ├── TransactionTable.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useTransactions.ts
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   │
│   │   ├── types/
│   │   │   ├── auth.ts
│   │   │   ├── wallet.ts
│   │   │   └── transaction.ts
│   │   │
│   │   └── routes/
│   │       └── AppRoutes.tsx
│   │
│   └── tests/
│
└── docs/
    ├── architecture.png
    └── api-spec.md
```

### Backend Responsibilities

| Module | Responsibility |
|---|---|
| `accounts/` | User accounts and authentication |
| `wallets/` | Wallet management and balances |
| `transactions/` | Transaction processing and business logic |
| `transactions/tasks.py` | Celery task orchestration |
| `transactions/services.py` | Transaction rules, status updates, audit creation, and failure handling |
| `transactions/provider.py` | External payment provider abstraction |
| `audit/` | Transaction audit logging |
| `tests/` | Backend automated tests |

---

## Features

- User Registration and Login
- JWT Authentication
- Wallet Management
- Money Transfers
- Asynchronous Transaction Processing
- Automatic Retry Mechanism
- Exponential Backoff Strategy
- Idempotency Protection
- Transaction Audit Logging
- Transaction History
- Mock Payment Provider Integration
- Docker Support

---

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis

### Frontend

- React
- TypeScript
- Vite
- Material UI
- React Query

### Infrastructure

- Docker
- Docker Compose
- PostgreSQL
- Redis

---

## Transaction Processing Architecture

The application uses asynchronous transaction processing to improve reliability and prevent long-running payment operations from blocking API requests.

```text
React Client
     |
     v
Django REST API
     |
     v
PostgreSQL
     |
     v
Celery + Redis
     |
     v
Mock Payment Provider
     |
     v
Transaction Status Update
     |
     v
Audit Logging
```

### Transaction Processing Flow

1. The user initiates a money transfer through the React application.
2. The Django REST API validates the request.
3. The transaction is created and persisted in PostgreSQL.
4. A Celery task is dispatched through Redis.
5. The payment provider processes the transaction.
6. The transaction status is updated based on the processing result.
7. An audit record is created to track the transaction lifecycle.
8. Failed transactions are automatically retried according to the retry strategy.

---

## Automatic Retry Strategy

Transactions are automatically retried through Celery using an exponential backoff strategy.

### Retry Schedule

| Attempt | Retry Delay |
|---|---:|
| Attempt 1 | 2 seconds |
| Attempt 2 | 4 seconds |
| Attempt 3 | 8 seconds |
| Attempt 4 | 16 seconds |
| Attempt 5 | 32 seconds |

**Maximum retries:** 5

The exponential backoff strategy helps handle temporary payment provider failures while avoiding excessive retry requests.

---

## Idempotency Protection

Each transaction is protected by a unique idempotency key to prevent duplicate payment execution.

This ensures that repeated requests with the same idempotency key do not result in multiple executions of the same payment operation.

Idempotency is particularly important when:

- A client retries a request after a timeout.
- A network failure occurs during transaction processing.
- A Celery task is executed more than once.
- A payment provider responds slowly or returns an uncertain result.

---

## Installation and Setup

### Prerequisites

Make sure the following tools are installed:

- Docker
- Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

cd YOUR_REPOSITORY
```

### 2. Configure Environment Variables

Create your environment configuration using the example file:

```bash
cp backend/.env.example backend/.env
```

Update the environment variables according to your local configuration.

### 3. Build and Start the Application

```bash
docker compose up --build
```

This command builds the application images and starts the configured services.

---

## Running Tests

Run the backend test suite inside the Django container:

### Run All Django Tests

```bash
docker compose exec django python manage.py test
```

### Run Specific Backend Tests

```bash
docker compose exec django python manage.py test backend.tests
```

### Run Tests Using Pytest

```bash
docker compose exec django pytest
```

---

## API Documentation

API documentation is maintained in:

```text
docs/api-spec.md
```

Refer to this file for available endpoints, request parameters, and response structures.

---

## Architecture Documentation

The architecture diagram is available at:

```text
docs/architecture.png
```

---

## Project Goals

This project demonstrates practical implementation of important fintech backend engineering concepts:

- Reliable financial transaction processing
- Asynchronous task orchestration
- Fault tolerance and retry mechanisms
- Idempotent payment operations
- Transaction lifecycle management
- Auditability and traceability
- Separation of business logic and external payment providers
- Full-stack application development

---

## Disclaimer

This project is intended for educational and demonstration purposes.

It uses a mock payment provider and is not intended for processing real financial transactions.
