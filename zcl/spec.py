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
# class DataType(IntEnum):
#   # ZCL Spec -- "2.5.2 Data Types"
#   BOOLEAN = 0x10
#   UINT8 = 0x20
#   UINT16 = 0x21
#   UINT64 = 0x27
#   ENUM8 = 0x30
#   ENUM16 = 0x31
#   CHARACTER_STRING = 0x42

PROFILES = {
  'zigbee': (0x0000,),
  'ha': (0x0104,),
  'zll': (0xc05e,),
}

STATUS = {
  'success': 0x00,
  'failure': 0x01,
  'not_authorized': 0x7e,
  'reserved_field_not_zero': 0x7f,
  'malformed_command': 0x80,
  'unsup_cluster_command': 0x81,
  'unsup_general_command': 0x82,
  'unsup_manuf_cluster_command': 0x83,
  'unsup_manuf_general_command': 0x84,
  'invalid_field': 0x85,
  'unsupported_attribute': 0x86,
  'invalid_value': 0x87,
  'insufficient_space': 0x89,
  'duplicate_exists': 0x8a,
  'not_found': 0x8b,
  'unreportable_attribute': 0x8c,
  'invalid_data_type': 0x8d,
  'invalid_selector': 0x8e,
  'write_only': 0x8f,
  'inconsistent_startup_state': 0x90,
  'defined_out_of_band': 0x91,
  'inconsistent': 0x92,
  'action_denied': 0x93,
  'timeout': 0x94,
  'abort': 0x95,
  'invalid_image': 0x96,
  'wait_for_data': 0x97,
  'no_image_available': 0x98,
  'require_more_image': 0x99,
  'notification_pending': 0x9a,
  'hardware_failure': 0xc0,
  'software_failure': 0xc1,
  'calibration_error': 0xc2,
  'unsupported_cluster': 0xc3,
}

ZDO = {
    # Zigbee Spec -- "2.4.3.1.5 Simple_Desc_req"
    'simple_desc': (0x0004, ('addr16:uint16', 'endpoint:uint8',),),
    # Zigbee Spec -- "2.4.4.1.5 Simple_Desc_resp"
    'simple_desc_resp': (0x8004, ('status:enum8:success,invalid_ep,not_active,device_not_found,inv_requesttype,no_descriptor', 'addr16:uint16', 'length:uint8', 'simple_descriptor:*simple_descriptor',),),
    #  Zigbee Spec -- "2.4.3.1.6 Active_EP_req"
    'active_ep': (0x0005, ('addr16:uint16',),),
    #  Zigbee Spec -- "2.4.4.1.6 Active_EP_resp"
    'active_ep_resp': (0x8005, ('status:enum8:success,device_not_found,inv_requesttype,no_descriptor', 'addr16:uint16', 'active_ep_count:uint8', 'active_eps:*uint8',),),
    #  Zigbee Spec -- "2.4.3.1.7 Match_Desc_req"
    'match_desc': (0x0006, ('addr16:uint16', 'profile:uint16', 'num_in_clusters:uint8', 'in_clusters:*uint16', 'num_out_clusters:uint8', 'out_clusters:*uint16',),),
    #  Zigbee Spec -- "2.4.4.1.7 Match_Desc_resp"
    'match_desc_resp': (0x8006, ('status:enum8:success,device_not_found,inv_requesttype,no_descriptor', 'addr16:uint16', 'match_length:uint8', 'match_list:*uint8',),),
    # Zigbee Spec -- "2.4.3.2.2 Bind_req"
    'bind': (0x0021, ('src_addr:uint64', 'src_ep:uint8', 'cluster:uint16', 'dst_addr_mode:enum8:_,addr16,_,addr64', 'dst_addr:uint64', 'dst_ep:uint8',),),
    # Zigbee Spec -- "2.4.3.2.3 Unbind_req"
    'unbind': (0x0022, ('src_addr:uint64', 'src_ep:uint8', 'cluster:uint16', 'dst_addr_mode:enum8:_,addr16,_,addr64', 'dst_addr:uint64', 'dst_ep:uint8',),),
    # Zigbee Spec -- "2.4.4.2.2 Bind_resp"
    'bind_resp': (0x8021, ('status:enum8:success,not_supported,invalid_ep,table_full,not_authorized',),),
    # Zigbee Spec -- "2.4.4.2.3 Unbind_resp"
    'bind_resp': (0x8022, ('status:enum8:success,not_supported,invalid_ep,table_full,not_authorized',),),
    #  Spec -- "2.4.3.1.11 Device_annce"
    'device_annce': (0x0013,  ('addr16:uint16', 'addr64:uint64', 'capability:uint8'),),  # See Figure 2.17
    # Zigbee Spec -- "2.4.4.3.9 Mgmt_NWK_Update_notify"
    'mgmt_nwk_update_notify': (0x8038, ('status:uint8', 'scanned_channels:uint32', 'total_transmissions:uint16', 'transmisson_failures:uint16', 'scanned_channels_list_count:uint8', 'energy_values:*uint8',),),
}

