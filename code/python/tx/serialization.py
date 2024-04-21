import struct

def invert_bytes(data):
    for i in range(0, len(data), 2):
        data = data[:i] + data[i+1] + data[i] + data[i+2:]
    return data

def compact_size(integer):
    if integer < 253:
        return struct.pack('<B', integer)
    elif integer < 65535:
        return b'\xfd' + struct.pack('<I', integer)
    elif integer < 4294967295:
        return b'\xfe' + struct.pack('<L', integer)
    else:
        return b'\xff' + struct.pack('<Q', integer)

def check_segwit(input_obj, is_list=False):
    if is_list:
        for input in input_obj:
            if input["scriptsig"] == "":
                return True
        return False
    elif input_obj["scriptsig"] == "":
        return True
    return False

def serialize_tx_data(tx_data):
    #version
    version = struct.pack('<I', tx_data['version'])
    is_segwit = check_segwit(tx_data["vin"], True) 
    if is_segwit:
        #if is segwit, concatenate the marker and flag to the version
        version += b'\x00\x01'
    input_count = bytearray(compact_size(len(tx_data['vin'])))
    output_count = bytearray(compact_size(len(tx_data['vout'])))
    # Serialize the inputs
    inputs = input_count
    
    for input_obj in tx_data['vin']:
        prevout_id = bytes.fromhex(input_obj['txid'])
        vout = struct.pack('<I', input_obj['vout'])
        inputs.extend(prevout_id)
        inputs.extend(vout)
        script_size = compact_size(len(bytes.fromhex(input_obj['scriptsig'])))
        script = bytes.fromhex(input_obj['scriptsig'])
        sequence = struct.pack('<L', input_obj['sequence'])
        inputs.extend(script_size)
        inputs.extend(script)
        inputs.extend(sequence)
            


    # Serialize the outputs
    outputs = output_count
    for output_obj in tx_data['vout']:
        value = struct.pack('<Q', int(output_obj['value']))
        script_size = compact_size(len(bytes.fromhex(output_obj['scriptpubkey'])))
        script = bytes.fromhex(output_obj['scriptpubkey'])
        outputs.extend(value) 
        outputs.extend(script_size)
        outputs.extend(script)

    # Serialize the locktime
    locktime = bytearray(struct.pack('<I', tx_data['locktime']))

    # Concatenate all serialized parts
    serialized_data = bytearray(version)
    serialized_data.extend(inputs) 
    serialized_data.extend(outputs) 
    witness = bytearray()
    for input_obj in tx_data['vin']:
        if check_segwit(input_obj):
            witness.extend(compact_size(len(input_obj['witness'])))
            for w in input_obj['witness']:
                witness.extend(compact_size(len(bytes.fromhex(w))))
                witness.extend(bytes.fromhex(w))
    return serialized_data, witness, locktime