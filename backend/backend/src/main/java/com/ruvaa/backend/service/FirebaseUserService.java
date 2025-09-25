package com.ruvaa.backend.service;

import com.google.api.core.ApiFuture;
import com.google.cloud.firestore.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutionException;

/**
 * Firebase Firestore service for user profile management
 * Handles CRUD operations for user data in Firestore
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class FirebaseUserService {

    private final Firestore firestore;

    private static final String USERS_COLLECTION = "users";
    private static final String PROFILES_COLLECTION = "profiles";
    private static final String ASSESSMENTS_COLLECTION = "assessments";
    private static final String CHAT_HISTORY_COLLECTION = "chatHistory";

    /**
     * Create or update user profile in Firestore
     */
    public void saveUserProfile(String userId, Map<String, Object> profileData) {
        if (firestore == null) {
            log.warn("Firestore not available, skipping user profile save for user: {}", userId);
            return;
        }

        try {
            DocumentReference docRef = firestore.collection(USERS_COLLECTION)
                    .document(userId)
                    .collection(PROFILES_COLLECTION)
                    .document("profile");

            // Add timestamp
            profileData.put("lastUpdated", FieldValue.serverTimestamp());

            ApiFuture<WriteResult> result = docRef.set(profileData);
            WriteResult writeResult = result.get();
            log.info("User profile saved successfully for user: {} at {}", userId, writeResult.getUpdateTime());
        } catch (Exception e) {
            log.error("Failed to save user profile for user: {}", userId, e);
            throw new RuntimeException("Failed to save user profile", e);
        }
    }

    /**
     * Get user profile from Firestore
     */
    public Map<String, Object> getUserProfile(String userId) {
        if (firestore == null) {
            log.warn("Firestore not available, returning empty profile for user: {}", userId);
            return new HashMap<>();
        }

        try {
            DocumentReference docRef = firestore.collection(USERS_COLLECTION)
                    .document(userId)
                    .collection(PROFILES_COLLECTION)
                    .document("profile");

            ApiFuture<DocumentSnapshot> future = docRef.get();
            DocumentSnapshot document = future.get();

            if (document.exists()) {
                Map<String, Object> data = document.getData();
                log.debug("Retrieved user profile for user: {}", userId);
                return data != null ? data : new HashMap<>();
            } else {
                log.debug("No profile found for user: {}", userId);
                return new HashMap<>();
            }
        } catch (Exception e) {
            log.error("Failed to get user profile for user: {}", userId, e);
            throw new RuntimeException("Failed to retrieve user profile", e);
        }
    }

    /**
     * Save assessment results to Firestore
     */
    public void saveAssessmentResults(String userId, Map<String, Object> assessmentData) {
        try {
            DocumentReference docRef = firestore.collection(USERS_COLLECTION)
                    .document(userId)
                    .collection(ASSESSMENTS_COLLECTION)
                    .document();

            assessmentData.put("timestamp", FieldValue.serverTimestamp());
            assessmentData.put("userId", userId);

            ApiFuture<WriteResult> result = docRef.set(assessmentData);
            WriteResult writeResult = result.get();
            log.info("Assessment results saved for user: {} at {}", userId, writeResult.getUpdateTime());
        } catch (Exception e) {
            log.error("Failed to save assessment results for user: {}", userId, e);
            throw new RuntimeException("Failed to save assessment results", e);
        }
    }

    /**
     * Get latest assessment results for a user
     */
    public Map<String, Object> getLatestAssessmentResults(String userId) {
        try {
            CollectionReference assessmentsRef = firestore.collection(USERS_COLLECTION)
                    .document(userId)
                    .collection(ASSESSMENTS_COLLECTION);

            ApiFuture<QuerySnapshot> query = assessmentsRef
                    .orderBy("timestamp", Query.Direction.DESCENDING)
                    .limit(1)
                    .get();

            QuerySnapshot querySnapshot = query.get();

            if (!querySnapshot.isEmpty()) {
                DocumentSnapshot document = querySnapshot.getDocuments().get(0);
                Map<String, Object> data = document.getData();
                log.debug("Retrieved latest assessment for user: {}", userId);
                return data != null ? data : new HashMap<>();
            } else {
                log.debug("No assessments found for user: {}", userId);
                return new HashMap<>();
            }
        } catch (Exception e) {
            log.error("Failed to get assessment results for user: {}", userId, e);
            throw new RuntimeException("Failed to retrieve assessment results", e);
        }
    }

    /**
     * Save chat message to Firestore
     */
    public void saveChatMessage(String userId, String message, String response) {
        try {
            DocumentReference docRef = firestore.collection(USERS_COLLECTION)
                    .document(userId)
                    .collection(CHAT_HISTORY_COLLECTION)
                    .document();

            Map<String, Object> chatData = new HashMap<>();
            chatData.put("userMessage", message);
            chatData.put("aiResponse", response);
            chatData.put("timestamp", FieldValue.serverTimestamp());
            chatData.put("userId", userId);

            ApiFuture<WriteResult> result = docRef.set(chatData);
            WriteResult writeResult = result.get();
            log.debug("Chat message saved for user: {} at {}", userId, writeResult.getUpdateTime());
        } catch (Exception e) {
            log.error("Failed to save chat message for user: {}", userId, e);
            // Don't throw exception for chat history - it's not critical
            log.warn("Continuing without saving chat history");
        }
    }

    /**
     * Get chat history for a user
     */
    public java.util.List<Map<String, Object>> getChatHistory(String userId, int limit) {
        try {
            CollectionReference chatRef = firestore.collection(USERS_COLLECTION)
                    .document(userId)
                    .collection(CHAT_HISTORY_COLLECTION);

            ApiFuture<QuerySnapshot> query = chatRef
                    .orderBy("timestamp", Query.Direction.DESCENDING)
                    .limit(limit)
                    .get();

            QuerySnapshot querySnapshot = query.get();

            java.util.List<Map<String, Object>> chatHistory = new java.util.ArrayList<>();
            for (DocumentSnapshot document : querySnapshot.getDocuments()) {
                Map<String, Object> data = document.getData();
                if (data != null) {
                    chatHistory.add(data);
                }
            }

            log.debug("Retrieved {} chat messages for user: {}", chatHistory.size(), userId);
            return chatHistory;
        } catch (Exception e) {
            log.error("Failed to get chat history for user: {}", userId, e);
            return new java.util.ArrayList<>();
        }
    }

    /**
     * Create basic user document when user registers
     */
    public void createUserDocument(String userId, String email, String displayName) {
        try {
            DocumentReference docRef = firestore.collection(USERS_COLLECTION).document(userId);

            Map<String, Object> userData = new HashMap<>();
            userData.put("email", email);
            userData.put("displayName", displayName);
            userData.put("createdAt", FieldValue.serverTimestamp());
            userData.put("lastLogin", FieldValue.serverTimestamp());

            ApiFuture<WriteResult> result = docRef.set(userData);
            WriteResult writeResult = result.get();
            log.info("User document created for: {} at {}", userId, writeResult.getUpdateTime());
        } catch (Exception e) {
            log.error("Failed to create user document for: {}", userId, e);
            throw new RuntimeException("Failed to create user document", e);
        }
    }

    /**
     * Update user's last login time
     */
    public void updateLastLogin(String userId) {
        try {
            DocumentReference docRef = firestore.collection(USERS_COLLECTION).document(userId);

            Map<String, Object> updates = new HashMap<>();
            updates.put("lastLogin", FieldValue.serverTimestamp());

            ApiFuture<WriteResult> result = docRef.update(updates);
            WriteResult writeResult = result.get();
            log.debug("Updated last login for user: {} at {}", userId, writeResult.getUpdateTime());
        } catch (Exception e) {
            log.error("Failed to update last login for user: {}", userId, e);
            // Don't throw exception - this is not critical
        }
    }

    /**
     * Check if Firestore is available and healthy
     */
    public boolean isFirestoreHealthy() {
        if (firestore == null) {
            return false;
        }

        try {
            // Try to read from a test collection to verify connectivity
            ApiFuture<QuerySnapshot> future = firestore.collection("health_check").limit(1).get();
            future.get();
            return true;
        } catch (Exception e) {
            log.warn("Firestore health check failed: {}", e.getMessage());
            return false;
        }
    }
}