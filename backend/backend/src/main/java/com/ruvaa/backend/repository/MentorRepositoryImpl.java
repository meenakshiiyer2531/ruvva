package com.ruvaa.backend.repository;

import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.QueryDocumentSnapshot;
import com.ruvaa.backend.entity.Mentor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutionException;

@Slf4j
@Repository
@RequiredArgsConstructor
public class MentorRepositoryImpl implements MentorRepository {

    private final Firestore firestore;
    private static final String COLLECTION_NAME = "mentors";

    @Override
    public List<Mentor> findBySpecialization(String specialization) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("specialization", specialization)
                    .get()
                    .get();

            List<Mentor> mentors = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Mentor mentor = document.toObject(Mentor.class);
                mentor.setId(Long.parseLong(document.getId()));
                mentors.add(mentor);
            }
            return mentors;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding mentors by specialization: {}", specialization, e);
            return new ArrayList<>();
        }
    }

    @Override
    public List<Mentor> findByRatingGreaterThanEqual(Double rating) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereGreaterThanOrEqualTo("rating", rating)
                    .get()
                    .get();

            List<Mentor> mentors = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Mentor mentor = document.toObject(Mentor.class);
                mentor.setId(Long.parseLong(document.getId()));
                mentors.add(mentor);
            }
            return mentors;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding mentors by rating >= {}", rating, e);
            return new ArrayList<>();
        }
    }

    @Override
    public Mentor save(Mentor mentor) {
        try {
            if (mentor.getId() == null) {
                mentor.setId(System.currentTimeMillis());
            }

            firestore.collection(COLLECTION_NAME)
                    .document(mentor.getId().toString())
                    .set(mentor)
                    .get();

            return mentor;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error saving mentor: {}", mentor.getName(), e);
            throw new RuntimeException("Failed to save mentor", e);
        }
    }

    @Override
    public Optional<Mentor> findById(Long id) {
        try {
            var document = firestore.collection(COLLECTION_NAME)
                    .document(id.toString())
                    .get()
                    .get();

            if (document.exists()) {
                Mentor mentor = document.toObject(Mentor.class);
                mentor.setId(id);
                return Optional.of(mentor);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding mentor by id: {}", id, e);
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
            log.error("Error deleting mentor by id: {}", id, e);
            throw new RuntimeException("Failed to delete mentor", e);
        }
    }

    @Override
    public List<Mentor> findAll() {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .get()
                    .get();

            List<Mentor> mentors = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Mentor mentor = document.toObject(Mentor.class);
                mentor.setId(Long.parseLong(document.getId()));
                mentors.add(mentor);
            }
            return mentors;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding all mentors", e);
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
            log.error("Error counting mentors", e);
            return 0;
        }
    }
}