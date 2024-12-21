Measurements
============

The ``JII-MultispeQ`` package allows the direct connection to a MultispeQ using a python script, instead of using a 
separate application. In the following examples, it's shown how to connect to a MultispeQ, use protocols or commands
with the device and save the measurements to your local computer, as well as analyze them with custom functions and 
load them for a later analysis.

.. important:: 
   
   The ``JII-MultispeQ`` package is for local measurements. If the measurements are intended to be saved with a project
   online, use the PhotosynQ, Inc. Desktop or Mobile app.

Connect a MultispeQ
"""""""""""""""""""

Make sure your MultispeQ is powered on and connect it to your computer either using USB or Bluetooth®. After that, you have
to open the connection by selecting the Serial port the device is connected to. Depending on the operating system used, the
port names have different names.

.. list-table:: Basic Serial Port Names depending on the OS
   :widths: 30 35 35
   :header-rows: 1

   * - Operating system
     - USB
     - Bluetooth®
   * - Windows
     - COM…
     - COM…
   * - macOS
     - usbmodem…
     - Instrument-Name
   * - Linux
     - ACM…
     - Not tested

.. note:: Connecting a Device
   
   1. When connecting the device via USB, make sure the mirco-USB cable is designed for data transfer, not just charging.
   2. When using Bluetooth®, the required pairing code is ``1234``.

Available Ports
^^^^^^^^^^^^^^^

Use the :func:`~jii_multispeq.device.get_ports` to see the list of available ports on your
computer. Make sure to use the port, not just the name when selecting your device's port.

.. literalinclude:: _static/examples/python/local-device-ports.py
   :language: python
   :caption: *Example:* Get a list of available serial ports and connected devices.
   :linenos:
   :lines: 5-
   :name: local-get-ports-1

.. literalinclude:: _static/examples/python/output/local-device-ports.txt
   :language: bash
   :caption: *Example:* Output of the :func:`jii_multispeq.device.get_ports` function (on macOS).
   :name: local-get-ports-2

Establish a Connection
^^^^^^^^^^^^^^^^^^^^^^

Once the serial port is identified, use the following code to open the connection to your MultispeQ device.
The returned connection (:class:`serial.serialposix.Serial`) will be used with all other functions.

.. literalinclude:: _static/examples/python/local-device-command.py
   :language: python
   :caption: *Example:* Open a connection to a MultispeQ device.
   :linenos:
   :lines: 6-9
   :name: local-device-connect-1

Test the Connection
^^^^^^^^^^^^^^^^^^^

When the connection is established, it needs to be checked it the MultispeQ device is properly responding.
The :func:`~jii_multispeq.device.is_connected` checks if the connection is open and identifies the MultispeQ.

.. literalinclude:: _static/examples/python/local-device-command.py
   :language: python
   :caption: *Example:* Check if the connection is open and the MultispeQ is responding
   :linenos:
   :lines: 11-12
   :name: local-device-connect-2

....

Take a Measurement
""""""""""""""""""

If the MultispeQ device is connected and the connection is open, measurements can be run now.
The example below shows how a single relative Chlorophyll (SPAD) measurement can be taken.

.. literalinclude:: _static/examples/python/local-device-measurement.py
   :language: python
   :caption: *Example:* Take a SPAD measurement with the MultispeQ
   :linenos:
   :lines: 6-
   :name: local-device-measurement-1


.. literalinclude:: _static/examples/python/output/local-device-measurement.txt
   :language: bash
   :caption: *Example:* Output from a SPAD measurement with the MultispeQ
   :emphasize-lines: 11,13
   :name: local-device-measurement-2

Save Measurement to Disk
^^^^^^^^^^^^^^^^^^^^^^^^

The :func:`jii_multispeq.measurement.measure` allows to save the data from the MultispeQ
to the disk as well. The example below shows how to only return the data, setting the
filename to ``None`` or returning the data and saving the output to a file by specifying
the file name and a directory. If the filename is not set, or defined as ``auto``, a
filename is generated based on date and time. In case the directory is not set, files will
automatically saved to the ``./local`` directory.

If a defined directory doesn't exists it will be created. Files will not be overwritten,
to prevent data loss. In case a filename already exists, a number will be appended to the
filename.

