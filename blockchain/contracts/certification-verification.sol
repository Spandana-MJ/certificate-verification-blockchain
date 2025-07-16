// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateVerification {
    struct Certificate {
        string studentName;
        string ipfsHash;
        uint256 dateOfIssue;
        bool isValid;
        address studentWallet;
    }

    mapping(string => Certificate) public certificates;
    mapping(address => string[]) private walletToCertificates;

    function issueCertificate(
        string memory _certId,
        string memory _studentName,
        string memory _ipfsHash,
        uint256 _dateOfIssue,
        address _studentWallet
    ) public {
        certificates[_certId] = Certificate(_studentName, _ipfsHash, _dateOfIssue, true, _studentWallet);
        walletToCertificates[_studentWallet].push(_certId);
    }

    function verifyCertificate(string memory _certId, string memory _studentName) public view returns (bool) {
        Certificate memory cert = certificates[_certId];
        return cert.isValid && keccak256(bytes(cert.studentName)) == keccak256(bytes(_studentName));
    }

    function getCertificateDetails(string memory _certId) public view returns (string memory, string memory, uint256, bool, address) {
        Certificate memory cert = certificates[_certId];
        return (cert.studentName, cert.ipfsHash, cert.dateOfIssue, cert.isValid, cert.studentWallet);
    }

    function getCertificatesByWallet(address _wallet) public view returns (string[] memory) {
        return walletToCertificates[_wallet];
    }
}
