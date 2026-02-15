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
