#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

# The messaging layer deﬁnes two concrete types (source and target) to be used as the source and target of a
# link. These types are supplied in the source and target ﬁelds of the attach frame when establishing or
# resuming link. The source is comprised of an address (which the container of the outgoing Link Endpoint will
# resolve to a Node within that container) coupled with properties which determine:
#
#   - which messages from the sending Node will be sent on the Link
#   - how sending the message affects the state of that message at the sending Node
#   - the behavior of Messages which have been transferred on the Link, but have not yet reached a
#     terminal state at the receiver, when the source is destroyed.

from enum import Enum

from .amqptypes import AMQPTypes, FieldDefinition, ObjDefinition
from .constants import FIELD
from .performatives import Performative


class TerminusDurability(Enum):
    #: No Terminus state is retained durably
    none = 0
    #: Only the existence and conﬁguration of the Terminus is retained durably.
    configuration = 1
    #: In addition to the existence and conﬁguration of the Terminus, the unsettled state for durable
    #: messages is retained durably.
    unsettled_state = 2


class ExpiryPolicy(Enum):
    #: The expiry timer starts when Terminus is detached.
    link_detach = b"link-detach"
    #: The expiry timer starts when the most recently associated session is ended.
    session_end = b"session-end"
    #: The expiry timer starts when most recently associated connection is closed.
    connection_close = b"connection-close"
    #: The Terminus never expires.
    never = b"never"


class DistributionMode(Enum):
    #: Once successfully transferred over the link, the message will no longer be available
    #: to other links from the same node.
    move = b'move'
    #: Once successfully transferred over the link, the message is still available for other
    #: links from the same node.
    copy = b'copy'


class LifeTimePolicy(Enum):
    #: Lifetime of dynamic node scoped to lifetime of link which caused creation.
    #: A node dynamically created with this lifetime policy will be deleted at the point that the link
    #: which caused its creation ceases to exist.
    delete_on_close = 0x0000002b
    #: Lifetime of dynamic node scoped to existence of links to the node.
    #: A node dynamically created with this lifetime policy will be deleted at the point that there remain
    #: no links for which the node is either the source or target.
    delete_on_no_links = 0x0000002c
    #: Lifetime of dynamic node scoped to existence of messages on the node.
    #: A node dynamically created with this lifetime policy will be deleted at the point that the link which
    #: caused its creation no longer exists and there remain no messages at the node.
    delete_on_no_messages = 0x0000002d
    #: Lifetime of node scoped to existence of messages on or links to the node.
    #: A node dynamically created with this lifetime policy will be deleted at the point that the there are no
    #: links which have this node as their source or target, and there remain no messages at the node.
    delete_on_no_links_or_messages = 0x0000002e


class SupportedOutcomes(object):
    #: Indicates successful processing at the receiver.
    accepted = b"amqp:accepted:list"
    #: Indicates an invalid and unprocessable message.
    rejected = b"amqp:rejected:list"
    #: Indicates that the message was not (and will not be) processed.
    released = b"amqp:released:list"
    #: Indicates that the message was modiﬁed, but not processed.
    modified = b"amqp:modified:list"


class ApacheFilters(object):
    #: Exact match on subject - analogous to legacy AMQP direct exchange bindings.
    legacy_amqp_direct_binding = b"apache.org:legacy-amqp-direct-binding:string"
    #: Pattern match on subject - analogous to legacy AMQP topic exchange bindings.
    legacy_amqp_topic_binding = b"apache.org:legacy-amqp-topic-binding:string"
    #: Matching on message headers - analogous to legacy AMQP headers exchange bindings.
    legacy_amqp_headers_binding = b"apache.org:legacy-amqp-headers-binding:map"
    #: Filter out messages sent from the same connection as the link is currently associated with.
    no_local_filter = b"apache.org:no-local-filter:list"
    #: SQL-based filtering syntax.
    selector_filter = b"apache.org:selector-filter:string"


