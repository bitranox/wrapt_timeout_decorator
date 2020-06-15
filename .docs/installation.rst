Before You start, its highly recommended to update pip and setup tools:


.. code-block:: bash

    python3 -m pip --upgrade pip
    python3 -m pip --upgrade setuptools
    python3 -m pip --upgrade wheel


install latest version with pip (recommended):

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    python3 -m pip install --upgrade git+https://github.com/{repository_slug}.git --upgrade-strategy eager

    # test without installing (can be skipped)
    python3 -m pip install git+https://github.com/{repository_slug}.git --install-option test

    # normal install
    python3 -m pip install --upgrade git+https://github.com/{repository_slug}.git


install latest pypi Release (if there is any):

.. code-block:: bash

    # latest Release from pypi
    python3 -m pip install --upgrade {repository}

    # test without installing (can be skipped)
    python3 -m pip install {repository} --install-option test

    # normal install
    python3 -m pip install --upgrade {repository}



include it into Your requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi (if any):
    {repository}
    # for the latest Development Version :
    {repository} @ git+https://github.com/{repository_slug}.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python3 -m pip install --upgrade -r /<path>/requirements.txt


Install from source code:

.. code-block:: bash

    # cd ~
    $ git clone https://github.com/{repository_slug}.git
    $ cd {repository}

    # test without installing (can be skipped)
    python3 setup.py test

    # normal install
    python3 setup.py install


via makefile:

if You are on linux, makefiles are a very convenient way to install. Here we can do much more, like installing virtual environment, clean caches and so on.
This is still in development and not recommended / working at the moment:

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/{repository_slug}.git
    $ cd {repository}

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall
