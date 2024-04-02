def verify_transaction(transaction):
    required_fields = ['txid', 'inputs', 'outputs']
    if not all(field in transaction for field in required_fields):
        return False
    # Check if the txid is a string
    if not isinstance(transaction['txid'], str):
        return False
    # Check if each input has the required fields
    for input in transaction['inputs']:
        required_input_fields = ['txid', 'index']
        if not all(field in input for field in required_input_fields):
            return False
        # Check if txid and index are strings
        if not isinstance(input['txid'], str) or not isinstance(input['index'], str):
            return False
    # Check if each output has the required fields
    for output in transaction['outputs']:
        required_output_fields = ['address', 'value']
        if not all(field in output for field in required_output_fields):
            return False

        # Check if address is a string and value is a positive number
        if not isinstance(output['address'], str) or not isinstance(output['value'], (int, float)) or output['value'] <= 0:
            return False

    
    return True

