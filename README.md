<a href="https://softserve.academy/"><img src=".github/logo.jpg" title="SoftServe IT Academy" alt="SoftServe IT Academy"></a>

# Repository Title Goes Here

> This project aims to facilitate the collaboration between startups and investors, providing a platform for them to discover and connect with each other. It serves as a business-to-business solution, enabling the exchange of information between startups and potential investors.

>  Business-to-business solution B2B

> Django backend serves, Custom Administrative Panel

**Badges will go here**

- build status
- coverage
- issues (waffle.io maybe)
- devDependencies
- npm package
- slack
- downloads
- gitter chat
- license
- etc.

[![Pending Pull-Requests](https://img.shields.io/github/issues-pr/ita-social-projects/Forum-Sandbox?style=flat-square)](https://github.com/mentorchita/PyForum/pulls)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- For more on these wonderful  badges, refer to <a href="#" target="_blank">#</a>.

---

## Table of Contents (Optional)

> If your `README` has a lot of info, section headers might be nice.

- [Repository Title Goes Here](#repository-title-goes-here)
  - [Table of Contents (Optional)](#table-of-contents-optional)
  - [Installation](#installation)
    - [Required to install](#required-to-install)
    - [Environment](#environment)
    - [Clone](#clone)
    - [Setup](#setup)
    - [How to run local](#how-to-run-local)
  - [Usage](#usage)
    - [How to work with swagger UI](#how-to-work-with-swagger-ui)
    - [How to run tests](#how-to-run-tests)
    - [How to Check](#how-to-check)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
    - [Git flow](#git-flow)
      - [Step 1](#step-1)
      - [Step 2](#step-2)
      - [Step 3](#step-3)
    - [Issue flow](#issue-flow)
   - [FAQ](#faq)
  - [Support](#support)
  - [License](#license)

---

## Installation

- All the `code` required to get started
- Images of what it should look like

### Required to install
* Python 3.9 or later
* PostgreSQL 14 or later
* Django 4.2.3
* NodeJS Frontend


### Environment
environmental variables
```properties
#db details
SECRET_KEY= key ...
PG_DB= forum
PG_USER= postgres
PG_PASSWORD= postgres
DB_HOST= localhost
DB_PORT= 5432
DB_PORT_OUT= 55432 # Check if there is a conflict with the setup on port 55432

#pgadmin user
PGADMIN_EMAIL: admin@admin.com
PGADMIN_PASSWORD: key ...

#SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST= someuser@gmail.com
EMAIL_PORT= 587
EMAIL_USE_TLS= 1
EMAIL_HOST_USER= test@test.com
EMAIL_HOST_PASSWORD= test-password

#origin hostnames allowed to make cross-site HTTP requests
CORS_ORIGIN_WHITELIST=
```

### Setup

- If you want more syntax highlighting, format your code like this:
- Localhost

> update and install this package first

```shell
$ pip install -r requirements.txt
```

> now install npm and bower packages

```shell
$ sudo apt update
$ sudo apt install nodejs
$ sudo apt install npm

```

In your settings.py, there is a list called ALLOWED_HOSTS. You need to add the IP address you see in the error to that list:
ALLOWED_HOSTS = ['XX.XX.XX.XX']
Note: only add the IP address, and not the port (e.g., 127.0.0.1 and not 127.0.0.1:8000)
For development, you can use the * wildcard to allow all hosts in settings.py:
ALLOWED_HOSTS = ['*']
Important
Modify this configuration when you deploy your app in production environment.

### How to run local
- Setup .env
> Setup .env
``` shell
SECRET_KEY= 'key ...'
PG_DB= forum
PG_USER= postgres
PG_PASSWORD= postgres
DB_HOST= localhost
DB_PORT= 5432
DB_PORT_OUT= 5432 # Check if there is a conflict with the setup on port 55432

#pgadmin user
PGADMIN_EMAIL: admin@admin.com
PGADMIN_PASSWORD: key ...

#SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST= someuser@gmail.com
EMAIL_PORT= 587
EMAIL_USE_TLS= 1
EMAIL_HOST_USER= test@test.com
EMAIL_HOST_PASSWORD= test-password

#origin hostnames allowed to make cross-site HTTP requests
CORS_ORIGIN_WHITELIST=
```
- User, run the local server on port localhost:8000
``` shell
$ psql -U postgres -d forum < dump_forum.sql
$ python manage.py runserver
or 
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser (custom_admin_panel_user)
$ python manage.py runserver
```

## Usage
### How to work with swagger UI
### How to run tests
- User, run test:
```shell
$ python manage.py test
```

### How to Check

You will see the following view after running the program using the specified path on port 8000:
![main page](.github/main_page.png)

When you try to log in, the following screen will appear:
![login screen](.github/login_page.png)

After logging in, the following screen will appear:
![logging](.github/logged_page.png)

Default user admin@admin.com  password: Password_1

## Documentation
- 🔃 Documentation <a href="https://github.com/mentorchita/PyForum/wiki" target="_blank">Forum-Sandbox/wiki</a>.

---

## Contributing

### Git flow
> To get started...
#### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine

#### Step 2

- **HACK AWAY!** 🔨🔨🔨

#### Step 3

- 🔃 Create a new pull request
### Issue flow

---

## FAQ

- **How do I do *specifically* so and so?**
    - No problem! Just do this.

---

## Support

Reach out to me at one of the following places!

- Website at <a href="#" target="_blank">`#`</a>
- Facebook at <a href="#" target="_blank">`#`</a>
- Insert more social links here.

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2024 © <a href="https://softserve.academy/" target="_blank"> SoftServe | Academy</a>.
