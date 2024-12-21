Protocols
=========

If you have successfully downloaded the **data** and **information** for a Project you can now access the Protocol
used with the MultispeQ as well.

When you look at the Protoject's information in it's raw format, you will notice, the dictionary has two keys related
to the Protocols. It is important to understand the difference before working with them.

+ ``protocols`` contains a list with the protocols associated with the Project. It contains detailed information like the 
  Protocol's name, its author, the actual code, the macro to analyze the raw output, and much more.
+ ``protocol_json`` is on the same level as ``protocols`` and contains the actual protocol code sent to the MultispeQ.

.. important::
   Since ``protocol_json`` contains the actual code sent to the MultispeQ, it is strongly recommended to use for the 
   analysis as well. All the functions described below use this protocol code.

MultispeQ Protocols
-------------------

The code below is a recap from the previous example on how to access the protocol name and code.

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 8-22
   :emphasize-lines: 7
   :caption: *Example:* Get the protocol from the project information
   :name: protocol-data-tutorial-0

In contrast to the Project example, here we only define the ``projectId`` variable, assuming we already saved the
project's data & information locally.

.. important::

   There are actually multiple ways to get the protocol's name. The names are also used in the dataframe dictionary called
   ``df`` in this examle. To list the names you can also run the following code:

   .. code-block:: python
      :emphasize-lines: 2

      df, info = project.download( projectId=projectId )
      print( df.keys() )

Protocol Code
^^^^^^^^^^^^^

In the above example the variable ``protocol_code`` is created to contain the protocol's code from a project. Instead of
receiving the protocol code from a project, it can also simply be defined in a script.

.. code-block:: python
   :linenos:
   :caption: *Example:* Protocol defined instead of received from project information

   protocol_code = {
      # Protocol Instructions   
   }

In the subsequent examples the varibale ``protocol_code`` will be used to access the diffent components of the protocol 
which can be used in the data analysis.

Variable Arrays (``v_arrays``)
""""""""""""""""""""""""""""""

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 24-26
   :caption: examples/python/protocol-data.py
   :name: protocol-data-tutorial-1

Sub-Protocols
^^^^^^^^^^^^^

Most more complex protocols are devided up into sub-protocols within the ``_protocol_sets_`` key of the protocol code. The functions
below allow to access such sub-protocols.

Labels
""""""

Each sub-protocol can be identified by a label. The function :func:`~jii_multispeq.protocol.get_subprotocol_labels` returns a list of
labels for each sub-protocol. In case a sub-protocol has no ``label``, None is returned.

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 28-30
   :caption: *Example:* Get sub-protocol labels
   :name: protocol-data-tutorial-2

.. literalinclude:: _static/examples/python/output/protocol-data-tutorial-1.py
   :language: python
   :caption: *Output:* List of sub-protocol labels
   :name: protocol-data-tutorial-output-1

Sub-Protocol (by Label)
"""""""""""""""""""""""

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 32-34
   :caption: *Example:* Get sub-protocol by label name
   :name: protocol-data-tutorial-3

.. literalinclude:: _static/examples/python/output/protocol-data-tutorial-2.py
   :language: python
   :caption: *Output:* Sub-protocol as returned by label name
   :name: protocol-data-tutorial-output-2

.. important::
   The :func:`~jii_multispeq.protocol.get_subprotocols_by_label` function returns a list with dictionaries.

Sub-Protocol (by Index)
"""""""""""""""""""""""

The :func:`~jii_multispeq.protocol.get_subprotocol_by_index` function returns a single sub-protocol based on the index position.

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 36-38
   :caption: *Example:* Get sub-protocol by index position
   :name: protocol-data-tutorial-4

.. literalinclude:: _static/examples/python/output/protocol-data-tutorial-2.py
   :language: python
   :caption: *Output:* Sub-protocol as returned by index
   :name: protocol-data-tutorial-output-3

.. important::
   The :func:`~jii_multispeq.protocol.get_subprotocol_by_index` function returns a dictionary.

Project Protocol Example
------------------------

To summarize, this is the full example to get a protocol from the Project's information and extract different
information from it for an advanced data analysis.

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :caption: examples/python/protocol-data.py
   :name: protocol-data-tutorial-5

**Download:** :download:`python script [.py] <_static/examples/python/protocol-data.py>` :download:`Jupyter Notebook [.ipynb] <_static/examples/jupyter/protocol-data.ipynb>`

Local Protocols
---------------

When using the MultispeQ locally, it can be beneficial, to save the protocol and the accompanying analysis function in a separate file,
instead of copying the protocol into separate script files.

The suggested template contains a header for a detailed description, the protocol code (``_protocol``), the analysis function
(``_analyze``) and an example response from a MultispeQ (``_example``).

.. note:: **More Resources**

   More information on the available protocol commands and structure as well as protocols to use with the MultispeQ are available
   with the `JII-MultispeQ-Protocols <https://github.com/Jan-IngenHousz-Institute/JII-MultispeQ-Protocols>`_ package and the accompanying
   `Documentation - JII-MultispeQ-Protocols <https://jan-ingenhousz-institute.github.io/JII-MultispeQ-Protocols>`_.


Protocol File -  Template
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: _static/protocols/template.py
   :language: python
   :caption: Example file for protocol and analysis code
   :name: protocol-template

**Download:** :download:`Template [.py] <_static/protocols/template.py>` - Protocol Template
