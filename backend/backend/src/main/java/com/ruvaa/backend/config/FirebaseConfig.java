package com.ruvaa.backend.config;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.firestore.Firestore;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.auth.FirebaseAuth;
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

    @Value("${firebase.service-account-key:classpath:credentials/serviceAccount.json}")
    private Resource serviceAccountKey;

    @Value("${firebase.database-url:https://ruvaa-cbcaa-default-rtdb.asia-southeast1.firebasedatabase.app/}")
    private String databaseUrl;

    @Value("${firebase.project-id:ruvaa-cbcaa}")
    private String projectId;

    private FirebaseApp firebaseApp;

    /**
     * Initialize Firebase application with proper error handling and security.
     */
    @PostConstruct
    public void initializeFirebase() {
        try {
            // Check if Firebase configuration is available
            if (serviceAccountKey == null || databaseUrl == null || projectId == null) {
                log.warn("Firebase configuration not available. Running without Firebase integration.");
                return;
            }

            // Check if the service account file exists
            if (!serviceAccountKey.exists()) {
                log.warn("Firebase service account file not found: {}. Running without Firebase integration.",
                        serviceAccountKey.getDescription());
                return;
            }

            // Check if the service account has valid credentials
            try (InputStream is = serviceAccountKey.getInputStream()) {
                String content = new String(is.readAllBytes());
                if (content.contains("YOUR_PRIVATE_KEY_HERE") || content.contains("your-private-key-id")) {
                    log.warn("Template Firebase service account detected. Please configure with real credentials. Running without Firebase integration.");
                    return;
                }
            } catch (Exception e) {
                log.warn("Could not read service account file. Running without Firebase integration.");
                return;
            }

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
            log.warn("Continuing without Firebase integration");
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
            log.warn("Firebase not initialized. Creating mock Firestore bean.");
            // Return a null placeholder - services will handle this gracefully
            return null;
        }

        try {
            Firestore firestore = FirestoreClient.getFirestore(firebaseApp);
            log.info("Firestore database connection established");
            return firestore;

        } catch (Exception e) {
            log.error("Failed to create Firestore instance", e);
            log.warn("Returning null Firestore bean");
            return null;
        }
    }

    /**
     * Provide FirebaseAuth instance.
     */
    @Bean
    public FirebaseAuth firebaseAuth() {
        if (firebaseApp == null) {
            log.warn("Firebase not initialized. Creating mock FirebaseAuth bean.");
            return null;
        }

        try {
            FirebaseAuth auth = FirebaseAuth.getInstance(firebaseApp);
            log.info("FirebaseAuth instance created");
            return auth;

        } catch (Exception e) {
            log.error("Failed to create FirebaseAuth instance", e);
            log.warn("Returning null FirebaseAuth bean");
            return null;
        }
    }

}