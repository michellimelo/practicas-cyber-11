#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-./dss_lab}"
PKG_DIR="$TARGET_DIR/src/main/java/es/practica/firmas"

mkdir -p "$PKG_DIR"

cat > "$TARGET_DIR/pom.xml" <<'POM'
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>es.practica</groupId>
    <artifactId>dss-lab</artifactId>
    <version>0.1.0-SNAPSHOT</version>
    <name>dss-lab</name>
    <description>Starter para firmas europeas con DSS (XAdES/CAdES/PAdES)</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <dss.version>6.1</dss.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>eu.europa.ec.joinup.sd-dss</groupId>
            <artifactId>dss-document</artifactId>
            <version>${dss.version}</version>
        </dependency>
        <dependency>
            <groupId>eu.europa.ec.joinup.sd-dss</groupId>
            <artifactId>dss-xades</artifactId>
            <version>${dss.version}</version>
        </dependency>
        <dependency>
            <groupId>eu.europa.ec.joinup.sd-dss</groupId>
            <artifactId>dss-cades</artifactId>
            <version>${dss.version}</version>
        </dependency>
        <dependency>
            <groupId>eu.europa.ec.joinup.sd-dss</groupId>
            <artifactId>dss-pades</artifactId>
            <version>${dss.version}</version>
        </dependency>
        <dependency>
            <groupId>eu.europa.ec.joinup.sd-dss</groupId>
            <artifactId>dss-service</artifactId>
            <version>${dss.version}</version>
        </dependency>
        <dependency>
            <groupId>eu.europa.ec.joinup.sd-dss</groupId>
            <artifactId>dss-token</artifactId>
            <version>${dss.version}</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>2.0.16</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <mainClass>es.practica.firmas.DssLabApp</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
POM

cat > "$TARGET_DIR/README.md" <<'README'
# DSS Lab (Java) - Base recomendada

Base práctica para firma avanzada europea con DSS.

## Estado del repositorio
- Se ha simplificado el proyecto para mantener una sola implementación activa en **Java + DSS**.
- El flujo principal (UI + CLI) vive en este módulo.

## Soporte objetivo
- XAdES (B/T/LT/LTA)
- CAdES
- PAdES
- TSP RFC3161

## Requisitos
- Java 17+
- Maven 3.9+

## Interfaz gráfica Java (recomendada)
```bash
mvn -q -DskipTests exec:java -Dexec.args="ui"
```

## CLI (alternativa)
1. Copia/edita `signing-example.properties`.
2. Ejecuta:

```bash
mvn -q -DskipTests exec:java -Dexec.args="sign-xades ./signing-example.properties"
```

## Notas
- Si `tsp.url` está vacío: genera **XAdES-B**.
- Si `tsp.url` está informado: intenta **XAdES-T**.
README

cat > "$TARGET_DIR/signing-example.properties" <<'PROPS'
# Entrada XML a firmar
input.xml=./sample-input.xml

# Salida XML firmada
output.signed.xml=./sample-signed.xml

# PKCS#12 del firmante
pkcs12.path=./firma-demo.p12
pkcs12.password=changeit

# Para elevar a XAdES-T, configura tsa url.
# Si lo dejas vacío, se firma en XAdES-B.
tsp.url=
tsp.username=
tsp.password=
PROPS

cat > "$TARGET_DIR/sample-input.xml" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<Factura>
  <Numero>2026-0001</Numero>
  <Emisor>Laboratorio Firma</Emisor>
  <Importe>100.00</Importe>
</Factura>
XML

cat > "$PKG_DIR/DssCapabilityReport.java" <<'JAVA'
package es.practica.firmas;

import java.util.LinkedHashMap;
import java.util.Map;

public record DssCapabilityReport(Map<String, String> capabilities) {

    public static DssCapabilityReport defaultReport() {
        Map<String, String> caps = new LinkedHashMap<>();
        caps.put("XMLDSig", "Soporte vía módulo dss-xades");
        caps.put("XAdES", "Soporte completo (B/T/LT/LTA) con DSS");
        caps.put("CAdES", "Soporte completo con dss-cades");
        caps.put("PAdES", "Soporte completo con dss-pades");
        caps.put("TSP", "Integrable con fuentes RFC3161 en servicios DSS");
        caps.put("Validación europea", "Compatible con políticas eIDAS en flujo DSS");
        return new DssCapabilityReport(caps);
    }
}
JAVA

