import enum
import timeit
import dataclasses
from collections import namedtuple
from typing_extensions import TypedDict

a = 'foo'
b = 'bar'
c = 'baz'
a_list = ['l'] * 10000
a_tuple = tuple('t' for _ in range(10000))
a_dict = {i: i for i in range(10000)}

GLOBAL_VAR = "foo"

class GlobalClass:

    def __init__(self):
        self.var = "foo"

    def get_var(self):
        return self.var

global_object = GlobalClass()

class GlobalEnum(enum.Enum):
    var = "foo"

def global_method():
    return "foo"


def string_formatting():
    # a = 'foo'
    # b = 'bar'
    # c = 'baz'

    results = []
    t = timeit.timeit(lambda: "foo" + "bar" + "baz", number=1000000)
    print("Using + without vars:", t)

    t = timeit.timeit(lambda: a + b + c, number=1000000)
    print("Using +:", t)
    results.append(t)

    t = timeit.timeit(lambda: "".join([a, b, c]), number=1000000)
    print("Using join:",t)
    results.append(t)

    t = timeit.timeit(lambda: "%s%s%s" % (a, b, c), number=1000000)
    print("Using %s:",t)
    results.append(t)

    t = timeit.timeit(lambda: "{}{}{}".format(a, b, c), number=1000000)
    print("Using format:",t)
    results.append(t)

    t = timeit.timeit(lambda: f"{a}{b}{c}", number=1000000)
    print("Using formatted literals:",t)
    results.append(t)

    biggest_diff = min(results)/max(results)*100
    print(f"The fastest result is {biggest_diff}% the runtime of the slowest.")


def different_object_types():
    class TestObj:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c
    
    @dataclasses.dataclass
    class TestDataclass:
        a: str
        b: str
        c: str
    
    TestTuple = namedtuple('TestTuple', ['a', 'b', 'c'])

    print("\n\nInstantiating:")
    t = timeit.timeit(lambda: TestObj(a=a, b=b, c=c), number=1000000)
    print("Using class:",t)

    t = timeit.timeit(lambda: TestDataclass(a=a, b=b, c=c), number=1000000)
    print("Using dataclass:",t)

    t = timeit.timeit(lambda: (a, b, c), number=1000000)
    print("Using tuple:",t)

    t = timeit.timeit(lambda: TestTuple(a, b, c), number=1000000)
    print("Using namedtuple:",t)

    t = timeit.timeit(lambda: {"a": a, "b": b, "c": c}, number=1000000)
    print("Using dict:",t)

    print("\n\nAccessing data:")
    test_obj = TestObj(a=a, b=b, c=c)
    t = timeit.timeit(lambda: test_obj.a, number=1000000)
    print("Using class:",t)

    test_obj = TestDataclass(a=a, b=b, c=c)
    t = timeit.timeit(lambda: test_obj.a, number=1000000)
    print("Using dataclass:",t)

    test_tuple = (a, b, c)
    t = timeit.timeit(lambda: test_tuple[0], number=1000000)
    print("Using tuple:",t)

    test_tuple = TestTuple(a, b, c)
    t = timeit.timeit(lambda: test_tuple.a, number=1000000)
    print("Using namedtuple by attr:",t)

    test_tuple = TestTuple(a, b, c)
    t = timeit.timeit(lambda: test_tuple[0], number=1000000)
    print("Using namedtuple by index:",t)

    test_dict = {"a": a, "b": b, "c": c}
    t = timeit.timeit(lambda: test_dict["a"], number=1000000)
    print("Using dict:",t)


def bytes_vs_bytearray_vs_memoryview():
    a_str = 'a' * 10000
    b_str = 'b' * 10000
    a_bytes = b'a' * 10000
    b_bytes = b'b' * 10000
    a_array = bytearray(b'foo')
    b_array = bytearray(b'bar')
    a_memview = memoryview(b'foo')
    b_memview = memoryview(b'bar')


    t = timeit.timeit(lambda: a_bytes[-1], number=1000000)
    print("Accessing bytes:", t)

    t = timeit.timeit(lambda: a_str[-1], number=1000000)
    print("Accessing str:", t)

    t = timeit.timeit(lambda: a_array[-1], number=1000000)
    print("Accessing bytearrays:", t)

    t = timeit.timeit(lambda: a_memview[-1], number=1000000)
    print("Accessing memoryview:", t)

    t = timeit.timeit(lambda: a_bytes[1:], number=1000000)
    print("Slicing bytes:", t)

    t = timeit.timeit(lambda: a_str[1:], number=1000000)
    print("Slicing str:", t)

    t = timeit.timeit(lambda: a_array[1:], number=1000000)
    print("Slicing bytearrays:", t)

    t = timeit.timeit(lambda: a_memview[1:], number=1000000)
    print("Slicing memoryview:", t)

