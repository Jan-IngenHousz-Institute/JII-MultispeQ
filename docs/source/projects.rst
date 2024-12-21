Online - Projects
=================

The code below is an example on how to download the MultispeQ data collected for a project as well as the information about the project.

.. literalinclude:: _static/examples/python/project-data.py
   :language: python
   :linenos:
   :lines: 8,10-15
   :emphasize-lines: 3,4
   :caption: examples/python/project-data.py
   :name: project-data-tutorial-0

.. .. literalinclude:: examples/jupyter/project-data.jpynb
..    :language: python
..    :linenos:
..    :caption: examples/python/project-data.jpynb
..    :name: project-data

You start by importing the :mod:`~jii_multispeq.project` module from the ``JII-MultispeQ`` package as ``project``.

Next you create two variables ``email`` and ``projectId`` with the respective values relevant for your data analysis (highlighted rows).

The following step is using the :func:`~jii_multispeq.project.download` function from the :mod:`~jii_multispeq.project` module to download the MultispeQ data.
If you run the code for the first time, you will be prompted to enter your ``Password`` to authenticate and download the data.
When all data has been downloaded, two files will be generated in the same folder as your script that you are running. The next time you run
the scipt it will load the data from your local files instead of downloading them again.

You see that the :func:`~jii_multispeq.project.download` function returns two variables, ``df`` holding a list of dataframes 
(`Pandas <https://pandas.pydata.org/>`_) and the project information (``dict``)

*Example of files for a data analysis*::

   <your project directory>/
   ├── PhotosynQ_123.json     # Project Information
   ├── PhotosynQ_123.pickle   # Project Data (dataframes)
   └── <your script>.py       # can be a *.jpynb as well

.. important::

   If you want to share your analysis with somebody not signed up with `PhotosynQ <https://photosynq.org>`_, you can share the two data files together with your analysis.
   The analysis will require to sign again to download the data.
   
   **Pro-Tip:** You can use the code below to load data locally, if you provide data files and don't want to share your email address.

   .. code-block:: python

      df, info = project.download( projectId=projectId )


Project Information ``info``
----------------------------

In the previous example we use the :func:`~jii_multispeq.project.download` function to access and save the project's MultispeQ data and information. 
The functions below allow you to view the information about the project.

Meta Data
"""""""""

Using the :func:`~jii_multispeq.project.print_info` (alias: :func:`~jii_multispeq.project.show`) function of the :mod:`~jii_multispeq.project` module,
a summary can be printed to view the project's information.

.. literalinclude:: _static/examples/python/project-data.py
   :language: python
   :lines: 17,18
   :caption: View the information about the selected project
   :name: project-data-tutorial-1

.. literalinclude:: _static/examples/python/output/project-data-tutorial-1.txt
   :language: none
   :caption: **Output:** Information about the selected Project
   :name: project-data-tutorial-output-1

.. tip::
   If you would like to see the protocol code used by the MultispeQ as well, set the ``show_code`` variable to ``True``.

   .. code-block:: python

      project.print_info(info, True)

Protocol
""""""""

The information about the protocol used in the project is stored inside the ``info`` variable as well. In addition to the :mod:`~jii_multispeq.project` module,
also the :mod:`~jii_multispeq.protocol.` module is required.

.. literalinclude:: _static/examples/python/project-data.py
   :language: python
   :lines: 9,10,20-26
   :emphasize-lines: 1
   :caption: *Example:* Get the protocol name and code
   :name: project-data-tutorial-2

.. literalinclude:: _static/examples/python/output/project-data-tutorial-2.txt
   :language: none
   :caption: *Output:* Information about the selected Project
   :name: project-data-tutorial-output-2.1

.. note::
   The example assumes, that the project has only one protocol. In case your project has more than one protocol, a specific protocol
   can be selected adding the index position of the protocol to the function as well.

.. literalinclude:: _static/examples/python/output/project-data-tutorial-2.json
   :language: json
   :caption: *Output:* Information about the selected Project
   :name: project-data-tutorial-output-2.2

Project Data ``df``
-------------------

When collecting the protocol information, the protocol name was stored in the ``protocol_name`` variable. Now we can use the name to access the dataframe
by the protocol name from the ``df`` dictionary. In the example, there is only one dataframe inside the ``df`` dictionary.

.. literalinclude:: _static/examples/python/project-data.py
   :language: python
   :lines: 28-
   :caption: *Example:* Get a dataframe and it's information
   :name: project-data-tutorial-3

.. literalinclude:: _static/examples/python/output/project-data-tutorial-3.txt
   :language: none
   :caption: *Output:* Information about the selected dataframe
   :name: project-data-tutorial-output-3

.. note::
   Most of the time, there is only one dataframe inside the ``df`` dictionary. But Projects can have multiple Protocols as well as data
   that was added later on ("Custom Data"), which would be stored in a separate dataframe. You can use the code below to quickly check if
   there are multiple dataframes in your ``df`` dictionary.

   .. code-block:: python

      print( df.keys() )


Complete Example
----------------

To summarize, this is the full example to download MultispeQ data from a Project, view the Project's information,
get the Protocol's name and code and access the protocols dataframe.

.. literalinclude:: _static/examples/python/project-data.py
   :language: python
   :caption: examples/python/project-data.py
   :name: project-data-tutorial-4

**Download:** :download:`python script [.py] <_static/examples/python/project-data.py>` :download:`Jupyter Notebook [.ipynb] <_static/examples/jupyter/project-data.ipynb>`
