Tools
-----

detect pickle errors
--------------------

Keep in mind that when employing subprocesses, both decorated functions and their return values must be pickleable.
To identify issues with pickling, you can utilize the ``detect_unpickable_objects`` function:

.. code-block:: python

    from wrapt_timeout_decorator import *
    detect_unpickable_objects(object_to_pickle, dill_trace=True)


set_subprocess_starting_method
------------------------------

Set the start Method for Subprocesses. Since we use multiprocess,
we set the starting method for multiprocess and multiprocessing to the same value.
we did not test what would happen if we set that to different values.

    - Windows Limitation: Only `spawn` is available on Windows.
    - Linux/Unix Options: Options include `fork`, `forkserver`, and `spawn`.
        - fork:       Efficiently clones the parent process, including memory space,
                      but may lead to issues with shared resources or in multi-threaded applications.
        - forkserver: Starts a server at program launch, creating new processes upon request
                      for better isolation but at a slower pace due to the server communication requirement.
        - spawn:      Initiates a fresh Python interpreter process, ensuring total independence
                      at the cost of slower start-up due to the need for full initialization.

    - Choosing the Right Start Method
        - fork          offers speed but can encounter issues with resource sharing or threading.
        - forkserver    enhances stability and isolation, ideal for applications requiring safety or managing unstable resources.
        - spawn         provides the highest level of isolation, recommended for a clean start and avoiding shared state complications.

    - Setting the Start Method
        Configure the start method with `set_subprocess_starting_method(method)`
        This should be done cautiously, ideally once, and within the `if __name__ == '__main__'` block to prevent unintended effects.

.. code-block:: python

    from wrapt_timeout_decorator import *
    set_subprocess_starting_method("forkserver")
