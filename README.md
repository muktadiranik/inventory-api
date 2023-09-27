# DevXhub Inventory

#### **DevXhub Inventory Team AIS**


### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-    **Docker** Command For localy run 
    
         $ docker-compose -f local.yml build
         $ docker-compose -f local.yml up

-   Makemigrations and migrate

        $ docker-compose -f local.yml run --rm django python manage.py makemigrations
        $ docker-compose -f local.yml run --rm django python manage.py migrate
       
-   To create a **superuser**, use this command:

        $ docker-compose -f local.yml run --rm django python manage.py createsuperuser


-   Or  Create 3 User just a **sample** Command

        $ docker-compose -f local.yml run --rm django python manage.py sample



-   Create `Default Data` In single Command

        $ docker-compose -f local.yml run --rm django python manage.py loaddata data.json


For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check [here](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`


## Deployment
###### **Ansible for macOS**
- Install `ansible` using [Homebrew](https://brew.sh/)
```
brew install ansible
```
- Install required ansible rules
```
ansible-galaxy install -r ./ansible/requirements.yml
```
- Deploy the latest changes in production server
```
ansible-playbook -i ./ansible/hosts ./ansible/prod.yml -u devxhub
```
