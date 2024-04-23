import calendar
from hashlib import sha256
import time
from tx import tx_knapsack as knap_mod, transactions as tx_mod, serialization as ser
import blockbuilder as bb_mod
def main():
    version = "00000020"
    gmt = time.gmtime()
    timestamp = calendar.timegm(gmt)
    difficulty = "0000ffff00000000000000000000000000000000000000000000000000000000"
    previous_block = "0000000000000000000000000000000000000000000000000000000000000000"
    difficulty_hash = bytes.fromhex(difficulty)
    difficulty_hash = difficulty_hash.hex()
    #gets in a list all the tx_ids in the mempool
    entries = tx_mod.get_tx_info("all")
    #gets some info about the txs, like fee and seralized size
    registered_txs = list()
    for entry in entries:
        registered_txs.append(tx_mod.valid_tx_values(entry))
    included_txs, fee = knap_mod.tx_KISS(registered_txs, 4000000 - 320)
    #concatenate version, transactions and sig  + locktime
    

    
    witnessroot = bb_mod.wmerkle_root(entries, 0, True)
    
    coinbase = bb_mod.build_coinbase_tx(fee, witnessroot)
    coinbaseid = coinbase[1]
    coinbase = coinbase[0]
    
    ##before entering the merkle root, the txids have to be inverted
    for i in range(len(included_txs)):
        included_txs[i] = tx_mod.get_tx_id(included_txs[i])

    merkle_root = bb_mod.merkle_root(included_txs, coinbaseid)
    included_txs.remove(coinbaseid)

    ##inverting all my txids, so it can be exposed as the real txid
    for i in range(len(included_txs)):
        included_txs[i] = ser.invert_bytes(included_txs[i])
    coinbaseid = ser.invert_bytes(coinbaseid.hex())

    timestamp = timestamp.to_bytes(4, byteorder='little')
    timestamp = timestamp.hex()
    merkle_root = merkle_root.hex()
    nonce = 0
    bits = bb_mod.build_bits(difficulty)
    bits = ser.invert_bytes(bits)
    is_mined = False
    while not is_mined:
        
        nonce_bytes = nonce.to_bytes(4, byteorder='little')
        nonce_bytes = nonce_bytes.hex()
        block_header = str(version) + str(previous_block) + str(merkle_root) + str(timestamp) + str(bits) + str(nonce_bytes)
        block_header = bytes.fromhex(block_header)
        block_hash = sha256(sha256(block_header).digest()).digest()
        block_header = block_header.hex()
        block_hash = block_hash.hex()
        block_hash_inverse = ser.invert_bytes(block_hash)
        
        if block_hash_inverse < difficulty_hash:
            block = bb_mod.build_block(block_header, included_txs, coinbase,coinbaseid)
            f = open("../../output.txt", "w")
            tx_output = open ("../../tx_output.txt", "w")
            f.write(block[0])
            f.write("\n")
            f.write(block[2])
            f.write("\n")
            for tx in block[3]:
                f.write(tx)
                f.write("\n")
                #tx_output.write(tx)
                #tx_output.write("\n")
                
            f.write("\n")
            is_mined = True
        else:
            nonce += 1


    
    
if __name__ == "__main__":
    main()