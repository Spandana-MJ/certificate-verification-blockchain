# 🎓 Blockchain Certificate Verification System

This project is a decentralized application (DApp) built with **Flask**, **Solidity**, and **IPFS**, allowing institutions to issue and verify academic certificates using the **blockchain**.

---

## 🚀 Features

- Admin login with MetaMask
- Upload certificate to IPFS
- Store metadata on blockchain
- Student login with wallet
- Verify, view, download, and share certificates

---

## 🛠️ Technologies Used

- Solidity (Smart Contract)
- Flask (Backend)
- HTML/CSS/JS
- IPFS (Certificate storage)
- Web3.js & MetaMask

---

## 🖼️ Project Screenshots

### 🧑‍💼 Admin Dashboard
![Admin Dashboard](images/admin-dashboard.png)

### 🗂️ Upload Certificate
![Upload Certificate](images/upload-certificate.png)

### 🦊 MetaMask Login
![MetaMask](images/metamask.png)

### 🎓 Student Dashboard
![Student Dashboard](images/student-dashboard.png)

### ✅ Certificate Verification System
![Certificate Verification System](images/Certificate-verification-system.png)

---

## 📁 Folder Structure

```
.
├── app.py                      # Flask backend
├── contracts/                 # Solidity smart contracts
│   └── CertificateVerification.sol
├── frontend/                  # Frontend templates and static files
│   ├── templates/
│   │   ├── admin_dashboard.html
│   │   ├── student_dashboard.html
│   └── static/
│       └── css, js, images...
├── images/                    # Screenshots used in README
├── .env                       # Environment variables (ignored in .gitignore)
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. 🔧 Clone the repository

```bash
git clone https://github.com/Spandana-MJ/blockchain-certificate-verification.git
cd blockchain-certificate-verification
```

### 2. 📦 Install backend dependencies

```bash
pip install -r requirements.txt
```

### 3. 🔗 Compile & deploy smart contract (using Hardhat or Remix)

- Compile `CertificateVerification.sol`
- Deploy to a local or test Ethereum network (e.g. Ganache or Polygon Mumbai)
- Copy the deployed contract address and ABI

### 4. 📝 Create `.env` file

```env
CONTRACT_ADDRESS=your_deployed_contract_address
WEB3_PROVIDER=https://your_rpc_provider
PINATA_API_KEY=your_pinata_key
PINATA_SECRET_API_KEY=your_pinata_secret
```

> Make sure `.env` is listed in `.gitignore`

---

## ▶️ Run the Application

```bash
python app.py
```

Access it at: `http://127.0.0.1:5000`

---

## 🧪 Usage Flow

1. **Admin logs in via MetaMask**  
2. **Uploads a certificate** → stored on **IPFS**  
3. **Smart contract** stores metadata  
4. **Student logs in** via wallet → can view, verify, and download the certificate  

---

## 📌 Future Enhancements

- Email notifications to students  
- Multi-user role support  
- Add QR code for certificate verification  
- Deploy on Ethereum mainnet or Polygon

---

## 🙌 Acknowledgements

- [Web3.py](https://web3py.readthedocs.io/)
- [Pinata](https://www.pinata.cloud/)
- [MetaMask](https://metamask.io/)
- [IPFS](https://ipfs.io/)
- [Ethereum](https://ethereum.org/)