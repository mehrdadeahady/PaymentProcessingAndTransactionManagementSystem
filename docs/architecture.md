# Architecture

## High Level

```text
React Frontend
        │
        ▼
Django REST API
        │
        ▼
PostgreSQL
        │
        ▼
Celery Worker
        │
        ▼
Mock Payment Provider
```

## Backend Structure

```text
apps/

├── accounts
├── wallets
├── transactions
└── audit
```

## Transaction Processing Flow

```text
Transfer Request
        │
        ▼
Transaction Created
        │
        ▼
PENDING
        │
        ▼
Celery Worker
        │
        ▼
PROCESSING
        │
        ▼
Provider Call
        │
 ┌──────┴──────┐
 ▼             ▼
SUCCESS      FAILURE
                │
                ▼
            RETRYING
                │
                ▼
          Exponential
            Backoff
                │
                ▼
SUCCESS OR FAILED
```

## Authentication Flow

```text
Login
  │
  ▼
JWT Access Token
  │
  ▼
Protected APIs
```

## Wallet Flow

```text
User
 │
 ▼
Wallet
 │
 ▼
Balance
```

## Retry Architecture

```text
Django
 │
 ▼
Redis Queue
 │
 ▼
Celery Worker
 │
 ▼
Payment Provider
```

## Audit Logging

```text
TRANSACTION_CREATED

TRANSACTION_SUCCESS

TRANSACTION_RETRY

TRANSACTION_FAILED
```