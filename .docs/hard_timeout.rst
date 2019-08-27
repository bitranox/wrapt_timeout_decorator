when use_signals = False (this is the only method available on Windows), the timeout function is realized by starting
another process and terminate that process after the given timeout.
Under Linux fork() of a new process is very fast, under Windows it might take some considerable time,
because the main context needs to be reloaded on spawn().
Spawning of a small module might take something like 0.5 seconds and more.

By default, when using signals=False, the timeout begins after the new process is created.

This means that the timeout given, is the time the decorated process is allowed to run, not included the time excluding the time to setup the process itself.
This is especially important if You use small timeout periods :

for Instance:


.. code-block:: py

    @timeout(0.1)
    def test():
        time.sleep(0.2)


the total time to timeout on linux with use_signals = False will be around 0.1 seconds, but on windows this can take
about 0.6 seconds: 0.5 seconds to spawn the new process, and giving the function test() 0.1 seconds to run !

If You need that a decorated function should timeout exactly** after the given timeout period, You can pass
the parameter dec_hard_timeout=True. in this case the called function will timeout exactly** after the given time,
no matter how long it took to spawn the process itself. In that case, if You set up the timeout too short,
the process might never run and will always timeout during spawning.

** well, more or less exactly - it still takes some short time to return from the spawned process - so be extra cautious on very short timeouts !
