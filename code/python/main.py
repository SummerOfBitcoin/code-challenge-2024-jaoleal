import transactions.transactions as tx_mod

def main():
    
    entries = tx_mod.get_tx_info("all")
    tx_array = [tx_mod.valid_tx_array(txs) for txs in entries]
    for array in tx_array:
        if len(array) > 2:
            print(array)
            print() 
    return 0

if __name__ == "__main__":
    main()