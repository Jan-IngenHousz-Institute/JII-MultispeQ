Getting Started
===============

If you have successfully installed the ``JII-MultispeQ`` library, you can start working with MultispeQ data. This includes
downloading and analyzing data from ``Project`` online, as well as taking measurements with the MultispeQ and using local data.

Projects (Online)
-----------------

To download and analyze a from online ``Projects`` you require their ``ID``. All you need to do is go to the project's page and
copy the ``Project ID`` from the menu on the left side. This ``ID`` can then be used with the :mod:`~jii_multispeq.project` 
module to download the project information and data for analysis.

.. important:: **User Account**

   To access MultispeQ data, you just need a `PhotosynQ, Inc. Account <https://photosynq.org>`_ and the project's ``ID``.

Measurements (Local)
--------------------

If you start an experiment on your local computer, you can use the :mod:`~jii_multispeq.device` and :mod:`~jii_multispeq.measurement`
modules to connect and control a MultispeQ and take measurements that get saved to your local drive.

.. important:: Local measurements can not be submitted to the online platform since the protocols and anlysis are not compatible!
