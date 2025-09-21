package com.ruvaa.backend.config;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.firestore.Firestore;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.cloud.FirestoreClient;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.Resource;

import javax.annotation.PostConstruct;
import java.io.IOException;
import java.io.InputStream;

/**
 * Firebase Configuration for CareerConnect
 * 
 * Provides secure Firebase initialization and Firestore database access.
 * Handles both file-based and environment-based service account configuration.
 */
@Slf4j
@Configuration
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class FirebaseConfig {

    @Value("${firebase.service-account-key}")
    private Resource serviceAccountKey;

    @Value("${firebase.database-url}")
    private String databaseUrl;

    @Value("${firebase.project-id}")
    private String projectId;

    private FirebaseApp firebaseApp;

    /**
     * Initialize Firebase application with proper error handling and security.
     */
    @PostConstruct
    public void initializeFirebase() {
        try {
            if (FirebaseApp.getApps().isEmpty()) {
                log.info("Initializing Firebase for project: {}", projectId);
                
                GoogleCredentials credentials = getCredentials();
                
                FirebaseOptions options = FirebaseOptions.builder()
                    .setCredentials(credentials)
                    .setDatabaseUrl(databaseUrl)
                    .setProjectId(projectId)
                    .build();

                firebaseApp = FirebaseApp.initializeApp(options);
                log.info("Firebase initialized successfully");
                
            } else {
                firebaseApp = FirebaseApp.getInstance();
                log.info("Firebase already initialized, using existing instance");
            }
            
        } catch (Exception e) {
            log.error("Failed to initialize Firebase", e);
            throw new RuntimeException("Firebase initialization failed", e);
        }
    }

    /**
     * Get Google credentials from either classpath resource or environment variable.
     */
    private GoogleCredentials getCredentials() throws IOException {
        try {
            // Check if resource exists and load from it
            if (serviceAccountKey.exists()) {
                log.debug("Loading Firebase credentials from resource: {}", serviceAccountKey.getDescription());
                try (InputStream serviceAccount = serviceAccountKey.getInputStream()) {
                    return GoogleCredentials.fromStream(serviceAccount);
                }
            } else {
                throw new IllegalArgumentException("Service account file not found: " + serviceAccountKey.getDescription());
            }
        } catch (Exception e) {
            log.error("Failed to load Firebase credentials from: {}", serviceAccountKey.getDescription(), e);
            throw new IOException("Could not load Firebase credentials", e);
        }
    }

    /**
     * Provide Firestore database instance.
     */
    @Bean
    public Firestore firestore() {
        if (firebaseApp == null) {
            throw new IllegalStateException("Firebase not initialized");
        }
        
        try {
            Firestore firestore = FirestoreClient.getFirestore(firebaseApp);
            log.info("Firestore database connection established");
            return firestore;
            
        } catch (Exception e) {
            log.error("Failed to create Firestore instance", e);
            throw new RuntimeException("Firestore initialization failed", e);
        }
    }

    /**
     * Health check method for Firebase connectivity.
     */
    public boolean isFirebaseHealthy() {
        try {
            return firebaseApp != null && 
                   FirebaseApp.getApps().contains(firebaseApp) &&
                   firestore() != null;
        } catch (Exception e) {
            log.warn("Firebase health check failed", e);
            return false;
        }
    }
}