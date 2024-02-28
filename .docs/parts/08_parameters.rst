Parameters
----------

.. code-block::

    @timeout(dec_timeout, use_signals, timeout_exception, exception_message, dec_allow_eval, dec_hard_timeout, dec_mp_reset_signals)
    def decorated_function(*args, **kwargs):
        # interesting things happens here ...
        ...

    """
    dec_timeout         This parameter sets the timeout duration. It accepts a float, integer, or a string
                        that can be evaluated to a number if dec_allow_eval is enabled.
                        By default, there's no timeout (None). You can change the timeout dynamically
                        by passing a dec_timeout keyword argument to the decorated function.

    use_signals         This boolean parameter controls whether to use UNIX signals for implementing timeouts.
                        It's the most accurate method but comes with certain limitations,
                        such as being available only on Linux and macOS, and only in the main thread.
                        By default, signals are not used (False). It's typically not necessary to modify
                        this setting manually, but you can override it by passing a use_signals keyword argument
                        to the decorated function.

    timeout_exception   Specifies the exception to raise when a timeout occurs.
                        by default, it's set to TimeoutError
                        type: exception
                        default: TimeoutError

    exception_message   You can customize the message of the timeout exception.
                        The default message includes the name of the function and the timeout duration.
                        This message gets formatted with the actual values when a timeout occurs.
                        type: str
                        default : 'Function {function_name} timed out after {dec_timeout} seconds' (will be formatted)

    dec_allow_eval      When enabled (True), this boolean parameter allows the dec_timeout string to be evaluated dynamically.
                        It provides access to the decorated function (wrapped), the instance it belongs to (instance),
                        the positional arguments (args), and keyword arguments (kwargs).
                        It's disabled (False) by default for safety reasons but can be enabled by passing a dec_allow_eval
                        keyword argument to the decorated function.

                        instance    Example: 'instance.x' - see example above or doku
                        args        Example: 'args[0]' - the timeout is the first argument in args
                        kwargs      Example: 'kwargs["max_time"] * 2'
                        type: bool
                        default: false

    dec_hard_timeout    This boolean parameter is relevant when signals cannot be used,
                        necessitating the creation of a new process for the timeout mechanism.
                        Setting it to True means the timeout strictly applies to the execution time of the function,
                        potentially not allowing enough time for process creation.
                        With False, the process creation time is not included in the timeout, giving the actual function
                        the full duration to execute.
                        You can override this setting by passing a dec_hard_timeout keyword argument to the decorated function.
                        type: bool
                        default: false
                        can be overridden by passing the kwarg dec_hard_timeout to the decorated function*

    dec_mp_reset_signals  This parameter is relevant when using the "fork" start method for multiprocessing.
                        Setting it to True accomplishes two primary objectives:

                        - Restores Default Signal Handlers in Child Processes:
                            It ensures that child processes revert to the default signal handling behavior,
                            rather than inheriting signal handlers from the parent process.
                            This adjustment is crucial for applications utilizing frameworks like "unicorn" or "FastAPI",
                            facilitating the use of the efficient "fork" method while maintaining correct signal handling.
                            For more context, refer to the Discussion on
                            FastAPI GitHub page: https://github.com/tiangolo/fastapi/discussions/7442

                        - Avoids Inheritance of the File Descriptor (fd) for Wakeup Signals:
                            Typically, if the parent process utilizes a wakeup_fd, child processes inherit this descriptor.
                            Consequently, when a signal is sent to a child, it is also received by the parent process
                            via this shared socket, potentially leading to unintended termination or shutdown of the application.
                            By resetting signal handlers and not using the inherited fd, this parameter prevents such conflicts,
                            ensuring isolated and correct signal handling in child processes.

                        Note: This parameter exclusively affects processes initiated with the "fork" method
                        and is not applicable to other multiprocessing start methods.

    For enhanced isolation of subprocesses, consider utilizing the "forkserver" or "spawn" start methods in multiprocessing.
    These methods provide a greater degree of independence between the parent process and its children,
    mitigating the risks associated with shared resources and ensuring a cleaner execution environment for each subprocess,
    at the cost of slower startup times. This slowdown is due to the additional overhead involved in setting up a completely
    new process environment for each child process, as opposed to directly duplicating the parent process's environment,
    which occurs with the "fork" method.

    * that means the decorated_function must not use that kwarg itself, since this kwarg will be popped from the kwargs
    """
