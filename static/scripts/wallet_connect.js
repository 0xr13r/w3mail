window.userWalletAddress = null
const connectWallet = document.getElementById('connectWallet')
const walletAddress = document.getElementById('walletAddress')
const connectToMetaMask = document.getElementById('connect_content')
const connectModalButton = document.getElementById('connectModalButton')
const composeButton = document.getElementById('composeButton')


function checkInstalled() {
    if (typeof window.ethereum == 'undefined') {
        console.log('Metamask not installed')
        connectToMetaMask.innerText = "MetaMask is not installed in this browser. Please install it to proceed 🦊."
        connectModalButton.innerText = "Install Metask"
        $("#connectModalButton").css("display", "none")
        $("#installMetaMask").css("display", "inline-block")
        $("#composeButton").css("display", "none")
        $('#connectedModal').modal({backdrop: 'static', keyboard: false},'show');
        connectToMetaMask.classList.remove()
        connectToMetaMask.classList.add()
        return false;
    }

    // connectWallet.addEventListener('click', connectWalletwithMetaMask)
    return true;
}

async function connectWalletwithMetaMask() {
    let accounts = await window.ethereum.request({
        method: 'eth_requestAccounts',
        params: [{
            eth_accounts: {},
        }]
    })
    .catch((e) => {
        console.error(e.message)
    });

    if( accounts[0] === window.userWalletAddress) {
        await window.ethereum.request({
            method: 'wallet_requestPermissions',
            params: [{
                eth_accounts: {},
            }]
        })
        .catch((e) => {
            console.error(e.message)
        })

        accounts = await window.ethereum.request({ method: 'eth_accounts' })
    }

    console.log(accounts)

    window.userWalletAddress = accounts[0]
    walletAddress.innerHTML = window.userWalletAddress

    storePublicKeyForMessageEncryption()
    return

}

async function storePublicKeyForMessageEncryption() {
    let pubkey_eth = await window.ethereum.request({
        method: "eth_getEncryptionPublicKey",
        params: [window.userWalletAddress], 
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
                window.location = "/inbox/"+ window.userWalletAddress;
            } 
            else {
                alert("Error connecting to wallet - public encryption key not stored. Please try again by reconnecting to MetaMask 🦊.");
                window.location = "/";
            };
        },
        error: function(err) {
            console.log(err);
        }
    });
}

async function checkConnectedWallet() {
    let accounts = await window.ethereum.request({ method: 'eth_accounts' })

    if ( accounts.length === 0 ){
        console.log("MetaMask installed but no wallet is connected")
        connectToMetaMask.innerText = "Please connect to MetaMask to begin 🦊."
        $("#installMetaMask").css("display", "none")
        $("#composeButton").css("display", "none")
        $('#connectedModal').modal({backdrop: 'static', keyboard: false},'show');
        return;
    }

    window.userWalletAddress = accounts[0]
    console.log("Connected with: " + window.userWalletAddress)

    walletAddress.innerText = window.userWalletAddress;
    if (connectToMetaMask) {
        connectToMetaMask.innerText = "";
    }
    
}


window.addEventListener('DOMContentLoaded', () => {
    if (checkInstalled()){
        console.log("MetaMask installed: True")
        checkConnectedWallet()
    }
    else {
        console.log("MetaMask installed: False")
    }
    
})