def lists_tuples_dicts():

    t = timeit.timeit(lambda: len(a_list), number=1000000)
    print("Length list:", t)

    t = timeit.timeit(lambda: len(a_tuple), number=1000000)
    print("Length tuple:", t)

    t = timeit.timeit(lambda: len(a_dict), number=1000000)
    print("Length dict:", t)

    t = timeit.timeit(lambda: a_list[888], number=1000000)
    print("Accessing list:", t)

    t = timeit.timeit(lambda: a_tuple[888], number=1000000)
    print("Accessing tuple:", t)

    t = timeit.timeit(lambda: a_dict[888], number=1000000)
    print("Accessing dict:", t)

    t = timeit.timeit(lambda: 888 in a_list, number=10000)
    print("Checking list:", t)

    t = timeit.timeit(lambda: 888 in a_tuple, number=10000)
    print("Checking tuple:", t)

    t = timeit.timeit(lambda: 888 in a_dict, number=10000)
    print("Checking dict:", t)

    t = timeit.timeit(lambda: [l for l in a_list], number=10000)
    print("Iterating list:", t)

    t = timeit.timeit(lambda: [t for t in a_tuple], number=10000)
    print("Iterating tuple:", t)

    t = timeit.timeit(lambda: [k for k in a_dict], number=10000)
    print("Iterating dict:", t)


empty_array = [0] * 10000

def _calculation(i):
    return i + i * 2

def _loop_a():
    new_array = []
    for i in range(1000):
        new_array.append(i + i * 2)
    return new_array

def _loop_b():
    new_array = []
    for i in range(1000):
        new_array.append(_calculation(i))
    return new_array

def _loop_c():
    for i in range(1000):
        empty_array[i] = i + i * 2
    return empty_array

def _loop_d():
    for i in range(1000):
        empty_array[i] = _calculation(i)
    return empty_array

def _loop_e():
    return [i + i * 2 for i in range(1000)]

def _loop_f():
    return [_calculation(i) for i in range(1000)]


def function_calls_and_loops():

    t = timeit.timeit(_loop_a, number=10000)
    print("Loop A:", t)

    t = timeit.timeit(_loop_b, number=10000)
    print("Loop B:", t)

    t = timeit.timeit(_loop_c, number=10000)
    print("Loop C:", t)

    t = timeit.timeit(_loop_d, number=10000)
    print("Loop D:", t)

    t = timeit.timeit(_loop_e, number=10000)
    print("Loop E:", t)

    t = timeit.timeit(_loop_f, number=10000)
    print("Loop F:", t)


def accessing_variables_and_attributes():
    local_var = "foo"

    def local_method():
        return "foo"

    class LocalClass:

        def __init__(self):
            self.var = "foo"

        def get_var(self):
            return self.var
    
    local_object = LocalClass()

    class LocalEnum(enum.Enum):
        var = "foo"
    
    t = timeit.timeit(lambda: "foo", number=1000000)
    print("Literal string:", t)

    t = timeit.timeit(lambda: local_var, number=1000000)
    print("Local variable:", t)

    t = timeit.timeit(lambda: local_method(), number=1000000)
    print("Local method:", t)

    t = timeit.timeit(lambda: local_object.var, number=1000000)
    print("Local object attribute:", t)

    t = timeit.timeit(lambda: local_object.get_var(), number=1000000)
    print("Local object method:", t)

    t = timeit.timeit(lambda: LocalEnum.var, number=1000000)
    print("Local class attr/enum:", t)

    t = timeit.timeit(lambda: GLOBAL_VAR, number=1000000)
    print("Global variable:", t)

    t = timeit.timeit(lambda: global_method(), number=1000000)
    print("Global method:", t)

    t = timeit.timeit(lambda: global_object.var, number=1000000)
    print("Global object attribute:", t)

    t = timeit.timeit(lambda: global_object.get_var(), number=1000000)
    print("Global object method:", t)

    t = timeit.timeit(lambda: GlobalEnum.var, number=1000000)
    print("Global class attr/enum:", t)

    


