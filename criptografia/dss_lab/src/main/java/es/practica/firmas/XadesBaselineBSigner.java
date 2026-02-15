package es.practica.firmas;

import eu.europa.esig.dss.enumerations.DigestAlgorithm;
import eu.europa.esig.dss.enumerations.SignatureLevel;
import eu.europa.esig.dss.model.DSSDocument;
import eu.europa.esig.dss.model.FileDocument;
import eu.europa.esig.dss.model.ToBeSigned;
import eu.europa.esig.dss.model.SignatureValue;
import eu.europa.esig.dss.model.x509.CertificateToken;
import eu.europa.esig.dss.spi.client.http.IgnoreDataLoader;
import eu.europa.esig.dss.spi.x509.CommonCertificateVerifier;
import eu.europa.esig.dss.token.DSSPrivateKeyEntry;
import eu.europa.esig.dss.token.Pkcs12SignatureToken;
import eu.europa.esig.dss.xades.XAdESService;
import eu.europa.esig.dss.xades.signature.XAdESSignatureParameters;

import java.io.IOException;
import java.nio.file.Files;
import java.security.KeyStore;
import java.util.List;

public final class XadesBaselineBSigner {

    public void sign(SigningConfig config) throws IOException {
        DSSDocument documentToSign = new FileDocument(config.inputXml().toFile());

        try (Pkcs12SignatureToken token = new Pkcs12SignatureToken(
                new KeyStore.PasswordProtection(config.pkcs12Password().toCharArray()),
                config.pkcs12Path().toFile())) {

            DSSPrivateKeyEntry privateKey = token.getKeys().get(0);
            CertificateToken signingCertificate = privateKey.getCertificate();
            List<CertificateToken> chain = privateKey.getCertificateChain();

            XAdESSignatureParameters parameters = new XAdESSignatureParameters();
            parameters.setSignatureLevel(SignatureLevel.XAdES_BASELINE_B);
            parameters.setDigestAlgorithm(DigestAlgorithm.SHA256);
            parameters.setSigningCertificate(signingCertificate);
            parameters.setCertificateChain(chain);

            CommonCertificateVerifier verifier = new CommonCertificateVerifier();
            verifier.setDataLoader(new IgnoreDataLoader());

            XAdESService service = new XAdESService(verifier);
            if (config.hasTsp()) {
                service.setTspSource(TspSourceFactory.create(config));
                parameters.setSignatureLevel(SignatureLevel.XAdES_BASELINE_T);
            }

            ToBeSigned dataToSign = service.getDataToSign(documentToSign, parameters);
            SignatureValue signatureValue = token.sign(dataToSign, parameters.getDigestAlgorithm(), privateKey);
            DSSDocument signed = service.signDocument(documentToSign, parameters, signatureValue);

            try (var in = signed.openStream()) {
                Files.write(config.outputXml(), in.readAllBytes());
            }
        }
    }
}
