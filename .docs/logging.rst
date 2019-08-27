when signals=False (on Windows), logging in the wrapped function can be tricky. Since a new process is
created, we can not use the logger object of the main process. Further development is needed to
connect to the main process logger via a socket or queue.

When the wrapped function is using logger=logging.getLogger(), a new Logger Object is created.
Setting up that Logger can be tricky (File Logging from two Processes is not supported ...)
I think I will use a socket to implement that (SocketHandler and some Receiver Thread)

Until then, You need to set up Your own new logger in the decorated function, if logging is needed.
Again - keep in mind that You can not write to the same logfile from different processes !
(although there are logging modules which can do that)