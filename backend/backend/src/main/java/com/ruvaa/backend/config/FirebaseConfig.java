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
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;

import javax.annotation.PostConstruct;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;

@Slf4j
@Configuration
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class FirebaseConfig {

    @Value("${firebase.database-url:https://ruvaa-cbcaa-default-rtdb.asia-southeast1.firebasedatabase.app/}")
    private String databaseUrl;

    @Value("${firebase.project-id:ruvaa-cbcaa}")
    private String projectId;

    private FirebaseApp firebaseApp;

    @PostConstruct
    public void initializeFirebase() {
        try {
            if (databaseUrl == null || projectId == null) {
                log.warn("Firebase configuration not available. Running without Firebase integration.");
                return;
            }

            // Try to get credentials from multiple locations
            Resource serviceAccountKey = getServiceAccountResource();

            if (serviceAccountKey == null || !serviceAccountKey.exists()) {
                log.warn("Firebase service account file not found. Running without Firebase integration.");
                return;
            }

            // Validate credentials are not template
            if (!validateCredentials(serviceAccountKey)) {
                log.warn("Template Firebase service account detected. Running without Firebase integration.");
                return;
            }

            if (FirebaseApp.getApps().isEmpty()) {
                log.info("Initializing Firebase for project: {}", projectId);

                GoogleCredentials credentials = getCredentials(serviceAccountKey);

                FirebaseOptions options = FirebaseOptions.builder()
                        .setCredentials(credentials)
                        .setDatabaseUrl(databaseUrl)
                        .setProjectId(projectId)
                        .build();

                firebaseApp = FirebaseApp.initializeApp(options);
                log.info("Firebase initialized successfully from: {}", serviceAccountKey.getDescription());

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
     * Get service account resource from multiple possible locations.
     * Priority:
     * 1. Render secret file: /etc/secrets/serviceAccount.json
     * 2. Local file: ./serviceAccount.json (for development)
     * 3. Classpath: credentials/serviceAccount.json
     */
    private Resource getServiceAccountResource() {
        // 1. Try Render secret file location
        File renderSecretFile = new File("/etc/secrets/serviceAccount.json");
        if (renderSecretFile.exists()) {
            log.info("Loading credentials from Render secret file");
            return new FileSystemResource(renderSecretFile);
        }

        // 2. Try local development file in project root
        File localFile = new File("serviceAccount.json");
        if (localFile.exists()) {
            log.info("Loading credentials from local file");
            return new FileSystemResource(localFile);
        }

        // 3. Try classpath (inside JAR)
        ClassPathResource classpathResource = new ClassPathResource("credentials/serviceAccount.json");
        if (classpathResource.exists()) {
            log.info("Loading credentials from classpath");
            return classpathResource;
        }

        log.warn("Service account file not found in any location");
        return null;
    }

    /**
     * Validate that credentials are not template values.
     */
    private boolean validateCredentials(Resource resource) {
        try (InputStream is = resource.getInputStream()) {
            String content = new String(is.readAllBytes());
            return !content.contains("YOUR_PRIVATE_KEY_HERE")
                    && !content.contains("your-private-key-id")
                    && !content.contains("your_projectid");
        } catch (Exception e) {
            log.warn("Could not validate service account file");
            return false;
        }
    }

    /**
     * Get Google credentials from resource.
     */
    private GoogleCredentials getCredentials(Resource resource) throws IOException {
        try (InputStream serviceAccount = resource.getInputStream()) {
            return GoogleCredentials.fromStream(serviceAccount);
        } catch (Exception e) {
            log.error("Failed to load Firebase credentials from: {}", resource.getDescription(), e);
            throw new IOException("Could not load Firebase credentials", e);
        }
    }

    @Bean
    public Firestore firestore() {
        if (firebaseApp == null) {
            log.warn("Firebase not initialized. Creating mock Firestore bean.");
            return null;
        }

        try {
            Firestore firestore = FirestoreClient.getFirestore(firebaseApp);
            log.info("Firestore database connection established");
            return firestore;
        } catch (Exception e) {
            log.error("Failed to create Firestore instance", e);
            return null;
        }
    }

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
            return null;
        }
    }
}