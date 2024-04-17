#A function that receives multiples items, with size and fee, and return the best combination
#of items that fit in a certain space. This is a modified version of the knapsack alg for this 
#app.
#
#example: list of logical transactions
# items = [txid1, txid2, txid3, txid4, txid5]
# txid1 = {'size': 100, 'fee': 10}
# txid2 = {'size': 200, 'fee': 20}
# txid3 = {'size': 300, 'fee': 30}
# txid4 = {'size': 400, 'fee': 40}
# txid5 = {'size': 500, 'fee': 50}
# remaining size = 1000
# result = [txid1, txid4, txid5]

def tx_knapsack(tx_dict, remaining_size):
    #the input is a dict with the txid as key
    # and a list with the fee and size as value
 

    #this is the adpated knapsack to find the best 
    #combination of transactions that fit in the block
    #
    #
    #the items input is a list of dicts
    #{txid: [fee, size in bytes]}
    #
    #the total size of a block is 1mb = 1000000 bytes
    n = len(tx_dict)
    # Inicialização da matriz de memoização e rastreamento de chaves
    dp = [[0] * (remaining_size + 1) for _ in range(n + 1)]
    selected = [[[] for _ in range(remaining_size + 1)] for _ in range(n + 1)]
    
    # Preenchendo a matriz usando programação dinâmica
    for i in range(1, n + 1):
        key = list(tx_dict.keys())[i - 1]
        value, weight = tx_dict[key]
        for w in range(1, remaining_size + 1):
            if weight > w:
                dp[i][w] = dp[i - 1][w]
                selected[i][w] = selected[i - 1][w]
            else:
                if dp[i - 1][w] > dp[i - 1][w - weight] + value:
                    dp[i][w] = dp[i - 1][w]
                    selected[i][w] = selected[i - 1][w]
                else:
                    dp[i][w] = dp[i - 1][w - weight] + value
                    selected[i][w] = selected[i - 1][w - weight] + [key]
    
    # Retornar o valor máximo e as chaves correspondentes
    return selected[n][remaining_size]
    
    # Retornar o valor máximo e as chaves dos itens selecionados
   