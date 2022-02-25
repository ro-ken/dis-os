# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: task.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='task.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ntask.proto\"\x0c\n\nAIRequesst\"\x1b\n\x0cImageRequest\x12\x0b\n\x03img\x18\x01 \x01(\x0c\"1\n\x0bTaskRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\x05\x12\x11\n\ttask_name\x18\x02 \x01(\t\"\x1e\n\x0b\x43ommonReply\x12\x0f\n\x07success\x18\x01 \x01(\x08\"3\n\x0b\x46ileRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x11\n\tfile_data\x18\x02 \x01(\x0c\"C\n\x0fResourceRequest\x12\x13\n\x04\x61\x64\x64r\x18\x01 \x01(\x0b\x32\x05.Addr\x12\x1b\n\x08resource\x18\x02 \x01(\x0b\x32\t.Resource\" \n\x04\x41\x64\x64r\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"H\n\x08Resource\x12\x11\n\x03\x63pu\x18\x01 \x01(\x0b\x32\x04.CPU\x12\x14\n\x03mem\x18\x02 \x01(\x0b\x32\x07.Memory\x12\x13\n\x04\x64isc\x18\x03 \x01(\x0b\x32\x05.Disc\"=\n\x03\x43PU\x12\x11\n\tuse_ratio\x18\x01 \x01(\x02\x12\x10\n\x08real_num\x18\x02 \x01(\x05\x12\x11\n\tlogic_num\x18\x03 \x01(\x05\"8\n\x06Memory\x12\r\n\x05total\x18\x01 \x01(\x03\x12\x0c\n\x04used\x18\x02 \x01(\x03\x12\x11\n\tavailable\x18\x03 \x01(\x03\"6\n\x04\x44isc\x12\r\n\x05total\x18\x01 \x01(\x03\x12\x0c\n\x04used\x18\x02 \x01(\x03\x12\x11\n\tavailable\x18\x03 \x01(\x03\x32\xf0\x01\n\x0bTaskService\x12.\n\x0etask_service_1\x12\x0c.TaskRequest\x1a\x0c.CommonReply\"\x00\x12)\n\tsend_file\x12\x0c.FileRequest\x1a\x0c.CommonReply\"\x00\x12\x31\n\rsend_resource\x12\x10.ResourceRequest\x1a\x0c.CommonReply\"\x00\x12+\n\nsend_image\x12\r.ImageRequest\x1a\x0c.CommonReply\"\x00\x12&\n\x07send_ai\x12\x0b.AIRequesst\x1a\x0c.CommonReply\"\x00\x62\x06proto3'
)




_AIREQUESST = _descriptor.Descriptor(
  name='AIRequesst',
  full_name='AIRequesst',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=14,
  serialized_end=26,
)


_IMAGEREQUEST = _descriptor.Descriptor(
  name='ImageRequest',
  full_name='ImageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='img', full_name='ImageRequest.img', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=28,
  serialized_end=55,
)


_TASKREQUEST = _descriptor.Descriptor(
  name='TaskRequest',
  full_name='TaskRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='TaskRequest.task_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_name', full_name='TaskRequest.task_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=57,
  serialized_end=106,
)


_COMMONREPLY = _descriptor.Descriptor(
  name='CommonReply',
  full_name='CommonReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='CommonReply.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=108,
  serialized_end=138,
)


_FILEREQUEST = _descriptor.Descriptor(
  name='FileRequest',
  full_name='FileRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_name', full_name='FileRequest.file_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_data', full_name='FileRequest.file_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=140,
  serialized_end=191,
)


_RESOURCEREQUEST = _descriptor.Descriptor(
  name='ResourceRequest',
  full_name='ResourceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='addr', full_name='ResourceRequest.addr', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource', full_name='ResourceRequest.resource', index=1,
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
  serialized_start=193,
  serialized_end=260,
)


_ADDR = _descriptor.Descriptor(
  name='Addr',
  full_name='Addr',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='Addr.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='Addr.port', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=262,
  serialized_end=294,
)


_RESOURCE = _descriptor.Descriptor(
  name='Resource',
  full_name='Resource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cpu', full_name='Resource.cpu', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mem', full_name='Resource.mem', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='disc', full_name='Resource.disc', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=296,
  serialized_end=368,
)


_CPU = _descriptor.Descriptor(
  name='CPU',
  full_name='CPU',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='use_ratio', full_name='CPU.use_ratio', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='real_num', full_name='CPU.real_num', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='logic_num', full_name='CPU.logic_num', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  serialized_start=370,
  serialized_end=431,
)


_MEMORY = _descriptor.Descriptor(
  name='Memory',
  full_name='Memory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='total', full_name='Memory.total', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='used', full_name='Memory.used', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='available', full_name='Memory.available', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  serialized_start=433,
  serialized_end=489,
)


