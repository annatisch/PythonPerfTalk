#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------
from collections import namedtuple
from enum import Enum

#: The IANA assigned port number for AMQP.The standard AMQP port number that has been assigned by IANA
#: for TCP, UDP, and SCTP.There are currently no UDP or SCTP mappings defined for AMQP.
#: The port number is reserved for future transport mappings to these protocols.
PORT = 5672


#: The IANA assigned port number for secure AMQP (amqps).The standard AMQP port number that has been assigned
#: by IANA for secure TCP using TLS. Implementations listening on this port should NOT expect a protocol
#: handshake before TLS is negotiated.
SECURE_PORT = 5671


MAJOR = 1  #: Major protocol version.
MINOR = 0  #: Minor protocol version.
REVISION = 0  #: Protocol revision.

TLS_MAJOR = 1  #: Major protocol version.
TLS_MINOR = 0  #: Minor protocol version.
TLS_REVISION = 0  #: Protocol revision.

SASL_MAJOR = 1  #: Major protocol version.
SASL_MINOR = 0  #: Minor protocol version.
SASL_REVISION = 0  #: Protocol revision.

#: The lower bound for the agreed maximum frame size (in bytes). During the initial Connection negotiation, the
#: two peers must agree upon a maximum frame size. This constant defines the minimum value to which the maximum
#: frame size can be set. By defining this value, the peers can guarantee that they can send frames of up to this
#: size until they have agreed a definitive maximum frame size for that Connection.
MIN_MAX_FRAME_SIZE = 512

INCOMING_WINDOW = 64 * 1024
OUTGOING_WIDNOW = 64 * 1024

DEFAULT_LINK_CREDIT = 10000

FIELD = namedtuple('field', 'name, type, mandatory, default, multiple')


class ConnectionState(Enum):
    #: In this state a Connection exists, but nothing has been sent or received. This is the state an
    #: implementation would be in immediately after performing a socket connect or socket accept.
    START = 0
    #: In this state the Connection header has been received from our peer, but we have not yet sent anything.
    HDR_RCVD = 1
    #: In this state the Connection header has been sent to our peer, but we have not yet received anything.
    HDR_SENT = 2
    #: In this state we have sent and received the Connection header, but we have not yet sent or
    #: received an open frame.
    HDR_EXCH = 3
    #: In this state we have sent both the Connection header and the open frame, but
    #: we have not yet received anything.
    OPEN_PIPE = 4
    #: In this state we have sent the Connection header, the open frame, any pipelined Connection traffic,
    #: and the close frame, but we have not yet received anything.
    OC_PIPE = 5
    #: In this state we have sent and received the Connection header, and received an open frame from
    #: our peer, but have not yet sent an open frame.
    OPEN_RCVD = 6
    #: In this state we have sent and received the Connection header, and sent an open frame to our peer,
    #: but have not yet received an open frame.
    OPEN_SENT = 7
    #: In this state we have send and received the Connection header, sent an open frame, any pipelined
    #: Connection traffic, and the close frame, but we have not yet received an open frame.
    CLOSE_PIPE = 8
    #: In this state the Connection header and the open frame have both been sent and received.
    OPENED = 9
    #: In this state we have received a close frame indicating that our partner has initiated a close.
    #: This means we will never have to read anything more from this Connection, however we can
    #: continue to write frames onto the Connection. If desired, an implementation could do a TCP half-close
    #: at this point to shutdown the read side of the Connection.
    CLOSE_RCVD = 10
    #: In this state we have sent a close frame to our partner. It is illegal to write anything more onto
    #: the Connection, however there may still be incoming frames. If desired, an implementation could do
    #: a TCP half-close at this point to shutdown the write side of the Connection.
    CLOSE_SENT = 11
    #: The DISCARDING state is a variant of the CLOSE_SENT state where the close is triggered by an error.
    #: In this case any incoming frames on the connection MUST be silently discarded until the peer's close
    #: frame is received.
    DISCARDING = 12
    #: In this state it is illegal for either endpoint to write anything more onto the Connection. The
    #: Connection may be safely closed and discarded.
    END = 13


class SessionState(Enum):
    #: In the UNMAPPED state, the Session endpoint is not mapped to any incoming or outgoing channels on the
    #: Connection endpoint. In this state an endpoint cannot send or receive frames.
    UNMAPPED = 0
    #: In the BEGIN_SENT state, the Session endpoint is assigned an outgoing channel number, but there is no entry
    #: in the incoming channel map. In this state the endpoint may send frames but cannot receive them.
    BEGIN_SENT = 1
    #: In the BEGIN_RCVD state, the Session endpoint has an entry in the incoming channel map, but has not yet
    #: been assigned an outgoing channel number. The endpoint may receive frames, but cannot send them.
    BEGIN_RCVD = 2
    #: In the MAPPED state, the Session endpoint has both an outgoing channel number and an entry in the incoming
    #: channel map. The endpoint may both send and receive frames.
    MAPPED = 3
    #: In the END_SENT state, the Session endpoint has an entry in the incoming channel map, but is no longer
    #: assigned an outgoing channel number. The endpoint may receive frames, but cannot send them.
    END_SENT = 4
    #: In the END_RCVD state, the Session endpoint is assigned an outgoing channel number, but there is no entry in
    #: the incoming channel map. The endpoint may send frames, but cannot receive them.
    END_RCVD = 5
    #: The DISCARDING state is a variant of the END_SENT state where the end is triggered by an error. In this
    #: case any incoming frames on the session MUST be silently discarded until the peer???s end frame is received.
    DISCARDING = 6


class SessionTransferState(Enum):

    Okay = 0
    Error = 1
    Busy = 2


class LinkDeliverySettleReason(Enum):

    DispositionReceived = 0
    Settled = 1
    NotDelivered = 2
    Timeout = 3
    Cancelled = 4


class LinkState(Enum):

    DETACHED = 0
    ATTACH_SENT = 1
    ATTACH_RCVD = 2
    ATTACHED = 3
    ERROR = 4