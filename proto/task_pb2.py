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
  serialized_pb=b'\n\ntask.proto\"7\n\x07\x46ile_x2\x12\x16\n\x07\x63ontent\x18\x01 \x01(\x0b\x32\x05.File\x12\x14\n\x05style\x18\x02 \x01(\x0b\x32\x05.File\",\n\x08Image_x2\x12\x0b\n\x03img\x18\x01 \x01(\x0c\x12\x13\n\x0bimg_compose\x18\x02 \x01(\x0c\"\x0c\n\nAIRequesst\"\x14\n\x05Image\x12\x0b\n\x03img\x18\x01 \x01(\x0c\"1\n\x0bTaskRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\x05\x12\x11\n\ttask_name\x18\x02 \x01(\t\"\x1e\n\x0b\x43ommonReply\x12\x0f\n\x07success\x18\x01 \x01(\x08\",\n\x04\x46ile\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x11\n\tfile_data\x18\x02 \x01(\x0c\"C\n\x0fResourceRequest\x12\x13\n\x04\x61\x64\x64r\x18\x01 \x01(\x0b\x32\x05.Addr\x12\x1b\n\x08resource\x18\x02 \x01(\x0b\x32\t.Resource\" \n\x04\x41\x64\x64r\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"H\n\x08Resource\x12\x11\n\x03\x63pu\x18\x01 \x01(\x0b\x32\x04.CPU\x12\x14\n\x03mem\x18\x02 \x01(\x0b\x32\x07.Memory\x12\x13\n\x04\x64isc\x18\x03 \x01(\x0b\x32\x05.Disc\"=\n\x03\x43PU\x12\x11\n\tuse_ratio\x18\x01 \x01(\x02\x12\x10\n\x08real_num\x18\x02 \x01(\x05\x12\x11\n\tlogic_num\x18\x03 \x01(\x05\"8\n\x06Memory\x12\r\n\x05total\x18\x01 \x01(\x03\x12\x0c\n\x04used\x18\x02 \x01(\x03\x12\x11\n\tavailable\x18\x03 \x01(\x03\"6\n\x04\x44isc\x12\r\n\x05total\x18\x01 \x01(\x03\x12\x0c\n\x04used\x18\x02 \x01(\x03\x12\x11\n\tavailable\x18\x03 \x01(\x03\x32\xc9\x03\n\x0bTaskService\x12)\n\ttask_test\x12\x0c.TaskRequest\x1a\x0c.CommonReply\"\x00\x12+\n\x12task_transfer_file\x12\x05.File\x1a\x0c.CommonReply\"\x00\x12\x30\n\x0ctask_get_res\x12\x10.ResourceRequest\x1a\x0c.CommonReply\"\x00\x12$\n\nsend_image\x12\x06.Image\x1a\x0c.CommonReply\"\x00\x12$\n\x10task_yolox_image\x12\x06.Image\x1a\x06.Image\"\x00\x12#\n\x0ftask_lic_detect\x12\x06.Image\x1a\x06.Image\"\x00\x12(\n\x10task_yolox_vedio\x12\x06.Image\x1a\x06.Image\"\x00(\x01\x30\x01\x12&\n\x07task_ai\x12\x0b.AIRequesst\x1a\x0c.CommonReply\"\x00\x12\x1d\n\ntask_yolo5\x12\x05.File\x1a\x06.Image\"\x00\x12#\n\x0ctask_face_ai\x12\t.Image_x2\x1a\x06.Image\"\x00\x12)\n\x13task_style_transfer\x12\x08.File_x2\x1a\x06.Image\"\x00\x62\x06proto3'
)




_FILE_X2 = _descriptor.Descriptor(
  name='File_x2',
  full_name='File_x2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='content', full_name='File_x2.content', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='style', full_name='File_x2.style', index=1,
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
  serialized_start=14,
  serialized_end=69,
)


_IMAGE_X2 = _descriptor.Descriptor(
  name='Image_x2',
  full_name='Image_x2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='img', full_name='Image_x2.img', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='img_compose', full_name='Image_x2.img_compose', index=1,
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
  serialized_start=71,
  serialized_end=115,
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
  serialized_start=117,
  serialized_end=129,
)


_IMAGE = _descriptor.Descriptor(
  name='Image',
  full_name='Image',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='img', full_name='Image.img', index=0,
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
  serialized_start=131,
  serialized_end=151,
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
  serialized_start=153,
  serialized_end=202,
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
  serialized_start=204,
  serialized_end=234,
)


_FILE = _descriptor.Descriptor(
  name='File',
  full_name='File',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_name', full_name='File.file_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_data', full_name='File.file_data', index=1,
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
  serialized_start=236,
  serialized_end=280,
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
  serialized_start=282,
  serialized_end=349,
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
  serialized_start=351,
  serialized_end=383,
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
  serialized_start=385,
  serialized_end=457,
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
  serialized_start=459,
  serialized_end=520,
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
  serialized_start=522,
  serialized_end=578,
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
  serialized_start=580,
  serialized_end=634,
)