class Source(Performative):
    """For containers which do not implement address resolution (and do not admit spontaneous link attachment
    from their partners) but are instead only used as producers of messages, it is unnecessary to provide
    spurious detail on the source. For this purpose it is possible to use a "minimal" source in which all the
    ﬁelds are left unset.

    :param str address: The address of the source.
        The address of the source MUST NOT be set when sent on a attach frame sent by the receiving Link Endpoint
        where the dynamic ﬂag is set to true (that is where the receiver is requesting the sender to create an
        addressable node). The address of the source MUST be set when sent on a attach frame sent by the sending
        Link Endpoint where the dynamic ﬂag is set to true (that is where the sender has created an addressable
        node at the request of the receiver and is now communicating the address of that created node).
        The generated name of the address SHOULD include the link name and the container-id of the remote container
        to allow for ease of identiﬁcation.
    :param ~uamqp.endpoints.TerminusDurability durable: Indicates the durability of the terminus.
        Indicates what state of the terminus will be retained durably: the state of durable messages, only
        existence and conﬁguration of the terminus, or no state at all.
    :param ~uamqp.endpoints.ExpiryPolicy expiry_policy: The expiry policy of the Source.
        Determines when the expiry timer of a Terminus starts counting down from the timeout value. If the link
        is subsequently re-attached before the Terminus is expired, then the count down is aborted. If the
        conditions for the terminus-expiry-policy are subsequently re-met, the expiry timer restarts from its
        originally conﬁgured timeout value.
    :param int timeout: Duration that an expiring Source will be retained in seconds.
        The Source starts expiring as indicated by the expiry-policy.
    :param bool dynamic: Request dynamic creation of a remote Node.
        When set to true by the receiving Link endpoint, this ﬁeld constitutes a request for the sending peer
        to dynamically create a Node at the source. In this case the address ﬁeld MUST NOT be set. When set to
        true by the sending Link Endpoint this ﬁeld indicates creation of a dynamically created Node. In this case
        the address ﬁeld will contain the address of the created Node. The generated address SHOULD include the
        Link name and Session-name or client-id in some recognizable form for ease of traceability.
    :param dict dynamic_node_properties: Properties of the dynamically created Node.
        If the dynamic ﬁeld is not set to true this ﬁeld must be left unset. When set by the receiving Link
        endpoint, this ﬁeld contains the desired properties of the Node the receiver wishes to be created. When
        set by the sending Link endpoint this ﬁeld contains the actual properties of the dynamically created node.
    :param uamqp.endpoints.DistributionMode distribution_mode: The distribution mode of the Link.
        This ﬁeld MUST be set by the sending end of the Link if the endpoint supports more than one
        distribution-mode. This ﬁeld MAY be set by the receiving end of the Link to indicate a preference when a
        Node supports multiple distribution modes.
    :param dict filters: A set of predicates to ﬁlter the Messages admitted onto the Link.
        The receiving endpoint sets its desired ﬁlter, the sending endpoint sets the ﬁlter actually in place
        (including any ﬁlters defaulted at the node). The receiving endpoint MUST check that the ﬁlter in place
        meets its needs and take responsibility for detaching if it does not.
         Common ﬁlter types, along with the capabilities they are associated with are registered
         here: http://www.amqp.org/specification/1.0/filters.
    :param ~uamqp.outcomes.DeliveryState default_outcome: Default outcome for unsettled transfers.
        Indicates the outcome to be used for transfers that have not reached a terminal state at the receiver
        when the transfer is settled, including when the Source is destroyed. The value MUST be a valid
        outcome (e.g. Released or Rejected).
    :param list(bytes) outcomes: Descriptors for the outcomes that can be chosen on this link.
        The values in this ﬁeld are the symbolic descriptors of the outcomes that can be chosen on this link.
        This ﬁeld MAY be empty, indicating that the default-outcome will be assumed for all message transfers
        (if the default-outcome is not set, and no outcomes are provided, then the accepted outcome must be
        supported by the source). When present, the values MUST be a symbolic descriptor of a valid outcome,
        e.g. "amqp:accepted:list".
    :param list(bytes) capabilities: The extension capabilities the sender supports/desires.
        See http://www.amqp.org/specification/1.0/source-capabilities.
    """
    NAME = "SOURCE"
    CODE = 0x00000028
    DEFINITION = (
        FIELD("address", AMQPTypes.string, False, None, False),
        FIELD("durable", FieldDefinition.terminus_durability, False, "none", False),
        FIELD("expiry_policy", FieldDefinition.expiry_policy, False, "session-end", False),
        FIELD("timeout", FieldDefinition.seconds, False, 0, False),
        FIELD("dynamic", AMQPTypes.boolean, False, False, False),
        FIELD("dynamic_node_properties", FieldDefinition.node_properties, False, None, False),
        FIELD("distribution_mode", FieldDefinition.distribution_mode, False, None, False),
        FIELD("filters", FieldDefinition.filter_set, False, None, False),
        FIELD("default_outcome", ObjDefinition.delivery_state, False, None, False),
        FIELD("outcomes", AMQPTypes.symbol, False, None, True),
        FIELD("capabilities", AMQPTypes.symbol, False, None, True),
    )

    def __repr__(self):
        return "Source({})".format(self.address)


