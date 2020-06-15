# PROJ
try:
    from . import __init__conf__
except ImportError:                 # pragma: no cover
    # imports for doctest
    import __init__conf__           # type: ignore  # pragma: no cover

__doc__ = """\

Usage:
    {shell_command} (-h | -v | -i)

Options:
    -h, --help          show help
    -v, --version       show version
    -i, --info          show Info

this module exposes no other useful functions to the commandline

""".format(shell_command=__init__conf__.shell_command)
