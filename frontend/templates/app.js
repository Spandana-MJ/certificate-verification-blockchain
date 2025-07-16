// app.js

const contractABI = [
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_certId",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_studentName",
          "type": "string"
        }
      ],
      "name": "verifyCertificate",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_certId",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_studentName",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_ipfsHash",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_dateOfIssue",
          "type": "uint256"
        }
      ],
      "name": "issueCertificate",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_certId",
          "type": "string"
        }
      ],
      "name": "getCertificateDetails",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ];
  const adminAddress = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"; // 🔥 Replace with your admin wallet

document.addEventListener('DOMContentLoaded', function () {
    const connectWalletButton = document.getElementById('connectWallet');
    const uploadForm = document.getElementById('uploadForm');
    const statusText = document.getElementById('status');

    if (connectWalletButton) {
        connectWalletButton.addEventListener('click', async () => {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                    const userAddress = accounts[0];

                    if (userAddress.toLowerCase() === adminAddress.toLowerCase()) {
                        uploadForm.style.display = "block";
                        connectWalletButton.style.display = "none";
                        statusText.innerText = "✅ Connected as Admin!";

                        // 🔥 Set wallet address into hidden input
                        document.getElementById('walletAddress').value = userAddress;

                    } else {
                        statusText.innerText = "❌ Access Denied: You are not Admin!";
                    }
                } catch (error) {
                    console.error(error);
                    statusText.innerText = "❌ Failed to connect wallet!";
                }
            } else {
                alert('Please install MetaMask extension first!');
            }
        });
    }
});
