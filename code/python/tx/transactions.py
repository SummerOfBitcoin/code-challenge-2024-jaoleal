from hashlib import sha256
import json
import os
import sys
import tx.serialization as ser
def get_tx_id(tx_filename):
    tx_info = get_tx_info(tx_filename + ".json")
    tx_ser = ser.serialize_tx_data(tx_info)
    tx_ser = tx_ser[0] + tx_ser[1] + tx_ser[3]
    hash = sha256(sha256(tx_ser).digest()).digest()
    return hash.hex()
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
    transactions = ser.serialize_tx_data(tx_info)
    version = transactions[0]
    tx = transactions[1]
    wit = transactions[2]
    locktime = transactions[3]
    to_include = version + tx  + locktime
    #will return the size of the serialized tx in bytes
    return sys.getsizeof(to_include)

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