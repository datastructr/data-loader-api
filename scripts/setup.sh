PATH=$WORKSPACE/env/bin:/usr/local/bin:$PATH
if [ ! -d "env" ]; then
        pyvenv env
fi
. env/bin/activate
pip install -r requirements.txt --download-cache=/tmp/$JOB_NAME