_DISC = _descriptor.Descriptor(
  name='Disc',
  full_name='Disc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='total', full_name='Disc.total', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='used', full_name='Disc.used', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='available', full_name='Disc.available', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  serialized_start=491,
  serialized_end=545,
)

_RESOURCEREQUEST.fields_by_name['addr'].message_type = _ADDR
_RESOURCEREQUEST.fields_by_name['resource'].message_type = _RESOURCE
_RESOURCE.fields_by_name['cpu'].message_type = _CPU
_RESOURCE.fields_by_name['mem'].message_type = _MEMORY
_RESOURCE.fields_by_name['disc'].message_type = _DISC
DESCRIPTOR.message_types_by_name['AIRequesst'] = _AIREQUESST
DESCRIPTOR.message_types_by_name['ImageRequest'] = _IMAGEREQUEST
DESCRIPTOR.message_types_by_name['TaskRequest'] = _TASKREQUEST
DESCRIPTOR.message_types_by_name['CommonReply'] = _COMMONREPLY
DESCRIPTOR.message_types_by_name['FileRequest'] = _FILEREQUEST
DESCRIPTOR.message_types_by_name['ResourceRequest'] = _RESOURCEREQUEST
DESCRIPTOR.message_types_by_name['Addr'] = _ADDR
DESCRIPTOR.message_types_by_name['Resource'] = _RESOURCE
DESCRIPTOR.message_types_by_name['CPU'] = _CPU
DESCRIPTOR.message_types_by_name['Memory'] = _MEMORY
DESCRIPTOR.message_types_by_name['Disc'] = _DISC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AIRequesst = _reflection.GeneratedProtocolMessageType('AIRequesst', (_message.Message,), {
  'DESCRIPTOR' : _AIREQUESST,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:AIRequesst)
  })
_sym_db.RegisterMessage(AIRequesst)

ImageRequest = _reflection.GeneratedProtocolMessageType('ImageRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEREQUEST,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:ImageRequest)
  })
_sym_db.RegisterMessage(ImageRequest)

TaskRequest = _reflection.GeneratedProtocolMessageType('TaskRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKREQUEST,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:TaskRequest)
  })
_sym_db.RegisterMessage(TaskRequest)

CommonReply = _reflection.GeneratedProtocolMessageType('CommonReply', (_message.Message,), {
  'DESCRIPTOR' : _COMMONREPLY,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:CommonReply)
  })
_sym_db.RegisterMessage(CommonReply)

FileRequest = _reflection.GeneratedProtocolMessageType('FileRequest', (_message.Message,), {
  'DESCRIPTOR' : _FILEREQUEST,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:FileRequest)
  })
_sym_db.RegisterMessage(FileRequest)

ResourceRequest = _reflection.GeneratedProtocolMessageType('ResourceRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCEREQUEST,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:ResourceRequest)
  })
_sym_db.RegisterMessage(ResourceRequest)

Addr = _reflection.GeneratedProtocolMessageType('Addr', (_message.Message,), {
  'DESCRIPTOR' : _ADDR,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:Addr)
  })
_sym_db.RegisterMessage(Addr)

Resource = _reflection.GeneratedProtocolMessageType('Resource', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCE,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:Resource)
  })
_sym_db.RegisterMessage(Resource)

CPU = _reflection.GeneratedProtocolMessageType('CPU', (_message.Message,), {
  'DESCRIPTOR' : _CPU,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:CPU)
  })
_sym_db.RegisterMessage(CPU)

Memory = _reflection.GeneratedProtocolMessageType('Memory', (_message.Message,), {
  'DESCRIPTOR' : _MEMORY,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:Memory)
  })
_sym_db.RegisterMessage(Memory)

Disc = _reflection.GeneratedProtocolMessageType('Disc', (_message.Message,), {
  'DESCRIPTOR' : _DISC,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:Disc)
  })
_sym_db.RegisterMessage(Disc)



_TASKSERVICE = _descriptor.ServiceDescriptor(
  name='TaskService',
  full_name='TaskService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=548,
  serialized_end=788,
  methods=[
  _descriptor.MethodDescriptor(
    name='task_service_1',
    full_name='TaskService.task_service_1',
    index=0,
    containing_service=None,
    input_type=_TASKREQUEST,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='send_file',
    full_name='TaskService.send_file',
    index=1,
    containing_service=None,
    input_type=_FILEREQUEST,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='send_resource',
    full_name='TaskService.send_resource',
    index=2,
    containing_service=None,
    input_type=_RESOURCEREQUEST,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='send_image',
    full_name='TaskService.send_image',
    index=3,
    containing_service=None,
    input_type=_IMAGEREQUEST,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='send_ai',
    full_name='TaskService.send_ai',
    index=4,
    containing_service=None,
    input_type=_AIREQUESST,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TASKSERVICE)

DESCRIPTOR.services_by_name['TaskService'] = _TASKSERVICE

# @@protoc_insertion_point(module_scope)