def _key_error_fail():
    try:
        a_dict[10000]
    except KeyError:
        a_dict[9999]

def _key_error_success():
    try:
        a_dict[9999]
    except KeyError:
        a_dict[8888]

def _key_check_fail():
    if 10000 in a_dict:
        a_dict[10000]
    else:
        a_dict[999]

def _key_check_success():
    if 9999 in a_dict:
        a_dict[9999]
    else:
        a_dict[8888]

def _key_get_fail():
    a_dict.get(10000, 9999)

def _key_get_success():
    a_dict.get(9999, 8888)

def _index_error_fail():
    try:
        a_list[10000]
    except IndexError:
        a_dict[9999]

def _index_error_success():
    try:
        a_list[9999]
    except IndexError:
        a_dict[8888]

def _index_check_success():
    if len(a_list) <= 10000:
        a_list[9999]
    else:
        a_list[10000]

def _index_check_fail():
    if len(a_list) <= 10001:
        a_list[10000]
    else:
        a_list[9999]

def checks_and_errors():
    t = timeit.timeit(_key_check_success, number=1000000)
    print("Dictionary key error passed:", t)

    t = timeit.timeit(_key_check_fail, number=1000000)
    print("Dictionary key error raised:", t)

    t = timeit.timeit(_key_check_success, number=1000000)
    print("Dictionary key check passed:", t)

    t = timeit.timeit(_key_check_fail, number=1000000)
    print("Dictionary key check failed:", t)

    t = timeit.timeit(_key_get_success, number=1000000)
    print("Dictionary key get passed:", t)

    t = timeit.timeit(_key_get_fail, number=1000000)
    print("Dictionary key get failed:", t)

    t = timeit.timeit(_index_error_success, number=1000000)
    print("List index error success:", t)

    t = timeit.timeit(_index_error_fail, number=1000000)
    print("List index error raised:", t)

    t = timeit.timeit(_index_check_success, number=1000000)
    print("List index check passed:", t)

    t = timeit.timeit(_index_check_success, number=1000000)
    print("List index check failed:", t)


_STATUS_CODE_DICT = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",
    110: "Response is Stale",
    111: "Revalidation Failed",
    112: "Disconnected Operation",
    113: "Heuristic Expiration",
    199: "Miscellaneous Warning",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    208: "Already Reported",
    214: "Transformation Applied",
    218: "This is fine",
    226: "IM Used",
    299: "Miscellaneous Persistent Warning",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect", 
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    419: "Page Expired",
    420: "Enhance Your Calm",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    430: "Request Header Fields Too Large",
    431: "Request Header Fields Too Large",
    440: "Login Time-out",
    444: "No Response",
    449: "Retry With",
    450: "Blocked by Windows Parental Controls",
    451: "Unavailable For Legal Reasons",
    494: "Request header too large",
    495: "SSL Certificate Error",
    496: "SSL Certificate Required",
    497: "HTTP Request Sent to HTTPS Port",
    498: "Invalid Token",
    499: "Token Required",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    509: "Bandwidth Limit Exceeded",
    510: "Not Extended",
    511: "Network Authentication Required",
    520: "Web Server Returned an Unknown Error",
    521: "Web Server Is Down",
    522: "Connection Timed Out",
    523: "Origin Is Unreachable",
    524: "A Timeout Occurred",
    525: "SSL Handshake Failed",
    526: "Invalid SSL Certificate",
    527: "Railgun Error",
    529: "Site is overloaded",
    530: "Site is frozen",
    561: "Unauthorized",
    598: "Network read timeout error",
    599: "Network Connect Timeout Error",
}

def _dict_conditional(status_code):
    return _STATUS_CODE_DICT[status_code]

