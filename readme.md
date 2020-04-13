

## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

## About The Project

A simple registry information service that provides information about IGSN allocating agents and namespaces through a simple API.

### Built With

* [FastAPI](https://pypi.org/project/fastapi/)
* [Pydantic](https://pypi.org/project/pydantic/)
* [lxml](https://pypi.org/project/lxml/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* python 3.8 and pip - I'll not go into how to get Python (see [here](https://www.python.org/downloads/) or [here](https://www.anaconda.com/distribution/)) and pip should come for free with your install. 
* [pipenv](https://github.com/pypa/pipenv) - we use this to manage dependencies. You can install it using pip by doing 

```sh
$ pip install pipenv
```

### Installation

1. Clone the repo

```bash
$ git clone https://github.com/jesserobertson/igsn_namespace_service.git

Cloning into 'igsn_namespace_service'...
# snp output
```

2. Install Python packages

```bash
$ cd igsn_namespace_service
$ pipenv install

[====] Creating virtual environment...
# snip output
Installing dependencies from Pipfile.lock (e902b8)…
  ================================ 46/46 - 00:00:19
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

3. To run the test suite or do development, include the `--dev` dependencies:

```bash
$ pipenv install --dev

# output as above, should include dev dependencies like pytest

$ pipenv run python -m pytest

========================== test session starts ===========================
# snip test output
Success: no issues found in 6 source files
========================== 39 passed in 10.36s ===========================
```

<!-- USAGE EXAMPLES -->
## Usage

The service is very basic and can run standalone. To run a local version of the service, you just need to stand up a test server and start making requests:

1. Run the test server using uvicorn (or similar ASGI webservice). This should start a
service listening on whatever port you bind it to

```bash
$ pipenv run uvicorn app:app --port 8080

INFO:     Started server process [21152]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

2. Now you should be able to start making requsts using whatever client takes your fancy. I quite like [httpie](), so I'd do

```bash
$ http :8080/agents/CSIRO

HTTP/1.1 200 OK
content-length: 459
content-type: application/json
date: Sun, 12 Apr 2020 05:29:34 GMT
server: uvicorn

{
    "name": "CSIRO",
    "namespaces": [
        {
            "date_created": "2013-05-24T15:07:34+02:00",
            "handle_prefix": "10273/ARRC",
            "namespace": "ARRC",
            "owner": "CSIRO"
        },
        {
            "date_created": "2015-01-22T13:01:15+01:00",
            "handle_prefix": "10273/CS",
            "namespace": "CS",
            "owner": "CSIRO"
        },
        {
            "date_created": "2014-05-19T08:44:04+02:00",
            "handle_prefix": "10273/CSD",
            "namespace": "CSD",
            "owner": "CSIRO"
        },
        {
            "date_created": "2013-05-24T15:06:59+02:00",
            "handle_prefix": "10273/CSI",
            "namespace": "CSI",
            "owner": "CSIRO"
        }
    ]
}
```

3. To see the Swagger documentation, head to [https://localhost:8080/docs](https://localhost:8080/docs).

_For more examples, please refer to the [Documentation](https://example.com)_

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/jesserobertson/igsn_namespace_service/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Your Name - [@jessrobertson](https://twitter.com/jessrobertson)

Project Link: [https://github.com/jesserobertson/igsn_namespace_service](https://github.com/jesserobertson/igsn_namespace_service)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()

<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/github/license/jesserobertson/igsn_namespace_service.svg?style=flat-square
[license-url]: https://github.com/jesserobertson/igsn_namespace_service/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/robertsonjess
