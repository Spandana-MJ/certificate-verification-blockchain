async function main() {
  const CertificateVerification = await ethers.getContractFactory("CertificateVerification");
  const certificate = await CertificateVerification.deploy();

  await certificate.waitForDeployment();

  console.log(`CertificateVerification deployed to: ${await certificate.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
