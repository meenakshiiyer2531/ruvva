package com.ruvaa.backend.repository;

import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.QueryDocumentSnapshot;
import com.ruvaa.backend.entity.User;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.concurrent.ExecutionException;

@Slf4j
@Repository
@RequiredArgsConstructor
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class UserRepositoryImpl implements UserRepository {

    private final Firestore firestore;
    private static final String COLLECTION_NAME = "users";

    @Override
    public Optional<User> findByUsername(String username) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("username", username)
                    .get()
                    .get();

            if (!query.isEmpty()) {
                QueryDocumentSnapshot document = query.getDocuments().get(0);
                User user = document.toObject(User.class);
                user.setId(Long.parseLong(document.getId()));
                return Optional.of(user);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding user by username: {}", username, e);
            return Optional.empty();
        }
    }

    @Override
    public boolean existsByUsername(String username) {
        return findByUsername(username).isPresent();
    }

    @Override
    public boolean existsByEmail(String email) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("email", email)
                    .get()
                    .get();

            return !query.isEmpty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error checking if email exists: {}", email, e);
            return false;
        }
    }

    @Override
    public User save(User user) {
        try {
            if (user.getId() == null) {
                user.setId(System.currentTimeMillis());
            }

            firestore.collection(COLLECTION_NAME)
                    .document(user.getId().toString())
                    .set(user)
                    .get();

            return user;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error saving user: {}", user.getUsername(), e);
            throw new RuntimeException("Failed to save user", e);
        }
    }

    @Override
    public Optional<User> findById(Long id) {
        try {
            var document = firestore.collection(COLLECTION_NAME)
                    .document(id.toString())
                    .get()
                    .get();

            if (document.exists()) {
                User user = document.toObject(User.class);
                user.setId(id);
                return Optional.of(user);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding user by id: {}", id, e);
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
            log.error("Error deleting user by id: {}", id, e);
            throw new RuntimeException("Failed to delete user", e);
        }
    }

    @Override
    public long count() {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .get()
                    .get();
            return query.size();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error counting users", e);
            return 0;
        }
    }
}