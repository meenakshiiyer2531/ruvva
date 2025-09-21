package com.ruvaa.backend.repository;

import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.QueryDocumentSnapshot;
import com.ruvaa.backend.entity.College;
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
public class CollegeRepositoryImpl implements CollegeRepository {

    private final Firestore firestore;
    private static final String COLLECTION_NAME = "colleges";

    @Override
    public List<College> searchColleges(String search) {
        try {
            String searchLower = search.toLowerCase();
            var allColleges = firestore.collection(COLLECTION_NAME)
                    .get()
                    .get();

            List<College> filteredColleges = new ArrayList<>();
            for (QueryDocumentSnapshot document : allColleges.getDocuments()) {
                College college = document.toObject(College.class);
                college.setId(Long.parseLong(document.getId()));

                // Manual search filtering since Firestore doesn't support complex text search
                if (college.getName().toLowerCase().contains(searchLower) ||
                    college.getLocation().toLowerCase().contains(searchLower) ||
                    college.getPrograms().toLowerCase().contains(searchLower)) {
                    filteredColleges.add(college);
                }
            }
            return filteredColleges;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error searching colleges with term: {}", search, e);
            return new ArrayList<>();
        }
    }

    @Override
    public List<College> findByLocation(String location) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("location", location)
                    .get()
                    .get();

            List<College> colleges = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                College college = document.toObject(College.class);
                college.setId(Long.parseLong(document.getId()));
                colleges.add(college);
            }
            return colleges;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding colleges by location: {}", location, e);
            return new ArrayList<>();
        }
    }

    @Override
    public College save(College college) {
        try {
            if (college.getId() == null) {
                college.setId(System.currentTimeMillis());
            }

            firestore.collection(COLLECTION_NAME)
                    .document(college.getId().toString())
                    .set(college)
                    .get();

            return college;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error saving college: {}", college.getName(), e);
            throw new RuntimeException("Failed to save college", e);
        }
    }

    @Override
    public Optional<College> findById(Long id) {
        try {
            var document = firestore.collection(COLLECTION_NAME)
                    .document(id.toString())
                    .get()
                    .get();

            if (document.exists()) {
                College college = document.toObject(College.class);
                college.setId(id);
                return Optional.of(college);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding college by id: {}", id, e);
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
            log.error("Error deleting college by id: {}", id, e);
            throw new RuntimeException("Failed to delete college", e);
        }
    }

    @Override
    public List<College> findAll() {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .get()
                    .get();

            List<College> colleges = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                College college = document.toObject(College.class);
                college.setId(Long.parseLong(document.getId()));
                colleges.add(college);
            }
            return colleges;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding all colleges", e);
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
            log.error("Error counting colleges", e);
            return 0;
        }
    }
}