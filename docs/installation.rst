From source code:

.. code-block:: bash

    # normal install
    python setup.py install
    # test without installing
    python setup.py test

via pip latest Release:

.. code-block:: bash

    # latest Release from pypi
    pip install {repository}

    # test without installing
    pip install {repository} --install-option test

via pip latest Development Version:

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    pip install --upgrade https://github.com/{repository_slug}/archive/master.zip --upgrade-strategy eager
    # normal install
    pip install --upgrade https://github.com/{repository_slug}/archive/master.zip
    # test without installing
    pip install https://github.com/{repository_slug}/archive/master.zip --install-option test

via requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release:
    {repository}
    # for the latest Development Version :
    https://github.com/{repository_slug}/archive/master.zip

    # to install and upgrade all modules mentioned in requirements.txt:
    pip install --upgrade -r /<path>/requirements.txt

via python:

.. code-block:: python

    # for the latest Release
    python -m pip install upgrade {repository}

    # for the latest Development Version
    python -m pip install upgrade https://github.com/{repository_slug}/archive/master.zip
