# Testing Strategy

## Backend Tests

```text
test_auth.py

test_wallets.py

test_provider.py

test_services.py

test_tasks.py

test_transactions_api.py

test_idempotency.py
```

## Covered Areas

### Authentication

- Registration
- JWT Login
- Token Generation

### Wallets

- Wallet Creation
- Balance Retrieval

### Services

- Transaction Creation
- Business Rules
- Balance Checks

### Transactions

- Transfers
- Retries
- Audit Logs

### Provider

- Health Check
- Transfer Simulation

### Idempotency

- Duplicate Request Prevention

### API

- Protected Endpoints
- Transfer Endpoints
- Wallet Endpoints