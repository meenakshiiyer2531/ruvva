package com.ruvaa.backend.service;

import com.google.cloud.firestore.*;
import com.ruvaa.backend.model.entity.Student;
import com.ruvaa.backend.model.dto.StudentRegistrationRequest;
import com.ruvaa.backend.model.dto.StudentProfileUpdateRequest;
import com.ruvaa.backend.exception.StudentNotFoundException;
import com.ruvaa.backend.exception.StudentAlreadyExistsException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;


import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

/**
 * Student Service for CareerConnect
 * 
 * Handles all student-related operations including registration, profile management,
 * and Firebase integration with proper error handling and caching.
 */
@Slf4j
@Service
@RequiredArgsConstructor
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class StudentService {

    private final Firestore firestore;
    private final ObjectProvider<PasswordEncoder> passwordEncoderProvider;
    private final GeminiAIService geminiAIService;
    
    private static final String STUDENTS_COLLECTION = "students";

    /**
     * Register a new student
     */
    public CompletableFuture<Student> registerStudent(StudentRegistrationRequest request) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                // Check if student already exists
                if (findByEmail(request.getEmail()).isPresent()) {
                    throw new StudentAlreadyExistsException("Student with email " + request.getEmail() + " already exists");
                }

                // Create new student
                Student student = Student.builder()
                    .email(request.getEmail())
                    .password(passwordEncoderProvider.getObject().encode(request.getPassword()))
                    .fullName(request.getFullName())
                    .phoneNumber(request.getPhoneNumber())
                    .age(request.getAge())
                    .city(request.getCity())
                    .state(request.getState())
                    .educationLevel(request.getEducationLevel())
                    .institutionName(request.getInstitutionName())
                    .stream(request.getStream())
                    .createdAt(com.google.cloud.Timestamp.now())
                    .updatedAt(com.google.cloud.Timestamp.now())
                    .active(true)
                    .emailVerified(true)
                    .profileCompleted(false)
                    .onboardingCompleted(false)
                    .build();

                // Save to Firebase
                DocumentReference docRef = firestore.collection(STUDENTS_COLLECTION).document();
                student.setId(docRef.getId());
                
                docRef.set(student).get();
                
                log.info("Student registered successfully: {}", student.getEmail());
                return student;
                
            } catch (InterruptedException | ExecutionException e) {
                log.error("Failed to register student: {}", request.getEmail(), e);
                throw new RuntimeException("Failed to register student", e);
            }
        });
    }

    /**
     * Find student by email
     */
    public Optional<Student> findByEmail(String email) {
        try {
            Query query = firestore.collection(STUDENTS_COLLECTION)
                .whereEqualTo("email", email)
                .limit(1);
                
            QuerySnapshot querySnapshot = query.get().get();
            
            if (querySnapshot.getDocuments().isEmpty()) {
                return Optional.empty();
            }
            
            DocumentSnapshot document = querySnapshot.getDocuments().get(0);
            Student student = document.toObject(Student.class);
            student.setId(document.getId());
            
            return Optional.of(student);
            
        } catch (InterruptedException | ExecutionException e) {
            log.error("Failed to find student by email: {}", email, e);
            return Optional.empty();
        }
    }

    /**
     * Find student by ID with caching
     */
    @Cacheable(value = "students", key = "#studentId")
    public CompletableFuture<Student> findById(String studentId) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                DocumentSnapshot document = firestore.collection(STUDENTS_COLLECTION)
                    .document(studentId)
                    .get()
                    .get();
                
                if (!document.exists()) {
                    throw new StudentNotFoundException("Student not found with ID: " + studentId);
                }
                
                Student student = document.toObject(Student.class);
                student.setId(document.getId());
                
                return student;
                
            } catch (InterruptedException | ExecutionException e) {
                log.error("Failed to find student by ID: {}", studentId, e);
                throw new RuntimeException("Failed to retrieve student", e);
            }
        });
    }

    /**
     * Update student profile
     */
    @CacheEvict(value = "students", key = "#studentId")
    public CompletableFuture<Student> updateProfile(String studentId, StudentProfileUpdateRequest request) {
        return findById(studentId).thenCompose(student -> {
            return CompletableFuture.supplyAsync(() -> {
                try {
                    // Update student fields
                    student.setUpdatedAt(com.google.cloud.Timestamp.now());
                    
                    // Calculate profile completion
                    student.setProfileCompleted(student.getProfileCompletionPercentage() >= 80);
                    
                    // Save to Firebase
                    firestore.collection(STUDENTS_COLLECTION)
                        .document(studentId)
                        .set(student)
                        .get();
                    
                    log.info("Student profile updated: {}", studentId);
                    return student;
                    
                } catch (InterruptedException | ExecutionException e) {
                    log.error("Failed to update student profile: {}", studentId, e);
                    throw new RuntimeException("Failed to update profile", e);
                }
            });
        });
    }

    /**
     * Update RIASEC scores after assessment
     */
    @CacheEvict(value = "students", key = "#studentId")
    public CompletableFuture<Student> updateRiasecScores(String studentId, Student.RiasecScores riasecScores) {
        return findById(studentId).thenCompose(student -> {
            return CompletableFuture.supplyAsync(() -> {
                try {
                    student.setRiasecScores(riasecScores);
                    student.setLastAssessmentDate(com.google.cloud.Timestamp.now());
                    student.setUpdatedAt(com.google.cloud.Timestamp.now());
                    
                    // Save to Firebase
                    firestore.collection(STUDENTS_COLLECTION)
                        .document(studentId)
                        .set(student)
                        .get();
                    
                    log.info("RIASEC scores updated for student: {}", studentId);
                    return student;
                    
                } catch (InterruptedException | ExecutionException e) {
                    log.error("Failed to update RIASEC scores: {}", studentId, e);
                    throw new RuntimeException("Failed to update RIASEC scores", e);
                }
            });
        });
    }

    /**
     * Add career to bookmarks
     */
    @CacheEvict(value = "students", key = "#studentId")
    public CompletableFuture<Void> bookmarkCareer(String studentId, String career) {
        return findById(studentId).thenCompose(student -> {
            return CompletableFuture.supplyAsync(() -> {
                try {
                    List<String> bookmarks = student.getBookmarkedCareers();
                    if (!bookmarks.contains(career)) {
                        bookmarks.add(career);
                        student.setUpdatedAt(com.google.cloud.Timestamp.now());
                        
                        firestore.collection(STUDENTS_COLLECTION)
                            .document(studentId)
                            .set(student)
                            .get();
                        
                        log.info("Career bookmarked for student {}: {}", studentId, career);
                    }
                    return null;
                    
                } catch (InterruptedException | ExecutionException e) {
                    log.error("Failed to bookmark career: {}", studentId, e);
                    throw new RuntimeException("Failed to bookmark career", e);
                }
            });
        });
    }

    /**
     * Update last login timestamp
     */
    @CacheEvict(value = "students", key = "#studentId")
    public CompletableFuture<Void> updateLastLogin(String studentId) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                firestore.collection(STUDENTS_COLLECTION)
                    .document(studentId)
                    .update("lastLoginAt", com.google.cloud.Timestamp.now())
                    .get();
                
                return null;
                
            } catch (InterruptedException | ExecutionException e) {
                log.error("Failed to update last login: {}", studentId, e);
                throw new RuntimeException("Failed to update last login", e);
            }
        });
    }

    /**
     * Verify student email
     */
    @CacheEvict(value = "students", key = "#studentId")
    public CompletableFuture<Void> verifyEmail(String studentId) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                firestore.collection(STUDENTS_COLLECTION)
                    .document(studentId)
                    .update("emailVerified", true, "updatedAt", com.google.cloud.Timestamp.now())
                    .get();
                
                log.info("Email verified for student: {}", studentId);
                return null;
                
            } catch (InterruptedException | ExecutionException e) {
                log.error("Failed to verify email: {}", studentId, e);
                throw new RuntimeException("Failed to verify email", e);
            }
        });
    }

    /**
     * Complete onboarding process
     */
    @CacheEvict(value = "students", key = "#studentId")
    public CompletableFuture<Void> completeOnboarding(String studentId) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                firestore.collection(STUDENTS_COLLECTION)
                    .document(studentId)
                    .update("onboardingCompleted", true, "updatedAt", com.google.cloud.Timestamp.now())
                    .get();
                
                log.info("Onboarding completed for student: {}", studentId);
                return null;
                
            } catch (InterruptedException | ExecutionException e) {
                log.error("Failed to complete onboarding: {}", studentId, e);
                throw new RuntimeException("Failed to complete onboarding", e);
            }
        });
    }

    /**
     * Get students requiring career assessment
     */
    public CompletableFuture<List<Student>> getStudentsNeedingAssessment() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Query query = firestore.collection(STUDENTS_COLLECTION)
                    .whereEqualTo("active", true)
                    .whereEqualTo("profileCompleted", true);
                
                QuerySnapshot querySnapshot = query.get().get();
                
                return querySnapshot.getDocuments().stream()
                    .map(doc -> {
                        Student student = doc.toObject(Student.class);
                        student.setId(doc.getId());
                        return student;
                    })
                    .filter(Student::needsCareerAssessment)
                    .toList();
                    
            } catch (InterruptedException | ExecutionException e) {
                log.error("Failed to get students needing assessment", e);
                throw new RuntimeException("Failed to retrieve students", e);
            }
        });
    }

    /**
     * Deactivate student account
     */
    @CacheEvict(value = "students", key = "#studentId")
    public CompletableFuture<Void> deactivateStudent(String studentId) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                firestore.collection(STUDENTS_COLLECTION)
                    .document(studentId)
                    .update("active", false, "updatedAt", com.google.cloud.Timestamp.now())
                    .get();
                
                log.info("Student deactivated: {}", studentId);
                return null;
                
            } catch (InterruptedException | ExecutionException e) {
                log.error("Failed to deactivate student: {}", studentId, e);
                throw new RuntimeException("Failed to deactivate student", e);
            }
        });
    }

    /**
     * Helper method to update student fields from request
     */
    private void updateStudentFields(Student student, StudentProfileUpdateRequest request) {
        if (request.getFullName() != null) student.setFullName(request.getFullName());
        if (request.getPhoneNumber() != null) student.setPhoneNumber(request.getPhoneNumber());
        if (request.getAge() != null) student.setAge(request.getAge());
        if (request.getCity() != null) student.setCity(request.getCity());
        if (request.getState() != null) student.setState(request.getState());
        if (request.getEducationLevel() != null) student.setEducationLevel(request.getEducationLevel());
        if (request.getInstitutionName() != null) student.setInstitutionName(request.getInstitutionName());
        if (request.getCollegeTier() != null) student.setCollegeTier(request.getCollegeTier());
        if (request.getStream() != null) student.setStream(request.getStream());
        if (request.getCgpa() != null) student.setCgpa(request.getCgpa());
        if (request.getPercentage() != null) student.setPercentage(request.getPercentage());
        if (request.getGraduationYear() != null) student.setGraduationYear(request.getGraduationYear());
        if (request.getInterestedDomains() != null) student.setInterestedDomains(request.getInterestedDomains());
        if (request.getSkillsAssessment() != null) student.setSkillsAssessment(request.getSkillsAssessment());
        if (request.getPreferredLocations() != null) student.setPreferredLocations(request.getPreferredLocations());
        if (request.getWorkPreference() != null) student.setWorkPreference(request.getWorkPreference());
        if (request.getExpectedSalaryLPA() != null) student.setExpectedSalaryLPA(request.getExpectedSalaryLPA());
        if (request.getCurrentCareerGoal() != null) student.setCurrentCareerGoal(request.getCurrentCareerGoal());
    }
}