hard timeout
------------

When employing subprocesses (which is the default behavior), the timeout functionality is achieved by initiating
a new subprocess and terminating it once the specified timeout period elapses.
The process creation speed varies significantly between operating systems.
On Linux, the ``fork()`` method allows rapid creation of a new process.
In contrast, on Windows, the ``spawn()`` method can introduce a noticeable delay due to the necessity of reloading the main context,
with spawning a small module potentially taking upwards of 0.5 seconds.

The timeout duration commences subsequent to the creation of the new process.
Consequently, the specified timeout reflects the period the decorated function is permitted to execute,
exclusive of the process setup time. This distinction is particularly vital for scenarios utilizing brief timeout intervals:

.. code-block:: py

    @timeout(0.1)
    def test():
        time.sleep(0.2)


Understanding Timeout Durations Across Platforms
------------------------------------------------

The implementation of timeouts, yields different total timeout durations on Linux (fork, forkserver) compared to Windows (spawn).
On Linux, the timeout process may for instance complete in approximately 0.1 seconds with "fork".
Conversely, on Windows, the total time to reach timeout could extend for instance to about 0.6 seconds,
comprising a 0.5-second delay to spawn a new process and then allowing 0.1 seconds for the function ``test()`` to execute.

To enforce a decorated function to timeout strictly after the specified timeout period,
you may use the ``dec_hard_timeout=True`` parameter.

With this setting, the targeted function will timeout precisely after the designated duration after start,
regardless of the process spawning time.
However, setting a very short timeout with this option may prevent the process from running at all,
resulting in an immediate timeout upon spawning.

.. note::

   The term "precisely" should be interpreted with a degree of flexibility.
   There remains a negligible delay in returning from the spawned process, making it imperative to approach very short timeouts with caution.
