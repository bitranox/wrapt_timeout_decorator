remember that decorated functions (and their results !) needs to be pickable under Windows. In order to detect pickle problems You can use :

.. code-block:: py

    from wrapt_timeout_decorator import *
    # always remember that the "object_to_pickle" should not be defined within the main context
    detect_unpickable_objects(object_to_pickle, dill_trace=True)  # type: (Any, bool) -> Dict
