import transactions.transactions as tx_mod
import transactions.tx_knapsack as tx_knapsack

def main():
    entries = tx_mod.get_tx_info("all")
    tx_dict = dict()
    for txs in entries:
        tx_dict.update(tx_mod.valid_tx_values(txs))
    print(tx_knapsack.tx_knapsack(tx_dict, 1000000))

if __name__ == "__main__":
    main()