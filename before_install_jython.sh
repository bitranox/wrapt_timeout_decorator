#!/bin/bash
# Copyright 2014 Bastian Bowe
#/home/travis/jython/Include
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

# pip install jip # hangs on Collecting chardet<3.1.0,>=3.0.2 (from requests->jip)
pip install jip==0.7
jip install $JYTHON
NON_GROUP_ID=${JYTHON#*:}
_JYTHON_BASENAME=${NON_GROUP_ID/:/-}
OLD_VIRTUAL_ENV=$VIRTUAL_ENV
java -jar $OLD_VIRTUAL_ENV/javalib/${_JYTHON_BASENAME}.jar -s -d $HOME/jython

BEFORE_PY_26=$($HOME/jython/bin/jython -c "import sys; print sys.version_info < (2, 6)")
if [ "$BEFORE_PY_26" == "True" ]
then
    # Travis CI virtualenv version is greater 1.9.1, which was the
    # last version compatible with Python < 2.6
    pip install virtualenv==1.9.1
fi

virtualenv --version
# --distribute is a workaround as setuptools don't install on Jython properly
virtualenv --distribute -p $HOME/jython/bin/jython $HOME/myvirtualenv

if [ "$BEFORE_PY_26" == "True" ]
then
    # No SSL support for Jython
    cat > $HOME/myvirtualenv/pip.conf <<EOF
[install]
insecure = true
EOF
    cat <<EOF >> $HOME/myvirtualenv/bin/activate
export PIP_CONFIG_FILE=$HOME/myvirtualenv/pip.conf
EOF
fi
