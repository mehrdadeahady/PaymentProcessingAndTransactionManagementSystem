"""
Ensures Celery loads
when Django starts.
"""

# Import celery application.
from .celery import app as celery_app

# Expose celery instance.
__all__ = (
    "celery_app",
)