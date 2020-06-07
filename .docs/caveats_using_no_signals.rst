by default we use multiprocessing to archive the timeout function.

Basically this is done like that :

- the program is forked
    - on Windows hat might take a long time
    - the __main__ context needs to be guarded (see section usage with windows)
    - on windows the function code itself and all arguments need to be pickable (we use dill to offer more types here)
    - function parameters and function results needs to be pickable
    - Bear in mind that if code run in a child process tries to access a global variable,
      then the value it sees (if any) may not be the same as the value in
      the parent process at the time that process was called.
      However, global variables which are just module level constants cause no problems.

- the forked function is run in a subprocess
- parameters and results are passed via pipe (pickled, we use dill here)
- if there is no result within the timeout period, the forked process will be terminated with SIGTERM
    - the subprocess needs to be able to terminate, so You must not disable the SIGTERM Handler
