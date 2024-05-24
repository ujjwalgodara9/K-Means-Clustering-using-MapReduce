# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kmeans.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ckmeans.proto\"\x7f\n\x11ParametersRequest\x12\x19\n\x11start_line_number\x18\x01 \x01(\x05\x12\x17\n\x0f\x65nd_line_number\x18\x02 \x01(\x05\x12 \n\tcentroids\x18\x03 \x03(\x0b\x32\r.CentroidInfo\x12\x14\n\x0cnum_reducers\x18\x04 \x01(\x05\"9\n\x0c\x43\x65ntroidInfo\x12\x13\n\x0b\x63\x65ntroid_id\x18\x01 \x01(\x05\x12\t\n\x01x\x18\x02 \x01(\x01\x12\t\n\x01y\x18\x03 \x01(\x01\"-\n\x13StatusUpdateRequest\x12\x16\n\x0estatus_message\x18\x01 \x01(\t\"\x81\x01\n\x0eStatusResponse\x12/\n\x0bstatus_code\x18\x01 \x01(\x0e\x32\x1a.StatusResponse.StatusCode\x12\x16\n\x0estatus_message\x18\x02 \x01(\t\"&\n\nStatusCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0b\n\x07\x46\x41ILURE\x10\x01\"P\n\x0eReducerRequest\x12\x14\n\x0cnum_reducers\x18\x01 \x01(\x05\x12\x12\n\nreducer_id\x18\x02 \x01(\x05\x12\x14\n\x0cmapper_ports\x18\x03 \x03(\x05\"#\n\rMapperRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\"B\n\x15PartitionFileResponse\x12)\n\x10partition_values\x18\x01 \x03(\x0b\x32\x0f.PartitionValue\";\n\x0ePartitionValue\x12\x13\n\x0b\x63\x65ntroid_id\x18\x01 \x01(\x05\x12\t\n\x01x\x18\x02 \x01(\x01\x12\t\n\x01y\x18\x03 \x01(\x01\x32\xfa\x01\n\rKMeansService\x12\x35\n\x0eSendParameters\x12\x12.ParametersRequest\x1a\x0f.StatusResponse\x12\x35\n\x0cStatusUpdate\x12\x14.StatusUpdateRequest\x1a\x0f.StatusResponse\x12\x39\n\x0eInvokeReducers\x12\x0f.ReducerRequest\x1a\x16.PartitionFileResponse\x12@\n\x16GetPartitionFileValues\x12\x0e.MapperRequest\x1a\x16.PartitionFileResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kmeans_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PARAMETERSREQUEST']._serialized_start=16
  _globals['_PARAMETERSREQUEST']._serialized_end=143
  _globals['_CENTROIDINFO']._serialized_start=145
  _globals['_CENTROIDINFO']._serialized_end=202
  _globals['_STATUSUPDATEREQUEST']._serialized_start=204
  _globals['_STATUSUPDATEREQUEST']._serialized_end=249
  _globals['_STATUSRESPONSE']._serialized_start=252
  _globals['_STATUSRESPONSE']._serialized_end=381
  _globals['_STATUSRESPONSE_STATUSCODE']._serialized_start=343
  _globals['_STATUSRESPONSE_STATUSCODE']._serialized_end=381
  _globals['_REDUCERREQUEST']._serialized_start=383
  _globals['_REDUCERREQUEST']._serialized_end=463
  _globals['_MAPPERREQUEST']._serialized_start=465
  _globals['_MAPPERREQUEST']._serialized_end=500
  _globals['_PARTITIONFILERESPONSE']._serialized_start=502
  _globals['_PARTITIONFILERESPONSE']._serialized_end=568
  _globals['_PARTITIONVALUE']._serialized_start=570
  _globals['_PARTITIONVALUE']._serialized_end=629
  _globals['_KMEANSSERVICE']._serialized_start=632
  _globals['_KMEANSSERVICE']._serialized_end=882
# @@protoc_insertion_point(module_scope)
