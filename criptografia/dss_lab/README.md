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

En la ventana podrás:
- seleccionar XML entrada/salida,
- cargar `.p12` + password,
- activar TSA para elevar a XAdES-T.

## CLI (alternativa)
1. Copia/edita `signing-example.properties`.
2. Ejecuta:

```bash
mvn -q -DskipTests exec:java -Dexec.args="sign-xades ./signing-example.properties"
```

## Notas
- Si `tsp.url` está vacío: genera **XAdES-B**.
- Si `tsp.url` está informado: intenta **XAdES-T**.
