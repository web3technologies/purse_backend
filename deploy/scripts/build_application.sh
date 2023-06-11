#!/bin/bash

echo "Creating the purse_backend Application"

while getopts ":e:" opt; do
  case $opt in
    e)
      environment=$OPTARG
      ;;
    *)
      echo 'Error in command line parsing' >&2
      exit 1
  esac
done

if [ -z "$environment" ]; then
        echo 'Missing -e' >&2
        exit 1
fi

rm -rf /applications/purse_backend/
mkdir /applications/purse_backend/

echo "BUILDING"

workspace_name="purse_backend_${environment}"
jenkins_proj_path="/var/lib/jenkins/workspace/$workspace_name"
JENKINS_VENV_DIR=$jenkins_proj_path/venv 

python -m venv $JENKINS_VENV_DIR
echo "VENV created"
. "${JENKINS_VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install $jenkins_proj_path .
pip install wheel
python setup.py bdist_wheel 
deactivate
echo "*** Purse Backend Module Created***"

echo "Building the application"
application_build_path=/applications/purse_backend.tar
python -m venv /applications/purse_backend/venv
. "/applications/purse_backend/venv/bin/activate"
pip install --upgrade pip
pip install wheel
pip install $jenkins_proj_path/dist/purse_backend-0.1.0-py3-none-any.whl
cp $jenkins_proj_path/manage.py /applications/purse_backend/
cp $jenkins_proj_path/purse_backend/purse_backend/wsgi.py /applications/purse_backend/
cp "/var/lib/jenkins/envs/purse_backend_${environment}/.env" /applications/purse_backend/
echo "Application packages installed into Venv"

echo "Gzipping Application"
tar -czf /tmp/purse_backend.tar /applications/purse_backend/
