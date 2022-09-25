# HA Spec -- http://www.zigbee.org/zigbee-for-developers/applicationstandards/zigbeehomeautomation/
# ZCL Spec -- http://www.zigbee.org/download/standards-zigbee-cluster-library/
# Zigbee & Zigbee Pro -- http://www.zigbee.org/zigbee-for-developers/network-specifications/zigbeepro/
# ZLL -- http://www.zigbee.org/zigbee-for-developers/applicationstandards/zigbee-light-link/

# Direct document downloads:
# HA Spec -- http://www.zigbee.org/?wpdmdl=2129
# Zigbee Pro Stack Profile -- http://www.zigbee.org/wp-content/uploads/2014/11/docs-07-4855-05-0csg-zigbee-pro-stack-profile-2.pdf
# Zigbee Spec -- http://www.zigbee.org/wp-content/uploads/2014/11/docs-05-3474-20-0csg-zigbee-specification.pdf
# ZCL Spec -- http://www.zigbee.org/~zigbeeor/wp-content/uploads/2014/10/07-5123-06-zigbee-cluster-library-specification.pdf
# ZLL - http://www.zigbee.org/?wpdmdl=2132

# A ZigBee device is made up of endpoints, each of which corresponds
# to a single piece of functionality on the device. Endpoint IDs are
# 8-bit. Endpoints have an associated 16-bit profile ID, which defines
# the category of functionality on that endpoint (e.g. "Home
# Automation").
#
# Each endpoint contains a set of input and output cluster IDs (also
# 16-bit), which correspond to a specific function in that
# profile. These clusters are defined in the Zigbee Cluster Library.
# The profile defines which clusters are expected to be implemented
# for a given device type.
#
# Input clusters allow you to send a message to the device. For
# example, a light bulb has an endpoint on the ZLL or HA profile with
# a 'level control' input cluster to set brightness.  Output clusters
# allow the device to send a message. For examplebutton has an HA
# endpoint with an 'on off' output cluster.
#
# Clusters provide commands and attributes (e.g. the "on/off" cluster
# has "turn on", "turn off" and "toggle" commands and an "on/off"
# attribute).
#
# Devices can send commands from an endpoint to clusters on endpoints
# on other devices.  There are two types of commands - profile
# commands and cluster commands. Profile commands are common to all
# clusters and allow you to perform actions such as querying an
# attribute from the specified cluster. Cluster commands are defined
# on each cluster.
#
# For example, to query the state of a bulb, you would send the "read
# attributes" profile command to the "on/off" cluster for the "on/off"
# attribute id. To turn on the bulb, you would send the "on" cluster
# command to the "on/off" cluster.
#
# There is a special "ZDO" endpoint (id=0) on all devices which uses
# the "ZigBee" profile, and this allows general device configuration
# and information. The ZDO clusters correspond to requests and
# responses. The response cluster IDs have the high bit set.
# Essentially each cluster only supports a single command, and there #
# are only cluster commands, so the command id and command type are
# not included in the request.
#
# Some common ZDO requests are:
#   "device announce" (broadcast from a device on power on)
#   "bind" (allows a device to connect an output cluster from another
#           device to an input cluster).
#   "active endpoints" (get the list of endpoint IDs)

# t_int = 0

import enum
import struct


class DataType(enum.IntEnum):
  # ZCL Spec -- "2.5.2 Data Types"
  NULL = 0x00
  BOOLEAN = 0x10
  BITMAP8 = 0x18
  BITMAP16 = 0x19
  BITMAP64 = 0x1f
  UINT8 = 0x20
  UINT16 = 0x21
  UINT64 = 0x27
  INT8 = 0x28
  INT16 = 0x29
  INT64 = 0x2f
  ENUM8 = 0x30
  ENUM16 = 0x31
  CHARACTER_STRING = 0x42
  EUI64 = 0xf0


ANALOG_DATATYPES = set([
  DataType.UINT8, DataType.UINT16, DataType.UINT64, DataType.INT8, DataType.INT16, DataType.INT64
])


class Profile(enum.IntEnum):
  ZIGBEE = 0x0000
  HOME_AUTOMATION = 0x0104
  ZIGBEE_LIGHT_LINK = 0xc05e


