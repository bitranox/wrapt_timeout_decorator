Dynamic Timeout Value Adjustment with eval
------------------------------------------

The timeout value can be dynamically adjusted, calculated from other parameters or methods accessible via the eval function.
This capability is highly potent yet bears significant risks, especially when evaluating strings from UNTRUSTED sources.

.. caution::

   Utilizing eval with untrusted input is perilous.
   For an in-depth understanding, refer to `this article by Ned Batchelder <https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html>`_.

When activated, the ``dec_timeout`` function parameter,
or the value passed through the ``dec_timeout`` keyword argument (kwarg), will undergo evaluation if it's a string type.

Accessible objects within the eval context include:

- **wrapped**: Represents the decorated function and its attributes.

- **instance**: Accesses attributes of the class instance, e.g., ``'instance.x'`` refers to an attribute ``x`` of the instance.

- **args**: Refers to positional arguments, e.g., ``'args[0]'`` might be used to indicate the first argument is the timeout.

- **kwargs**: Accesses keyword arguments, e.g., ``'kwargs["max_time"] * 2'`` doubles the value of ``max_time``.

These elements underscore the feature's versatility but also highlight its potential hazards.
By default, ``allow_eval`` is turned off to mitigate risks.
However, it can be enabled to address specific use cases without altering the timeout decorator's core functionality.


.. code-block:: python

    # this example does NOT work on windows, please check the section
    # "use with Windows" in the README.rst
    def class FunnyMemes(object):
        def __init__(self,x):
            self.x=x

        @timeout('instance.x', dec_allow_eval=True)
        def swallow(self):
            while True:
                time.sleep(0.5)
                print('swallow')

        @timeout(1)
        def parrot(self):
            while True:
                time.sleep(0.5)
                print('parrot')

        @timeout(dec_timeout='args[0] + kwargs.pop("more_time",0)', dec_allow_eval=True)
        def knight(self,base_delay):
            while True:
                time.sleep(base_delay)
                print('knight')


    def main():
        my_memes = FunnyMemes(2)
        my_memes.swallow()                                                      # this will time out after 2 seconds
        my_memes.swallow(dec_timeout='instance.x * 2 + 1')                      # this will time out after 5 seconds
        my_memes.parrot(dec_timeout='instance.x * 2 + 1', dec_allow_eval=True)  # this will time out after 5 seconds
        my_memes.knight(1,more_time=4)                                          # this will time out after 5 seconds

    if __name__ == '__main__':
        main()
