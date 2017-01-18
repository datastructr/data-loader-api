# Adding virtualenv to PATH
PATH=/usr/local/bin:$PATH
cd $WORKSPACE/

pyvenv --no-site-packages env
source env/bin/activate

pip install -r requirements.txt --download-cache=/tmp/$JOB_NAME

py.test
