-- `docker exec -it postgres psql -U postgres`

/*

 - Create 'sigint_users' role
 - Create 'sigint' database
 - Configure permissions to permit 'sigint_users' role to alter 'sigint' database
 - Enable 'postgis' extension

 */

-- configure sigint-api server user
CREATE ROLE sigint_users;
GRANT sigint_users TO sigint_api;

CREATE DATABASE sigint;
GRANT CREATE ON DATABASE sigint TO sigint_users; -- Allows creating objects in the database

\c sigint

ALTER SCHEMA public OWNER TO sigint_users;

GRANT USAGE, CREATE ON SCHEMA public TO sigint_users; -- Allows usage of the schema and creating tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO sigint_users; -- Grants table-level privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES, TRIGGER ON TABLES TO sigint_users; -- Ensures future tables have these permissions
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO sigint_users;
GRANT USAGE ON SCHEMA public TO sigint_users;
GRANT CREATE ON SCHEMA public TO sigint_users;

CREATE EXTENSION postgis; -- enable postgis extension on sigint database



/* MISC

-- list user roles
SELECT
    grantee.rolname AS member,
    granted.rolname AS role
FROM
    pg_auth_members m
JOIN
    pg_roles grantee ON m.member = grantee.oid
JOIN
    pg_roles granted ON m.roleid = granted.oid;



-- confirm user member of a role

SELECT
    grantee.rolname AS member,
    granted.rolname AS role
FROM
    pg_auth_members m
JOIN
    pg_roles grantee ON m.member = grantee.oid
JOIN
    pg_roles granted ON m.roleid = granted.oid
WHERE
    grantee.rolname = 've7mjc';


*/