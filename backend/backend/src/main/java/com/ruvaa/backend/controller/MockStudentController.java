package com.ruvaa.backend.controller;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import java.time.LocalDateTime;
import java.util.Map;
import com.ruvaa.backend.mock.MockDataStore;

/**
 * Mock Student Controller active only when firebase.enabled = false.
 * Provides a simplified /students/register endpoint for local frontend integration
 * without needing Firebase or persistent storage.
 */
@Slf4j
@RestController
@RequestMapping("/students")
@Validated
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "false", matchIfMissing = true)
public class MockStudentController {

    private final MockDataStore store;

    public MockStudentController(MockDataStore store) {
        this.store = store;
    }

    private static final String SUCCESS_KEY = "success";
    private static final String MESSAGE_KEY = "message";
    private static final String DATA_KEY = "data";
    private static final String EMAIL_KEY = "email";
    private static final String GRADE_LEVEL_KEY = "gradeLevel";
    private static final String PROFILE_KEY = "profile";
    private static final String RIASEC_KEY = "riasecScores";
    private static final String CREATED_AT_KEY = "createdAt";
    private static final String CITY_KEY = "city";
    private static final String STATE_KEY = "state";
    private static final String EDUCATION_LEVEL_KEY = "educationLevel";
    private static final String INSTITUTION_NAME_KEY = "institutionName";
    private static final String STREAM_KEY = "stream";
    private static final String AGREE_TERMS_KEY = "agreeToTerms";
    private static final String AGREE_PRIVACY_KEY = "agreeToPrivacyPolicy";
    private static final String NOT_FOUND_PREFIX = "Student not found with id: ";

    @GetMapping("/{id}")
    public ResponseEntity<Map<String,Object>> getStudent(@PathVariable String id) {
        MockDataStore.MockStudent s = store.getStudentsById().get(id);
        if (s == null) {
            Map<String,Object> nf = new java.util.HashMap<>();
            nf.put(SUCCESS_KEY,false);
            nf.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(nf);
        }
        Map<String,Object> profile = store.getProfiles().getOrDefault(id, java.util.Collections.emptyMap());
        java.util.List<Map<String,Object>> assessments = store.getAssessmentHistory().getOrDefault(id, java.util.Collections.emptyList());
        java.util.List<MockDataStore.MockBooking> bookings = store.getBookingsByStudentId().getOrDefault(id, java.util.Collections.emptyList());
        Map<String,Object> data = new java.util.HashMap<>();
        data.put("id", s.getId());
        data.put(EMAIL_KEY, s.getEmail());
        data.put("name", s.getName());
        putIfNotNull(data, GRADE_LEVEL_KEY, s.getGradeLevel());
        data.put(PROFILE_KEY, profile);
        if (!assessments.isEmpty()) data.put("assessmentHistory", assessments);
        if (!bookings.isEmpty()) {
            java.util.List<Map<String,Object>> bookingDtos = new java.util.ArrayList<>();
            for (MockDataStore.MockBooking b : bookings) {
                Map<String,Object> bMap = new java.util.HashMap<>();
                bMap.put("id", b.getId());
                bMap.put("mentorId", b.getMentorId());
                MockDataStore.MockMentor m = store.getMentorsById().get(b.getMentorId());
                if (m != null) bMap.put("mentorName", m.getName());
                bMap.put("date", b.getDate());
                bMap.put("status", b.getStatus());
                bMap.put(CREATED_AT_KEY, b.getCreatedAt().toString());
                bookingDtos.add(bMap);
            }
            data.put("bookings", bookingDtos);
        }
        // notifications removed per updated requirements
        Map<String,Object> resp = new java.util.HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(MESSAGE_KEY,"Student retrieved (mock mode)");
        resp.put(DATA_KEY,data);
        return ResponseEntity.ok(resp);
    }

