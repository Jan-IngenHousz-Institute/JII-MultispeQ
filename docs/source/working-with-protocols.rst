Working with Protocols
======================

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

The MultispeQ Protocol
----------------------

The code below is a recap from the previous example on how to access the protocol name and code.

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 8-22
   :emphasize-lines: 7
   :caption: examples/python/protocol-data.py
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

In the above example the variable  ``protocol_code`` is created to contain the protocol's code. In the subsequent examples it will
be used to access the diffent components of the protocol which can be used in the data analysis.

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

List Labels
"""""""""""

Each sub-protocol can be identified by a label. The function :func:`~jii_multispeq.protocol.get_subprotocol_labels` returns a list of
labels for each sub-protocol. In case a sub-protocol has no ``label``, None is returned.

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 28-30
   :caption: examples/python/protocol-data.py
   :name: protocol-data-tutorial-2

.. literalinclude:: _static/examples/python/output/protocol-data-tutorial-1.py
   :language: python
   :caption: **Output:** List of protocol labels
   :name: protocol-data-tutorial-output-1

Sub-Protocol (by Label)
"""""""""""""""""""""""

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 32-34
   :caption: examples/python/protocol-data.py
   :name: protocol-data-tutorial-3

.. literalinclude:: _static/examples/python/output/protocol-data-tutorial-2.py
   :language: python
   :caption: **Output:** Sub-Protocol as returned by label name
   :name: protocol-data-tutorial-output-2

.. important::
   The :func:`~jii_multispeq.protocol.get_subprotocols_by_label` function returns a list with dictionaries.

Sub-Protocol (by Index)
"""""""""""""""""""""""

The :func:`~jii_multispeq.protocol.get_subprotocol_by_index` function returns a single sub-protocol based on the index position.

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :lines: 36-38
   :caption: examples/python/protocol-data.py
   :name: protocol-data-tutorial-4

.. literalinclude:: _static/examples/python/output/protocol-data-tutorial-2.py
   :language: python
   :caption: **Output:** Sub-Protocol as returned by index
   :name: protocol-data-tutorial-output-3

.. important::
   The :func:`~jii_multispeq.protocol.get_subprotocol_by_index` function returns a dictionary.

Full Example
^^^^^^^^^^^^

To summarize, this is the full example to get a protocol from the Project's information and extract different
information from it for an advanced data analysis.

.. literalinclude:: _static/examples/python/protocol-data.py
   :language: python
   :caption: examples/python/protocol-data.py
   :name: protocol-data-tutorial-5

Download Example: :download:`python script [.py] <_static/examples/python/protocol-data.py>` :download:`Jupyter Notebook [.ipynb] <_static/examples/jupyter/protocol-data.ipynb>`
