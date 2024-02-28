Logging Challenges with Subprocesses
------------------------------------

When `signals=False` is set, implementing logging within a subprocess poses challenges.
A new process does not inherit the main process's logger object, necessitating further development
for integration with the main process's logger via mechanisms like sockets or queues.

Utilizing `logger=logging.getLogger()` within the wrapped function results in the instantiation of a new Logger Object.
Configuring this Logger, especially for file logging from concurrent processes, presents complications as direct file
logging from multiple processes is generally unsupported.
A potential solution involves employing a SocketHandler coupled with a Receiver Thread to facilitate logging.

In the interim, it's necessary to initialize a separate logger within the decorated function for logging purposes.
It's crucial to remember that writing to the same logfile from multiple processes is not advisable.
While certain logging modules may offer solutions for concurrent logging, they require specific setup and configuration.
