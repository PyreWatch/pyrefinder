# TimescaleDB

For the database, we are using TimescaleDB, a time series database utilizing Postgres. We decided on this database as it allows us to have the time series performance requirements for repeated inserttions into the database at any given time while allowing us to utilize pure SQL and reliability and familiarity that other time series databases do not have.

## Getting started

In order to launch the database independently, you can run the following docker command, adding in a password to be used by the postgres user, since TimescaleDB is still Postgres:

`docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=<:password> -v <:location>:/var/lib/postgresql/data timescale/timescaledb:latest-pg12`
