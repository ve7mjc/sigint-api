-- docker exec -it postgres psql -U postgres

/* Configure sigint-api server user for use with 'sigint' database

 - 'sigint' database should already exist
 - 'sigint_users' role should already exist

 */

CREATE ROLE sigint_api WITH LOGIN PASSWORD 'changeme';
GRANT sigint_users TO sigint_api;
