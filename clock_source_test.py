from clock_source import ClockSource
from asynctest import TestCase, main

class MockClockSource(ClockSource):
    def __init__(self, update_period):
        super().__init__(update_period)

    def start(self):
        pass

class TestClockSourceCanHandleCoroutinesAndRegularMethods(TestCase):
    async def my_coroutine(self):
        self.my_coroutine_called = True

    def regular_func(self):
        self.regular_func_called = True
    
    def setUp(self):
        self.clock_source = MockClockSource(22)
        self.clock_source.callbacks = [ self.my_coroutine, self.regular_func ]
        
    def runTest(self):
        self.clock_source._timer_callback()

        assert self.regular_func_called == True
        assert self.my_coroutine_called == True