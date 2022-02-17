import timeit

"""
from uamqp._encode import encode_value, encode_value_by_method
from uamqp.types import AMQPTypes

output1 = bytearray()
output2 = bytearray()

encode_value_by_method(output1, {"TYPE": AMQPTypes.string, "VALUE": "test string value"})
encode_value(output2, {"TYPE": AMQPTypes.string, "VALUE": "test string value"})

assert output1 == output2
"""


def encode_primitive_playground(run_time):

    SETUP_CODE = '''
from uamqp._encode import encode_value, encode_value_by_method
from uamqp.types import AMQPTypes
output = bytearray()
    '''

    TEST_CODE_UNOPTIMIZED = '''
encode_value_by_method(output, {"TYPE": AMQPTypes.string, "VALUE": "test string value"})
    '''
    unoptimized = timeit.timeit(TEST_CODE_UNOPTIMIZED, setup=SETUP_CODE, number=run_time)

    TEST_CODE_OPTIMIZED = '''
encode_value(output, {"TYPE": AMQPTypes.string, "VALUE": "test string value"})
    '''
    optimized = timeit.timeit(TEST_CODE_OPTIMIZED, setup=SETUP_CODE, number=run_time)

    print(
        'unoptimized: {}, optimized: {}, optimized - unoptimized: {}, optimized / unoptimized: {}'.format(
            unoptimized, optimized, optimized - unoptimized, optimized / unoptimized
        )
    )


# encode_primitive_playground(run_time=1)
# encode_primitive_playground(run_time=10_000)
# encode_primitive_playground(run_time=1_000_000)
