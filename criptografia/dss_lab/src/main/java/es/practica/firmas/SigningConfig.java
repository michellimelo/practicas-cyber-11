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
