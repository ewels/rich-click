## Overview

**rich-click** comes with a CLI tool that allows you to format the Click help output for any CLI that uses Click.

To use, simply prefix to your normal command.
For example, to get richified click help text from a package called `awesometool`, you could run:

```console
$ flask --help
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  An application to load must be given with the '--app' option, 'FLASK_APP'
  environment variable, or with a 'wsgi.py' or 'app.py' file in the current
  directory.

Options:
  -e, --env-file FILE   Load environment variables from this file. python-
                        dotenv must be installed.
  -A, --app IMPORT      The Flask application or factory function to load, in
                        the form 'module:name'. Module can be a dotted import
                        or file path. Name is not required if it is 'app',
                        'application', 'create_app', or 'make_app', and can be
                        'name(args)' to pass arguments.
  --debug / --no-debug  Set debug mode.
  --version             Show the Flask version.
  --help                Show this message and exit.

Commands:
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
```

```console
 Usage: flask [OPTIONS] COMMAND [ARGS]...

 A general utility script for Flask applications.
 An application to load must be given with the '--app' option, 'FLASK_APP' environment variable, or
 with a 'wsgi.py' or 'app.py' file in the current directory.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --env-file          -e  FILE    Load environment variables from this file. python-dotenv must be │
│                                 installed.                                                       │
│ --app               -A  IMPORT  The Flask application or factory function to load, in the form   │
│                                 'module:name'. Module can be a dotted import or file path. Name  │
│                                 is not required if it is 'app', 'application', 'create_app', or  │
│                                 'make_app', and can be 'name(args)' to pass arguments.           │
│ --debug/--no-debug              Set debug mode.                                                  │
│ --version                       Show the Flask version.                                          │
│ --help                          Show this message and exit.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
