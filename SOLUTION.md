# Solution
To mine a block and get the maximum amout of sats i have to build to build the block header that consist in;
- Version (at the moment, not specified, so i'll use 00000001)
- Merkle root see [Making Merkle Root](#Making_The_Merkle_Root)
- Timestamp I will use 1710997192 or some function to get the timestamp at the minig process
- Difficulty target that is 0000ffff00000000000000000000000000000000000000000000000000000000, meaning 4 zeroes.
- and the nonce, see [Finding the nonce](#Finding_The_Nonce)


## Making The Merkle Root

The Merkle Root is basically a tree structure that hashes the tx ids until you got only one for validating the transactions composition... in this way, changing one tx id will change all the Merkle Root.
![alt text](image.png)
but the Merkle root can only have valid tx ids and you have to verify the weight of the block when adding transactions, the weight being 4 mbs.

To achieve this i need

## Finding The Nonce


## Development Process
Since i have the transactions, I will focus in finding the best Merkle Root building an efficient Merkle Root algorithm

### Eficiency and optimization 
First i will prototype in python and later re-write everything in rust... i think that this is the best way to write good code, without bugs and test covered.