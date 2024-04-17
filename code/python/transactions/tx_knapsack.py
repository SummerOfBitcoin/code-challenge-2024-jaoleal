def tx_knapsack(txs_dict, remaining_size):
    #the input is a dict with the txid as key
    # and a list with the fee and size as value
    #{txid: [fee, size in bytes]}
    #
    #the total size of a block is 1mb = 1000000 bytes
    # A matrix of number of items x remaining size

    dp = [[0] * (remaining_size + 1) for _ in range(len(txs_dict) + 1)]
    selected_index = []
    for i in range(1, len(txs_dict) + 1):
        value, weight = txs_dict[i - 1]
        for w in range(1, remaining_size + 1):
            if weight > w:
                dp[i][w] = dp[i - 1][w]
            else:
                selected_index.append(i-1)
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
    selected_index = set(selected_index)
    
 
    # the return should be a new dict containing the selected txs with max possible fee
    return dp[len(txs_dict)][remaining_size], selected_index

def tx_greedy(tx_dict, remaining_size):
    #the input is a dict with the txid as key
    # and a list with the fee and size as value
    #{txid: [fee, size in bytes]}
    #
    #the total size of a block is 1mb = 1000000 bytes
    # A matrix of number of items x remaining size
    selected_index = []
    total_fee = 0
    total_size = 0
    for i in range(len(tx_dict)):
        if total_size + tx_dict[i][1] <= remaining_size:
            total_fee += tx_dict[i][0]
            total_size += tx_dict[i][1]
            selected_index.append(i)
    selected_index = set(selected_index)
    return total_fee, selected_index, total_size

def tx_KISS(tx_list, remaining_size):
    #sort the list by fee/size ratio
    tx_list = sorted(tx_list, key=lambda x: x[0]/x[1], reverse=True)
    used_size = int()
    fee = int()
    used_tx_list = list()
    for i in range(len(tx_list)):
        if used_size + tx_list[i][1] <= remaining_size:
            used_size += tx_list[i][1]
            fee += tx_list[i][0]
            used_tx_list.append(i)

    return fee, used_tx_list, set(used_tx_list)