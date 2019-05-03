.. code-block:: py

    @timeout(dec_timeout, use_signals, timeout_exception, exception_message, dec_allow_eval, dec_hard_timeout)
    def decorated_function(*args, **kwargs):
        # interesting things happens here ...
        ...

    """
    dec_timeout         the timeout period in seconds, or a string that can be evaluated when dec_allow_eval = True
                        type: float, integer or string
                        default: None (no Timeout set)
                        can be overridden by passing the kwarg dec_timeout to the decorated function*

    use_signals         if to use signals (linux, osx) to realize the timeout. The most accurate and preferred method.
                        Please note that signals can only be used in the main thread and only on linux. In all other cases
                        (not the main thread, or under Windows) signals cant be used and will be disabled automatically.
                        In general You dont need to set use_signals Yourself - Signals are used when possible and disabled
                        if necessary.
                        type: boolean
                        default: True
                        can be overridden by passing the kwarg use_signals to the decorated function*

    timeout_exception   the Exception that will be raised if a timeout occurs.
                        type: exception
                        default: TimeoutError, on Python < 3.3: Assertion Error (since TimeoutError does not exist on that Python Versions)

    exception_message   custom Exception message.
                        type: str
                        default : 'Function {function_name} timed out after {dec_timeout} seconds' (will be formatted)

    dec_allow_eval      will allow to evaluate the parameter dec_timeout.
                        If enabled, the parameter of the function dec_timeout, or the parameter passed
                        by kwarg dec_timeout will be evaluated if its type is string. You can access :
                        wrapped (the decorated function object and all the exposed objects below)
                        instance    Example: 'instance.x' - see example above or doku
                        args        Example: 'args[0]' - the timeout is the first argument in args
                        kwargs      Example: 'kwargs["max_time"] * 2'
                        type: bool
                        default: false
                        can be overridden by passing the kwarg dec_allow_eval to the decorated function*

    dec_hard_timeout    only relevant when signals can not be used. In that case a new process needs to be created.
                        The creation of the process on windows might take 0.5 seconds and more, depending on the size
                        of the main module and modules to be imported. Especially useful for small timeout periods.

                        dec_hard_timeout = True : the decorated function will time out after dec_timeout, no matter what -
                        that means if You set 0.1 seconds here, the subprocess can not be created in that time and the
                        function will always time out and never run.

                        dec_hard_timeout = False : the decorated function will time out after the called function
                        is allowed to run for dec_timeout seconds. The time needed to create that process is not considered.
                        That means if You set 0.1 seconds here, and the time to create the subprocess is 0.5 seconds,
                        the decorated function will time out after 0.6 seconds in total, allowing the decorated function to run
                        for 0.1 seconds.

                        type: bool
                        default: false
                        can be overridden by passing the kwarg dec_hard_timeout to the decorated function*

    * that means the decorated_function must not use that kwarg itself, since this kwarg will be popped from the kwargs
    """
