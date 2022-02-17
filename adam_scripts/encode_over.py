import timeit

"""
from uamqp._encode import encode_payload, encode_payload_expanded
from uamqp.message import Message

output1 = bytearray()
output2 = bytearray()

encode_payload(output1, Message(data='test string value'))
encode_payload_expanded(output2, Message(data='test string value'))

assert output1 == output2
"""


def encode_message_playground(run_time):

    SETUP_CODE = '''
from uamqp._encode import encode_payload, encode_payload_expanded
from uamqp.message import Message
output = bytearray()
    '''

    TEST_CODE_UNOPTIMIZED = '''
encode_payload(output, Message(data='test string value'))
    '''
    unoptimized = timeit.timeit(TEST_CODE_UNOPTIMIZED, setup=SETUP_CODE, number=run_time)


    TEST_CODE_OPTIMIZED = '''
encode_payload_expanded(output, Message(data='test string value'))
    '''
    optimized = timeit.timeit(TEST_CODE_OPTIMIZED, setup=SETUP_CODE, number=run_time)

    print(
        'unoptimized: {}, optimized: {}, optimized - unoptimized: {}, optimized / unoptimized: {}'.format(
            unoptimized, optimized, optimized - unoptimized, optimized / unoptimized
        )
    )


encode_message_playground(run_time=1)
# encode_message_playground(run_time=1_00)
# encode_message_playground(run_time=10_000)