def get_profile_by_name(n):
  return getattr(Profile, n.upper(), None)


class Endpoint(enum.IntEnum):
  ZDO = 0x00


class ZclCommandType(enum.IntEnum):
  PROFILE = 0
  CLUSTER = 1


class Status(enum.IntEnum):
  SUCCESS = 0x00
  FAILURE = 0x01
  REQUEST_DENIED = 0x70
  NOT_AUTHORIZED = 0x7E
  RESERVED_FIELD_NOT_ZERO = 0x7F
  MALFORMED_COMMAND = 0x80
  UNSUP_CLUSTER_COMMAND = 0x81
  UNSUP_GENERAL_COMMAND = 0x82
  UNSUP_MANUF_CLUSTER_COMMAND = 0x83
  UNSUP_MANUF_GENERAL_COMMAND = 0x84
  INVALID_FIELD = 0x85
  UNSUPPORTED_ATTRIBUTE = 0x86
  INVALID_VALUE = 0x87
  INSUFFICIENT_SPACE = 0x89
  DUPLICATE_EXISTS = 0x8A
  NOT_FOUND = 0x8B
  UNREPORTABLE_ATTRIBUTE = 0x8C
  INVALID_DATA_TYPE = 0x8D
  INVALID_SELECTOR = 0x8E
  WRITE_ONLY = 0x8F
  INCONSISTENT_STARTUP_STATE = 0x90
  DEFINED_OUT_OF_BAND = 0x91
  INCONSISTENT = 0x92
  ACTION_DENIED = 0x93
  TIMEOUT = 0x94
  ABORT = 0x95
  INVALID_IMAGE = 0x96
  WAIT_FOR_DATA = 0x97
  NO_IMAGE_AVAILABLE = 0x98
  REQUIRE_MORE_IMAGE = 0x99
  NOTIFICATION_PENDING = 0x9A
  HARDWARE_FAILURE = 0xC0
  SOFTWARE_FAILURE = 0xC1
  CALIBRATION_ERROR = 0xC2
  UNSUPPORTED_CLUSTER = 0xC3


ZDO_BY_NAME = {
  # Zigbee Spec -- "2.4.3.1.5 Simple_Desc_req"
  'simple_desc': (0x0004, ('addr16:uint16', 'endpoint:uint8',),),
  # Zigbee Spec -- "2.4.4.1.5 Simple_Desc_resp"
  'simple_desc_resp': (0x8004, ('status:enum8:success,invalid_ep,not_active,device_not_found,inv_requesttype,no_descriptor', 'addr16:uint16', 'b_simple_descriptors:uint8', 'simple_descriptors:#simple_descriptor',),),
  #  Zigbee Spec -- "2.4.3.1.6 Active_EP_req"
  'active_ep': (0x0005, ('addr16:uint16',),),
  #  Zigbee Spec -- "2.4.4.1.6 Active_EP_resp"
  'active_ep_resp': (0x8005, ('status:enum8:success,device_not_found,inv_requesttype,no_descriptor', 'addr16:uint16', 'n_active_eps:uint8', 'active_eps:*uint8',),),
  #  Zigbee Spec -- "2.4.3.1.7 Match_Desc_req"
  'match_desc': (0x0006, ('addr16:uint16', 'profile:uint16', 'n_in_clusters:uint8', 'in_clusters:*uint16', 'n_out_clusters:uint8', 'out_clusters:*uint16',),),
  #  Zigbee Spec -- "2.4.4.1.7 Match_Desc_resp"
  'match_desc_resp': (0x8006, ('status:enum8:success,device_not_found,inv_requesttype,no_descriptor', 'addr16:uint16', 'n_match_list:uint8', 'match_list:*uint8',),),
  # Zigbee Spec -- "2.4.3.2.2 Bind_req"
  'bind': (0x0021, ('src_addr:uint64', 'src_ep:uint8', 'cluster:uint16', 'dst_addr_mode:enum8:_,addr16,_,addr64', 'dst_addr:uint64', 'dst_ep:uint8',),),
  # Zigbee Spec -- "2.4.3.2.3 Unbind_req"
  'unbind': (0x0022, ('src_addr:uint64', 'src_ep:uint8', 'cluster:uint16', 'dst_addr_mode:enum8:_,addr16,_,addr64', 'dst_addr:uint64', 'dst_ep:uint8',),),
  # Zigbee Spec -- "2.4.4.2.2 Bind_resp"
  'bind_resp': (0x8021, ('status:enum8:success,not_supported,invalid_ep,table_full,not_authorized',),),
  # Zigbee Spec -- "2.4.4.2.3 Unbind_resp"
  'unbind_resp': (0x8022, ('status:enum8:success,not_supported,invalid_ep,table_full,not_authorized',),),
  #  Spec -- "2.4.3.1.11 Device_annce"
  'device_annce': (0x0013,  ('addr16:uint16', 'addr64:uint64', 'capability:uint8'),),  # See Figure 2.17
  # Zigbee Spec -- "2.4.4.3.9 Mgmt_NWK_Update_notify"
  'mgmt_nwk_update_notify': (0x8038, ('status:uint8', 'scanned_channels:uint32', 'total_transmissions:uint16', 'transmisson_failures:uint16', 'n_energy_values:uint8', 'energy_values:*uint8',),),
}


