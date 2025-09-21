package com.ruvaa.backend.repository;

import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.Query;
import com.google.cloud.firestore.QueryDocumentSnapshot;
import com.ruvaa.backend.entity.Assessment;
import com.ruvaa.backend.entity.User;
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
public class AssessmentRepositoryImpl implements AssessmentRepository {

    private final Firestore firestore;
    private static final String COLLECTION_NAME = "assessments";

    @Override
    public List<Assessment> findByUserOrderByCreatedAtDesc(User user) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("userId", user.getId())
                    .orderBy("createdAt", Query.Direction.DESCENDING)
                    .get()
                    .get();

            List<Assessment> assessments = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Assessment assessment = document.toObject(Assessment.class);
                assessment.setId(Long.parseLong(document.getId()));
                assessments.add(assessment);
            }
            return assessments;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding assessments by user: {}", user.getId(), e);
            return new ArrayList<>();
        }
    }

    @Override
    public Optional<Assessment> findFirstByUserOrderByCreatedAtDesc(User user) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("userId", user.getId())
                    .orderBy("createdAt", Query.Direction.DESCENDING)
                    .limit(1)
                    .get()
                    .get();

            if (!query.isEmpty()) {
                QueryDocumentSnapshot document = query.getDocuments().get(0);
                Assessment assessment = document.toObject(Assessment.class);
                assessment.setId(Long.parseLong(document.getId()));
                return Optional.of(assessment);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding first assessment by user: {}", user.getId(), e);
            return Optional.empty();
        }
    }

    @Override
    public Assessment save(Assessment assessment) {
        try {
            if (assessment.getId() == null) {
                assessment.setId(System.currentTimeMillis());
            }

            firestore.collection(COLLECTION_NAME)
                    .document(assessment.getId().toString())
                    .set(assessment)
                    .get();

            return assessment;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error saving assessment: {}", assessment.getId(), e);
            throw new RuntimeException("Failed to save assessment", e);
        }
    }

    @Override
    public Optional<Assessment> findById(Long id) {
        try {
            var document = firestore.collection(COLLECTION_NAME)
                    .document(id.toString())
                    .get()
                    .get();

            if (document.exists()) {
                Assessment assessment = document.toObject(Assessment.class);
                assessment.setId(id);
                return Optional.of(assessment);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding assessment by id: {}", id, e);
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
            log.error("Error deleting assessment by id: {}", id, e);
            throw new RuntimeException("Failed to delete assessment", e);
        }
    }
}