General Recommendations
-----------------------
dont sprincle Your code with timeouts. Just use it were absolutely necessary, for instance when reading or writing a file. And do that on the lowest
abstraction level possible to avoid unwanted side effects (Exceptions caught by some other code, non pickable functions or arguments, and so on, but not TOO
low. Remember that forking the program takes some time (when use multiprocessing).

Most functions and libraries You call, they HAVE already some timeouts. use those. This Timeout Decorator should be only the last ressort, if everything else
fails.

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
