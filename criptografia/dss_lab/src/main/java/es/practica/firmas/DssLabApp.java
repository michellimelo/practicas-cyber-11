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
