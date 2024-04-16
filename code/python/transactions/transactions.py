import json
import os


def valid_tx_array(tx_id):    
    # get raw json data
    tx_info = get_tx_info(tx_id)
    if tx_info == False:
        return {"end": ["0", "0"]}
        
    #this block of code is just for calculating the fee.
    in_value = 0
    out_value = 0
    for in_values in tx_info["vin"]:    
       in_value += in_values["prevout"]["value"]
    for out_values in tx_info["vout"]:
        out_value += out_values["value"]
    fee = in_value - out_value
    tx_array = {tx_id: [fee, get_tx_size(tx_id)]}
    #recursion for each input
    for tx in tx_info["vin"]:
        if tx["txid"] not in tx_array:
            tx_array.update(valid_tx_array(tx["txid"]))

    return tx_array 

def get_tx_size(tx_id):
    #will return the size of the tx in bytes
    path = "../../mempool/" + tx_id
    if not (os.path.exists(path)):
        return False
    return os.path.getsize(path)

def get_tx_info(tx_id):
    #will return the json raw data or False if 
    #if does not found it
    #
    #if input of the function is "all" will return
    #all txs in the mempool
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