#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from .amqptypes import AMQPTypes, FieldDefinition, ObjDefinition
from .constants import FIELD
from .performatives import Performative


class DeliveryState(Performative):
    """The Messaging layer deﬁnes a concrete set of delivery states which can be used (via the disposition frame)
    to indicate the state of the message at the receiver.

    Delivery states may be either terminal or non-terminal. Once a delivery reaches a terminal delivery-state,
    the state for that delivery will no longer change. A terminal delivery-state is referred to as an outcome.

    The following outcomes are formally deﬁned by the messaging layer to indicate the result of processing at the
    receiver:

        - accepted: indicates successful processing at the receiver
        - rejected: indicates an invalid and unprocessable message
        - released: indicates that the message was not (and will not be) processed
        - modified: indicates that the message was modiﬁed, but not processed

    The following non-terminal delivery-state is formally deﬁned by the messaging layer for use during link
    recovery to allow the sender to resume the transfer of a large message without retransmitting all the
    message data:

        - received: indicates partial message data seen by the receiver as well as the starting point for a
          resumed transfer

    """
    NAME = None
    CODE = None


class Received(DeliveryState):
    """At the target the received state indicates the furthest point in the payload of the message which the
    target will not need to have resent if the link is resumed. At the source the received state represents the
    earliest point in the payload which the Sender is able to resume transferring at in the case of link
    resumption. When resuming a delivery, if this state is set on the ﬁrst transfer performative it indicates
    the offset in the payload at which the ﬁrst resumed delivery is starting. The Sender MUST NOT send the
    received state on transfer or disposition performatives except on the ﬁrst transfer performative on a
    resumed delivery.

    :param int section_number:
        When sent by the Sender this indicates the ﬁrst section of the message (with sectionnumber 0 being the
        ﬁrst section) for which data can be resent. Data from sections prior to the given section cannot be
        retransmitted for this delivery. When sent by the Receiver this indicates the ﬁrst section of the message
        for which all data may not yet have been received.
    :param int section_offset:
        When sent by the Sender this indicates the ﬁrst byte of the encoded section data of the section given by
        section-number for which data can be resent (with section-oﬀset 0 being the ﬁrst byte). Bytes from the
        same section prior to the given oﬀset section cannot be retransmitted for this delivery. When sent by the
        Receiver this indicates the ﬁrst byte of the given section which has not yet been received. Note that if
        a receiver has received all of section number X (which contains N bytes of data), but none of section
        number X + 1, then it may indicate this by sending either Received(section-number=X, section-oﬀset=N) or
        Received(section-number=X+1, section-oﬀset=0). The state Received(sectionnumber=0, section-oﬀset=0)
        indicates that no message data at all has been transferred.
    """
    NAME = "RECEIVED"
    CODE = 0x00000023
    DEFINITION = (
        FIELD("section_number", AMQPTypes.uint, True, None, False),
        FIELD("section_offset", AMQPTypes.ulong, True, None, False)
    )


class Accepted(DeliveryState):
    """The accepted outcome.

    At the source the accepted state means that the message has been retired from the node, and transfer of
    payload data will not be able to be resumed if the link becomes suspended. A delivery may become accepted at
    the source even before all transfer frames have been sent, this does not imply that the remaining transfers
    for the delivery will not be sent - only the aborted ﬂag on the transfer performative can be used to indicate
    a premature termination of the transfer. At the target, the accepted outcome is used to indicate that an
    incoming Message has been successfully processed, and that the receiver of the Message is expecting the sender
    to transition the delivery to the accepted state at the source. The accepted outcome does not increment the
    delivery-count in the header of the accepted Message.
    """
    NAME = "ACCEPTED"
    CODE = 0x00000024
    DEFINITION = ()


class Rejected(DeliveryState):
    """The rejected outcome.

    At the target, the rejected outcome is used to indicate that an incoming Message is invalid and therefore
    unprocessable. The rejected outcome when applied to a Message will cause the delivery-count to be incremented
    in the header of the rejected Message. At the source, the rejected outcome means that the target has informed
    the source that the message was rejected, and the source has taken the required action. The delivery SHOULD
    NOT ever spontaneously attain the rejected state at the source.

    :param ~uamqp.error.AMQPError error: The error that caused the message to be rejected.
        The value supplied in this ﬁeld will be placed in the delivery-annotations of the rejected Message
        associated with the symbolic key ”rejected”.
    """
    NAME = "REJECTED"
    CODE = 0x00000025
    DEFINITION = (FIELD("error", ObjDefinition.error, False, None, False),)

    def __repr__(self):
        return "Rejected(error={})".format(self.error)

class Released(DeliveryState):
    """The released outcome.

    At the source the released outcome means that the message is no longer acquired by the receiver, and has been
    made available for (re-)delivery to the same or other targets receiving from the node. The message is unchanged
    at the node (i.e. the delivery-count of the header of the released Message MUST NOT be incremented).
    As released is a terminal outcome, transfer of payload data will not be able to be resumed if the link becomes
    suspended. A delivery may become released at the source even before all transfer frames have been sent, this
    does not imply that the remaining transfers for the delivery will not be sent. The source MAY spontaneously
    attain the released outcome for a Message (for example the source may implement some sort of time bound
    acquisition lock, after which the acquisition of a message at a node is revoked to allow for delivery to an
    alternative consumer).

    At the target, the released outcome is used to indicate that a given transfer was not and will not be acted upon.
    """
    NAME = "RELEASED"
    CODE = 0x00000026
    DEFINITION = ()


class Modified(DeliveryState):
    """The modiﬁed outcome.

    At the source the modiﬁed outcome means that the message is no longer acquired by the receiver, and has been
    made available for (re-)delivery to the same or other targets receiving from the node. The message has been
    changed at the node in the ways indicated by the ﬁelds of the outcome. As modiﬁed is a terminal outcome,
    transfer of payload data will not be able to be resumed if the link becomes suspended. A delivery may become
    modiﬁed at the source even before all transfer frames have been sent, this does not imply that the remaining
    transfers for the delivery will not be sent. The source MAY spontaneously attain the modiﬁed outcome for a
    Message (for example the source may implement some sort of time bound acquisition lock, after which the
    acquisition of a message at a node is revoked to allow for delivery to an alternative consumer with the
    message modiﬁed in some way to denote the previous failed, e.g. with delivery-failed set to true).
    At the target, the modiﬁed outcome is used to indicate that a given transfer was not and will not be acted
    upon, and that the message should be modiﬁed in the speciﬁed ways at the node.

    :param bool delivery_failed: Count the transfer as an unsuccessful delivery attempt.
        If the delivery-failed ﬂag is set, any Messages modiﬁed MUST have their deliverycount incremented.
    :param bool undeliverable_here: Prevent redelivery.
        If the undeliverable-here is set, then any Messages released MUST NOT be redelivered to the modifying
        Link Endpoint.
    :param dict message_annotations: Message attributes.
        Map containing attributes to combine with the existing message-annotations held in the Message's header
        section. Where the existing message-annotations of the Message contain an entry with the same key as an
        entry in this ﬁeld, the value in this ﬁeld associated with that key replaces the one in the existing
        headers; where the existing message-annotations has no such value, the value in this map is added.
    """
    NAME = "MODIFIED"
    CODE = 0x00000027
    DEFINITION = (
        FIELD('delivery_failed', AMQPTypes.boolean, False, None, False),
        FIELD('undeliverable_here', AMQPTypes.boolean, False, None, False),
        FIELD('message_annotations', FieldDefinition.fields, False, None, False)
    )