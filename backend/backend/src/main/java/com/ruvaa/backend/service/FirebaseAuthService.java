package com.ruvaa.backend.service;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseToken;
import com.google.firebase.auth.UserRecord;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

import java.util.Map;

/**
 * Firebase Authentication Service
 * Handles Firebase user authentication and token verification
 */
@Slf4j
@Service
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class FirebaseAuthService {

    private final FirebaseAuth firebaseAuth;

    public FirebaseAuthService(FirebaseAuth firebaseAuth) {
        this.firebaseAuth = firebaseAuth;
    }

    /**
     * Verify Firebase ID token and return user information
     */
    public FirebaseToken verifyIdToken(String idToken) throws FirebaseAuthException {
        try {
            FirebaseToken decodedToken = firebaseAuth.verifyIdToken(idToken);
            log.debug("Successfully verified Firebase token for user: {}", decodedToken.getUid());
            return decodedToken;
        } catch (FirebaseAuthException e) {
            log.error("Failed to verify Firebase token: {}", e.getMessage());
            throw e;
        }
    }

    /**
     * Get user record by UID
     */
    public UserRecord getUserRecord(String uid) throws FirebaseAuthException {
        try {
            UserRecord userRecord = firebaseAuth.getUser(uid);
            log.debug("Retrieved user record for: {}", uid);
            return userRecord;
        } catch (FirebaseAuthException e) {
            log.error("Failed to get user record for UID {}: {}", uid, e.getMessage());
            throw e;
        }
    }

    /**
     * Create a custom token for a user
     */
    public String createCustomToken(String uid) throws FirebaseAuthException {
        return createCustomToken(uid, null);
    }

    /**
     * Create a custom token for a user with additional claims
     */
    public String createCustomToken(String uid, Map<String, Object> additionalClaims) throws FirebaseAuthException {
        try {
            String customToken;
            if (additionalClaims != null && !additionalClaims.isEmpty()) {
                customToken = firebaseAuth.createCustomToken(uid, additionalClaims);
            } else {
                customToken = firebaseAuth.createCustomToken(uid);
            }
            log.debug("Created custom token for user: {}", uid);
            return customToken;
        } catch (FirebaseAuthException e) {
            log.error("Failed to create custom token for UID {}: {}", uid, e.getMessage());
            throw e;
        }
    }

    /**
     * Create a new user in Firebase Auth
     */
    public UserRecord createUser(String email, String password, String displayName) throws FirebaseAuthException {
        try {
            UserRecord.CreateRequest request = new UserRecord.CreateRequest()
                    .setEmail(email)
                    .setPassword(password)
                    .setDisplayName(displayName)
                    .setEmailVerified(false);

            UserRecord userRecord = firebaseAuth.createUser(request);
            log.info("Successfully created new user: {}", userRecord.getUid());
            return userRecord;
        } catch (FirebaseAuthException e) {
            log.error("Failed to create user: {}", e.getMessage());
            throw e;
        }
    }

    /**
     * Update user information
     */
    public UserRecord updateUser(String uid, String email, String displayName) throws FirebaseAuthException {
        try {
            UserRecord.UpdateRequest request = new UserRecord.UpdateRequest(uid)
                    .setEmail(email)
                    .setDisplayName(displayName);

            UserRecord userRecord = firebaseAuth.updateUser(request);
            log.info("Successfully updated user: {}", uid);
            return userRecord;
        } catch (FirebaseAuthException e) {
            log.error("Failed to update user {}: {}", uid, e.getMessage());
            throw e;
        }
    }

    /**
     * Delete a user from Firebase Auth
     */
    public void deleteUser(String uid) throws FirebaseAuthException {
        try {
            firebaseAuth.deleteUser(uid);
            log.info("Successfully deleted user: {}", uid);
        } catch (FirebaseAuthException e) {
            log.error("Failed to delete user {}: {}", uid, e.getMessage());
            throw e;
        }
    }

    /**
     * Set custom user claims for role-based access control
     */
    public void setCustomUserClaims(String uid, Map<String, Object> customClaims) throws FirebaseAuthException {
        try {
            firebaseAuth.setCustomUserClaims(uid, customClaims);
            log.info("Successfully set custom claims for user: {}", uid);
        } catch (FirebaseAuthException e) {
            log.error("Failed to set custom claims for user {}: {}", uid, e.getMessage());
            throw e;
        }
    }

    /**
     * Check if Firebase Auth is available
     */
    public boolean isFirebaseAuthAvailable() {
        if (firebaseAuth == null) {
            return false;
        }

        return true;
    }
}