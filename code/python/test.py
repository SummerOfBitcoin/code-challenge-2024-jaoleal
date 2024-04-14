import transactions.transactions as txmod
import transactions.bitcoin_script as btcscript

def test_btc_script():
    interpreter = btcscript.BitcoinScriptInterpreter()
    stack = []
    tx_data = {'locktime': 1633649812, 'sequence': 4294967295}

    # P2PKH
    script_pubkey_p2pkh = "OP_DUP OP_HASH160 6ac8a68e42d499b8d8a12e8b1ea794dbd75c3f56 OP_EQUALVERIFY OP_CHECKSIG"
    script_sig_p2pkh = "3045022100abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 04abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    stack_p2pkh = (script_sig_p2pkh +  script_pubkey_p2pkh).split()

    # P2SH
    script_pubkey_p2sh = "OP_HASH160 6ac8a68e42d499b8d8a12e8b1ea794dbd75c3f56 OP_EQUAL"
    script_sig_p2sh = "0 3045022100abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 [OP_DUP OP_HASH160 6ac8a68e42d499b8d8a12e8b1ea794dbd75c3f56 OP_EQUALVERIFY OP_CHECKSIG]"
    stack_p2sh = [script_sig_p2sh, script_pubkey_p2sh]

    # P2MS
    script_pubkey_p2ms = "2 OP_1 6ac8a68e42d499b8d8a12e8b1ea794dbd75c3f56 OP_1 OP_CHECKMULTISIG"
    script_sig_p2ms = "0 3045022100abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 3045022100abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    stack_p2ms = [script_sig_p2ms, script_pubkey_p2ms]

    # P2PK
    script_pubkey_p2pk = "6ac8a68e42d499b8d8a12e8b1ea794dbd75c3f56 OP_CHECKSIG"
    script_sig_p2pk = "3045022100abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    stack_p2pk = [script_sig_p2pk, script_pubkey_p2pk]

    result_p2pkh = interpreter.execute_script(script_pubkey_p2pkh, stack_p2pkh, tx_data)
    result_p2sh = interpreter.execute_script(script_pubkey_p2sh, stack_p2sh, tx_data)
    result_p2ms = interpreter.execute_script(script_pubkey_p2ms, stack_p2ms, tx_data)
    result_p2pk = interpreter.execute_script(script_pubkey_p2pk, stack_p2pk, tx_data)
    
    assert (result_p2pkh and result_p2sh and result_p2ms and result_p2pk) == True

def test_verify_transaction():
    # Arrange
    valid_transaction = {
        'txid': '123',
        'inputs': [{'txid': 'abc', 'index': '0'}],
        'outputs': [{'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'value': 50}]
    }

    invalid_transaction = {
        'txid': 123,
        'inputs': [{'txid': 'abc', 'index': '0'}],
        'outputs': [{'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'value': 50}]
    }

    # Act
    result_valid = txmod.tx_syntax_validation(valid_transaction)
    result_invalid = txmod.tx_syntax_validation(invalid_transaction)

    # Assert
    assert result_valid == True
    assert result_invalid == False