_FILE_X2.fields_by_name['content'].message_type = _FILE
_FILE_X2.fields_by_name['style'].message_type = _FILE
_RESOURCEREQUEST.fields_by_name['addr'].message_type = _ADDR
_RESOURCEREQUEST.fields_by_name['resource'].message_type = _RESOURCE
_RESOURCE.fields_by_name['cpu'].message_type = _CPU
_RESOURCE.fields_by_name['mem'].message_type = _MEMORY
_RESOURCE.fields_by_name['disc'].message_type = _DISC
DESCRIPTOR.message_types_by_name['File_x2'] = _FILE_X2
DESCRIPTOR.message_types_by_name['Image_x2'] = _IMAGE_X2
DESCRIPTOR.message_types_by_name['AIRequesst'] = _AIREQUESST
DESCRIPTOR.message_types_by_name['Image'] = _IMAGE
DESCRIPTOR.message_types_by_name['TaskRequest'] = _TASKREQUEST
DESCRIPTOR.message_types_by_name['CommonReply'] = _COMMONREPLY
DESCRIPTOR.message_types_by_name['File'] = _FILE
DESCRIPTOR.message_types_by_name['ResourceRequest'] = _RESOURCEREQUEST
DESCRIPTOR.message_types_by_name['Addr'] = _ADDR
DESCRIPTOR.message_types_by_name['Resource'] = _RESOURCE
DESCRIPTOR.message_types_by_name['CPU'] = _CPU
DESCRIPTOR.message_types_by_name['Memory'] = _MEMORY
DESCRIPTOR.message_types_by_name['Disc'] = _DISC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

File_x2 = _reflection.GeneratedProtocolMessageType('File_x2', (_message.Message,), {
  'DESCRIPTOR' : _FILE_X2,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:File_x2)
  })
_sym_db.RegisterMessage(File_x2)

Image_x2 = _reflection.GeneratedProtocolMessageType('Image_x2', (_message.Message,), {
  'DESCRIPTOR' : _IMAGE_X2,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:Image_x2)
  })
_sym_db.RegisterMessage(Image_x2)

AIRequesst = _reflection.GeneratedProtocolMessageType('AIRequesst', (_message.Message,), {
  'DESCRIPTOR' : _AIREQUESST,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:AIRequesst)
  })
_sym_db.RegisterMessage(AIRequesst)

Image = _reflection.GeneratedProtocolMessageType('Image', (_message.Message,), {
  'DESCRIPTOR' : _IMAGE,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:Image)
  })
_sym_db.RegisterMessage(Image)

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

File = _reflection.GeneratedProtocolMessageType('File', (_message.Message,), {
  'DESCRIPTOR' : _FILE,
  '__module__' : 'task_pb2'
  # @@protoc_insertion_point(class_scope:File)
  })
_sym_db.RegisterMessage(File)

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
  serialized_start=637,
  serialized_end=1094,
  methods=[
  _descriptor.MethodDescriptor(
    name='task_test',
    full_name='TaskService.task_test',
    index=0,
    containing_service=None,
    input_type=_TASKREQUEST,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_transfer_file',
    full_name='TaskService.task_transfer_file',
    index=1,
    containing_service=None,
    input_type=_FILE,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_get_res',
    full_name='TaskService.task_get_res',
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
    input_type=_IMAGE,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_yolox_image',
    full_name='TaskService.task_yolox_image',
    index=4,
    containing_service=None,
    input_type=_IMAGE,
    output_type=_IMAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_lic_detect',
    full_name='TaskService.task_lic_detect',
    index=5,
    containing_service=None,
    input_type=_IMAGE,
    output_type=_IMAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_yolox_vedio',
    full_name='TaskService.task_yolox_vedio',
    index=6,
    containing_service=None,
    input_type=_IMAGE,
    output_type=_IMAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_ai',
    full_name='TaskService.task_ai',
    index=7,
    containing_service=None,
    input_type=_AIREQUESST,
    output_type=_COMMONREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_yolo5',
    full_name='TaskService.task_yolo5',
    index=8,
    containing_service=None,
    input_type=_FILE,
    output_type=_IMAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_face_ai',
    full_name='TaskService.task_face_ai',
    index=9,
    containing_service=None,
    input_type=_IMAGE_X2,
    output_type=_IMAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='task_style_transfer',
    full_name='TaskService.task_style_transfer',
    index=10,
    containing_service=None,
    input_type=_FILE_X2,
    output_type=_IMAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TASKSERVICE)

DESCRIPTOR.services_by_name['TaskService'] = _TASKSERVICE

# @@protoc_insertion_point(module_scope)
