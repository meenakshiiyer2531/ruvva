package com.ruvaa.backend.repository;

import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.Query;
import com.google.cloud.firestore.QueryDocumentSnapshot;
import com.ruvaa.backend.entity.ChatMessage;
import com.ruvaa.backend.entity.User;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutionException;

@Slf4j
@Repository
@RequiredArgsConstructor
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class ChatMessageRepositoryImpl implements ChatMessageRepository {

    private final Firestore firestore;
    private static final String COLLECTION_NAME = "chat_messages";

    @Override
    public List<ChatMessage> findByUserOrderByCreatedAtAsc(User user) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("userId", user.getId())
                    .orderBy("createdAt", Query.Direction.ASCENDING)
                    .get()
                    .get();

            List<ChatMessage> messages = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                ChatMessage message = document.toObject(ChatMessage.class);
                message.setId(Long.parseLong(document.getId()));
                messages.add(message);
            }
            return messages;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding chat messages by user: {}", user.getId(), e);
            return new ArrayList<>();
        }
    }

    @Override
    public List<ChatMessage> findTop20ByUserOrderByCreatedAtDesc(User user) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("userId", user.getId())
                    .orderBy("createdAt", Query.Direction.DESCENDING)
                    .limit(20)
                    .get()
                    .get();

            List<ChatMessage> messages = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                ChatMessage message = document.toObject(ChatMessage.class);
                message.setId(Long.parseLong(document.getId()));
                messages.add(message);
            }

            // Reverse to get chronological order
            Collections.reverse(messages);
            return messages;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding top 20 chat messages by user: {}", user.getId(), e);
            return new ArrayList<>();
        }
    }

    @Override
    public ChatMessage save(ChatMessage chatMessage) {
        try {
            if (chatMessage.getId() == null) {
                chatMessage.setId(System.currentTimeMillis());
            }

            firestore.collection(COLLECTION_NAME)
                    .document(chatMessage.getId().toString())
                    .set(chatMessage)
                    .get();

            return chatMessage;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error saving chat message: {}", chatMessage.getId(), e);
            throw new RuntimeException("Failed to save chat message", e);
        }
    }

    @Override
    public Optional<ChatMessage> findById(Long id) {
        try {
            var document = firestore.collection(COLLECTION_NAME)
                    .document(id.toString())
                    .get()
                    .get();

            if (document.exists()) {
                ChatMessage message = document.toObject(ChatMessage.class);
                message.setId(id);
                return Optional.of(message);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding chat message by id: {}", id, e);
            return Optional.empty();
        }
    }

    @Override
    public void deleteById(Long id) {
        try {
            firestore.collection(COLLECTION_NAME)
                    .document(id.toString())
                    .delete()
                    .get();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error deleting chat message by id: {}", id, e);
            throw new RuntimeException("Failed to delete chat message", e);
        }
    }
}