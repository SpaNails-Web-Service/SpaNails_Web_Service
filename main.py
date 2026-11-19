"""Entry point retained for `uvicorn main:app` commands."""

from app.main import app

__all__ = ["app"]