PROFILE_COMMANDS = {
  # ZCL Spec -- "2.4 General Command Frames"
  'read_attributes': (0x00, ('*uint16',),),
  'read_attributes_response': (0x01, ('*read_attr_status',),),
  'write_attributes': (0x02, ('*write_attr',),),
  'write_attributes_undivided': (0x03, ('*write_attr',),),
  'write_attributes_response': (0x04, ('*write_attr_status',),),
  'write_attributes_no_response': (0x05, ('*write_attr',),),
  'configure_reporting': (0x06, ('*attr_reporting_config',),),
  'configure_reporting_response': (0x07, ('*attr_status',),),
  # 'read_reporting_configuration': (0x08, (),),
  # 'read_reporting_configuration_response': (0x09, (),),
  # 'report_attributes': (0x0a, (),),
  # 'default_response': (0x0b, (),),
  # 'discover_attributes': (0x0c, (),),
  # 'discover_attributes_response': (0x0d, (),),
  # 'read_attributes_structured': (0x0e, (),),
  # 'write_attributes_structured': (0x0f, (),),
  # 'write_attributes_structured_response': (0x10, (),),
}

CLUSTERS = {
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
    'get_group_membership': (0x02, ('count:uint8', 'ids:*uint16'),),
    'remove_group': (0x03, ('id:uint16',),),
    'remove_all_groups': (0x04, (),),
    'add_group_if_identifying': (0x05, ('id:uint16', 'name:string'),),
  }, {
    'add_group_response': (0x00, ('status:status8:success,duplicate_exists,insufficient_space', 'id:uint16',),),
    'view_group_response': (0x01, ('status:status8', 'id:uint16', 'name:string'),),
    'get_group_membership_response': (0x02, ('capacity:uint8', 'count:uint8', 'ids:*uint16',),),
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
    'move_to_satuation': (0x03, ('saturation:uint8', 'dir:enum8:shortest,longest,up,down', 'time:uint16',),),
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

ZDO_ENDPOINT = 0x00

# class FrameControl(IntEnum):
#   # ZCL Spec - "2.3.1.1 Frame Control Field"

#   # 0 == entire profile, 1 == cluster specific.
#   FRAME_TYPE_MASK = 1 << 0
#   FRAME_TYPE_PROFILE_COMMAND = 0
#   FRAME_TYPE_CLUSTER_COMMAND = 1 << 0

#   # Is this a manufacturer-specific frame?
#   MANUFACTURER_SPECIFIC_MASK = 1 << 2
#   MANUFACTURER_SPECIFIC = 1 << 2

#   # Direction (0 == client to server 1 == server to client).
#   DIRECTION_MASK = 1 << 3
#   DIRECTION_CLIENT_TO_SERVER = 0
#   DIRECTION_SERVER_TO_CLIENT = 1

#   # Disable the default response (1 == only default response if error).
#   DISABLE_DEFAULT_RESPONSE_MASK = 1 << 4


# class Status(IntEnum):
#   SUCCESS = 0x00
#print(ZCL_SPEC)


for profile_name, (profile_id,) in PROFILES.items():
  print('{} (0x{:04x})'.format(profile_name, profile_id))

for cluster_name, (cluster_id, rx, tx, attrs) in CLUSTERS.items():
  print('  {} (0x{:04x})'.format(cluster_name, cluster_id))
  if rx:
    print('    rx:    {}'.format(', '.join(rx.keys())))
  if tx:
    print('    tx:    {}'.format(', '.join(tx.keys())))
  if attrs:
    print('    attrs: {}'.format(', '.join(attrs.keys())))
