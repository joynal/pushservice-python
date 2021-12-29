# an app services (use cases as peadar calls them) are the procedural glue
# of the application. this means they wire together the IO with the business
# logic.
# For example a naive example might look something like this:

class MyService:
    def __init__(self, my_port):
        self.my_port


    def run(self, args):
        interim_data = pure_function_foo(args)
        io_data = my_port.get(interim_data)
        resulting_data = pure_function_bar(io_data)

        return result_data