class Target(Performative):
    """For containers which do not implement address resolution (and do not admit spontaneous link attachment
    from their partners) but are instead only used as consumers of messages, it is unnecessary to provide spurious
    detail on the source. For this purpose it is possible to use a 'minimal' target in which all the
    ﬁelds are left unset.

    :param str address: The address of the source.
        The address of the source MUST NOT be set when sent on a attach frame sent by the receiving Link Endpoint
        where the dynamic ﬂag is set to true (that is where the receiver is requesting the sender to create an
        addressable node). The address of the source MUST be set when sent on a attach frame sent by the sending
        Link Endpoint where the dynamic ﬂag is set to true (that is where the sender has created an addressable
        node at the request of the receiver and is now communicating the address of that created node).
        The generated name of the address SHOULD include the link name and the container-id of the remote container
        to allow for ease of identiﬁcation.
    :param ~uamqp.endpoints.TerminusDurability durable: Indicates the durability of the terminus.
        Indicates what state of the terminus will be retained durably: the state of durable messages, only
        existence and conﬁguration of the terminus, or no state at all.
    :param ~uamqp.endpoints.ExpiryPolicy expiry_policy: The expiry policy of the Source.
        Determines when the expiry timer of a Terminus starts counting down from the timeout value. If the link
        is subsequently re-attached before the Terminus is expired, then the count down is aborted. If the
        conditions for the terminus-expiry-policy are subsequently re-met, the expiry timer restarts from its
        originally conﬁgured timeout value.
    :param int timeout: Duration that an expiring Source will be retained in seconds.
        The Source starts expiring as indicated by the expiry-policy.
    :param bool dynamic: Request dynamic creation of a remote Node.
        When set to true by the receiving Link endpoint, this ﬁeld constitutes a request for the sending peer
        to dynamically create a Node at the source. In this case the address ﬁeld MUST NOT be set. When set to
        true by the sending Link Endpoint this ﬁeld indicates creation of a dynamically created Node. In this case
        the address ﬁeld will contain the address of the created Node. The generated address SHOULD include the
        Link name and Session-name or client-id in some recognizable form for ease of traceability.
    :param dict dynamic_node_properties: Properties of the dynamically created Node.
        If the dynamic ﬁeld is not set to true this ﬁeld must be left unset. When set by the receiving Link
        endpoint, this ﬁeld contains the desired properties of the Node the receiver wishes to be created. When
        set by the sending Link endpoint this ﬁeld contains the actual properties of the dynamically created node.
    :param list(bytes) capabilities: The extension capabilities the sender supports/desires.
        See http://www.amqp.org/specification/1.0/source-capabilities.
    """
    NAME = "TARGET"
    CODE = 0x00000029
    DEFINITION = (
        FIELD("address", AMQPTypes.string, False, None, False),
        FIELD("durable", FieldDefinition.terminus_durability, False, "none", False),
        FIELD("expiry_policy", FieldDefinition.expiry_policy, False, "session-end", False),
        FIELD("timeout", FieldDefinition.seconds, False, 0, False),
        FIELD("dynamic", AMQPTypes.boolean, False, False, False),
        FIELD("dynamic_node_properties", FieldDefinition.node_properties, False, None, False),
        FIELD("capabilities", AMQPTypes.symbol, False, None, True),
    )

    def __repr__(self):
        return "Target({})".format(self.address)