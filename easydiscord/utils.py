from contextlib import contextmanager


@contextmanager
def _no_print(self):
    _print = self.print
    self.print = lambda *args, **kwargs: None
    yield
    self.print = _print
