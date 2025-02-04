# Project

[ GATEWAY NOTIFICATION DELIVERY ](https://project.com)

### Author

- gautier.tiehoule@ngser.com

##### Prerequisites

The setups steps expect following tools installed on the system.

- Git [2.34.1](https://git-scm.com)
- Python [3.9.9](https://ruby-doc.org)
- FastAPI [0.113.0](https://fastapi.tiangolo.com/)
- Docker [27.5.1](https://www.docker.com)

## Install and Run

### Clone the repository

```shell
git clone gitlab.ngser.com/project_name
cd project_name
```

### Create environment variables file

Copy the sample .example.env file and edit the variables configuration as required.

```bash
cp .example.env .env
```

### Create docker image

```bash
docker build -t notification .
```

### Run a container from the docker image

```bash
docker run -d --name notify -p 4545:4545 notification
```