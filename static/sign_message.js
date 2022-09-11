async function signMessage(message_to_sign) {
    let signature = await window.ethereum.request({ method: "personal_sign",
    params: [
      window.userWalletAddress,
      message_to_sign
    ]
    }).catch((err)=> {
        console.log(err)
    })
    

    console.log(signature)

    if (!signature) { return messageSigned.innerText = "Not signed in. Connect your Metamask" }
        
    messageSigned.innerText = "Message signature: " + signature
  }