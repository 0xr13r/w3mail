const ethUtil = require('ethereumjs-util');
const sigUtil = require('@metamask/eth-sig-util');
const atob = require('atob');

async function encryptData(publicKey, message, nonce) {

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


async function decryptData(cid) {

  console.log("Fetch encrypted message from IPFS")
  const accounts = await window.ethereum.request({ method: 'eth_accounts' })

  jQuery.ajax({
    type: "POST",
    url: '/fetch_cid_data',
    contentType: "application/json",
    data: JSON.stringify({ "ipfs_cid": cid }),
    dataType: "json",
    success: function (response) {
      if (response.success == true) {

        console.log("Decrypting your message")

        let data = response.data
        decryptMessageWithMM(data, accounts[0])

      }
      else {
        alert("Error fetching message from IPFS - please send a message with the IPFS CID of the message you are unable to open, to 0x4541906862a922b1149a408a4e1f197a3a558510 to raise a support ticket with us.");
        window.location = "/inbox/" + accounts[0];
      };
    },
    error: function (err) {
      console.log(err);
    }
  });

}

async function decryptMessageWithMM(data, account) {

  console.log(data.ipfs_cid)

  const decrypt = await window.ethereum.request({
    method: 'eth_decrypt',
    params: [data.encrypted_message_hex, account]
  });

  if (decrypt) {
    const decryptedMessage = decrypt.replace('b&#39;', '').replace('&#39;', '')

    var message_box = document.getElementById("messageContent");
    var message_from = document.getElementById("messageFrom");

    message_from.innerText =  "From: "+ data.sender_address + "\nSent At:" +data.message_sent_timestamp
    message_box.innerText = atob(decryptedMessage)
    $('#decryptedMessageBox').modal('show');


    jQuery.ajax({
      type: "POST",
      url: '/mark_read',
      contentType: "application/json",
      data: JSON.stringify({ "ipfs_cid": data.ipfs_cid }),
      dataType: "json",
      success: function (response) {
        if (response.success == true) {
          return true;
        }
      },
      error: function (err) {
        console.log(err);
      }
    });

  }
  else {
    alert("Get to fuck mate - You are unable to decrypt this message as your are not the recipient.");
    return false;
  };
  
}

module.exports = {
  'encryptData': encryptData,
  'decryptData': decryptData
};