ZDO_BY_ID = {
  cluster: (name, args) for name, (cluster, args) in ZDO_BY_NAME.items()
}


def _decode_helper(args, data, i=0):
  kwargs = {}

  n = 1
  b = 0

  for arg in args:
    arg = arg.split(':')
    name, datatype = arg[0], arg[1],

    v = None

    decode, encode = STRUCT_TYPES[datatype.strip('*#%')]
    if not callable(decode):
      fmt, nbytes, = decode, encode
      decode = lambda dd, ii, _: (struct.unpack(fmt, dd[ii:ii + nbytes])[0], ii + nbytes,)

    if datatype.startswith('*'):
      # Repeat n times
      v = []
      for _i in range(n):
        x, i = decode(data, i, kwargs)
        v.append(x)
    elif datatype.startswith('#'):
      # There are b bytes of records
      v = []
      ii = i + b
      while i < ii:
        x, i = decode(data, i, kwargs)
        v.append(x)
    elif datatype.startswith('%'):
      # Keep reading records until end of frame
      v = []
      ii = len(data)
      while i < ii:
        x, i = decode(data, i, kwargs)
        v.append(x)
    else:
      v, i = decode(data, i, kwargs)

    stop = False
    if name.startswith('s_'):
      name = name[2:]
      if v != 'SUCCESS':
        stop = True

    if name.startswith('n_'):
      n = v
    elif name.startswith('b_'):
      b = v
    else:
      kwargs[name] = v
      n = 1
      b = 0

    if stop:
      break

  return kwargs, i


def _decode_simple_descriptor(data, i, obj):
  return _decode_helper(('endpoint:uint8', 'profile:uint16', 'device_identifier:uint16', 'device_version:uint8', 'n_in_clusters:uint8', 'in_clusters:*uint16', 'n_out_clusters:uint8', 'out_clusters:*uint16',), data, i)

def _encode_simple_descriptor():
  pass


def _decode_read_attr_status(data, i, obj):
  return _decode_helper(('attribute:uint16', 's_status:status8', 'datatype:uint8', 'value:datatype',), data, i)

def _encode_read_attr_status(obj):
  pass


def _encode_value_field_helper(datatype, value):
  decode, encode = STRUCT_TYPES[datatype]
  if not callable(decode):
    fmt, _nbytes = decode, encode
    if datatype == 'uint64' and isinstance(value, str):
      value = int(value, 16)
    return struct.pack(fmt, value)
  else:
    return encode(value)


def _decode_write_attr(data, i, obj):
  return _decode_helper(('attribute:uint16', 'datatype:uint8', 'value:datatype',), data, i)

def _encode_write_attr(obj):
  return struct.pack('<HB', obj['attribute'], DATATYPES_BY_NAME[obj['datatype']]) + _encode_value_field_helper(obj['datatype'], obj['value'])


def _decode_write_attr_status(data, i, obj):
  # , 'attribute:uint16',
  return _decode_helper(('status:status8', ), data, i)

def _encode_write_attr_status(obj):
  return struct.pack('<BH', obj['status'], obj['attribute'])


