import json
import tx.transactions as txmod
import tx.bitcoin_script as btcscript
import tx.serialization as txser
import hashlib as h

def test_serialization():
    entry = "0a70cacb1ac276056e57ebfb0587d2091563e098c618eebf4ed205d123a3e8c4"
    tx_info = txmod.get_tx_info(entry + ".json")
    ser = txser.serialize_tx_data(tx_info)
    hash1 = h.sha256(ser[0]+ ser[2]).digest()
    hash2 = h.sha256(hash1).digest()
    hash = hash2.hex()
    assert hash == "1c80292abf033e400d29c6a7df5852ea68dbffc2788b3afbfe451c8e9c0803eb"


def test_get_tx_info():
    tx_id = "0a3c3139b32f021a35ac9a7bef4d59d4abba9ee0160910ac94b4bcefb294f196.json"
    info = txmod.get_tx_info(tx_id)
    assert info == json.loads("""{
  "version": 1,
  "locktime": 0,
  "vin": [
    {
      "txid": "3b7dc918e5671037effad7848727da3d3bf302b05f5ded9bec89449460473bbb",
      "vout": 16,
      "prevout": {
        "scriptpubkey": "0014f8d9f2203c6f0773983392a487d45c0c818f9573",
        "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 f8d9f2203c6f0773983392a487d45c0c818f9573",
        "scriptpubkey_type": "v0_p2wpkh",
        "scriptpubkey_address": "bc1qlrvlygpudurh8xpnj2jg04zupjqcl9tnk5np40",
        "value": 37079526
      },
      "scriptsig": "",
      "scriptsig_asm": "",
      "witness": [
        "30440220780ad409b4d13eb1882aaf2e7a53a206734aa302279d6859e254a7f0a7633556022011fd0cbdf5d4374513ef60f850b7059c6a093ab9e46beb002505b7cba0623cf301",
        "022bf8c45da789f695d59f93983c813ec205203056e19ec5d3fbefa809af67e2ec"
      ],
      "is_coinbase": false,
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "scriptpubkey": "76a9146085312a9c500ff9cc35b571b0a1e5efb7fb9f1688ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 6085312a9c500ff9cc35b571b0a1e5efb7fb9f16 OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "19oMRmCWMYuhnP5W61ABrjjxHc6RphZh11",
      "value": 100000
    },
    {
      "scriptpubkey": "0014ad4cc1cc859c57477bf90d0f944360d90a3998bf",
      "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 ad4cc1cc859c57477bf90d0f944360d90a3998bf",
      "scriptpubkey_type": "v0_p2wpkh",
      "scriptpubkey_address": "bc1q44xvrny9n3t5w7lep58egsmqmy9rnx9lt6u0tc",
      "value": 36977942
    }
  ]
}""")

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