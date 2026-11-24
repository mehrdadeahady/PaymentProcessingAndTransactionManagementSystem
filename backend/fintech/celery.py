"""
Celery Application Configuration

This file creates and configures the Celery app.

Responsibilities:

1. Connect Celery to Django settings
2. Discover tasks automatically
3. Enable background processing

Example:

Transfer API
    ↓
Create Transaction
    ↓
process_transaction.delay()
    ↓
Redis Queue
    ↓
Celery Worker
    ↓
Transaction Processed
"""

# Access environment variables
import os

# Celery framework
from celery import Celery


# =====================================
# DJANGO SETTINGS
# =====================================

# Tell Celery where Django settings live.
#
# Equivalent to:
#
# export DJANGO_SETTINGS_MODULE=fintech.settings
#
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "fintech.settings"
)


# =====================================
# CREATE CELERY APPLICATION
# =====================================

app = Celery("fintech")


# =====================================
# LOAD CONFIGURATION
# =====================================

# Read values from settings.py
#
# Example:
#
# CELERY_BROKER_URL
#
# CELERY_RESULT_BACKEND
#
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)


# =====================================
# AUTO DISCOVER TASKS
# =====================================

# Automatically finds:
#
# apps/transactions/tasks.py
#
# apps/payments/tasks.py
#
# etc.
#
app.autodiscover_tasks()