cat > "$PKG_DIR/SigningConfig.java" <<'JAVA'
package es.practica.firmas;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

public record SigningConfig(
        Path inputXml,
        Path outputXml,
        Path pkcs12Path,
        String pkcs12Password,
        String tspUrl,
        String tspUsername,
        String tspPassword
) {

    public static SigningConfig fromPropertiesFile(Path file) throws IOException {
        Properties p = new Properties();
        try (InputStream in = Files.newInputStream(file)) {
            p.load(in);
        }

        return new SigningConfig(
                Path.of(require(p, "input.xml")),
                Path.of(require(p, "output.signed.xml")),
                Path.of(require(p, "pkcs12.path")),
                require(p, "pkcs12.password"),
                p.getProperty("tsp.url", "").trim(),
                p.getProperty("tsp.username", "").trim(),
                p.getProperty("tsp.password", "").trim()
        );
    }

    public boolean hasTsp() {
        return !tspUrl.isBlank();
    }

    private static String require(Properties p, String key) {
        String value = p.getProperty(key);
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Falta propiedad requerida: " + key);
        }
        return value.trim();
    }
}
JAVA

cat > "$PKG_DIR/TspSourceFactory.java" <<'JAVA'
package es.practica.firmas;

import eu.europa.esig.dss.service.http.commons.CommonsDataLoader;
import eu.europa.esig.dss.service.tsp.OnlineTSPSource;

public final class TspSourceFactory {

    private TspSourceFactory() {
    }

    public static OnlineTSPSource create(SigningConfig config) {
        OnlineTSPSource tspSource = new OnlineTSPSource(config.tspUrl());
        CommonsDataLoader dataLoader = new CommonsDataLoader();
        if (!config.tspUsername().isBlank()) {
            dataLoader.addAuthentication(config.tspUrl(), config.tspUsername(), config.tspPassword());
        }
        tspSource.setDataLoader(dataLoader);
        return tspSource;
    }
}
JAVA

cat > "$PKG_DIR/XadesBaselineBSigner.java" <<'JAVA'
package es.practica.firmas;

import eu.europa.esig.dss.enumerations.DigestAlgorithm;
import eu.europa.esig.dss.enumerations.SignatureLevel;
import eu.europa.esig.dss.model.DSSDocument;
import eu.europa.esig.dss.model.FileDocument;
import eu.europa.esig.dss.model.SignatureValue;
import eu.europa.esig.dss.model.ToBeSigned;
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
JAVA

cat > "$PKG_DIR/DssLabDesktopApp.java" <<'JAVA'
package es.practica.firmas;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.nio.file.Path;

public final class DssLabDesktopApp {

    private final JTextField inputXml = new JTextField();
    private final JTextField outputXml = new JTextField();
    private final JTextField p12Path = new JTextField();
    private final JPasswordField p12Password = new JPasswordField();
    private final JTextField tspUrl = new JTextField();
    private final JTextField tspUser = new JTextField();
    private final JPasswordField tspPassword = new JPasswordField();
    private final JCheckBox enableTsp = new JCheckBox("Habilitar TSA (XAdES-T)");
    private final JTextArea logs = new JTextArea(10, 80);

    public static void launch() {
        SwingUtilities.invokeLater(() -> new DssLabDesktopApp().buildAndShow());
    }

