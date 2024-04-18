import json
import os
import struct
import sys

import struct
import binascii

def reverse_bytes(byte_array):
    return byte_array[::-1]

def serialize_varint(value):
    if value < 0xFD:
        return struct.pack("<B", value)
    elif value <= 0xFFFF:
        return b'\xFD' + struct.pack("<H", value)
    elif value <= 0xFFFFFFFF:
        return b'\xFE' + struct.pack("<I", value)
    else:
        return b'\xFF' + struct.pack("<Q", value)

def tx_serialization(tx):
    serialized = bytearray()

    # Serialize version
    serialized.extend(struct.pack("<I", tx['version']))

    # Serialize vin count
    vin_count = len(tx['vin'])
    serialized.extend(serialize_varint(vin_count))

    # Serialize vin
    for vin in tx['vin']:
        txid_bytes = binascii.unhexlify(vin['txid'])
        serialized.extend(reverse_bytes(txid_bytes))

        serialized.extend(struct.pack("<I", vin['vout']))

        scriptsig_bytes = binascii.unhexlify(vin['scriptsig'])
        serialized.extend(serialize_varint(len(scriptsig_bytes)))
        serialized.extend(scriptsig_bytes)

        serialized.extend(struct.pack("<I", vin['sequence']))

    # Serialize vout count
    vout_count = len(tx['vout'])
    serialized.extend(serialize_varint(vout_count))

    # Serialize vout
    for vout in tx['vout']:
        serialized.extend(struct.pack("<Q", vout['value']))

        scriptpubkey_bytes = binascii.unhexlify(vout['scriptpubkey'])
        serialized.extend(serialize_varint(len(scriptpubkey_bytes)))
        serialized.extend(scriptpubkey_bytes)

    # Serialize locktime
    serialized.extend(struct.pack("<I", tx['locktime']))

    return serialized

def segwit_serialize(tx):
    serialized = bytearray()
    is_segwit = check_segwit(tx)

    # Serialize version
    serialized.extend(struct.pack("<I", tx['version']))

    # Serialize vin count
    if is_segwit:
        serialized.extend(b'\x00\x01')

    vin_count = len(tx['vin'])
    serialized.extend(serialize_varint(vin_count))

    # Serialize vin
    for vin in tx['vin']:
        txid_bytes = binascii.unhexlify(vin['txid'])
        serialized.extend(reverse_bytes(txid_bytes))

        serialized.extend(struct.pack("<I", vin['vout']))

        scriptsig_bytes = binascii.unhexlify(vin['scriptsig'])
        serialized.extend(serialize_varint(len(scriptsig_bytes)))
        serialized.extend(scriptsig_bytes)

        serialized.extend(struct.pack("<I", vin['sequence']))

    # Serialize vout count
    vout_count = len(tx['vout'])
    serialized.extend(serialize_varint(vout_count))

    # Serialize vout
    for vout in tx['vout']:
        serialized.extend(struct.pack("<Q", vout['value']))

        scriptpubkey_bytes = binascii.unhexlify(vout['scriptpubkey'])
        serialized.extend(serialize_varint(len(scriptpubkey_bytes)))
        serialized.extend(scriptpubkey_bytes)

    # Serialize locktime
    if is_segwit:
        for vin in tx['vin']:
            witness_count = len(vin['witness'])
            serialized.extend(serialize_varint(witness_count))
            for witness in vin['witness']:
                witness_bytes = binascii.unhexlify(witness)
                serialized.extend(serialize_varint(len(witness_bytes)))
                serialized.extend(witness_bytes)

    serialized.extend(struct.pack("<I", tx['locktime']))

    return serialized

def check_segwit(tx):
    for vin in tx['vin']:
        if len(vin['witness']) > 0:
            return True
    return False


def valid_tx_values(tx_id):
    
    # get raw json data
    tx_info = get_tx_info(tx_id)
    #this block of code is just for calculating the fee.
    in_value = 0
    out_value = 0
    for in_values in tx_info["vin"]:    
       in_value += in_values["prevout"]["value"]
    for out_values in tx_info["vout"]:
        out_value += out_values["value"]
    fee = in_value - out_value
    #recursion for each input
    return [fee, get_tx_size(tx_info), tx_id]

def get_tx_size(tx_info):
    #will return the size of the serialized tx in bytes
    return sys.getsizeof(tx_serialization(tx_info))

def get_tx_info(tx_id):
    #will return the json raw data or False if 
    #if does not found it
    #
    #if input of the function is "all" will return
    #all tx_ids in the mempool
    path = "../../mempool/" + tx_id

    if tx_id == "all":
        return os.listdir("../../mempool/")
    
    if not (os.path.exists(path)):
        return False

    return json.load(open(path))

def tx_syntax_validation(tx):
    required_fields = ['txid', 'inputs', 'outputs']
    if not all(field in tx for field in required_fields):
        return False
    if not isinstance(tx['txid'], str):
        return False
    for input in tx['inputs']:
        required_input_fields = ['txid', 'index']
        if not all(field in input for field in required_input_fields):
            return False
        if not isinstance(input['txid'], str) or not isinstance(input['index'], str):
            return False
    for output in tx['outputs']:
        required_output_fields = ['address', 'value']
        if not all(field in output for field in required_output_fields):
            return False
        if not isinstance(output['address'], str) or not isinstance(output['value'], (int, float)) or output['value'] <= 0:
            return False
    return True

def verify_sig(tx):
    interpreter = btcscript.BitcoinScriptInterpreter()
    interpreter.execute_script(tx['script_pubkey'], tx['script_sig'], tx['tx_data'])