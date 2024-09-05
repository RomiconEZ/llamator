..  _venv_setup:

Setup developer environment
============================

Setup Python virtual environment
++++++++++++++++++++++++++++++++++

There are a few ways to create virtual environment. To boostrap project it is the best to run:

    .. code:: bash

        $ . ./setup_dev_env.sh

or

    .. code:: bash

        $ source ./setup_dev_env.sh

This will create a single **venv** directory and install project-related packages.

.. warning:: This script works only in project root directory.

To activate the environment in your terminal just type:

    .. code:: bash

        $ source venv/bin/activate


Finalize environment
-----------------------
After completing above steps, you will have a virtual Python environment set up and almost ready to use.

.. warning:: Ensure you installed correct version of pytorch, torchvision and cudatoolkit for **your hardware configuration**. Refer to the official Pytorch guide.

To install project dependencies run:

.. code:: bash

    $ pip install -r requirements-dev.txt

It installs current package in edit mode, developer tools and so on.

