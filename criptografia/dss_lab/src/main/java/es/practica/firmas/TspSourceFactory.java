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
