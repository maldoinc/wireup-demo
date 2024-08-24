## Wireup demo

Demo application for [Wireup](https://maldoinc.github.io/wireup/), a Python dependency injection library.

Demo contains a Flask application and a set of commands using Click. 
The web application and commands share the same service layer using Wireup.

## Usage

This is intended as a demo to showcase various aspects of wireup. Feel free to explore 
and play around with to get familiar with the library.

### Points of interest

* `demoapp/app.py` - Flask app initialization.
* `demoapp/cli.py` - Cli for this application via Click.
* `demoapp/service` - Service declaration.
* `demoapp/blueprint` - Autowiring api views.
* `test` - Tests. Various examples on testing the services in isolation.


### Running the cli

`python -m demoapp.cli`

* Create initial db with `python -m demoapp.cli create-db`
* Add a blog post `python -m demoapp.cli create-post "Hello World" "This is my first blog"`

### Running the api

`FLASK_APP=demoapp/app.py python -m flask run`
