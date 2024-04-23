import json
import tx.transactions as txmod
import tx.bitcoin_script as btcscript
import tx.serialization as txser
import hashlib as h

def test_serialization():
    entry = "0a70cacb1ac276056e57ebfb0587d2091563e098c618eebf4ed205d123a3e8c4"
    tx_info = txmod.get_tx_info(entry + ".json")
    ser = txser.serialize_tx_data(tx_info)
    ser_hex = ser[0].hex() + ser[1].hex() + ser[3].hex()
    hash2 = h.sha256(h.sha256(bytes.fromhex(ser_hex)).digest()).digest()
    print(hash2.hex())
    hash = txser.invert_bytes(hash2.hex())
    hash = h.sha256(bytes.fromhex(hash)).digest()
    hash = hash.hex()

    assert hash == "0a70cacb1ac276056e57ebfb0587d2091563e098c618eebf4ed205d123a3e8c4"


def test_get_tx_info():
    tx_id = "0a3fd98f8b3d89d2080489d75029ebaed0c8c631d061c2e9e90957a40e99eb4c.json"
    info = txmod.get_tx_info(tx_id)
    assert info == json.loads("""{
  "version": 2,
  "locktime": 834637,
  "vin": [
    {
      "txid": "b9b515b6171b47940809366f5d58591a56063db03fc39f678a03cb2b455f9428",
      "vout": 0,
      "prevout": {
        "scriptpubkey": "0014371e036c75b663254314287faa19c7b3f6c35e8a",
        "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 371e036c75b663254314287faa19c7b3f6c35e8a",
        "scriptpubkey_type": "v0_p2wpkh",
        "scriptpubkey_address": "bc1qxu0qxmr4ke3j2sc59pl65xw8k0mvxh52kt0x5m",
        "value": 293400650
      },
      "scriptsig": "",
      "scriptsig_asm": "",
      "witness": [
        "304402207ed00dfbbf904a6f24d43725fe3cd9d8fec2f5b6f6a7ac7b1e0816e39266ff7602200966bdee875f64538a655dd2a0bc548c3deb5fd717ec3e9e107d1233533cc23a01",
        "021160ee898d5480f4a193254338a6f289ab33a56ed639ca0b1504c9acffdf4fda"
      ],
      "is_coinbase": false,
      "sequence": 4294967294
    }
  ],
  "vout": [
    {
      "scriptpubkey": "00140d1c76c89fbba64867349c1ad0f3313e6b4b7d36",
      "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 0d1c76c89fbba64867349c1ad0f3313e6b4b7d36",
      "scriptpubkey_type": "v0_p2wpkh",
      "scriptpubkey_address": "bc1qp5w8djylhwnysee5nsddpue38e45klfk893yee",
      "value": 4402400
    },
    {
      "scriptpubkey": "001414989c53e65d603069bf506996f24f45f4a12107",
      "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 14989c53e65d603069bf506996f24f45f4a12107",
      "scriptpubkey_type": "v0_p2wpkh",
      "scriptpubkey_address": "bc1qzjvfc5lxt4srq6dl2p5eduj0gh62zgg8mqeurg",
      "value": 288994794
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