def _decode_datatype(data, i, obj):
  if 'datatype' not in obj:
    raise ValueError('Object needs datatype field.')
  datatype = obj['datatype']

  if datatype == DataType.NULL:
    return None, i,

  if datatype not in DATATYPE_STRUCT_TYPES:
    raise ValueError('Unknown struct type')

  decode, encode = STRUCT_TYPES[DATATYPE_STRUCT_TYPES[datatype]]
  if not callable(decode):
    fmt, nbytes, = decode, encode
    decode = lambda dd, ii, _: (struct.unpack(fmt, dd[ii:ii + nbytes])[0], ii + nbytes,)

  return decode(data, i, obj)

def _encode_datatype():
  pass


def _decode_attr_reporting_config():
  pass

def _encode_attr_reporting_config(obj):
  data = bytes()
  datatype = DATATYPES_BY_NAME[obj['datatype']]
  # min=1s, max=60s
  data += struct.pack('<BHBHH', 0, obj['attribute'], datatype, obj['minimum'], obj['maximum'])
  if datatype in ANALOG_DATATYPES:
    decode, encode = STRUCT_TYPES[DATATYPE_STRUCT_TYPES[datatype]]
    fmt, _nbytes = decode, encode
    data += struct.pack(fmt, obj.get('delta', 1))
  return data

def _decode_attr_reporting_status(data, i, obj):
  # Note that attribute status records are not included for successfully configured attributes, in order to save bandwidth. In the case of successful configuration of all attributes, only a single attribute status record SHALL be included in the command, with the status field set to SUCCESS and the direction and attribute identifier fields omitted.
  if data[i] == 0x00 and len(data) - i == 1:
    return {
      'status': 'SUCCESS',
    }, i + 1
  return _decode_helper(('status:status8', 'direction:uint8', 'attribute:uint16',), data, i)


def _encode_attr_reporting_status():
  pass


def _decode_reported_attribute(data, i, obj):
  return _decode_helper(('attribute:uint16', 'datatype:uint8', 'value:datatype',), data, i)

def _encode_reported_attribute():
  pass


def _decode_string(data, i, obj):
  nbytes, = struct.unpack('<B', data[i:i+1])
  nbytes += 1
  return data[i+1:i+nbytes].decode(), i + nbytes


def _encode_string(val):
  val = val.encode()
  return struct.pack('<B', len(val)) + val


def _decode_status(data, i, obj):
  status, = struct.unpack('<B', data[i:i+1])
  for s in Status:
    if s.value == status:
      return s.name, i + 1
  raise ValueError('Unknown status {}'.format(status))


def _encode_status(val):
  for s in Status:
    if s.name == val:
      return struct.pack('<B', s.value)
  raise ValueError('Unknown status {}'.format(val))


STRUCT_TYPES = {
  'uint8': ('<B', 1,),
  'uint16': ('<H', 2,),
  'uint32': ('<I', 4,),
  'uint64': ('<Q', 8,),
  'int8': ('<b', 1,),
  'int16': ('<h', 2,),
  'int32': ('<i', 4,),
  'int64': ('<q', 8,),
  'enum8': ('<B', 1,),
  'enum16': ('<H', 2,),
  'status8': (_decode_status, _encode_status,),
  'string': (_decode_string, _encode_string,),
  'EUI64': ('<Q', 8,),
  'simple_descriptor': (_decode_simple_descriptor, _encode_simple_descriptor,),
  'read_attr_status': (_decode_read_attr_status, _encode_read_attr_status,),
  'datatype': (_decode_datatype, _encode_datatype,),
  'attr_reporting_config': (_decode_attr_reporting_config, _encode_attr_reporting_config,),
  'attr_reporting_status': (_decode_attr_reporting_status, _encode_attr_reporting_status,),
  'reported_attribute': (_decode_reported_attribute, _encode_reported_attribute,),
  'write_attr': (_decode_write_attr, _encode_write_attr,),
  'write_attr_status': (_decode_write_attr_status, _encode_write_attr_status,),
}


