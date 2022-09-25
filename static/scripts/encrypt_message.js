

// in order to encrypt the message with the recipients public key we need to retrieve this from a previous 
// txn from their address. All w3mail users will have to make a txn on ethereum to purchase a w3mail erc721
// token, which is used to tokengate the dapp, so only users holding the token can send messages via w3mail
async function getRecipientPublicKey() {
    const Transaction = require('ethereumjs-tx')
    let txHash = '0x0a44e9331278e3ea48ac29e30fd77ce0252cf53812da873c800f862a2fefda7f' 
    const tx = web3.eth.getTransaction(txHash) 
    const pubkey = new Transaction({
        nonce: tx.nonce,
        gasPrice: `0x${tx.gasPrice.toString(16)}`,
        gasLimit: tx.gas,
        to: tx.to,
        value: `0x${tx.value.toString(16)}`,
        data: tx.input,
        chainId: 1,
        r: tx.r,
        s: tx.s,
        v: tx.v,
    }).getSenderPublicKey()
    console.log(pubkey.toString('hex'))
}

// async function encryptMessage(address) {
//     const keyB64 = await window.ethereum.request({
//         method: 'eth_getEncryptionPublicKey',
//         params: [address],
//     });
//     const publicKey = Buffer.from(String(keyB64), 'base64');

//     console.log(publicKey)
// }