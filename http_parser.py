class HttpParser:
    def __init__(self):
        self.method = ""
        self.path = ""

    def execute(self, request: bytes):
        request_str = request.decode()
        split_request = request_str.splitlines()

        try:
            first_string = split_request[0]
        except IndexError:
            first_string = ""
        self.method, self.path, _ = first_string.split(" ")

        query_param_index = self.path.find("?")
        if query_param_index > 0:
            self.path = self.path[:query_param_index]

    def get_method(self):
        return self.method

    def get_path(self):
        return self.path