DATATYPE_STRUCT_TYPES = {
  DataType.BOOLEAN: 'uint8',
  DataType.BITMAP8: 'uint8',
  DataType.BITMAP16: 'uint16',
  DataType.BITMAP64: 'uint64',
  DataType.UINT8: 'uint8',
  DataType.UINT16: 'uint16',
  DataType.UINT64: 'uint64',
  DataType.INT8: 'int8',
  DataType.INT16: 'int16',
  DataType.INT64: 'int64',
  DataType.ENUM8: 'enum8',
  DataType.ENUM16: 'enum16',
  DataType.CHARACTER_STRING: 'string',
  DataType.EUI64: 'EUI64',
}

DATATYPES_BY_NAME = {
  'bool': DataType.BOOLEAN,
  'bitmap8': DataType.BITMAP8,
  'bitmap16': DataType.BITMAP16,
  'bitmap64': DataType.BITMAP64,
  'uint8': DataType.UINT8,
  'uint16': DataType.UINT16,
  'uint64': DataType.UINT64,
  'int8': DataType.INT8,
  'int16': DataType.INT16,
  'int64': DataType.INT64,
  'enum8': DataType.ENUM8,
  'enum16': DataType.ENUM16,
  'string': DataType.CHARACTER_STRING,
  'EUI64': DataType.EUI64,
}


def decode_zdo(cluster, data):
  if cluster not in ZDO_BY_ID:
    raise ValueError('Unknown ZDO 0x{:04x}'.format(cluster))

  #print([hex(b) for b in data])

  cluster_name, args = ZDO_BY_ID[cluster]

  seq, = struct.unpack('<B', data[:1])
  data = data[1:]

  kwargs, _nbytes =_decode_helper(args, data)

  return cluster_name, seq, kwargs


def _encode_helper(args, kwargs):
  data = bytes()

  for arg in args:
    arg = arg.split(':')
    name, datatype = arg[0], arg[1],

    if name.startswith('n_'):
      name = name[2:]
      values = [len(kwargs[name])]
    else:
      values = [kwargs[name]]

    if datatype.startswith('*'):
      datatype = datatype[1:]
      values = kwargs[name]

    decode, encode = STRUCT_TYPES[datatype]

    for value in values:
      if not callable(decode):
        fmt, _nbytes = decode, encode
        if datatype == 'uint64' and isinstance(value, str):
          value = int(value, 16)
        data += struct.pack(fmt, value)
      else:
        data += encode(value)

  return data


def encode_zdo(cluster_name, seq, **kwargs):
  if cluster_name not in ZDO_BY_NAME:
    raise ValueError('Unknown ZDO "{}"'.format(cluster_name))

  cluster, args = ZDO_BY_NAME[cluster_name]

  data = struct.pack('<B', seq) + _encode_helper(args, kwargs)

  return cluster, data


PROFILE_COMMANDS_BY_NAME = {
  # ZCL Spec -- "2.5 General Command Frames"
  'read_attributes': (0x00, ('attributes:*uint16',),),
  'read_attributes_response': (0x01, ('attributes:%read_attr_status',),),
  'write_attributes': (0x02, ('attributes:*write_attr',),),
  'write_attributes_undivided': (0x03, ('attributes:*write_attr',),),
  'write_attributes_response': (0x04, ('attributes:%write_attr_status',),),
  'write_attributes_no_response': (0x05, ('attributes:*write_attr',),),
  'configure_reporting': (0x06, ('configs:*attr_reporting_config',),),
  'configure_reporting_response': (0x07, ('results:%attr_reporting_status',),),
  # 'read_reporting_configuration': (0x08, (),),
  # 'read_reporting_configuration_response': (0x09, (),),
  'report_attributes': (0x0a, ('attributes:%reported_attribute',),),
  'default_response': (0x0b, ('command:uint8', 'status:uint8',),),
  # 'discover_attributes': (0x0c, (),),
  # 'discover_attributes_response': (0x0d, (),),
  # 'read_attributes_structured': (0x0e, (),),
  # 'write_attributes_structured': (0x0f, (),),
  # 'write_attributes_structured_response': (0x10, (),),
}


PROFILE_COMMANDS_BY_ID = {
  command: (command_name, args) for command_name, (command, args) in PROFILE_COMMANDS_BY_NAME.items()
}


