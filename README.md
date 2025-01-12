# service-borrow

Borrow microservice

## Overview

The `service-borrow` is a microservice responsible for managing the borrowing of books. It provides endpoints for 
listing borrows, creating new borrows, returning books, and extending borrow periods. It also includes a health check 
endpoint.

## Endpoints

The endpoints are described with swagger and can be accessed at `http://<domain-ip>/api/borrows/schema/swagger-ui/`.

## Environment Variables

- `DJANGO_SECRET_KEY`: Secret key for Django.
- `ENV_ALLOWED_HOST`: Allowed hosts for the Django application.
- `DEBUG`: Debug mode (1 for true, 0 for false).
- `DJANGO_SUPERUSER_USERNAME`: Username for the Django superuser.
- `DJANGO_SUPERUSER_PASSWORD`: Password for the Django superuser.
- `DJANGO_SUPERUSER_EMAIL`: Email for the Django superuser.
- `DB_IGNORE_SSL`: Ignore SSL for the database connection (true or false).
- `DB_HOST`: Host for the database connection.
- `DB_PORT`: Port for the database connection.
- `DB_NAME`: Name of the database.
- `DB_USER`: Username for the database connection.
- `DB_PASSWORD`: Password for the database connection.
- `ETCD_HOST`: ETCD host.
- `ETCD_PORT`: ETCD port.
- `ETCD_USERNAME`: ETCD username.
- `ETCD_PASSWORD`: ETCD password.
- `MESSAGE_BROKER_URL`: URL for the message broker.

## Setup

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up environment variables in the `.env` file.
4. Start the server using `docker-compose up`.
5. Run migrations:
- `python manage.py makemigrations` 
- `python manage.py migrate`.

## Running Tests

To run tests, use the following command:

`python manage.py test`

## Production

The microservice gets deployed with Github Actions.

To run the service in production:

1. Install kubectl*.
2. Install doctl*.
3. Add GitHub secrets for the environment variables.
4. Install Helm*.
5. Set up environment variables in the `values.yaml` file.
6. Install etcd*:
- `helm repo add bitnami https://charts.bitnami.com/bitnami`
- `helm repo update`
- `helm install etcd bitnami/etcd --namespace default`
- `$ROOT_PASSWORD = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl get secret --namespace default etcd -o jsonpath="{.data.etcd-root-password}")))`
- `kubectl run etcd-client --restart='Never' --image docker.io/bitnami/etcd:3.5.17-debian-12-r1 --env ROOT_PASSWORD=$ROOT_PASSWORD --env ETCDCTL_ENDPOINTS="etcd.default.svc.cluster.local:2379" --namespace default --command -- sleep infinity`
7. Set etcd environment variables.
8. Create a pull request to main branch or commit to main branch to trigger the deployment.

\* Only needed once per project (not required for every microservice).
