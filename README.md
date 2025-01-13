# SIGINT API

Accept signal intercept reports and supporting media from remote nodes.


## Dependencies


### Alembic - Migration tool compatible with SQLAlchemy for handling schema changes

Alembic uses a table called `alembic_version` in the database to track the currently applied migration version. Each migration script has a unique ID that corresponds to a row in this table.

When you run alembic upgrade or downgrade, Alembic:
- Reads the current version from the alembic_version table.
- Compares it to the version defined in the migration script.
- Applies or rolls back the necessary changes to bring the database schema to the target version.

Initial Migration: `alembic revision --autogenerate -m "Initial migration"`
apply to database: `alembic upgrade head`

Subsequent Migrations: `alembic revision --autogenerate -m "Add age column to users"`
apply to database: `alembic upgrade head`

## Misc

```sql
CREATE ROLE sigint;
CREATE ROLE intercept_api WITH LOGIN PASSWORD '<REDACTED>';
GRANT sigint TO intercept_api;
CREATE database sigint;
GRANT ALL PRIVILEGES ON DATABASE sigint TO sigint;
ALTER DATABASE sigint OWNER TO sigint;
```

