# PaymentProcessingAndTransactionManagementSystem

Fintech Wallet Platform
A full-stack fintech wallet application demonstrating reliable money transfer processing using Django, React, PostgreSQL, Redis, and Celery.

Architecture

fintech-wallet-platform/
│
├── README.md
│
backend/
│
├── manage.py
├── requirements.txt
├── .env.example
│
├── fintech/
│   ├── __init__.py
│   ├── settings.py      <-- REST + CELERY configs go here
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── celery.py
│
├── apps/
│   ├── accounts/
│   │   └── models.py
│   │
│   ├── wallets/
│   │   └── models.py
│   │
│   ├── transactions/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── provider.py
│   │   ├── tasks.py
│   │   │       ├── orchestration only
│   │   ├── services.py
│   │   │       ├── transaction rules
│   │   │       ├── status updates
│   │   │       ├── audit creation
│   │   │       └── failure handling
│   │   ├── provider.py
│   │           └── external provider abstraction
│   │
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── audit/
│       └── models.py
│
└── tests/
    ├── test_auth.py
    ├── test_wallets.py
    ├── test_provider.py
    ├── test_services.py
    ├── test_tasks.py
    ├── test_transactions_api.py
    └── test_idempotency.py
│
├── frontend/
│    │
│    ├── package.json
│    ├── vite.config.ts
│    ├── tsconfig.json
│    ├── .env
│    │
│    ├── public/
│    │
│    ├── src/
│    │   │
│    │   ├── App.tsx
│    │   ├── main.tsx
│    │   │
│    │   ├── api/
│    │   │   └── axios.ts
│    │   │
|    |   ├── services/
|    |   │   ├── authService.ts
|    |   │   ├── walletService.ts
|    |   │   └── transactionService.ts
│    │   ├── pages/
│    │   │   ├── LoginPage.tsx
│    │   │   ├── RegisterPage.tsx
│    │   │   ├── DashboardPage.tsx
│    │   │   └── TransferPage.tsx
│    │   │
│    │   ├── components/
│    │   │   ├── Navbar.tsx
│    │   │   ├── WalletCard.tsx
│    │   │   ├── TransactionTable.tsx
│    │   │   └── ProtectedRoute.tsx
│    │   │
│    │   ├── hooks/
│    │   │   ├── useAuth.ts
│    │   │   └── useTransactions.ts
│    │   │
│    │   ├── context/
│    │   │   └── AuthContext.tsx
│    │   │
│    │   ├── types/
│    │   │   ├── auth.ts
│    │   │   ├── wallet.ts
│    │   │   └── transaction.ts
│    │   │
│    │   └── routes/
│    │       └── AppRoutes.tsx
│    │
│    └── tests/  
│
├── docker-compose.yml
│
└── docs/
    ├── architecture.png
    └── api-spec.md

Features
User Registration/Login
JWT Authentication
Wallet Management
Money Transfer
Transaction Processing
Automatic Retry Mechanism
Idempotency Protection
Audit Logging
Transaction History
Docker Support
Tech Stack
Backend
Django
Django REST Framework
PostgreSQL
Celery
Redis
Frontend
React
Typescript
Vite
Material UI
React Query
Retry Strategy
Transactions are retried automatically through Celery with exponential backoff.

Retry schedule:

Attempt 1 -> 2 seconds

Attempt 2 -> 4 seconds

Attempt 3 -> 8 seconds

Attempt 4 -> 16 seconds

Attempt 5 -> 32 seconds

Maximum retries: 5

Idempotency
Each transaction is protected by a unique idempotency key to avoid duplicate payment execution.

Architecture
React Client ↓ Django REST API ↓ PostgreSQL ↓ Celery + Redis ↓ Mock Payment Provider

Run
docker compose up --build

Run Tests
Shell
docker compose exec django \
python manage.py test
Or:
Shell
docker compose exec django \
python manage.py test backend.tests
Or with pytest:
Shell
docker compose exec django \
pytest