#!/bin/bash

echo "Creating the Purse Backend Application"

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

rm -rf /applications/purse_backend_$environment/
mkdir /applications/purse_backend_$environment/

echo "BUILDING FOR ENV $environment"

package_name=purse_backend_$environment
jenkins_proj_path="/var/lib/jenkins/workspace/$package_name"
JENKINS_VENV_DIR=$jenkins_proj_path/venv 

python -m venv $JENKINS_VENV_DIR
echo "VENV created"
. "${JENKINS_VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install -e $jenkins_proj_path .
pip install wheel
python setup.py bdist_wheel 
deactivate
echo "*** Purse Module Created***"

echo "Building the application"
application_build_path=/applications/purse_backend_$environment.tar
python -m venv /applications/purse_backend_$environment/venv
. "/applications/purse_backend_$environment/venv/bin/activate"
pip install --upgrade pip
pip install wheel
pip install /var/lib/jenkins/workspace/purse_backend_$environment/dist/purse_backend-0.1.0-py3-none-any.whl
echo "Application packages installed into Venv"

echo "Gzipping Application"
#tar -czf  "$package_name.tar" "/applications/$package_name/"
tar -czf /tmp/purse_backend_int.tar purse_backend_int/
