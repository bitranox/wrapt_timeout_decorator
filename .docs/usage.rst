- `Basic Usage`_
- `General Recommendations`_
- `use with Windows`_
    - `Quick Guide for the Eager`_
    - `In-Depth Explanation for the Curious`_
    - `Windows Compatibility Issue`_
    - `Timing Considerations`_
- `Considerations using Signals`_
- `Considerations using Subprocesses`_
    - `Overview`_
    - `Initialization`_
    - `Process Execution and Communication`_
    - `Subprocess Start Methods`_
    - `Choosing the Right Start Method`_
    - `Setting the Start Method`_
    - `Special Considerations for Uvicorn, FastAPI, asyncio`_
- `Handling Nested Timeouts`_
- `Custom Timeout Exception`_
- `Parameters`_
- `Override Parameters`_
- `Multithreading`_
- `Subprocess Monitoring`_
- `use as function not as decorator`_
- `Dynamic Timeout Value Adjustment with eval`_
- `Tools`_
    - `detect pickle errors`_
    - `set_subprocess_starting_method`_
- `Logging Challenges with Subprocesses`_
- `hard timeout`_
- `Understanding Timeout Durations Across Platforms`_
- `MYPY Testing`_

.. include:: ./parts/01_basic_usage.rst
.. include:: ./parts/02_general_recommendations.rst
.. include:: ./parts/03_use_with_windows.rst
.. include:: ./parts/04_considerations_using_signals.rst
.. include:: ./parts/05_considerations_using_subprocesses.rst
.. include:: ./parts/06_nested_timeouts.rst
.. include:: ./parts/07_custom_timeout_exception.rst
.. include:: ./parts/08_parameters.rst
.. include:: ./parts/09_override_parameters.rst
.. include:: ./parts/10_multithreading.rst
.. include:: ./parts/11_subprocess_monitoring.rst
.. include:: ./parts/12_use_as_function.rst
.. include:: ./parts/13_use_eval.rst
.. include:: ./parts/14_tools.rst
.. include:: ./parts/15_logging.rst
.. include:: ./parts/16_hard_timeout.rst


MYPY Testing
------------
for local MYPY Testing please make sure that the stub file "wrapt.pyi" is in in the MYPY Path (once!), in order to preserve the decorated function signature.


