## Wireup demo

Demo application for [WireUp](https://maldoinc.github.io/wireup/), a Python dependency injection library.

Additionally uses [request-mapper](https://github.com/maldoinc/python-request-mapper/) to map
incoming request data to Pydantic models.

## Usage

This is intended as a demo to showcase various aspects of wireup. Feel free to explore 
and play around with to get familiar with the library.

### Points of interest

* `app/app.py` - Container parameter initialization.
* `app/service` - Service declaration.
* `app/blueprint` - Autowiring api views.
* `test` - Tests. Various examples on testing the services in isolation.

### Running the api

`DB_CONNECTION_URL=sqlite://blog.db MAILER_DSN="smtp://..." python -m app.app`
