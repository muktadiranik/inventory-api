# Ansible

## Initial server setup
```
ansible-playbook -i hosts -u root -l server setup.yml
```
## Encrypt secret credentials
```
ansible-vault encrypt vars/secret.yml
```
## Setup Nginx, Postgresql, SSL, etc
```
ansible-playbook --ask-vault-password -i ./hosts devxhub-inventory.yml -u devxhub
```
