// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "./Certification.sol"; 

contract CertificateVerifier {
    Certification public certificationContract;

    constructor(address _certificationAddress) {
        certificationContract = Certification(_certificationAddress);
    }

    function isCertificateTampered(
        string memory _certificate_id,
        string memory _uid,
        string memory _candidate_name,
        string memory _course_name,
        string memory _org_name,
        string memory _ipfs_hash
    ) 
    public view returns (bool) {(
            string memory storedUid,
            string memory storedCandidateName,
            string memory storedCourseName,
            string memory storedOrgName,
            string memory storedIpfsHash
        ) = certificationContract.getCertificate(_certificate_id);

        bool tampered = keccak256(abi.encodePacked(_uid)) !=
            keccak256(abi.encodePacked(storedUid)) ||
            keccak256(abi.encodePacked(_candidate_name)) !=
            keccak256(abi.encodePacked(storedCandidateName)) ||
            keccak256(abi.encodePacked(_course_name)) !=
            keccak256(abi.encodePacked(storedCourseName)) ||
            keccak256(abi.encodePacked(_org_name)) !=
            keccak256(abi.encodePacked(storedOrgName)) ||
            keccak256(abi.encodePacked(_ipfs_hash)) !=
            keccak256(abi.encodePacked(storedIpfsHash));

        return tampered;
    }

    // Function to get the stored certificate details for comparison purposes
    function getStoredCertificate(
        string memory _certificate_id
    )
        public
        view
        returns (
            string memory _uid,
            string memory _candidate_name,
            string memory _course_name,
            string memory _org_name,
            string memory _ipfs_hash
        )
    {
        return certificationContract.getCertificate(_certificate_id);
    }
}