_STATUS_CODE_LIST = [None] * 600
_STATUS_CODE_LIST[100] = "Continue",
_STATUS_CODE_LIST[101] = "Switching Protocols",
_STATUS_CODE_LIST[102] = "Processing",
_STATUS_CODE_LIST[103] = "Early Hints",
_STATUS_CODE_LIST[110] = "Response is Stale",
_STATUS_CODE_LIST[111] = "Revalidation Failed",
_STATUS_CODE_LIST[112] = "Disconnected Operation",
_STATUS_CODE_LIST[113] = "Heuristic Expiration",
_STATUS_CODE_LIST[199] = "Miscellaneous Warning",
_STATUS_CODE_LIST[200] = "OK",
_STATUS_CODE_LIST[201] = "Created",
_STATUS_CODE_LIST[202] = "Accepted",
_STATUS_CODE_LIST[203] = "Non-Authoritative Information",
_STATUS_CODE_LIST[204] = "No Content",
_STATUS_CODE_LIST[205] = "Reset Content",
_STATUS_CODE_LIST[206] = "Partial Content",
_STATUS_CODE_LIST[207] = "Multi-Status",
_STATUS_CODE_LIST[208] = "Already Reported",
_STATUS_CODE_LIST[214] = "Transformation Applied",
_STATUS_CODE_LIST[218] = "This is fine",
_STATUS_CODE_LIST[226] = "IM Used",
_STATUS_CODE_LIST[299] = "Miscellaneous Persistent Warning",
_STATUS_CODE_LIST[300] = "Multiple Choices",
_STATUS_CODE_LIST[301] = "Moved Permanently",
_STATUS_CODE_LIST[302] = "Found",
_STATUS_CODE_LIST[303] = "See Other",
_STATUS_CODE_LIST[304] = "Not Modified",
_STATUS_CODE_LIST[305] = "Use Proxy",
_STATUS_CODE_LIST[306] = "Switch Proxy",
_STATUS_CODE_LIST[307] = "Temporary Redirect",
_STATUS_CODE_LIST[308] = "Permanent Redirect", 
_STATUS_CODE_LIST[400] = "Bad Request",
_STATUS_CODE_LIST[401] = "Unauthorized",
_STATUS_CODE_LIST[402] = "Payment Required",
_STATUS_CODE_LIST[403] = "Forbidden",
_STATUS_CODE_LIST[404] = "Not Found",
_STATUS_CODE_LIST[405] = "Method Not Allowed",
_STATUS_CODE_LIST[406] = "Not Acceptable",
_STATUS_CODE_LIST[407] = "Proxy Authentication Required",
_STATUS_CODE_LIST[408] = "Request Timeout",
_STATUS_CODE_LIST[409] = "Conflict",
_STATUS_CODE_LIST[410] = "Gone",
_STATUS_CODE_LIST[411] = "Length Required",
_STATUS_CODE_LIST[412] = "Precondition Failed",
_STATUS_CODE_LIST[413] = "Payload Too Large",
_STATUS_CODE_LIST[414] = "URI Too Long",
_STATUS_CODE_LIST[415] = "Unsupported Media Type",
_STATUS_CODE_LIST[416] = "Range Not Satisfiable",
_STATUS_CODE_LIST[417] = "Expectation Failed",
_STATUS_CODE_LIST[418] = "I'm a teapot",
_STATUS_CODE_LIST[419] = "Page Expired",
_STATUS_CODE_LIST[420] = "Enhance Your Calm",
_STATUS_CODE_LIST[421] = "Misdirected Request",
_STATUS_CODE_LIST[422] = "Unprocessable Entity",
_STATUS_CODE_LIST[423] = "Locked",
_STATUS_CODE_LIST[424] = "Failed Dependency",
_STATUS_CODE_LIST[425] = "Too Early",
_STATUS_CODE_LIST[426] = "Upgrade Required",
_STATUS_CODE_LIST[428] = "Precondition Required",
_STATUS_CODE_LIST[429] = "Too Many Requests",
_STATUS_CODE_LIST[430] = "Request Header Fields Too Large",
_STATUS_CODE_LIST[431] = "Request Header Fields Too Large",
_STATUS_CODE_LIST[440] = "Login Time-out",
_STATUS_CODE_LIST[444] = "No Response",
_STATUS_CODE_LIST[449] = "Retry With",
_STATUS_CODE_LIST[450] = "Blocked by Windows Parental Controls",
_STATUS_CODE_LIST[451] = "Unavailable For Legal Reasons",
_STATUS_CODE_LIST[494] = "Request header too large",
_STATUS_CODE_LIST[495] = "SSL Certificate Error",
_STATUS_CODE_LIST[496] = "SSL Certificate Required",
_STATUS_CODE_LIST[497] = "HTTP Request Sent to HTTPS Port",
_STATUS_CODE_LIST[498] = "Invalid Token",
_STATUS_CODE_LIST[499] = "Token Required",
_STATUS_CODE_LIST[500] = "Internal Server Error",
_STATUS_CODE_LIST[501] = "Not Implemented",
_STATUS_CODE_LIST[502] = "Bad Gateway",
_STATUS_CODE_LIST[503] = "Service Unavailable",
_STATUS_CODE_LIST[504] = "Gateway Timeout",
_STATUS_CODE_LIST[505] = "HTTP Version Not Supported",
_STATUS_CODE_LIST[506] = "Variant Also Negotiates",
_STATUS_CODE_LIST[507] = "Insufficient Storage",
_STATUS_CODE_LIST[508] = "Loop Detected",
_STATUS_CODE_LIST[509] = "Bandwidth Limit Exceeded",
_STATUS_CODE_LIST[510] = "Not Extended",
_STATUS_CODE_LIST[511] = "Network Authentication Required",
_STATUS_CODE_LIST[520] = "Web Server Returned an Unknown Error",
_STATUS_CODE_LIST[521] = "Web Server Is Down",
_STATUS_CODE_LIST[522] = "Connection Timed Out",
_STATUS_CODE_LIST[523] = "Origin Is Unreachable",
_STATUS_CODE_LIST[524] = "A Timeout Occurred",
_STATUS_CODE_LIST[525] = "SSL Handshake Failed",
_STATUS_CODE_LIST[526] = "Invalid SSL Certificate",
_STATUS_CODE_LIST[527] = "Railgun Error",
_STATUS_CODE_LIST[529] = "Site is overloaded",
_STATUS_CODE_LIST[530] = "Site is frozen",
_STATUS_CODE_LIST[561] = "Unauthorized",
_STATUS_CODE_LIST[598] = "Network read timeout error",
_STATUS_CODE_LIST[599] = "Network Connect Timeout Error",

