from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from web3 import Web3
from dotenv import load_dotenv
from flask import make_response
import os
import json
import datetime
import requests
import hashlib

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_key")

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS").strip())
ADMIN_WALLET = Web3.to_checksum_address(os.getenv("ADMIN_WALLET").strip())

# Load smart contract ABI
with open('blockchain/artifacts/contracts/certification-verification.sol/CertificateVerification.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# Pinata API keys
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")

# =================== Routes ===================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/verify_wallet', methods=['POST'])
def verify_wallet():
    data = request.get_json()
    wallet = data.get('wallet', '').strip()
    if not wallet:
        return jsonify({"status": "error", "message": "Wallet address is required."}), 400

    try:
        wallet_checksum = Web3.to_checksum_address(wallet)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid wallet address format."}), 400

    if wallet_checksum == ADMIN_WALLET:
        session['role'] = 'admin'
        return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "Unauthorized wallet"}), 401



@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))

    response = make_response(render_template('admin_dashboard.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/admin/upload', methods=['GET', 'POST'])
def admin_upload():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        student_name = request.form.get('student_name')
        wallet_address_raw = request.form.get('wallet_address', '').strip()
        certificate_file = request.files.get('certificate_file')

        if not certificate_file:
            return "No file selected", 400

        try:
            wallet_address = Web3.to_checksum_address(wallet_address_raw)
        except ValueError:
            return "Invalid wallet address format", 400

        # Calculate SHA-256 hash of the certificate file
        certificate_file.stream.seek(0)
        file_bytes = certificate_file.read()
        cert_hash = hashlib.sha256(file_bytes).hexdigest()
        certificate_file.stream.seek(0)

        # Upload to Pinata
        headers = {
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_SECRET_API_KEY
        }
        files = {'file': (certificate_file.filename, certificate_file.stream, certificate_file.content_type)}
        res = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS", files=files, headers=headers)

        if res.status_code != 200:
            return f"Pinata upload failed: {res.text}", 500

        ipfs_hash = res.json()['IpfsHash']
        timestamp = int(datetime.datetime.now().timestamp())

        tx_hash = contract.functions.issueCertificate(
            cert_hash,
            student_name,
            ipfs_hash,
            timestamp,
            wallet_address
        ).transact({'from': ADMIN_WALLET})
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return render_template('upload_success.html', cert_hash=cert_hash, student_name=student_name)

    return render_template('upload.html')

@app.route('/student_login')
def student_login_page():
    return render_template('student_login.html')

@app.route('/login/student', methods=['POST'])
def login_student():
    session['role'] = 'student'
    session['wallet'] = request.form.get('wallet_address', '').strip()
    return redirect(url_for('student_dashboard'))

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('home'))

    wallet = session.get('wallet')
    if not wallet:
        return redirect(url_for('home'))

    try:
        wallet_checksum = Web3.to_checksum_address(wallet)
    except ValueError:
        return "Invalid wallet address", 400

    try:
        cert_hashes = contract.functions.getCertificatesByWallet(wallet_checksum).call()
    except:
        cert_hashes = []

    certs = []
    for cert_hash in cert_hashes:
        try:
            cert = contract.functions.getCertificateDetails(cert_hash).call()
            certs.append({
                'cert_hash': cert_hash,
                'student_name': cert[0],
                'ipfs_url': f"https://gateway.pinata.cloud/ipfs/{cert[1]}",
                'ipfs_hash': cert[1], 
                'timestamp': datetime.datetime.fromtimestamp(cert[2], datetime.UTC).strftime('%Y-%m-%d %H:%M:%S'),
                'is_valid': cert[3]
            })
        except:
            continue

    return render_template('student_dashboard.html', certs=certs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))



@app.route('/verify', methods=['GET', 'POST'])
def verify_certificate():
    if request.method == 'POST':
        certificate_file = request.files.get('certificate_file')
        student_name = request.form.get('student_name').strip()

        if not certificate_file:
            return render_template('verify.html', error="No certificate file uploaded.")

        # Generate SHA-256 hash of the uploaded file
        certificate_file.stream.seek(0)
        file_bytes = certificate_file.read()
        cert_hash = hashlib.sha256(file_bytes).hexdigest()

        try:
            cert = contract.functions.getCertificateDetails(cert_hash).call()
        except:
            return render_template('verify.html', error="Certificate not found on blockchain.")

        # Verify name and validity
        is_valid = cert[3] and cert[0] == student_name
        if not is_valid:
            return render_template('verify.html', error="Invalid certificate or name mismatch.")

        cert_data = {
            'student_name': cert[0],
            'cert_hash': cert_hash,
            'ipfs_hash': cert[1],
            'timestamp': datetime.datetime.fromtimestamp(cert[2], datetime.UTC).strftime('%Y-%m-%d %H:%M:%S'),
            'is_valid': cert[3]
        }

        return render_template('certificate_view.html', cert=cert_data)

    return render_template('verify.html')


@app.route('/download', methods=['POST'])
def download_certificate():
    cert_hash = request.form.get('cert_hash')
    student_name = request.form.get('student_name')

    try:
        cert = contract.functions.getCertificateDetails(cert_hash).call()
    except:
        return render_template('download.html', error="Certificate not found.")

    if cert[0] != student_name or not cert[3]:
        return render_template('download.html', error="Invalid details or not verified.")

    ipfs_url = f"https://gateway.pinata.cloud/ipfs/{cert[1]}"
    return render_template('download.html', cert_hash=cert_hash, ipfs_url=ipfs_url)

# =================== Run App ===================

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(debug=True) 