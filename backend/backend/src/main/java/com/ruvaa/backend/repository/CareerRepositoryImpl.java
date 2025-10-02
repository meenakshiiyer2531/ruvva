package com.ruvaa.backend.repository;

import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.QueryDocumentSnapshot;
import com.ruvaa.backend.entity.Career;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutionException;

@Slf4j
@Repository
@RequiredArgsConstructor
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class CareerRepositoryImpl implements CareerRepository {

    private final Firestore firestore;
    private static final String COLLECTION_NAME = "careers";

    @Override
    public List<Career> searchCareers(String search) {
        try {
            String searchLower = search.toLowerCase();
            var allCareers = firestore.collection(COLLECTION_NAME)
                    .get()
                    .get();

            List<Career> filteredCareers = new ArrayList<>();
            for (QueryDocumentSnapshot document : allCareers.getDocuments()) {
                Career career = document.toObject(Career.class);
                career.setId(Long.parseLong(document.getId()));

                // Manual search filtering since Firestore doesn't support complex text search
                if (career.getName().toLowerCase().contains(searchLower) ||
                    career.getDescription().toLowerCase().contains(searchLower) ||
                    career.getCategory().toLowerCase().contains(searchLower)) {
                    filteredCareers.add(career);
                }
            }
            return filteredCareers;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error searching careers with term: {}", search, e);
            return new ArrayList<>();
        }
    }

    @Override
    public List<Career> findByCategory(String category) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("category", category)
                    .get()
                    .get();

            List<Career> careers = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Career career = document.toObject(Career.class);
                career.setId(Long.parseLong(document.getId()));
                careers.add(career);
            }
            return careers;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding careers by category: {}", category, e);
            return new ArrayList<>();
        }
    }

    @Override
    public Career save(Career career) {
        try {
            if (career.getId() == null) {
                career.setId(System.currentTimeMillis());
            }

            firestore.collection(COLLECTION_NAME)
                    .document(career.getId().toString())
                    .set(career)
                    .get();

            return career;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error saving career: {}", career.getName(), e);
            throw new RuntimeException("Failed to save career", e);
        }
    }

    @Override
    public Optional<Career> findById(Long id) {
        try {
            var document = firestore.collection(COLLECTION_NAME)
                    .document(id.toString())
                    .get()
                    .get();

            if (document.exists()) {
                Career career = document.toObject(Career.class);
                career.setId(id);
                return Optional.of(career);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding career by id: {}", id, e);
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
            log.error("Error deleting career by id: {}", id, e);
            throw new RuntimeException("Failed to delete career", e);
        }
    }

    @Override
    public List<Career> findAll() {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .get()
                    .get();

            List<Career> careers = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Career career = document.toObject(Career.class);
                career.setId(Long.parseLong(document.getId()));
                careers.add(career);
            }
            return careers;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding all careers", e);
            return new ArrayList<>();
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
            log.error("Error counting careers", e);
            return 0;
        }
    }
}