    private void buildAndShow() {
        JFrame frame = new JFrame("DSS Lab - Firma XAdES");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel form = new JPanel(new GridLayout(0, 3, 8, 8));
        addFileRow(form, "XML entrada", inputXml, false);
        addFileRow(form, "XML salida", outputXml, true);
        addFileRow(form, "PKCS#12 (.p12)", p12Path, false);

        form.add(new JLabel("Password PKCS#12"));
        form.add(p12Password);
        form.add(new JLabel());

        form.add(enableTsp);
        form.add(new JLabel());
        form.add(new JLabel());

        form.add(new JLabel("TSA URL"));
        form.add(tspUrl);
        form.add(new JLabel());

        form.add(new JLabel("TSA usuario"));
        form.add(tspUser);
        form.add(new JLabel());

        form.add(new JLabel("TSA password"));
        form.add(tspPassword);
        form.add(new JLabel());

        JButton signButton = new JButton("Firmar (XAdES-B/T)");
        signButton.addActionListener(e -> sign());

        logs.setEditable(false);

        JPanel root = new JPanel(new BorderLayout(10, 10));
        root.add(form, BorderLayout.NORTH);
        root.add(signButton, BorderLayout.CENTER);
        root.add(new JScrollPane(logs), BorderLayout.SOUTH);

        frame.setContentPane(root);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);

        logs.append("UI Java lista. Completa campos y pulsa Firmar.\n");
    }

    private void addFileRow(JPanel form, String label, JTextField field, boolean saveDialog) {
        form.add(new JLabel(label));
        form.add(field);
        JButton browse = new JButton("...");
        browse.addActionListener(e -> chooseFile(field, saveDialog));
        form.add(browse);
    }

    private void chooseFile(JTextField target, boolean saveDialog) {
        JFileChooser chooser = new JFileChooser();
        int result = saveDialog ? chooser.showSaveDialog(null) : chooser.showOpenDialog(null);
        if (result == JFileChooser.APPROVE_OPTION) {
            target.setText(chooser.getSelectedFile().getAbsolutePath());
        }
    }

    private void sign() {
        try {
            String tsp = enableTsp.isSelected() ? tspUrl.getText().trim() : "";
            SigningConfig config = new SigningConfig(
                    Path.of(inputXml.getText().trim()),
                    Path.of(outputXml.getText().trim()),
                    Path.of(p12Path.getText().trim()),
                    new String(p12Password.getPassword()),
                    tsp,
                    tspUser.getText().trim(),
                    new String(tspPassword.getPassword())
            );

            new XadesBaselineBSigner().sign(config);
            String level = config.hasTsp() ? "XAdES-T" : "XAdES-B";
            logs.append("OK: Firma creada en " + config.outputXml() + " (" + level + ")\n");
            JOptionPane.showMessageDialog(null, "Firma completada: " + level);
        } catch (Exception exc) {
            logs.append("ERROR: " + exc.getMessage() + "\n");
            JOptionPane.showMessageDialog(null, exc.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
JAVA

cat > "$PKG_DIR/DssLabApp.java" <<'JAVA'
package es.practica.firmas;

import java.nio.file.Path;
import java.util.Map;

public final class DssLabApp {

    public static void main(String[] args) throws Exception {
        if (args.length >= 1 && "ui".equalsIgnoreCase(args[0])) {
            DssLabDesktopApp.launch();
            return;
        }

        if (args.length >= 2 && "sign-xades".equalsIgnoreCase(args[0])) {
            Path configPath = Path.of(args[1]);
            SigningConfig config = SigningConfig.fromPropertiesFile(configPath);
            new XadesBaselineBSigner().sign(config);
            System.out.println("Firma generada en: " + config.outputXml());
            System.out.println("Nivel: " + (config.hasTsp() ? "XAdES-T" : "XAdES-B"));
            return;
        }

        DssCapabilityReport report = DssCapabilityReport.defaultReport();
        System.out.println("=== DSS Lab (Java) ===");
        System.out.println("Uso:");
        System.out.println("  mvn -q -DskipTests exec:java -Dexec.args=\"ui\"");
        System.out.println("  mvn -q -DskipTests exec:java -Dexec.args=\"sign-xades ./signing-example.properties\"");
        System.out.println();

        for (Map.Entry<String, String> entry : report.capabilities().entrySet()) {
            System.out.printf("- %s: %s%n", entry.getKey(), entry.getValue());
        }
    }
}
JAVA


echo "Proyecto generado en: $TARGET_DIR"
echo "Siguiente paso: cd $TARGET_DIR && mvn -q -DskipTests exec:java -Dexec.args=\"ui\""
