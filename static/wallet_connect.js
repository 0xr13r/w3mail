window.userWalletAddress = null
const connectWallet = document.getElementById('connectWallet')
const walletAddress = document.getElementById('walletAddress')

function checkInstalled() {
    if (typeof window.ethereum == 'undefined') {
        console.log(connectWallet)
        connectWallet.innerText = 'MetaMask isnt installed, please install it'
        connectWallet.classList.remove()
        connectWallet.classList.add()
        return false
    }

    connectWallet.addEventListener('click', connectWalletwithMetaMask)
}

async function connectWalletwithMetaMask() {
    let accounts = await window.ethereum.request({ method: 'eth_accounts' })

    if (!accounts) {
        await window.ethereum.request({ method: 'eth_requestAccounts' })
            .catch((e) => {
                console.error(e.message)
            })
    }
    else {
        await window.ethereum.request({
            method: 'wallet_requestPermissions',
            params: [{
                eth_accounts: {},
            }]
        })
            .catch((e) => {
                console.error(e.message)
            })
       
        await window.ethereum.request({ method: 'eth_requestAccounts' })

    }

    accounts = await window.ethereum.request({ method: 'eth_accounts' })
    window.userWalletAddress = accounts[0]
    walletAddress.innerHTML = "You are signed in with: " + window.userWalletAddress
    return

}


async function checkConnectedWallet() {
    const accounts = await window.ethereum.request({ method: 'eth_accounts' })

    if (!accounts || accounts[0] == undefined) {
        walletAddress.innerHTML = "No Wallet Connected"
        connectWallet.innerText = "Connect Wallet"
        return
    }

    window.userWalletAddress = accounts[0]
    walletAddress.innerHTML = "You are signed in with: " + window.userWalletAddress
    connectWallet.innerText = "Switch Wallet"
}

window.addEventListener('DOMContentLoaded', () => {
    checkInstalled()
    checkConnectedWallet()
})