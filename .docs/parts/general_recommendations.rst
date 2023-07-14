General Recommendations
-----------------------
Minimize the excessive use of timeouts in your code and reserve their usage for essential cases.

Implement timeouts at the lowest possible abstraction level to prevent unintended
consequences such as exceptions being caught by unrelated code or non-pickable
functions and arguments.

Avoid incorporating the Timeout Decorator within a loop that iterates multiple times,
as this can result in considerable time overhead,
especially on Windows systems, when utilizing multiprocessing.

Whenever feasible, leverage the existing built-in timeouts already provided by the functions
and libraries you utilize. These built-in timeouts can handle most situations effectively.
Only resort to use this Timeout Decorator as a last resort when all other alternatives have been exhausted.


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
