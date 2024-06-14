def run_test(func):
        def wrapper_func(self):
            print("\n=================================")
            print("Running " + func.__name__)
            func(self)
        return wrapper_func