def _list_conditional(status_code):
    return _STATUS_CODE_LIST[status_code]

def _match_conditional(status_code):
    match status_code:
        case 100: return "Continue"
        case 101: return "Switching Protocols"
        case 102: return "Processing"
        case 103: return "Early Hints"
        case 110: return "Response is Stale"
        case 111: return "Revalidation Failed"
        case 112: return "Disconnected Operation"
        case 113: return "Heuristic Expiration"
        case 199: return "Miscellaneous Warning"
        case 200: return "OK"
        case 201: return "Created"
        case 202: return "Accepted"
        case 203: return "Non-Authoritative Information"
        case 204: return "No Content"
        case 205: return "Reset Content"
        case 206: return "Partial Content"
        case 207: return "Multi-Status"
        case 208: return "Already Reported"
        case 214: return "Transformation Applied"
        case 218: return "This is fine"
        case 226: return "IM Used"
        case 299: return "Miscellaneous Persistent Warning"
        case 300: return "Multiple Choices"
        case 301: return "Moved Permanently"
        case 302: return "Found"
        case 303: return "See Other"
        case 304: return "Not Modified"
        case 305: return "Use Proxy"
        case 306: return "Switch Proxy"
        case 307: return "Temporary Redirect"
        case 308: return "Permanent Redirect"
        case 400: return "Bad Request"
        case 401: return "Unauthorized"
        case 402: return "Payment Required"
        case 403: return "Forbidden"
        case 404: return "Not Found"
        case 405: return "Method Not Allowed"
        case 406: return "Not Acceptable"
        case 407: return "Proxy Authentication Required"
        case 408: return "Request Timeout"
        case 409: return "Conflict"
        case 410: return "Gone"
        case 411: return "Length Required"
        case 412: return "Precondition Failed"
        case 413: return "Payload Too Large"
        case 414: return "URI Too Long"
        case 415: return "Unsupported Media Type"
        case 416: return "Range Not Satisfiable"
        case 417: return "Expectation Failed"
        case 418: return "I'm a teapot"
        case 419: return "Page Expired"
        case 420: return "Enhance Your Calm"
        case 421: return "Misdirected Request"
        case 422: return "Unprocessable Entity"
        case 423: return "Locked"
        case 424: return "Failed Dependency"
        case 425: return "Too Early"
        case 426: return "Upgrade Required"
        case 428: return "Precondition Required"
        case 429: return "Too Many Requests"
        case 430: return "Request Header Fields Too Large"
        case 431: return "Request Header Fields Too Large"
        case 440: return "Login Time-out"
        case 444: return "No Response"
        case 449: return "Retry With"
        case 450: return "Blocked by Windows Parental Controls"
        case 451: return "Unavailable For Legal Reasons"
        case 494: return "Request header too large"
        case 495: return "SSL Certificate Error"
        case 496: return "SSL Certificate Required"
        case 497: return "HTTP Request Sent to HTTPS Port"
        case 498: return "Invalid Token"
        case 499: return "Token Required"
        case 500: return "Internal Server Error"
        case 501: return "Not Implemented"
        case 502: return "Bad Gateway"
        case 503: return "Service Unavailable"
        case 504: return "Gateway Timeout"
        case 505: return "HTTP Version Not Supported"
        case 506: return "Variant Also Negotiates"
        case 507: return "Insufficient Storage"
        case 508: return "Loop Detected"
        case 509: return "Bandwidth Limit Exceeded"
        case 510: return "Not Extended"
        case 511: return "Network Authentication Required"
        case 520: return "Web Server Returned an Unknown Error"
        case 521: return "Web Server Is Down"
        case 522: return "Connection Timed Out"
        case 523: return "Origin Is Unreachable"
        case 524: return "A Timeout Occurred"
        case 525: return "SSL Handshake Failed"
        case 526: return "Invalid SSL Certificate"
        case 527: return "Railgun Error"
        case 529: return "Site is overloaded"
        case 530: return "Site is frozen"
        case 561: return "Unauthorized"
        case 598: return "Network read timeout error"
        case 599: return "Network Connect Timeout Error"
    