CLUSTERS_BY_NAME = {
  # ZCL Spec -- Chapter 3 -- General
  'basic': (0x0000, {
    'reset': (0x00, (),),
  }, {
  },{
    'zclversion': (0x0000, 'uint8',),
    'application_version': (0x0001, 'uint8',),
    'stack_version': (0x0002, 'uint8',),
    'hw_version': (0x0003, 'uint8',),
    'manufacturer_name': (0x0004, 'string',),
    'model_id': (0x0005, 'string',),
    'date_code': (0x0006, 'string',),
    'power_source': (0x0007, 'enum8:unknown,mains-single,mains-three,battery,dc,emergency-constat,emergency-transfer',),
    'location': (0x0010, 'string',),
    'physical_environment': (0x0011, 'uint8',),
    'device_enabled': (0x0012, 'bool',),
    'sw_build_id': (0x4000, 'string',),
  },),
  'power_configuration': (0x0001, {
  }, {
  }, {
  },),
  'identify': (0x0003, {
    'identify': (0x00, ('identify_time:uint16',),),
    'identify_query': (0x01, (),),
    'trigger_effect': (0x40, ('effect_id:uint8', 'effect_variant:uint8',),),
  }, {
    'identify_query_response': (0x00, ('timeout:uint16'),),
  },{
    'identify_time': (0x0000, 'uint16',),
  },),
  'groups': (0x0004, {
    'add_group': (0x00, ('id:uint16', 'name:string'),),
    'view_group': (0x01, ('id:uint16',),),
    'get_group_membership': (0x02, ('n_ids:uint8', 'ids:*uint16'),),
    'remove_group': (0x03, ('id:uint16',),),
    'remove_all_groups': (0x04, (),),
    'add_group_if_identifying': (0x05, ('id:uint16', 'name:string'),),
  }, {
    'add_group_response': (0x00, ('status:status8', 'id:uint16',),),
    'view_group_response': (0x01, ('status:status8', 'id:uint16', 'name:string'),),
    'get_group_membership_response': (0x02, ('capacity:uint8', 'n_ids:uint8', 'ids:*uint16',),),
    'remove_group_response': (0x03, ('status:status8', 'id:uint16',),),
  }, {
    'name_support': (0x0000, 'uint8',),
  },),
  'scenes': (0x0005, {
  }, {
  }, {
  },),
  'onoff': (0x0006, {
    'off': (0x00, (),),
    'on': (0x01, (),),
    'toggle': (0x02, (),),
    'off_with_effect': (0x40, ('effect_id:uint8', 'effect_variant:uint8',),),
    'on_with_recall_global_scene': (0x41, (),),
    'on_with_timed_off': (0x42, ('control:uint8', 'on_time:uint16', 'off_wait_time:uint16',),),
  }, {
  }, {
    'onoff': (0x0000, 'bool',),
    'global_scene_control': (0x4000, 'bool',),
    'on_time': (0x4001, 'uint16',),
    'off_wait_time': (0x4002, 'uint16',),
  },),
  'onoff_configuration': (0x0007, {
  }, {
  }, {
  },),
  'level_control': (0x0008, {
    'move_to_level': (0x00, ('level:uint8', 'time:uint16',),),
    'move': (0x01, ('mode:enum8:up,down', 'rate:uint8',),),
    'step': (0x02, ('mode:enum8:up,down', 'size:uint8', 'time:uint16',),),
    'stop': (0x03, (),),
    'move_to_level_on_off': (0x04, ('level:uint8', 'time:uint16',),),
    'move_on_off': (0x05, ('mode:enum8:up,down', 'rate:uint8',),),
    'step_on_off': (0x06, ('mode:enum8:up,down', 'size:uint8', 'time:uint16',),),
    'stop_on_off': (0x07, (),),
  }, {
  }, {
    'current_level': (0x0000, 'uint8',),
    'remaining_time': (0x0001, 'uint16',),
    'on_off_transition_time': (0x0010, 'uint16',),
    'on_level': (0x0011, 'uint8',),
    'on_transition_time': (0x0012, 'uint16',),
    'off_transition_time': (0x0013, 'uint16',),
    'default_move_rate': (0x0014, 'uint16',),
  },),
  'poll_control': (0x0020, {
  }, {
  }, {
  },),
  'ias_zone': (0x0500, {
    'zone_enrol': (0x00, ('enroll_response_code:uint8', 'zone_id:uint8',),),
  }, {
    'zone_status_change': (0x00, ('zone_status:uint16', 'extended_status:uint8', 'zone_id:uint8', 'delay:uint16',),),
    'zone_enrol_request': (0x01, ('zone_type:uint16', 'manufacturer_code:uint16',),),
  }, {
    'zone_state': (0x0000, 'uint8',),
    'zone_type': (0x0001, 'uint16',),
    'zone_status': (0x0002, 'uint16',),

    'ias_cie_address': (0x0010, 'uint64',),
    'zone_id': (0x0011, 'uint8',),
    'number_of_zone_sensitivity_levels_supported': (0x0012, 'uint8',),
    'current_zone_sensitivity_level': (0x0013, 'uint8',),
  },),
  'diagnostics': (0x0b05, {
  }, {
  }, {
  },),

  # ZCL Spec -- Chapter 4 -- Measurement and Sensing
  'electrical_measurement': (0x0b04, {
  }, {
  }, {
  },),

  # ZCL Spec -- Chapter 5 -- Lighting
  'color': (0x0300, {
    'move_to_hue': (0x00, ('hue:uint8', 'dir:enum8:shortest,longest,up,down', 'time:uint16',),),
    'move_hue': (0x01, ('mode:enum8:stop,up,_,down', 'rate:uint8',),),
    'step_hue': (0x02, ('mode:enum8:_,up,_,down', 'size:uint8', 'time:uint8',),),
    'move_to_saturation': (0x03, ('saturation:uint8', 'dir:enum8:shortest,longest,up,down', 'time:uint16',),),
    'move_saturation': (0x04, ('mode:enum8:stop,up,_,down', 'rate:uint8',),),
    'step_saturation': (0x05, ('mode:enum8:_,up,_,down', 'size:uint8', 'time:uint8',),),
    'move_to_hue_saturation': (0x06, ('hue:uint8', 'saturation:uint8', 'time:uint16',),),
    'move_to_color_temperature': (0x0a, ('mireds:uint16', 'time:uint16',),),
  }, {
  }, {
    'hue': (0x0000, 'uint8',),
    'saturation': (0x0001, 'uint8',),
    'remaining_time': (0x0002, 'uint16',),
    'temperature': (0x0007, 'uint16',),  # mireds, e.g. 1e6/K
  },),

  # ZCL Spec -- Chapter 13 -- Commissioning
  'commissioning': (0x0015, {
  }, {
  }, {
  },),
  'touchlink': (0x1000, {
  }, {
  }, {
  },),
}


