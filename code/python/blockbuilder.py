import hashlib as h
import json
import tx.transactions as txmod
import tx.serialization as txser

def build_block(block_header, txids, coinbase, coinbaseid):
    tx_count = ((len(txids) + 1).to_bytes(4, byteorder='big')).hex()
    ids = []
    for i in range(len(txids)):
        buff =str(txids[i])
        buff.replace(".json", "")
        ids.insert(len(ids),buff)
    ids.insert(0, coinbaseid)
    return block_header,tx_count, coinbase, ids

def build_coinbase_tx(fee, witness_root):
    tx_json = """
        {
        "version": 1,
        "locktime": 0,
        "vin": [
            {
            "txid": "0000000000000000000000000000000000000000000000000000000000000000",
            "vout": 4294967295,
            "scriptsig": "04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73",
            "sequence": 4294967295
            }
        ],
        "vout": [
            {
            "value": "00f2052a01000000",
            "scriptpubkeysize": "43",
            "scriptpubkey": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac"
            }
        ]
        }
        """
    tx_data = json.loads(tx_json)
    tx_data["vout"][0]["value"] = fee + 50
    tx_data["vout"].insert(1, json.loads(
        """ 
            {
            "value": 0,
            "scriptpubkeysize": "43",
            "scriptpubkey": ""
            }
            """
    ))
    witness_hash = h.sha256(h.sha256(witness_root +  bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000")).digest()).digest()
    tx_data["vout"][1]["scriptpubkey"] = bytes.fromhex("6a24aa21a9ed").hex() + txser.invert_bytes(witness_hash.hex() )
    witness = bytes.fromhex("01200000000000000000000000000000000000000000000000000000000000000000")

    ret = txser.serialize_tx_data(tx_data)
    marker =  bytes.fromhex("0001")
    coinbaseid = h.sha256(h.sha256(ret[1] + ret[2] + ret[4]).digest()).digest()
    ret = ret[1].hex()+ marker.hex()+ ret[2].hex()  + ret[3].hex() + witness.hex() + ret[4].hex()
    return ret, coinbaseid 

def merkle_root(txids,coinbase = 0, first_wave = True, ):
    #The default value for coinbase is 0, if zero, does not include coinbase
    if coinbase != 0:
        txids.insert(0, coinbase)
    if len(txids)  <= 1:
        return txids[0]
    new_txids = []
    for i in range(0, len(txids), 2):
        hash1 = txids[i]
        if i+1 >= len(txids):
            hash2 = txids[i]
        else:
            hash2 = txids[i+1]
        
        #if is the first wave, we need to calculate the hash of the txs
        if first_wave:
            #If the first txid is not coinbase, we need to calculate the hash of the of the first tx
            if not txids[i] == coinbase:
                hash1 = bytes.fromhex(txids[i])
            if i+1 >= len(txids):
                hash2 = bytes.fromhex(txids[i])
            else:    
                hash2 = bytes.fromhex(txids[i + 1])
        new_txids.append((h.sha256(h.sha256(hash1 + hash2).digest()).digest()))
    return merkle_root(new_txids,0, False)

def wmerkle_root(txids, first_wave = True, ):
    #The default value for coinbase is 0, if zero, does not include coinbase
    if first_wave:
        txids.insert(0, bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"))
    if len(txids)  <= 1:
        return txids[0]
    new_txids = []
    for i in range(0, len(txids), 2):
        hash1 = txids[i]
        if i+1 >= len(txids):
            hash2 = txids[i]
        else:
            hash2 = txids[i+1]
        
        #if is the first wave, we need to calculate the hash of the txs
        if first_wave:
            #If the first txid is not coinbase, we need to calculate the hash of the of the first tx
            if txids[i] != bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"):
                txid = txser.serialize_tx_data(txmod.get_tx_info(txids[i]))
                if txid[0]:
                    hash1 = txid[1].hex() + txid[2].hex() + txid[3].hex() + txid[4].hex() + txid[5].hex()
                else:
                    hash1 = txid[1].hex() + txid[2].hex()+ txid[4].hex()
                hash1 = h.sha256(h.sha256(bytes.fromhex(hash1)).digest()).digest()
            else:
                hash1 = txids[i]
            if i+1 >= len(txids):
                txid = txser.serialize_tx_data(txmod.get_tx_info(txids[i]))
                if txid[0]:
                    hash2 = txid[1].hex() + txid[2].hex() + txid[3].hex() + txid[4].hex() + txid[5].hex()
                else:
                    hash2 = txid[1].hex() + txid[2].hex()+ txid[4].hex()
                hash2 = h.sha256(h.sha256(bytes.fromhex(hash2)).digest()).digest()
            else:
                txid = txser.serialize_tx_data(txmod.get_tx_info(txids[i + 1]))
                if txid[0]:
                    hash2 = txid[1].hex() + txid[2].hex() + txid[3].hex() + txid[4].hex() + txid[5].hex()
                else:
                    hash2 = txid[1].hex() + txid[2].hex()+ txid[4].hex()
                hash2 = h.sha256(h.sha256(bytes.fromhex(hash2)).digest()).digest()

        new_txids.append((h.sha256(h.sha256(hash1 + hash2).digest()).digest()))
    return merkle_root(new_txids,0, False)

def build_bits(difficulty):
    # convert the difficulty to shorty format
    # the function input is the difficulty in hex format
    difficulty = bytes.fromhex(difficulty)
    difficulty =  difficulty[::-1]
    exponent = bytearray()
    coefficient = bytearray()

    for i, val in enumerate(difficulty):
        if val != 0x00:
            back = int()
            
            for j in range(0, len(difficulty) - i):
                if difficulty[i + j] == 0x00:
                    back = j
                    coefficient = difficulty[i + j - 3:i + j]
                    coefficient = coefficient[::-1]
                    if coefficient[2] == 0x00:
                        coefficient = (0x00).to_bytes(1, byteorder='big') + coefficient[:2]
                        back += 1
                    break
            exponent = (i + back).to_bytes(1, byteorder='big')
            break
    coefficient_hex = coefficient.hex()
    exponent_hex = exponent.hex()
    bits = exponent_hex + coefficient_hex
    return bits