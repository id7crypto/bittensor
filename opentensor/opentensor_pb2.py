# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: opentensor/opentensor.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='opentensor/opentensor.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1bopentensor/opentensor.proto\"Y\n\tAxonBatch\x12\x0f\n\x07version\x18\x01 \x01(\x02\x12\x12\n\nneuron_key\x18\x02 \x01(\t\x12\x11\n\tsignature\x18\x03 \x01(\x0c\x12\x14\n\x05\x61xons\x18\x04 \x03(\x0b\x32\x05.Axon\"\xd1\x01\n\x04\x41xon\x12\x0f\n\x07version\x18\x01 \x01(\x02\x12\x12\n\nneuron_key\x18\x02 \x01(\t\x12\x11\n\tsignature\x18\x03 \x01(\x0c\x12\x12\n\nblock_hash\x18\x04 \x01(\x0c\x12\x15\n\rproof_of_work\x18\x05 \x01(\x0c\x12\x10\n\x08identity\x18\x06 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x07 \x01(\t\x12\x0c\n\x04port\x18\x08 \x01(\t\x12\x19\n\x05indef\x18\n \x01(\x0b\x32\n.TensorDef\x12\x1a\n\x06outdef\x18\x0b \x01(\x0b\x32\n.TensorDef\"\x97\x01\n\rTensorMessage\x12\x0f\n\x07version\x18\x01 \x01(\x02\x12\x12\n\nneuron_key\x18\x02 \x01(\t\x12\x11\n\tsource_id\x18\x03 \x01(\t\x12\x11\n\ttarget_id\x18\x04 \x01(\t\x12\x0e\n\x06nounce\x18\x05 \x01(\x0c\x12\x11\n\tsignature\x18\x06 \x01(\x0c\x12\x18\n\x07tensors\x18\x07 \x03(\x0b\x32\x07.Tensor\"8\n\x06Tensor\x12\x0e\n\x06\x62uffer\x18\x01 \x01(\x0c\x12\x1e\n\ntensor_def\x18\x02 \x01(\x0b\x32\n.TensorDef\"4\n\tTensorDef\x12\r\n\x05shape\x18\x02 \x03(\x03\x12\x18\n\x05\x64type\x18\x04 \x01(\x0e\x32\t.DataType*S\n\x08\x44\x61taType\x12\x0e\n\nDT_FLOAT32\x10\x00\x12\x0e\n\nDT_FLOAT64\x10\x01\x12\x0c\n\x08\x44T_INT32\x10\x02\x12\x0c\n\x08\x44T_INT64\x10\x03\x12\x0b\n\x07UNKNOWN\x10\x04\x32^\n\nOpentensor\x12\'\n\x03\x46wd\x12\x0e.TensorMessage\x1a\x0e.TensorMessage\"\x00\x12\'\n\x03\x42wd\x12\x0e.TensorMessage\x1a\x0e.TensorMessage\"\x00\x32/\n\tMetagraph\x12\"\n\x06Gossip\x12\n.AxonBatch\x1a\n.AxonBatch\"\x00\x62\x06proto3'
)

_DATATYPE = _descriptor.EnumDescriptor(
  name='DataType',
  full_name='DataType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DT_FLOAT32', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DT_FLOAT64', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DT_INT32', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DT_INT64', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=600,
  serialized_end=683,
)
_sym_db.RegisterEnumDescriptor(_DATATYPE)

DataType = enum_type_wrapper.EnumTypeWrapper(_DATATYPE)
DT_FLOAT32 = 0
DT_FLOAT64 = 1
DT_INT32 = 2
DT_INT64 = 3
UNKNOWN = 4



_AXONBATCH = _descriptor.Descriptor(
  name='AxonBatch',
  full_name='AxonBatch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='AxonBatch.version', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='neuron_key', full_name='AxonBatch.neuron_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature', full_name='AxonBatch.signature', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='axons', full_name='AxonBatch.axons', index=3,
      number=4, type=11, cpp_type=10, label=3,
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
  serialized_start=31,
  serialized_end=120,
)


_AXON = _descriptor.Descriptor(
  name='Axon',
  full_name='Axon',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='Axon.version', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='neuron_key', full_name='Axon.neuron_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature', full_name='Axon.signature', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='block_hash', full_name='Axon.block_hash', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='proof_of_work', full_name='Axon.proof_of_work', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='identity', full_name='Axon.identity', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='address', full_name='Axon.address', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='Axon.port', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='indef', full_name='Axon.indef', index=8,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='outdef', full_name='Axon.outdef', index=9,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=123,
  serialized_end=332,
)


