# FinTech Wallet Platform API Specification

## Authentication

### Register User

POST /api/accounts/register/

Request:

```json
{
  "email": "user@example.com",
  "username": "john",
  "password": "Password123!"
}
```

Response:

```json
{
  "message": "User created successfully"
}
```

### Login

POST /api/accounts/login/

Request:

```json
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

Response:

```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

### Refresh Token

POST /api/token/refresh/

Request:

```json
{
  "refresh": "jwt_refresh_token"
}
```

Response:

```json
{
  "access": "new_jwt_access_token"
}
```

## Wallets

### Current User Wallet

GET /api/wallets/me/

Headers:

```http
Authorization: Bearer <token>
```

Response:

```json
{
  "id": 1,
  "user": 1,
  "balance": "1000.00",
  "updated_at": "2026-01-01T10:00:00Z"
}
```

## Transactions

### Create Transfer

POST /api/transactions/transfer/

Headers:

```http
Authorization: Bearer <token>
Idempotency-Key: 7dfc1fbb-8e04-4f37-8ef3-b9435534dc3d
```

Request:

```json
{
  "receiver_id": 2,
  "amount": "100.00"
}
```

Response:

```json
{
  "transaction_id": 15,
  "status": "PENDING"
}
```

### List Transactions

GET /api/transactions/

Headers:

```http
Authorization: Bearer <token>
```

Response:

```json
[
  {
    "id": 15,
    "amount": "100.00",
    "status": "SUCCESS",
    "retry_count": 0
  }
]
```

### Transaction Details

GET /api/transactions/{id}/

Headers:

```http
Authorization: Bearer <token>
```

Response:

```json
{
  "id": 15,
  "sender": 1,
  "receiver": 2,
  "amount": "100.00",
  "status": "SUCCESS",
  "retry_count": 0,
  "provider_reference": "PAY-20260101-ABC12345"
}
```

## Transaction States

```text
PENDING
PROCESSING
RETRYING
SUCCESS
FAILED
```

## Retry Mechanism

```text
Retry 1 -> 2 Seconds
Retry 2 -> 4 Seconds
Retry 3 -> 8 Seconds
Retry 4 -> 16 Seconds
Retry 5 -> 32 Seconds
```

Maximum Retries:

```text
5
```

## Idempotency

All transfer requests should include:

```http
Idempotency-Key
```

This prevents duplicate transfers caused by:

- Double clicks
- Network retries
- Browser refreshes
- Provider timeouts