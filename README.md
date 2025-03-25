# SwEng25_Group_23_IBM

### Docker 

Run and Build:

Please request the environment variable .env file from the developers before proceeding.

The following steps are written for Linux.

For Windows users please execute commands without "$ sudo" at the beginning.

Example, for Windows, "$ sudo command" becomes simply "command". 

Additionally, Windows users should also ensure that Docker Desktop is running on their machine. Docker can be downloaded here: https://www.docker.com/products/docker-desktop/

After executing the command, please navigate to http://localhost:3000 in your browser

```console
$ sudo docker compose up -d --build
```

Run without Build:

```console
$ sudo docker compose up -d
```

Run with errors:

```console
$ sudo docker compose up
```

Tests are Automatically Run in the CI/CD Pipeline here on GitLab!! (not currently on the main branch!)