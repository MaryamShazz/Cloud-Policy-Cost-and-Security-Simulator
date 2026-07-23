# Database Migrations

This directory contains the Alembic database migration files used by the Cloud Policy, Cost and Security Simulator.

Alembic manages database schema versioning, allowing the project to evolve while preserving existing data.

## Contents

- **versions/** – Individual migration scripts.
- **env.py** – Alembic environment configuration.
- **script.py.mako** – Template used when generating new migration files.
- **alembic.ini** – Alembic configuration.

## Creating a Migration

```bash
alembic revision --autogenerate -m "Describe your changes"
```

## Applying Migrations

```bash
alembic upgrade head
```

## Notes

- Do not modify existing migration files after they have been applied.
- Create a new migration whenever the database schema changes.
- Keep migration history intact to ensure consistent database versioning.