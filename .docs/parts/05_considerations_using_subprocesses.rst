Considerations using Subprocesses
---------------------------------

Overview
--------
Subprocesses ares utilized by default to implement timeout functionality. This involves forking or spawning subprocesses, each with its own set of
considerations and caveats.

Initialization
--------------
- **Windows Considerations:** On Windows, the spawn method can significantly slow down the process initiation.
- **Main Context Protection:** It is crucial to protect the ``__main__`` context for compatibility, especially on Windows. See the "Usage with Windows" section for more details.
- **Pickle Requirements:** Function codes and arguments must be pickleable. To accommodate a wider range of types, `dill` is used for serialization.
- **Global Variables:** Access to global variables from a child process might not reflect the parent process's state at the time of the fork. Module-level constants are generally unaffected.

Process Execution and Communication
------------------------------------
- **Subprocess Execution:** Functions run in a separate subprocess, whether forked or spawned.
- **Data Transmission:** Parameters and results are communicated through pipes, with `dill` used for serialization.
- **Timeout Management:** Absent a result within the specified timeout, the subprocess is terminated using `SIGTERM`. Ensuring subprocesses can terminate safely is essential; thus, disabling the `SIGTERM` handler is not advisable.

Subprocess Start Methods
------------------------
- **Windows Limitation:** Only `spawn` is available on Windows.
- **Linux/Unix Options:** Options include `fork`, `forkserver`, and `spawn`.
    - **Fork:** Efficiently clones the parent process, including memory space, but may lead to issues with shared resources or in multi-threaded applications.
    - **Forkserver:** Starts a server at program launch, creating new processes upon request for better isolation but at a slower pace due to the server communication requirement.
    - **Spawn:** Initiates a fresh Python interpreter process, ensuring total independence at the cost of slower start-up due to the need for full initialization.

Choosing the Right Start Method
-------------------------------
- **fork** offers speed but can encounter issues with resource sharing or threading.
- **forkserver** enhances stability and isolation, ideal for applications requiring safety or managing unstable resources.
- **spawn** provides the highest level of isolation, recommended for a clean start and avoiding shared state complications.

Setting the Start Method
------------------------
Configure the start method with ``multiprocessing.set_start_method(method, force=False)``. This should be done cautiously, ideally once, and within the ``if __name__ == '__main__'`` block to prevent unintended effects.
Since we use ``multiprocess`` instead of ``multiprocessing``, we provide a method to set the starting method on both at the same time.
see : `set_subprocess_starting_method`_

Special Considerations for Uvicorn, FastAPI, asyncio
----------------------------------------------------
For Uvicorn or FastAPI applications, a specific approach to the `fork` method is recommended to ensure proper signal handling and isolation, facilitated by the `dec_mp_reset_signals` parameter. This design aims to reset signal handlers and manage file descriptors in child processes effectively.
You can set that by using the parameter `dec_mp_reset_signals`
