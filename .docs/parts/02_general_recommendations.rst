General Recommendations
-----------------------
It is advised to limit the use of timeouts in your code, applying them only in critical situations.

Ensure that timeouts are implemented at the right granular level which is specific to Your application.

On one hand, this approach helps in avoiding undesired effects, such as exceptions being intercepted by unrelated segments of code,
or issues with non-pickable entities.

On the other hand, incorporating a Timeout Decorator within a repetitive loop should be avoided.
This practice can lead to significant delays, particularly on Windows platforms
due to the overhead associated with spawning subprocesses.

Preferably, make use of the native timeouts provided by the functions and libraries you are working with.
These built-in mechanisms typically suffice for most scenarios.
The Timeout Decorator should only be considered as a fallback option, after all other possibilities have been thoroughly explored.

Be aware that the isolation and performance of subprocesses can be very different, depending on the Platform (Windows or Linux) and the selected subprecess
start method. - see STARTMETHOD


It's recommended to minimize the utilization of timeouts in your programming, reserving them for truly essential instances.

Timers should be applied at an appropriate level of detail, tailored specifically to the needs of your application.
This precision aids in circumventing unwanted outcomes, such as the mishandling of exceptions by unrelated code sections
or complications with entities that cannot be pickled.

Conversely, it's prudent to refrain from embedding a Timeout Decorator within loops that execute multiple times.
Such an approach can induce notable delays, especially on Windows systems, owing to the additional burden of initiating subprocesses.

Where possible, opt for the timeout features natively available in the functions and libraries at your disposal.
These inherent capabilities are often adequate for the majority of use cases.
The implementation of a Timeout Decorator is best reserved as a measure of last resort,
subsequent to the exhaustive consideration of alternative strategies.

Additionally, be cognizant of the fact that the behavior and efficiency of subprocesses may vary significantly across platforms
(Windows versus Linux) and depending on the chosen method for subprocess initiation.
Refer to the documentation on STARTMETHOD for further details.


    BAD EXAMPLE (Pseudocode) - lets assume the write to the database fails sometimes for unknown reasons, and "hangs"

    .. code-block:: py

        # module file_analyzer
        import time
        from wrapt_timeout_decorator import *

        def read_the_file(filename):
            ...

        def analyze_the_file(filename):
            ...

        def write_to_database(file_content):
            ...


        @timeout(5)  # try to minimize the scope of the timeout
        def import_file(filename):
            file_content = read_the_file(filename)
            structured_data = analyze_the_file(file_content)
            write_to_database(structured_data)


    BETTER EXAMPLE (Pseudocode)

    .. code-block:: py

        # module file_analyzer
        import time
        from wrapt_timeout_decorator import *

        def read_the_file(filename):
            ...

        def analyze_the_file(filename):
            ...

        @timeout(5)     # better, because smaller scope
        def write_to_database(file_content):
            ...

        def import_file(filename):
            file_content = read_the_file(filename)
            structured_data = analyze_the_file(file_content)
            write_to_database(structured_data)