CLUSTERS_BY_ID = {}
for cluster_name, (cluster, rx_commands, tx_commands, attributes,) in CLUSTERS_BY_NAME.items():
  CLUSTERS_BY_ID[cluster] = (
    cluster_name,
    {
      command: (command_name, args) for command_name, (command, args) in rx_commands.items()
    },
    {
      command: (command_name, args) for command_name, (command, args) in tx_commands.items()
    },
    {
      attribute: (attribute_name, datatype) for attribute_name, (attribute, datatype) in attributes.items()
    }
  )


def decode_zcl(cluster, data):
  frame_control, = struct.unpack('<B', data[:1])
  frame_type = frame_control & 1
  direction = frame_control & (1 << 3)
  disable_default_response = frame_control & (1 << 4)
  manufacturer_specific = 0 #frame_control & (1 << 2)      ??
  #print(frame_type, direction, manufacturer_specific)

  if manufacturer_specific:
    manufacturer_code, seq, command = struct.unpack('<HBB', data[1:5])
    data = data[5:]
  else:
    manufacturer_code = 0
    seq, command = struct.unpack('<BB', data[1:3])
    data = data[3:]

  #print(manufacturer_code, seq, command)

  if cluster not in CLUSTERS_BY_ID:
    raise ValueError('Unknown cluster {}'.format(cluster))
  cluster_name, rx_commands, tx_commands, attributes = CLUSTERS_BY_ID[cluster]

  if direction == 0:
    commands = rx_commands
  else:
    commands = tx_commands

  if frame_type == 0:
    # Profile command
    if command not in PROFILE_COMMANDS_BY_ID:
      raise ValueError('Unknown profile command {} for cluster "{}"'.format(command, cluster_name))
    command_name, args = PROFILE_COMMANDS_BY_ID[command]
    kwargs, _nbytes = _decode_helper(args, data)
    return cluster_name, seq, ZclCommandType.PROFILE, command_name, not disable_default_response, kwargs
  else:
    # Cluster command
    if command not in commands:
      raise ValueError('Unknown cluster command {} for cluster "{}" (direction={})'.format(command, cluster_name, direction))
    command_name, args = commands[command]
    kwargs, _nbytes = _decode_helper(args, data)
    return cluster_name, seq, ZclCommandType.CLUSTER, command_name, not disable_default_response, kwargs


