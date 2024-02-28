Subprocess Monitoring
---------------------

when using subprocesses, the subprocess is monitored if it is still alive.
if the subprocess was terminated or killed (for instance by OOMKiller),
``multiprocessing.context.ProcessError`` will be raised.
By default the subprocess is monitored every 5 seconds, but can be set with parameter
``dec_poll_subprocess``. polling can be turned off by setting to 0.0 seconds

.. include:: ../../tests/test_subprocess_alive_polling.py
    :code: python
    :start-after: # TestPolling{{{
    :end-before:  # TestPolling}}}
