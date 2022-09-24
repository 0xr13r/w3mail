const ethUtil = require('ethereumjs-util');
const sigUtil = require('@metamask/eth-sig-util');
const atob = require('atob');
const utf8 = require('utf8');

async function encryptData(publicKey, message, nonce)  {

  console.log("Encrypting your message")

  const encryptedMessage = ethUtil.bufferToHex(
    Buffer.from(
      JSON.stringify(
        sigUtil.encrypt({
          publicKey: publicKey,
          data: message,
          nonce: nonce,
          version: 'x25519-xsalsa20-poly1305',
        })
      ),
      'utf8'
    )
  );


  window.encrypted_message = encryptedMessage
  return encryptedMessage;
}


async function decryptData(data) {

  console.log("Decrypting your message")

  let accounts = await window.ethereum.request({ method: 'eth_accounts' })

  const decrypt = await window.ethereum.request({
    method: 'eth_decrypt',
    params: [data, accounts[0]],
  });

  const decryptedMessage = decrypt.replace('b&#39;','').replace('&#39;','')

  return atob(decryptedMessage);
}

module.exports = {
    'encryptData': encryptData,
    'decryptData': decryptData
};
