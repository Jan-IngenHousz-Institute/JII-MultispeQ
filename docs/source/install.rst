Installation
============

First we must make sure we have the ``JII MultispeQ`` library installed:

.. code-block:: bash
  
    pip install git+https://github.com/JII/JII-MultispeQ.git --upgrade --no-cache-dir

Now you have all the tools available to download your ``Project`` data and information to get started.

.. important::
  `PhotosynQ Inc. <https://photosynq.inc>`_ is offering a library called `PhotosynQ-Python <https://github.com/Photosynq/PhotosynQ-Python>`_ which supports donwloading ``Project`` data and information as well. It is actually running in the background of this library.

  ``JII MultispeQ`` is providing more functionality, including saving data locally, so you don't have to download the ``Project`` every time or you can work offline. Also, it provides additional functions on viewing the Project's information and gives you access to the measurement ``Protocol`` and all the information related to your analysis.


Jupyter Notebooks
-----------------

The ``JII-MultispeQ`` library will work using a regular ``Python`` file you execute from your ``Terminal``, but most users will probably want to use a more interactive approach like `Jupyter Notebooks <https://jupyter.org/>`_.

Most convinently, ``Jupyter Notebooks`` can be used in combination with `Anaconda <https://anaconda.com/>`_ to manage ``packages`` and ``environments``. You have two options, using the Anaconda Distribution including a GUI (Graphical User Interface) or Miniconda (without the GUI to be used with the Terminal): `Download and Install <https://docs.anaconda.com/distro-or-miniconda/>`_.

Conda Environments
^^^^^^^^^^^^^^^^^^

With ``Conda`` it is beneficial, to use an ``environment`` when performing your data analysis.
This environment will contain all the libraries like ``JII MultispeQ`` including a specific version of ``Python``.
That way, you can keep exact track of all the dependencies needed for your analysis.

In case you want to share your work, you can export the ``environment`` as well, so the person you are sharing your work with can set it up 
on their computer, avoiding problems with different versions of the used libraries when setting everything up. Further, you don't have to explain,
which libraries need to be installed to run your analysis.

.. hint::
    Find the detailed documentation on `Environments` in the `Anaconda Documentation <https://docs.anaconda.com/working-with-conda/environments/>`_.

Miniconda (Terminal)
""""""""""""""""""""

When you are using ``Conda`` and you open a Terminal, you will most likely see a ``(base)`` in your command prompt. That is the currently active environment.
If it is not showing ``(base)`` or any other name, make sure to ``activate`` the environment, before installing any libraries.

To activate an ``environment`` use the following command:

.. code-block:: bash

    ## Activate the standard environment
    conda activate

    ## Activate a specific environment
    conda activate <environment name>


To deactivate an `environment` use the following command. You don't have to add the name of the current envrionment, since there is only one active `envrionment` at a time.

.. code-block:: bash

    conda deactivate

.. tip::
  By default, conda is loading the base environment. To remove this default behavior when opening a terminal, use:

  .. code-block:: bash

      conda config --set auto_activate_base false

Anaconda (GUI)
""""""""""""""

For how to use ``environments`` with Anaconda, please refer to the `official documentation <https://docs.anaconda.com/working-with-conda/environments/>`_.