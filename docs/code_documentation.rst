Code Documentation
==================

Main Functions
~~~~~~~~~~~~~~

.. autofunction:: llamator.start_testing
   :noindex:

.. note::

   This function starts the testing process with different configurations.

Abstract Classes
~~~~~~~~~~~~~~~~

.. autoclass:: llamator.ClientBase
   :undoc-members:

.. note::

   ClientBase is an abstract base class for client implementations.

.. autoclass:: llamator.TestBase
   :undoc-members:

.. note::

   TestBase is an abstract base class designed for attack handling in the testing framework.

Available Clients
~~~~~~~~~~~~~~~~~

.. autoclass:: llamator.ClientLangChain
   :undoc-members:
   :show-inheritance:
   :noindex:

.. note::

   ClientLangChain is a client implementation for LangChain-based services.

.. autoclass:: llamator.ClientOpenAI
   :undoc-members:
   :show-inheritance:
   :noindex:

.. note::

   ClientOpenAI is a client implementation for OpenAI-based services.
