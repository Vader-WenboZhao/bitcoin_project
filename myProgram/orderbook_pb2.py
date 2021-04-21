# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: orderbook.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='orderbook.proto',
  package='tutorial',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0forderbook.proto\x12\x08tutorial\"\xae\x02\n\tOrderbook\x12\x10\n\x08\x65xchange\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\r\n\x05nonce\x18\x03 \x01(\x03\x12\x11\n\ttimestamp\x18\x04 \x01(\x03\x12&\n\x04\x62ids\x18\x05 \x01(\x0b\x32\x18.tutorial.Orderbook.Bids\x12&\n\x04\x61sks\x18\x06 \x01(\x0b\x32\x18.tutorial.Orderbook.Asks\x1a%\n\x04Unit\x12\r\n\x05price\x18\x01 \x01(\x02\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x02\x1a\x32\n\x04\x42ids\x12*\n\x08\x62idUnits\x18\x01 \x03(\x0b\x32\x18.tutorial.Orderbook.Unit\x1a\x32\n\x04\x41sks\x12*\n\x08\x61skUnits\x18\x01 \x03(\x0b\x32\x18.tutorial.Orderbook.Unit\"\xb5\x01\n\nTradesInfo\x12*\n\x06trades\x18\x01 \x03(\x0b\x32\x1a.tutorial.TradesInfo.Trade\x1a{\n\x05Trade\x12\x10\n\x08\x65xchange\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\x10\n\x08\x64\x61tetime\x18\x04 \x01(\t\x12\x0c\n\x04side\x18\x05 \x01(\t\x12\r\n\x05price\x18\x06 \x01(\x02\x12\x0e\n\x06\x61mount\x18\x07 \x01(\x02\x62\x06proto3'
)




_ORDERBOOK_UNIT = _descriptor.Descriptor(
  name='Unit',
  full_name='tutorial.Orderbook.Unit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='price', full_name='tutorial.Orderbook.Unit.price', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='amount', full_name='tutorial.Orderbook.Unit.amount', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=191,
  serialized_end=228,
)

_ORDERBOOK_BIDS = _descriptor.Descriptor(
  name='Bids',
  full_name='tutorial.Orderbook.Bids',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bidUnits', full_name='tutorial.Orderbook.Bids.bidUnits', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=230,
  serialized_end=280,
)

_ORDERBOOK_ASKS = _descriptor.Descriptor(
  name='Asks',
  full_name='tutorial.Orderbook.Asks',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='askUnits', full_name='tutorial.Orderbook.Asks.askUnits', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=282,
  serialized_end=332,
)

_ORDERBOOK = _descriptor.Descriptor(
  name='Orderbook',
  full_name='tutorial.Orderbook',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='exchange', full_name='tutorial.Orderbook.exchange', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='symbol', full_name='tutorial.Orderbook.symbol', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nonce', full_name='tutorial.Orderbook.nonce', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='tutorial.Orderbook.timestamp', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bids', full_name='tutorial.Orderbook.bids', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='asks', full_name='tutorial.Orderbook.asks', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_ORDERBOOK_UNIT, _ORDERBOOK_BIDS, _ORDERBOOK_ASKS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=332,
)


_TRADESINFO_TRADE = _descriptor.Descriptor(
  name='Trade',
  full_name='tutorial.TradesInfo.Trade',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='exchange', full_name='tutorial.TradesInfo.Trade.exchange', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='symbol', full_name='tutorial.TradesInfo.Trade.symbol', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='tutorial.TradesInfo.Trade.timestamp', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='datetime', full_name='tutorial.TradesInfo.Trade.datetime', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='side', full_name='tutorial.TradesInfo.Trade.side', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='price', full_name='tutorial.TradesInfo.Trade.price', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='amount', full_name='tutorial.TradesInfo.Trade.amount', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=393,
  serialized_end=516,
)

_TRADESINFO = _descriptor.Descriptor(
  name='TradesInfo',
  full_name='tutorial.TradesInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='trades', full_name='tutorial.TradesInfo.trades', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TRADESINFO_TRADE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=335,
  serialized_end=516,
)

_ORDERBOOK_UNIT.containing_type = _ORDERBOOK
_ORDERBOOK_BIDS.fields_by_name['bidUnits'].message_type = _ORDERBOOK_UNIT
_ORDERBOOK_BIDS.containing_type = _ORDERBOOK
_ORDERBOOK_ASKS.fields_by_name['askUnits'].message_type = _ORDERBOOK_UNIT
_ORDERBOOK_ASKS.containing_type = _ORDERBOOK
_ORDERBOOK.fields_by_name['bids'].message_type = _ORDERBOOK_BIDS
_ORDERBOOK.fields_by_name['asks'].message_type = _ORDERBOOK_ASKS
_TRADESINFO_TRADE.containing_type = _TRADESINFO
_TRADESINFO.fields_by_name['trades'].message_type = _TRADESINFO_TRADE
DESCRIPTOR.message_types_by_name['Orderbook'] = _ORDERBOOK
DESCRIPTOR.message_types_by_name['TradesInfo'] = _TRADESINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Orderbook = _reflection.GeneratedProtocolMessageType('Orderbook', (_message.Message,), {

  'Unit' : _reflection.GeneratedProtocolMessageType('Unit', (_message.Message,), {
    'DESCRIPTOR' : _ORDERBOOK_UNIT,
    '__module__' : 'orderbook_pb2'
    # @@protoc_insertion_point(class_scope:tutorial.Orderbook.Unit)
    })
  ,

  'Bids' : _reflection.GeneratedProtocolMessageType('Bids', (_message.Message,), {
    'DESCRIPTOR' : _ORDERBOOK_BIDS,
    '__module__' : 'orderbook_pb2'
    # @@protoc_insertion_point(class_scope:tutorial.Orderbook.Bids)
    })
  ,

  'Asks' : _reflection.GeneratedProtocolMessageType('Asks', (_message.Message,), {
    'DESCRIPTOR' : _ORDERBOOK_ASKS,
    '__module__' : 'orderbook_pb2'
    # @@protoc_insertion_point(class_scope:tutorial.Orderbook.Asks)
    })
  ,
  'DESCRIPTOR' : _ORDERBOOK,
  '__module__' : 'orderbook_pb2'
  # @@protoc_insertion_point(class_scope:tutorial.Orderbook)
  })
_sym_db.RegisterMessage(Orderbook)
_sym_db.RegisterMessage(Orderbook.Unit)
_sym_db.RegisterMessage(Orderbook.Bids)
_sym_db.RegisterMessage(Orderbook.Asks)

TradesInfo = _reflection.GeneratedProtocolMessageType('TradesInfo', (_message.Message,), {

  'Trade' : _reflection.GeneratedProtocolMessageType('Trade', (_message.Message,), {
    'DESCRIPTOR' : _TRADESINFO_TRADE,
    '__module__' : 'orderbook_pb2'
    # @@protoc_insertion_point(class_scope:tutorial.TradesInfo.Trade)
    })
  ,
  'DESCRIPTOR' : _TRADESINFO,
  '__module__' : 'orderbook_pb2'
  # @@protoc_insertion_point(class_scope:tutorial.TradesInfo)
  })
_sym_db.RegisterMessage(TradesInfo)
_sym_db.RegisterMessage(TradesInfo.Trade)


# @@protoc_insertion_point(module_scope)
