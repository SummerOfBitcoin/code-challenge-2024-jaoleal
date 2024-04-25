import struct

def invert_bytes(data):
    for i in range(0, len(data), 2):
        data = data[:i] + data[i+1] + data[i] + data[i+2:]
    data = data[::-1]
    return data

def compact_size(integer):
    if integer < 253:
        return struct.pack('<B', integer)
    elif integer < 65535:
        return b'\xfd' + struct.pack('<H', integer)
    elif integer < 4294967295:
        return b'\xfe' + struct.pack('<I', integer)
    else:
        return b'\xff' + struct.pack('<Q', integer)

def check_segwit(input_obj, is_list=False):
    if is_list:
        for input in input_obj:
            if "witness" in input:
                return True
        return False
    elif "witness" in input_obj:
        return True
    return False

def serialize_tx_data(tx_data):
    #version
    version = struct.pack('<I', tx_data['version'])
    is_segwit = check_segwit(tx_data["vin"], True)
    input_count = bytearray(compact_size(len(tx_data['vin'])))
    output_count = bytearray(compact_size(len(tx_data['vout'])))
    # Serialize the inputs
    inputs = input_count
    for input_obj in tx_data['vin']:
        has_witness = check_segwit(input_obj)
        prevout_id = bytes.fromhex(invert_bytes(input_obj['txid']))
        vout = struct.pack('<I', input_obj['vout'])
        if "scriptsig" in input_obj:
            script_size = compact_size(len(bytes.fromhex(input_obj['scriptsig'])))
            script = bytes.fromhex(input_obj['scriptsig'])
        else:
            script_size = b'\x00'
            script = b''
        sequence = struct.pack('<L', input_obj['sequence'])
        inputs.extend(prevout_id)
        inputs.extend(vout)
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
    serialized_tx_data = bytearray()
    serialized_tx_data.extend(inputs) 
    serialized_tx_data.extend(outputs)
    witness = bytearray()
    for input_obj in tx_data['vin']:
        if check_segwit(input_obj):
            witness.extend(compact_size(len(input_obj['witness'])))
            for w in input_obj['witness']:
                witness.extend(compact_size(len(bytes.fromhex(w))))
                witness.extend(bytes.fromhex(w))
        elif is_segwit:
            witness.extend(b'\x00')
    if is_segwit:
        #if is segwit, concatenate the marker and flag to the version
        marker = bytes.fromhex("0001")
        return is_segwit, version, marker, serialized_tx_data, witness, locktime
    return is_segwit, version, serialized_tx_data, witness, locktime
