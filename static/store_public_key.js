async function storePublicKeyForMessageEncryption() {
    let pubkey_eth = await window.ethereum.request({
        "method": "eth_getEncryptionPublicKey",
        "params": [window.userWalletAddress], 
    });

    var address_pubkey_kv = {
        "wallet_address": window.userWalletAddress,
        "public_key": pubkey_eth
    }

    jQuery.ajax({
        type: "POST",
        url: '/',
        contentType: "application/json",
        data: JSON.stringify(address_pubkey_kv),
        dataType: "json",
        success: function(response) {
            if (response.success == true) {
                alert("Wallet: "+  window.userWalletAddress + " succesfully connected. Redirecting to inbox 📥");
                window.location = "/inbox";
            };
        },
        error: function(err) {
            console.log(err);
        }
    });
}