    @PostMapping("/register")
    public ResponseEntity<Map<String, Object>> register(@Valid @RequestBody MockStudentRegistrationRequest request) {
        try {
            log.info("[Mock] Student registration request: {}", request.getEmail());
            logDebugIncoming(request);
            normalizeName(request);
            ResponseEntity<Map<String, Object>> conflict = checkConflict(request.getEmail());
            if (conflict != null) return conflict;
            MockStudent student = createStudentRecord(request);
            String token = generateToken();
            Map<String, Object> studentData = buildStudentDataMap(student, request, token);
            seedInitialProfile(student.getId(), request);
            return buildSuccessResponse(studentData);
        } catch (Exception e) {
            return buildErrorResponse(e);
        }
    }

    // ---- Helper methods to reduce complexity ----
    private void logDebugIncoming(MockStudentRegistrationRequest r) {
        log.debug("Incoming payload - name: '{}', fullName: '{}', passwordPresent: {}, gradeLevel: '{}', age: '{}', city: '{}', state: '{}', educationLevel: '{}', institution: '{}', stream: '{}'",
            r.getName(), r.getFullName(), r.getPassword() != null && !r.getPassword().isBlank(), r.getGradeLevel(), r.getAge(), r.getCity(), r.getState(), r.getEducationLevel(), r.getInstitutionName(), r.getStream());
    }
    private void normalizeName(MockStudentRegistrationRequest r) {
        if ((r.getName() == null || r.getName().isBlank()) && r.getFullName() != null && !r.getFullName().isBlank()) {
            r.setName(r.getFullName().trim());
        }
        log.debug("Normalized name value: '{}'", r.getName());
    }
    private ResponseEntity<Map<String, Object>> checkConflict(String email) {
        if (store.getStudentsByEmail().containsKey(email)) {
            Map<String, Object> conflict = new java.util.HashMap<>();
            conflict.put(SUCCESS_KEY, false);
            conflict.put(MESSAGE_KEY, "Student already exists with email: " + email);
            return ResponseEntity.status(HttpStatus.CONFLICT).body(conflict);
        }
        return null;
    }
    private MockStudent createStudentRecord(MockStudentRegistrationRequest r) {
        MockStudent student = new MockStudent(String.valueOf(System.currentTimeMillis()), r.getEmail(), r.getName(), r.getGradeLevel(), LocalDateTime.now());
        store.getStudentsByEmail().put(r.getEmail(), new MockDataStore.MockStudent(student.getId(), student.getEmail(), student.getName(), student.getGradeLevel(), student.getCreatedAt()));
        store.getStudentsById().put(student.getId(), store.getStudentsByEmail().get(r.getEmail()));
        store.getAuthUsers().computeIfAbsent(r.getEmail(), em -> new MockDataStore.MockUserAuth(student.getId(), em, r.getPassword() == null ? "mock-pass" : r.getPassword(), student.getName(), student.getCreatedAt()));
        return student;
    }
    private String generateToken() { return "mock-student-token-" + System.currentTimeMillis(); }
    private Map<String, Object> buildStudentDataMap(MockStudent s, MockStudentRegistrationRequest r, String token) {
        Map<String, Object> studentData = new java.util.HashMap<>();
        studentData.put("id", s.getId());
        studentData.put(EMAIL_KEY, s.getEmail());
        studentData.put("name", s.getName());
        if (s.getGradeLevel() != null) studentData.put(GRADE_LEVEL_KEY, s.getGradeLevel());
    studentData.put(CREATED_AT_KEY, s.getCreatedAt().toString());
        studentData.put("token", token);
    putIfNotNull(studentData, CITY_KEY, r.getCity());
    putIfNotNull(studentData, STATE_KEY, r.getState());
    putIfNotNull(studentData, EDUCATION_LEVEL_KEY, r.getEducationLevel());
    putIfNotNull(studentData, INSTITUTION_NAME_KEY, r.getInstitutionName());
    putIfNotNull(studentData, STREAM_KEY, r.getStream());
    studentData.put(AGREE_TERMS_KEY, r.isAgreeToTerms());
    studentData.put(AGREE_PRIVACY_KEY, r.isAgreeToPrivacyPolicy());
        // Include initial seeded profile to avoid second fetch
        Map<String,Object> initialProfile = new java.util.HashMap<>();
    putIfNotNull(initialProfile, CITY_KEY, r.getCity());
    putIfNotNull(initialProfile, STATE_KEY, r.getState());
    putIfNotNull(initialProfile, EDUCATION_LEVEL_KEY, r.getEducationLevel());
    putIfNotNull(initialProfile, INSTITUTION_NAME_KEY, r.getInstitutionName());
    putIfNotNull(initialProfile, STREAM_KEY, r.getStream());
        putIfNotNull(initialProfile, "age", r.getAge());
        putIfNotNull(initialProfile, "phoneNumber", r.getPhoneNumber());
    initialProfile.put(AGREE_TERMS_KEY, r.isAgreeToTerms());
    initialProfile.put(AGREE_PRIVACY_KEY, r.isAgreeToPrivacyPolicy());
        studentData.put(PROFILE_KEY, initialProfile);
        return studentData;
    }
    private void seedInitialProfile(String studentId, MockStudentRegistrationRequest r) {
        Map<String,Object> profile = new java.util.HashMap<>();
    putIfNotNull(profile, CITY_KEY, r.getCity());
    putIfNotNull(profile, STATE_KEY, r.getState());
    putIfNotNull(profile, EDUCATION_LEVEL_KEY, r.getEducationLevel());
    putIfNotNull(profile, INSTITUTION_NAME_KEY, r.getInstitutionName());
    putIfNotNull(profile, STREAM_KEY, r.getStream());
        putIfNotNull(profile, "age", r.getAge());
        putIfNotNull(profile, "phoneNumber", r.getPhoneNumber());
    profile.put(AGREE_TERMS_KEY, r.isAgreeToTerms());
    profile.put(AGREE_PRIVACY_KEY, r.isAgreeToPrivacyPolicy());
        store.getProfiles().put(studentId, profile);
    }
    private ResponseEntity<Map<String, Object>> buildSuccessResponse(Map<String,Object> studentData) {
        Map<String,Object> resp = new java.util.HashMap<>();
        resp.put(SUCCESS_KEY, true);
        resp.put(MESSAGE_KEY, "Student registered successfully (mock mode)");
        resp.put(DATA_KEY, studentData);
        return ResponseEntity.status(HttpStatus.CREATED).body(resp);
    }
    private ResponseEntity<Map<String, Object>> buildErrorResponse(Exception e) {
        log.error("[Mock] Student registration failed", e);
        Map<String,Object> err = new java.util.HashMap<>();
        err.put(SUCCESS_KEY, false);
        err.put(MESSAGE_KEY, "Registration failed: " + e.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
    }
    private void putIfNotNull(Map<String,Object> target, String key, Object value) { if (value != null) target.put(key, value); }

    @GetMapping("/health")
    public Map<String, Object> health() {
        Map<String, Object> health = new java.util.HashMap<>();
        health.put("status", "UP");
        health.put("mode", "mock");
        health.put("students", store.getStudentsByEmail().size());
        health.put("profiles", store.getProfiles().size());
        return health;
    }

    /**
     * List all registered mock students (basic fields only) to assist manual verification.
     */
    @GetMapping("/mock-users")
    public ResponseEntity<Map<String, Object>> listMockUsers() {
        java.util.List<Map<String, Object>> list = new java.util.ArrayList<>();
        for (MockDataStore.MockStudent s : store.getStudentsByEmail().values()) {
            Map<String, Object> item = new java.util.HashMap<>();
            item.put("id", s.getId());
            item.put(EMAIL_KEY, s.getEmail());
            item.put("name", s.getName());
            if (s.getGradeLevel() != null) item.put(GRADE_LEVEL_KEY, s.getGradeLevel());
            list.add(item);
        }
        Map<String, Object> response = new java.util.HashMap<>();
        response.put(SUCCESS_KEY, true);
        response.put(DATA_KEY, list);
        response.put(MESSAGE_KEY, "Mock users listed");
        return ResponseEntity.ok(response);
    }

    /**
     * Update (create or merge) a student's profile data in mock mode.
     * Accepts an arbitrary JSON object and stores it under the student's id.
     */
    @PutMapping("/{id}/profile")
    public ResponseEntity<Map<String, Object>> updateProfile(
        @PathVariable("id") String id,
        @RequestBody(required = false) Map<String, Object> profilePayload
    ) {
        try {
            MockDataStore.MockStudent student = store.getStudentsById().get(id);
            if (student == null) {
                Map<String, Object> notFound = new java.util.HashMap<>();
                notFound.put(SUCCESS_KEY, false);
                notFound.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(notFound);
            }

            if (profilePayload == null) {
                profilePayload = new java.util.HashMap<>();
            }

            // Merge with existing profile if present
            Map<String, Object> existing = store.getProfiles().getOrDefault(id, new java.util.HashMap<>());
            existing.putAll(profilePayload); // shallow merge
            store.getProfiles().put(id, existing);

            Map<String, Object> data = new java.util.HashMap<>();
            data.put("id", student.getId());
            data.put(EMAIL_KEY, student.getEmail());
            data.put("name", student.getName());
            if (student.getGradeLevel() != null) data.put(GRADE_LEVEL_KEY, student.getGradeLevel());
            data.put(PROFILE_KEY, existing);

            Map<String, Object> response = new java.util.HashMap<>();
            response.put(SUCCESS_KEY, true);
            response.put(MESSAGE_KEY, "Profile updated (mock mode)");
            response.put(DATA_KEY, data);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("[Mock] Profile update failed for id {}", id, e);
            Map<String, Object> err = new java.util.HashMap<>();
            err.put(SUCCESS_KEY, false);
            err.put(MESSAGE_KEY, "Profile update failed: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }

    /**
     * Retrieve a student's profile plus basic registration data.
     */
    @GetMapping("/{id}/profile")
    public ResponseEntity<Map<String, Object>> getProfile(@PathVariable("id") String id) {
        try {
            MockDataStore.MockStudent student = store.getStudentsById().get(id);
            if (student == null) {
                Map<String, Object> notFound = new java.util.HashMap<>();
                notFound.put(SUCCESS_KEY, false);
                notFound.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(notFound);
            }

            Map<String, Object> profile = store.getProfiles().getOrDefault(id, new java.util.HashMap<>());

            Map<String, Object> data = new java.util.HashMap<>();
            data.put("id", student.getId());
            data.put(EMAIL_KEY, student.getEmail());
            data.put("name", student.getName());
            if (student.getGradeLevel() != null) data.put(GRADE_LEVEL_KEY, student.getGradeLevel());
            data.put(PROFILE_KEY, profile);

            Map<String, Object> response = new java.util.HashMap<>();
            response.put(SUCCESS_KEY, true);
            response.put(MESSAGE_KEY, "Profile retrieved (mock mode)");
            response.put(DATA_KEY, data);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("[Mock] Profile retrieval failed for id {}", id, e);
            Map<String, Object> err = new java.util.HashMap<>();
            err.put(SUCCESS_KEY, false);
            err.put(MESSAGE_KEY, "Profile retrieval failed: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(err);
        }
    }

    /**
     * Create a profile only if none exists yet (idempotent create semantics).
     */
    @PostMapping("/{id}/profile")
    public ResponseEntity<Map<String, Object>> createProfile(
        @PathVariable("id") String id,
        @RequestBody(required = false) Map<String, Object> profilePayload
    ) {
    MockDataStore.MockStudent student = store.getStudentsById().get(id);
        if (student == null) {
            Map<String, Object> notFound = new java.util.HashMap<>();
            notFound.put(SUCCESS_KEY, false);
            notFound.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(notFound);
        }
        if (store.getProfiles().containsKey(id)) {
            Map<String, Object> conflict = new java.util.HashMap<>();
            conflict.put(SUCCESS_KEY, false);
            conflict.put(MESSAGE_KEY, "Profile already exists for student id: " + id);
            return ResponseEntity.status(HttpStatus.CONFLICT).body(conflict);
        }
        if (profilePayload == null) profilePayload = new java.util.HashMap<>();
        store.getProfiles().put(id, new java.util.HashMap<>(profilePayload));
        return buildProfileResponse(student, store.getProfiles().get(id), HttpStatus.CREATED, "Profile created (mock mode)");
    }

    /**
     * Replace a profile entirely (PUT semantics). If none exists, creates one.
     */
    @PutMapping("/{id}/profile/replace")
    public ResponseEntity<Map<String, Object>> replaceProfile(
        @PathVariable("id") String id,
        @RequestBody(required = false) Map<String, Object> profilePayload
    ) {
    MockDataStore.MockStudent student = store.getStudentsById().get(id);
        if (student == null) {
            Map<String, Object> notFound = new java.util.HashMap<>();
            notFound.put(SUCCESS_KEY, false);
            notFound.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(notFound);
        }
        Map<String, Object> replacement = profilePayload == null ? new java.util.HashMap<>() : new java.util.HashMap<>(profilePayload);
    store.getProfiles().put(id, replacement);
        return buildProfileResponse(student, replacement, HttpStatus.OK, "Profile replaced (mock mode)");
    }

    /**
     * Patch (merge) a profile partially. Creates if absent.
     */
    @PatchMapping("/{id}/profile")
    public ResponseEntity<Map<String, Object>> patchProfile(
        @PathVariable("id") String id,
        @RequestBody(required = false) Map<String, Object> profilePayload
    ) {
    MockDataStore.MockStudent student = store.getStudentsById().get(id);
        if (student == null) {
            Map<String, Object> notFound = new java.util.HashMap<>();
            notFound.put(SUCCESS_KEY, false);
            notFound.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(notFound);
        }
        if (profilePayload == null) profilePayload = new java.util.HashMap<>();
    Map<String, Object> existing = store.getProfiles().getOrDefault(id, new java.util.HashMap<>());
        existing.putAll(profilePayload);
    store.getProfiles().put(id, existing);
        return buildProfileResponse(student, existing, HttpStatus.OK, "Profile patched (mock mode)");
    }

    /**
     * Persist RIASEC scores separately (also merges into profile). Payload shape: { riasecScores: {Realistic:%, ...}, rawAnswers:[...] }
     */
    @PostMapping("/{id}/assessments")
    public ResponseEntity<Map<String,Object>> addAssessmentRun(@PathVariable("id") String id, @RequestBody Map<String,Object> body) {
        MockDataStore.MockStudent student = store.getStudentsById().get(id);
        if (student == null) {
            Map<String,Object> nf = new java.util.HashMap<>();
            nf.put(SUCCESS_KEY,false);
            nf.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(nf);
        }
        java.util.List<Map<String,Object>> history = store.getAssessmentHistory().computeIfAbsent(id, k -> new java.util.ArrayList<>());
        Map<String,Object> run = new java.util.HashMap<>();
        run.put("timestamp", java.time.Instant.now().toString());
        if (body != null) run.putAll(body);
        history.add(run);
        // Merge RIASEC scores into profile if present
        if (body != null && body.containsKey(RIASEC_KEY)) {
            Map<String,Object> profile = store.getProfiles().getOrDefault(id, new java.util.HashMap<>());
            profile.put(RIASEC_KEY, body.get(RIASEC_KEY));
            store.getProfiles().put(id, profile);
        }
        Map<String,Object> resp = new java.util.HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(MESSAGE_KEY,"Assessment run stored (mock mode)");
        resp.put(DATA_KEY, run);
        return ResponseEntity.status(HttpStatus.CREATED).body(resp);
    }

    @GetMapping("/{id}/assessments")
    public ResponseEntity<Map<String,Object>> listAssessmentRuns(@PathVariable("id") String id) {
        MockDataStore.MockStudent student = store.getStudentsById().get(id);
        if (student == null) {
            Map<String,Object> nf = new java.util.HashMap<>();
            nf.put(SUCCESS_KEY,false);
            nf.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(nf);
        }
        java.util.List<Map<String,Object>> history = store.getAssessmentHistory().getOrDefault(id, java.util.Collections.emptyList());
        Map<String,Object> resp = new java.util.HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(MESSAGE_KEY,"Assessment history retrieved (mock mode)");
        resp.put(DATA_KEY, history);
        return ResponseEntity.ok(resp);
    }

    /**
     * Delete a student's profile if present.
     */
    @DeleteMapping("/{id}/profile")
    public ResponseEntity<Map<String, Object>> deleteProfile(@PathVariable("id") String id) {
    MockDataStore.MockStudent student = store.getStudentsById().get(id);
        if (student == null) {
            Map<String, Object> notFound = new java.util.HashMap<>();
            notFound.put(SUCCESS_KEY, false);
            notFound.put(MESSAGE_KEY, NOT_FOUND_PREFIX + id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(notFound);
        }
    Map<String, Object> removed = store.getProfiles().remove(id);
        Map<String, Object> resp = new java.util.HashMap<>();
        resp.put(SUCCESS_KEY, true);
        resp.put(MESSAGE_KEY, removed == null ? "No profile existed to delete" : "Profile deleted (mock mode)");
        if (removed != null) resp.put("deletedProfile", removed);
        return ResponseEntity.ok(resp);
    }

    /**
     * List all profiles (basic student info + profile map).
     */
    @GetMapping("/profiles")
    public ResponseEntity<Map<String, Object>> listProfiles() {
        java.util.List<Map<String, Object>> list = new java.util.ArrayList<>();
        for (Map.Entry<String, Map<String, Object>> entry : store.getProfiles().entrySet()) {
            MockDataStore.MockStudent student = store.getStudentsById().get(entry.getKey());
            if (student == null) continue; // defensive
            Map<String, Object> item = new java.util.HashMap<>();
            item.put("id", student.getId());
            item.put(EMAIL_KEY, student.getEmail());
            item.put("name", student.getName());
            if (student.getGradeLevel() != null) item.put(GRADE_LEVEL_KEY, student.getGradeLevel());
            item.put(PROFILE_KEY, entry.getValue());
            list.add(item);
        }
        Map<String, Object> response = new java.util.HashMap<>();
        response.put(SUCCESS_KEY, true);
        response.put(DATA_KEY, list);
        response.put(MESSAGE_KEY, "Profiles listed (mock mode)");
        return ResponseEntity.ok(response);
    }

    // Helper to standardize profile responses
    private ResponseEntity<Map<String, Object>> buildProfileResponse(MockDataStore.MockStudent student, Map<String, Object> profile, HttpStatus status, String message) {
        Map<String, Object> data = new java.util.HashMap<>();
        data.put("id", student.getId());
        data.put(EMAIL_KEY, student.getEmail());
        data.put("name", student.getName());
        if (student.getGradeLevel() != null) data.put(GRADE_LEVEL_KEY, student.getGradeLevel());
        data.put(PROFILE_KEY, profile);
        Map<String, Object> response = new java.util.HashMap<>();
        response.put(SUCCESS_KEY, true);
        response.put(MESSAGE_KEY, message);
        response.put(DATA_KEY, data);
        return ResponseEntity.status(status).body(response);
    }

    // Simple DTOs for mock registration
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MockStudentRegistrationRequest {
        @Email
        @NotBlank
        private String email;

        // Name may come as either 'name' or 'fullName' from frontend; derive later if needed
        private String name;
        private String fullName;

        // Additional fields coming from UI
        @NotBlank(message = "Password is required")
        private String password; // NOT hashed (mock mode only)
        private String phoneNumber;
        private Integer age;
        private String gradeLevel;
    // Extended fields
    private String city;
    private String state;
    private String educationLevel;
    private String institutionName;
    private String stream;
    private boolean agreeToTerms;
    private boolean agreeToPrivacyPolicy;

        // Custom validation: ensure either name or fullName present
        @jakarta.validation.constraints.AssertTrue(message = "Either name or fullName must be provided")
        public boolean isNameProvided() {
            return (name != null && !name.isBlank()) || (fullName != null && !fullName.isBlank());
        }

        // Getters for extended fields (Lombok @Data will generate but explicit methods helpful if needed)
        // (No additional logic needed)

        // Getters / Setters generated by Lombok (@Data)
    }

    @Data
    @AllArgsConstructor
    public static class MockStudent {
        private String id;
        private String email;
        private String name;
        private String gradeLevel;
        private LocalDateTime createdAt;
    }
}
