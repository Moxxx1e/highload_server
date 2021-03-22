def read_config(filename: str):
    cpu_limit = 4
    document_root = "/var/www/html"
    with open(filename, "r") as config_file:
        for line in config_file:
            split_line = line.split(" ")
            if split_line[0] == "cpu_limit":
                cpu_limit = int(split_line[1])

            if split_line[0] == "document_root":
                document_root = split_line[1].rstrip("\n")

    return cpu_limit, document_root


HOST = "0.0.0.0"
PORT = 80
CONFIG_FILE = "/etc/httpd.conf"

CPU_LIMIT, DOCUMENT_ROOT = read_config(CONFIG_FILE)