def _if_conditional(status_code):
    if status_code == 100: return "Continue"
    if status_code == 101: return "Switching Protocols"
    if status_code == 102: return "Processing"
    if status_code == 103: return "Early Hints"
    if status_code == 110: return "Response is Stale"
    if status_code == 111: return "Revalidation Failed"
    if status_code == 112: return "Disconnected Operation"
    if status_code == 113: return "Heuristic Expiration"
    if status_code == 199: return "Miscellaneous Warning"
    if status_code == 200: return "OK"
    if status_code == 201: return "Created"
    if status_code == 202: return "Accepted"
    if status_code == 203: return "Non-Authoritative Information"
    if status_code == 204: return "No Content"
    if status_code == 205: return "Reset Content"
    if status_code == 206: return "Partial Content"
    if status_code == 207: return "Multi-Status"
    if status_code == 208: return "Already Reported"
    if status_code == 214: return "Transformation Applied"
    if status_code == 218: return "This is fine"
    if status_code == 226: return "IM Used"
    if status_code == 299: return "Miscellaneous Persistent Warning"
    if status_code == 300: return "Multiple Choices"
    if status_code == 301: return "Moved Permanently"
    if status_code == 302: return "Found"
    if status_code == 303: return "See Other"
    if status_code == 304: return "Not Modified"
    if status_code == 305: return "Use Proxy"
    if status_code == 306: return "Switch Proxy"
    if status_code == 307: return "Temporary Redirect"
    if status_code == 308: return "Permanent Redirect"
    if status_code == 400: return "Bad Request"
    if status_code == 401: return "Unauthorized"
    if status_code == 402: return "Payment Required"
    if status_code == 403: return "Forbidden"
    if status_code == 404: return "Not Found"
    if status_code == 405: return "Method Not Allowed"
    if status_code == 406: return "Not Acceptable"
    if status_code == 407: return "Proxy Authentication Required"
    if status_code == 408: return "Request Timeout"
    if status_code == 409: return "Conflict"
    if status_code == 410: return "Gone"
    if status_code == 411: return "Length Required"
    if status_code == 412: return "Precondition Failed"
    if status_code == 413: return "Payload Too Large"
    if status_code == 414: return "URI Too Long"
    if status_code == 415: return "Unsupported Media Type"
    if status_code == 416: return "Range Not Satisfiable"
    if status_code == 417: return "Expectation Failed"
    if status_code == 418: return "I'm a teapot"
    if status_code == 419: return "Page Expired"
    if status_code == 420: return "Enhance Your Calm"
    if status_code == 421: return "Misdirected Request"
    if status_code == 422: return "Unprocessable Entity"
    if status_code == 423: return "Locked"
    if status_code == 424: return "Failed Dependency"
    if status_code == 425: return "Too Early"
    if status_code == 426: return "Upgrade Required"
    if status_code == 428: return "Precondition Required"
    if status_code == 429: return "Too Many Requests"
    if status_code == 430: return "Request Header Fields Too Large"
    if status_code == 431: return "Request Header Fields Too Large"
    if status_code == 440: return "Login Time-out"
    if status_code == 444: return "No Response"
    if status_code == 449: return "Retry With"
    if status_code == 450: return "Blocked by Windows Parental Controls"
    if status_code == 451: return "Unavailable For Legal Reasons"
    if status_code == 494: return "Request header too large"
    if status_code == 495: return "SSL Certificate Error"
    if status_code == 496: return "SSL Certificate Required"
    if status_code == 497: return "HTTP Request Sent to HTTPS Port"
    if status_code == 498: return "Invalid Token"
    if status_code == 499: return "Token Required"
    if status_code == 500: return "Internal Server Error"
    if status_code == 501: return "Not Implemented"
    if status_code == 502: return "Bad Gateway"
    if status_code == 503: return "Service Unavailable"
    if status_code == 504: return "Gateway Timeout"
    if status_code == 505: return "HTTP Version Not Supported"
    if status_code == 506: return "Variant Also Negotiates"
    if status_code == 507: return "Insufficient Storage"
    if status_code == 508: return "Loop Detected"
    if status_code == 509: return "Bandwidth Limit Exceeded"
    if status_code == 510: return "Not Extended"
    if status_code == 511: return "Network Authentication Required"
    if status_code == 520: return "Web Server Returned an Unknown Error"
    if status_code == 521: return "Web Server Is Down"
    if status_code == 522: return "Connection Timed Out"
    if status_code == 523: return "Origin Is Unreachable"
    if status_code == 524: return "A Timeout Occurred"
    if status_code == 525: return "SSL Handshake Failed"
    if status_code == 526: return "Invalid SSL Certificate"
    if status_code == 527: return "Railgun Error"
    if status_code == 529: return "Site is overloaded"
    if status_code == 530: return "Site is frozen"
    if status_code == 561: return "Unauthorized"
    if status_code == 598: return "Network read timeout error"
    if status_code == 599: return "Network Connect Timeout Error"

