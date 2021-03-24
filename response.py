from response_messages import response_msg_dict
import datetime
from consts import CRLF

header_template = "{}: {}\r\n"
protocol = "HTTP/1.1"
headers = {
    'Server': 'Moxxx1e server',
    'Date': "",
    'Connection': 'Closed',
}


def build_headers(code: int) -> str:
    response = str.format("{} {} {}\r\n", protocol, code, response_msg_dict[code])
    for key in headers:
        if key == "Date":
            headers[key] = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        response += str.format(header_template, key, headers[key])
    return response


def build_bad_client_response(code: int) -> bytes:
    response = build_headers(code)
    return response.encode()


def build_ok_response(code: int, content_type: str, content_length: int) -> bytes:
    response = build_headers(code)
    response += str.format(header_template, 'Content-Type', content_type)
    response += str.format(header_template, 'Content-Length', content_length)
    response += CRLF

    return response.encode()
