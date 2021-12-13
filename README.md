# Introduction to Deep Learning Systems project

**Authors**: Maksim Eremeev (eremeev@nyu.edu), Anya Trivedi (anya.trivedi@nyu.edu), Anastasia Shaura (as15846@nyu.edu)

Brief description: https://www.overleaf.com/read/qqqcdqhndqdy

# VM setup

```bash
su -

git clone https://github.com/maks5507/idls.git

snap install docker

cd idls/
cd services/

docker pull rabbitmq:3.7.14-management
docker-compose up -d

cd backend/
docker-compose build
docker-compose up -d

cd ..
cd frontend
docker-compose build
docker-compose up -d

cd ..
docker-compose build
docker-compose up -d
```

## Codestyle check

Before making a pull-request, please check the coding style with bash script in `codestyle` directory. Make sure that your folder is included in `codestyle/pycodestyle_files.txt` list.

Your changes will not be approved if the script indicates any incongruities (this does not apply to 3rd-party code). 

Usage:

```bash
cd codestyle
sh check_code_style.sh
```