def conditionals():
    t = timeit.timeit(lambda: _dict_conditional(100), number=100000)
    print("Dict for conditional status 100:", t)

    t = timeit.timeit(lambda: _list_conditional(100), number=100000)
    print("List for conditional status 100:", t)

    t = timeit.timeit(lambda: _if_conditional(100), number=100000)
    print("If for conditional status 100:", t)

    t = timeit.timeit(lambda: _match_conditional(100), number=100000)
    print("Match for conditional status 100:", t)


    t = timeit.timeit(lambda: _dict_conditional(300), number=100000)
    print("Dict for conditional status 300:", t)

    t = timeit.timeit(lambda: _list_conditional(300), number=100000)
    print("List for conditional status 300:", t)

    t = timeit.timeit(lambda: _if_conditional(300), number=100000)
    print("If for conditional status 300:", t)

    t = timeit.timeit(lambda: _match_conditional(300), number=100000)
    print("Match for conditional status 300:", t)


    t = timeit.timeit(lambda: _dict_conditional(599), number=100000)
    print("Dict for conditional status 599:", t)

    t = timeit.timeit(lambda: _list_conditional(599), number=100000)
    print("List for conditional status 599:", t)

    t = timeit.timeit(lambda: _if_conditional(599), number=100000)
    print("If for conditional status 599:", t)

    t = timeit.timeit(lambda: _match_conditional(599), number=100000)
    print("Match for conditional status 599:", t)




if __name__ == '__main__':
    string_formatting()
    #different_object_types()
    #bytes_vs_bytearray_vs_memoryview()
    #function_calls_and_loops()
    #lists_tuples_dicts()
    #accessing_variables_and_attributes()
    #checks_and_errors()
    #conditionals()
