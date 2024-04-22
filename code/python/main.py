from hashlib import sha256
from tx import tx_knapsack as knap_mod, transactions as tx_mod
import blockbuilder as bb_mod
def main():
    version = "00000020"
    timestamp = 1710997192
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
    included_txs, fee = knap_mod.tx_KISS(registered_txs, 1000000 - 100)

    coinbase = bb_mod.build_coinbase_tx(fee)
    #concatenate transactions and sig  + locktime 
    coinbase = coinbase[0] + coinbase[2]
    coinbaseid = sha256(sha256(coinbase).digest()).digest()
    merkle_root = bb_mod.merkle_root(included_txs, coinbaseid)
    #for some reason python decides now that will use pointers to list
    included_txs.remove(coinbaseid)
    timestamp = timestamp.to_bytes(4, byteorder='little')
    timestamp = timestamp.hex()
    merkle_root = merkle_root.hex()
    nonce = 0
    bits = bb_mod.build_bits(difficulty)
    is_mined = False
    while not is_mined:
        
        nonce_bytes = nonce.to_bytes(4, byteorder='little')
        nonce_bytes = nonce_bytes.hex()
        block_header = str(version) + str(previous_block) + str(merkle_root) + str(timestamp) + str(bits) + str(nonce_bytes)
        block_hash = sha256(sha256(block_header.encode()).digest()).hexdigest()
        if block_hash < difficulty_hash:
            block = bb_mod.build_block(block_header, included_txs, coinbase,coinbaseid)
            f = open("../../output.txt", "w")
            print(block_header)
            f.write(block[0])
            f.write("\n")
            f.write(block[1])
            f.write("\n")
            for tx in block[2]:
                tx.replace(".json", "")
                f.write(tx)
            f.write("\n")
            is_mined = True
        else:
            nonce += 1


    
    
if __name__ == "__main__":
    main()