.. code-block:: python
   :caption: *Example:* Take a SPAD measurement with the MultispeQ and save to disk
   :linenos:
   :emphasize-lines: 3,8,10
   :name: local-device-measurement-3

   ## Only return data
   data, crc32 = _measurement.measure( _connection, spad_protocol, 
                                     None, 
                                     'Single SPAD meaurement' )

   ## Save data to defined file and define directory 
   data, crc32 = _measurement.measure( _connection, spad_protocol, 
                                     "SPAD", 
                                     'Single SPAD meaurement',
                                     './chlorophyll-measurements' )

   ## Save data automatically
   data, crc32 = _measurement.measure( _connection, spad_protocol, 
                                     'Single SPAD meaurement' )

.. note:: Available Protocols

   The `JII-MultispeQ-Protocols <https://github.com/Jan-IngenHousz-Institute/JII-MultispeQ-Protocols>`_
   package provides preset protocols for the MultispeQ. In addition, it provides a validation function 
   for custom MultispeQ protocols, helping to identify potential issues with a protocol before running it.

Load Saved Measurement(s)
"""""""""""""""""""""""""

Saved measurement files can be loaded into a list of dictionaries (``list[dict]``) or they can be loaded
into a pandas dataframe.

File Summary
^^^^^^^^^^^^

It might be helpful to list files in the selected directory, to check what the content is without having to
open individual files using the :func:`~jii_multispeq.measurement.list_files` function of the 
:mod:`~jii_multispeq.measurement` module. The filenames, the date and time the measurement was saved and 
also the notes are listed by individual directories.

.. literalinclude:: _static/examples/python/local-files.py
   :language: python
   :caption: *Example:* View all the files in a directory including all sub-directories
   :linenos:
   :lines: 7,8,13,14
   :name: local-files-1

Load Files
^^^^^^^^^^^^^^^^^

.. literalinclude:: _static/examples/python/local-files.py
   :language: python
   :caption: *Example:* View all the files in a directory including all sub-directories
   :linenos:
   :lines: 7-8,16-18,22-23
   :name: local-files-2

Recursive Loading
^^^^^^^^^^^^^^^^^

.. literalinclude:: _static/examples/python/local-files.py
   :language: python
   :caption: *Example:* View all the files in a directory including all sub-directories
   :linenos:
   :lines: 19-20
   :name: local-files-3

.. code-block:: bash
   :caption: *Example:* Take a SPAD measurement with the MultispeQ and save to disk
   :emphasize-lines: 9-11
   :name: local-files-recursive-1

   MultispeQ/
   ├── local/
   │   ├── Measurement.json
   │   ├── Measurement - 1.json
   │   ├── Measurement - 2.json
   │   ├── Measurement - 3.json
   │   ├── Measurement - 4.json
   │   └── sub-directory/
   │       ├── Measurement.json
   │       ├── Measurement - 1.json
   │       └── Measurement - 2.json
   └── script.py

Process Data
^^^^^^^^^^^^

.. literalinclude:: _static/examples/python/local-files.py
   :language: python
   :caption: *Example:* View all the files in a directory including all sub-directories
   :linenos:
   :lines: 9-12,25-26
   :name: local-files-4

TL;DR
"""""

The following functions are available in the applications and probably more convinient to use.

Send a Command
^^^^^^^^^^^^^^

.. literalinclude:: _static/examples/python/local-device-command.py
   :language: python
   :caption: *Example:* Sending a command to a connected MultispeQ device.
   :linenos:
   :lines: 6-
   :emphasize-lines: 10,13
   :name: local-device-command-1
   
.. literalinclude:: _static/examples/python/output/local-device-command.json
   :language: json
   :caption: *Example:* Response from connected MultispeQ device for command ``print_memory``.
   :linenos:
   :name: local-device-command-2

Get Device Settings
^^^^^^^^^^^^^^^^^^^

The device's settings can be viewed using the ``print_memory`` command like in the example above, but there
is also a dedicated function for it. The code example below shows how to use this function.

In addition, the  :func:`~jii_multispeq.measurement.view` of the :mod:`~jii_multispeq.measurement` module is
used to print it out in a more convinient way.

.. literalinclude:: _static/examples/python/local-device-info.py
   :language: python
   :caption: *Example:* Getting the device settings from a connected MultispeQ device.
   :linenos:
   :lines: 6-
   :emphasize-lines: 2,11,14
   :name: local-device-info-1

.. literalinclude:: _static/examples/python/output/local-device-info.txt
   :language: bash
   :caption: *Example:* Settings from a connected MultispeQ device.
   :linenos:
   :name: local-device-info-2
