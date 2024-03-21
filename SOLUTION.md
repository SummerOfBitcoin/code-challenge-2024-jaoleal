# Solution
To mine a block and get the maximum amout of sats i have to build to build the block header that consist in;
- Version (at the moment, not specified, so ill 00000001)
- previousblockhash (at the moment, not specified, so ill use some random sha256 hash or ingore it).
- Merkle root see [Making Merkle Root](#Making_The_Merkle_Root)
- Timestamp I will use 1710997192 or some function to get the timestamp at the minig process
- Difficulty target that is 0000ffff00000000000000000000000000000000000000000000000000000000, meaning 4 zeroes.
- and the nonce, see [Finding the nonce](#Finding_The_Nonce)


## Making The Merkle Root


## Finding The Nonce


## Development Process
Since i have the transactions, I will focus in finding the best Merkle Root building an efficient Merkle Root algorithm

### Eficiency and optimization 
First i will prototype in python and later re-write everything in rust... i think that this is the best way to write good code, without bugs and test covered.