import json
import os
def valid_tx_array(tx_id, tx_array):
    tx_info = get_tx_info(tx_id)
    in_values = 0
    out_values = 0
    for in_values in tx_info["vin"]:    
        in_values += in_values["value"]
    for out_values in tx_info["vout"]:
        out_values += out_values["value"]
    fee = in_values - out_values
    if in_values > out_values:
        tx_array.append({tx_id: [fee, get_tx_size(tx_id)]})
    for vout in tx_info["vin"]:
        valid_tx_array(vout["txid"], tx_array)

def get_tx_info(tx_id):
    tx_id =  tx_id + ".json"
    tx_entries = os.listdir("../../mempool/")
    for tx_entry in tx_entries:
        if tx_id == tx_entry:
            path = "../../mempool/" + tx_entry
            tx_file = open(path)
            return json.load(tx_file)

    print(tx_id + " not found in mempool")
    
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