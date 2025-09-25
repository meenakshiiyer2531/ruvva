package com.ruvaa.backend.service;

import com.google.cloud.firestore.Firestore;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Service to check Firebase health status
 */
@Slf4j
@Service
public class FirebaseHealthService {

    private final Firestore firestore;

    public FirebaseHealthService(@Autowired(required = false) Firestore firestore) {
        this.firestore = firestore;
    }

    /**
     * Check if Firebase is healthy and available
     */
    public boolean isFirebaseHealthy() {
        if (firestore == null) {
            return false;
        }

        try {
            // Try to read from a test collection to verify connectivity
            firestore.collection("health_check").limit(1).get().get();
            return true;
        } catch (Exception e) {
            log.warn("Firebase health check failed: {}", e.getMessage());
            return false;
        }
    }
}