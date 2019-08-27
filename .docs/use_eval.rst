This is very powerful, but can be also very dangerous if you accept strings to evaluate from UNTRUSTED input.

read: https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html

If enabled, the parameter of the function dec_timeout, or the parameter passed by kwarg dec_timeout will
be evaluated if its type is string.

You can access :

- "wrapped"
   (the decorated function and his attributes)

- "instance"
   Example: 'instance.x' - an attribute of the instance of the class instance

- "args"
   Example: 'args[0]' - the timeout is the first argument in args

- "kwargs"
   Example: 'kwargs["max_time"] * 2'

- and of course all attributes You can think of - that makes it powerful but dangerous.
   by default allow_eval is disabled - but You can enable it in order to cover some edge cases without
   modifying the timeout decorator.


.. code-block:: py

    # this example does NOT work on windows, please check the section
    # "use with Windows" in the README.rst
    def class ClassTest4(object):
        def __init__(self,x):
            self.x=x

        @timeout('instance.x', dec_allow_eval=True)
        def test_method(self):
            print('swallow')

        @timeout(1)
        def foo3(self):
            print('parrot')

        @timeout(dec_timeout='args[0] + kwargs.pop("more_time",0)', dec_allow_eval=True)
        def foo4(self,base_delay):
            time.sleep(base_delay)
            print('knight')


    if __name__ == '__main__':
        # or override via kwarg :
        my_foo = ClassTest4(3)
        my_foo.test_method(dec_timeout='instance.x * 2.5 +1')
        my_foo.foo3(dec_timeout='instance.x * 2.5 +1', dec_allow_eval=True)
        my_foo.foo4(1,more_time=3)  # this will time out in 4 seconds