_TENSORMESSAGE = _descriptor.Descriptor(
  name='TensorMessage',
  full_name='TensorMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='TensorMessage.version', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='neuron_key', full_name='TensorMessage.neuron_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source_id', full_name='TensorMessage.source_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='target_id', full_name='TensorMessage.target_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nounce', full_name='TensorMessage.nounce', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature', full_name='TensorMessage.signature', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tensors', full_name='TensorMessage.tensors', index=6,
      number=7, type=11, cpp_type=10, label=3,
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
  serialized_start=335,
  serialized_end=486,
)


_TENSOR = _descriptor.Descriptor(
  name='Tensor',
  full_name='Tensor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='buffer', full_name='Tensor.buffer', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tensor_def', full_name='Tensor.tensor_def', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=488,
  serialized_end=544,
)


_TENSORDEF = _descriptor.Descriptor(
  name='TensorDef',
  full_name='TensorDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='TensorDef.shape', index=0,
      number=2, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dtype', full_name='TensorDef.dtype', index=1,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=546,
  serialized_end=598,
)

_AXONBATCH.fields_by_name['axons'].message_type = _AXON
_AXON.fields_by_name['indef'].message_type = _TENSORDEF
_AXON.fields_by_name['outdef'].message_type = _TENSORDEF
_TENSORMESSAGE.fields_by_name['tensors'].message_type = _TENSOR
_TENSOR.fields_by_name['tensor_def'].message_type = _TENSORDEF
_TENSORDEF.fields_by_name['dtype'].enum_type = _DATATYPE
DESCRIPTOR.message_types_by_name['AxonBatch'] = _AXONBATCH
DESCRIPTOR.message_types_by_name['Axon'] = _AXON
DESCRIPTOR.message_types_by_name['TensorMessage'] = _TENSORMESSAGE
DESCRIPTOR.message_types_by_name['Tensor'] = _TENSOR
DESCRIPTOR.message_types_by_name['TensorDef'] = _TENSORDEF
DESCRIPTOR.enum_types_by_name['DataType'] = _DATATYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AxonBatch = _reflection.GeneratedProtocolMessageType('AxonBatch', (_message.Message,), {
  'DESCRIPTOR' : _AXONBATCH,
  '__module__' : 'opentensor.opentensor_pb2'
  # @@protoc_insertion_point(class_scope:AxonBatch)
  })
_sym_db.RegisterMessage(AxonBatch)

Axon = _reflection.GeneratedProtocolMessageType('Axon', (_message.Message,), {
  'DESCRIPTOR' : _AXON,
  '__module__' : 'opentensor.opentensor_pb2'
  # @@protoc_insertion_point(class_scope:Axon)
  })
_sym_db.RegisterMessage(Axon)

TensorMessage = _reflection.GeneratedProtocolMessageType('TensorMessage', (_message.Message,), {
  'DESCRIPTOR' : _TENSORMESSAGE,
  '__module__' : 'opentensor.opentensor_pb2'
  # @@protoc_insertion_point(class_scope:TensorMessage)
  })
_sym_db.RegisterMessage(TensorMessage)

Tensor = _reflection.GeneratedProtocolMessageType('Tensor', (_message.Message,), {
  'DESCRIPTOR' : _TENSOR,
  '__module__' : 'opentensor.opentensor_pb2'
  # @@protoc_insertion_point(class_scope:Tensor)
  })
_sym_db.RegisterMessage(Tensor)

TensorDef = _reflection.GeneratedProtocolMessageType('TensorDef', (_message.Message,), {
  'DESCRIPTOR' : _TENSORDEF,
  '__module__' : 'opentensor.opentensor_pb2'
  # @@protoc_insertion_point(class_scope:TensorDef)
  })
_sym_db.RegisterMessage(TensorDef)



_OPENTENSOR = _descriptor.ServiceDescriptor(
  name='Opentensor',
  full_name='Opentensor',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=685,
  serialized_end=779,
  methods=[
  _descriptor.MethodDescriptor(
    name='Fwd',
    full_name='Opentensor.Fwd',
    index=0,
    containing_service=None,
    input_type=_TENSORMESSAGE,
    output_type=_TENSORMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Bwd',
    full_name='Opentensor.Bwd',
    index=1,
    containing_service=None,
    input_type=_TENSORMESSAGE,
    output_type=_TENSORMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_OPENTENSOR)

DESCRIPTOR.services_by_name['Opentensor'] = _OPENTENSOR


_METAGRAPH = _descriptor.ServiceDescriptor(
  name='Metagraph',
  full_name='Metagraph',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=781,
  serialized_end=828,
  methods=[
  _descriptor.MethodDescriptor(
    name='Gossip',
    full_name='Metagraph.Gossip',
    index=0,
    containing_service=None,
    input_type=_AXONBATCH,
    output_type=_AXONBATCH,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_METAGRAPH)

DESCRIPTOR.services_by_name['Metagraph'] = _METAGRAPH

# @@protoc_insertion_point(module_scope)