def get_cluster_by_name(cluster_name):
  if cluster_name not in CLUSTERS_BY_NAME:
    raise ValueError('Unknown cluster "{}"'.format(cluster_name))

  cluster, _rx_commands, _tx_commands, _attributes = CLUSTERS_BY_NAME[cluster_name]
  return cluster


def get_cluster_rx_command(cluster_name, command_name):
  if cluster_name not in CLUSTERS_BY_NAME:
    raise ValueError('Unknown cluster "{}"'.format(cluster_name))

  cluster, rx_commands, _tx_commands, _attributes = CLUSTERS_BY_NAME[cluster_name]

  if command_name not in rx_commands:
    raise ValueError('Unknown command "{}"'.format(command_name))

  command, args = rx_commands[command_name]
  return cluster, command, args


def encode_cluster_command(cluster_name, command_name, seq, direction=0, default_response=True, manufacturer_code=None, **kwargs):
  cluster, command, args = get_cluster_rx_command(cluster_name, command_name)

  # ZCL Spec - "2.4.1.1 Frame Control Field"
  frame_control = 1  # Cluster command (command is specific to this cluster)
  if direction:
    frame_control |= 1 << 3
  if not default_response:
    frame_control |= 1 << 4

  if manufacturer_code is not None:
    frame_control |= 1 << 2
    data = struct.pack('<BHBB', frame_control, manufacturer_code, seq, command)
  else:
    data = struct.pack('<BBB', frame_control, seq, command)

  data += _encode_helper(args, kwargs)

  return cluster, data


def encode_profile_command(cluster_name, command_name, seq, direction=0, default_response=True, manufacturer_code=None, **kwargs):
  if cluster_name not in CLUSTERS_BY_NAME:
    raise ValueError('Unknown cluster "{}"'.format(cluster_name))

  cluster, rx_commands, tx_commands, attributes = CLUSTERS_BY_NAME[cluster_name]

  if command_name not in PROFILE_COMMANDS_BY_NAME:
    raise ValueError('Unknown command "{}"'.format(command_name))

  command, args = PROFILE_COMMANDS_BY_NAME[command_name]

  # ZCL Spec - "2.4.1.1 Frame Control Field"
  frame_control = 0  # Profile  command (command applies to all clusters)
  data = struct.pack('<BBB', frame_control, seq, command)

  data += _encode_helper(args, kwargs)

  return cluster, data


def get_json():
  return {
    'profile': [
      {
        'name': p.name,
        'profile': p
      } for p in Profile
    ],
    'zdo': [
      {
        'cluster_name': cluster_name,
        'cluster': cluster,
        'args': args
      } for cluster_name, (cluster, args) in ZDO_BY_NAME.items()
    ],
    'status': [s.name for s in Status],
    'profile_command': [
      {
        'name': command_name,
        'command': command,
        'args': args
      } for command_name, (command, args) in PROFILE_COMMANDS_BY_NAME.items()
    ],
    'cluster': [
      {
        'name': cluster_name,
        'cluster': cluster,
        'rx_commands': [
          {
            'name': command_name,
            'command': command,
            'args': args
          } for command_name, (command, args) in rx_commands.items()
        ],
        'tx_commands': [
          {
            'name': command_name,
            'command': command,
            'args': args
          } for command_name, (command, args) in tx_commands.items()
        ],
        'attributes': [
          {
            'name': attribute_name,
            'attribute': attribute,
            'datatype': datatype
          } for attribute_name, (attribute, datatype) in attributes.items()
        ],
      } for cluster_name, (cluster, rx_commands, tx_commands, attributes) in CLUSTERS_BY_NAME.items()
    ]
  }
