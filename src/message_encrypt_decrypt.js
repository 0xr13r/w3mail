const ethUtil = require('ethereumjs-util');
const sigUtil = require('@metamask/eth-sig-util');
const ascii85 = require('ascii85');

async function encryptData(publicKey, message)  {

  console.log("Encrypting message")

  const encryptedMessage = ethUtil.bufferToHex(
    Buffer.from(
      JSON.stringify(
        sigUtil.encrypt({
          publicKey: publicKey,
          data: message,
          version: 'x25519-xsalsa20-poly1305',
        })
      ),
      'utf8'
    )
  );

  window.encrypted_message = encryptedMessage

  console.log(encryptedMessage);
  return encryptedMessage;
}


async function decryptData(data) {

  console.log("Decrypting Data")

  let accounts = await window.ethereum.request({ method: 'eth_accounts' })

  console.log(accounts[0])

  console.log(data)

  const structuredData = {
    version: 'x25519-xsalsa20-poly1305',
    ephemPublicKey: data.slice(0, 32).toString('base64'),
    nonce: data.slice(32, 56).toString('base64'),
    ciphertext: data.slice(56).toString('base64'),
  };

  const ct = `0x${Buffer.from(JSON.stringify(structuredData), 'utf8').toString('hex')}`;

  
  const decrypt = await window.ethereum.request({
    method: 'eth_decrypt',
    params: [data, accounts[0]],
  });

  console.log(ascii85.decode(decrypt))
  
  return ascii85.decode(decrypt);
}


module.exports = {
    'encryptData': encryptData,
    'decryptData':decryptData
};
