package com.ruvaa.backend.mock;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Simple JSON-based persistence for mock mode so data survives restarts during local dev.
 * NOT for production use.
 */
@Slf4j
@Component
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "false", matchIfMissing = true)
public class MockDataPersistenceService {

    private final MockDataStore store;
    private final Path file = Path.of("mock-data-store.json");
    private static final String STUDENTS_KEY = "students";
    private static final String PROFILES_KEY = "profiles";
    private static final String AUTH_USERS_KEY = "authUsers";
    private static final String MENTORS_KEY = "mentors";
    private static final String BOOKINGS_KEY = "bookings";
    private static final String CREATED_AT_KEY = "createdAt";
    private static final String NAME_KEY = "name";
    private static final String ID_KEY = "id";
    private static final String PASSWORD_KEY = "password";
    private static final String GRADE_LEVEL_KEY = "gradeLevel";

    public MockDataPersistenceService(MockDataStore store) { this.store = store; }

    @PostConstruct
    @SuppressWarnings("unchecked")
    public void load() {
        if (!Files.exists(file)) {
            log.info("[MockPersist] No existing store file found.");
            return;
        }
        String json;
        try { json = Files.readString(file); } catch (IOException e) { log.error("[MockPersist] Read file failed", e); return; }
        if (json.isBlank()) return;
        Map<String,Object> root;
        try { root = new ObjectMapper().readValue(json, Map.class); } catch (Exception e) { log.error("[MockPersist] Parse JSON failed", e); return; }
        parseStudents(root.get(STUDENTS_KEY));
        parseProfiles(root.get(PROFILES_KEY));
        parseAuth(root.get(AUTH_USERS_KEY));
        parseMentors(root.get(MENTORS_KEY));
        parseBookings(root.get(BOOKINGS_KEY));
        log.info("[MockPersist] Loaded mock store: students={}, profiles={}, authUsers={}", store.getStudentsByEmail().size(), store.getProfiles().size(), store.getAuthUsers().size());
    }

    private void parseStudents(Object obj) {
        if (!(obj instanceof Map<?,?> map)) return;
        map.forEach((emailRaw, dataRaw) -> {
            if (!(dataRaw instanceof Map<?,?> data)) return;
            String email = String.valueOf(emailRaw);
            String id = stringVal(data.get(ID_KEY));
            String name = optionalString(data.get(NAME_KEY));
            String grade = data.get(GRADE_LEVEL_KEY) == null ? null : stringVal(data.get(GRADE_LEVEL_KEY));
            java.time.LocalDateTime created = parseDate(data.get(CREATED_AT_KEY));
            MockDataStore.MockStudent student = new MockDataStore.MockStudent(id, email, name, grade, created);
            store.getStudentsByEmail().put(email, student);
            store.getStudentsById().put(id, student);
        });
    }

    private void parseProfiles(Object obj) {
        if (!(obj instanceof Map<?,?> map)) return;
        map.forEach((idRaw, profileRaw) -> {
            if (!(profileRaw instanceof Map<?,?> pMap)) return;
            String sid = String.valueOf(idRaw);
            Map<String,Object> converted = new HashMap<>();
            pMap.forEach((k,v) -> converted.put(String.valueOf(k), v));
            store.getProfiles().put(sid, converted);
        });
    }

    private void parseAuth(Object obj) {
        if (!(obj instanceof Map<?,?> map)) return;
        map.forEach((emailRaw, dataRaw) -> {
            if (!(dataRaw instanceof Map<?,?> data)) return;
            String email = String.valueOf(emailRaw);
            String id = stringVal(data.get(ID_KEY));
            String pwd = data.get(PASSWORD_KEY) == null ? "mock-pass" : stringVal(data.get(PASSWORD_KEY));
            String name = optionalString(data.get(NAME_KEY));
            java.time.LocalDateTime created = parseDate(data.get(CREATED_AT_KEY));
            store.getAuthUsers().put(email, new MockDataStore.MockUserAuth(id, email, pwd, name, created));
        });
    }

    private void parseMentors(Object obj) {
        if (!(obj instanceof Map<?,?> map)) return;
        map.forEach((idRaw, dataRaw) -> {
            if (!(dataRaw instanceof Map<?,?> data)) return;
            String id = String.valueOf(idRaw);
            String name = optionalString(data.get(NAME_KEY));
            java.util.List<String> expertise = data.get("expertise") instanceof java.util.List<?> l ? l.stream().map(String::valueOf).toList() : java.util.Collections.emptyList();
            String bio = optionalString(data.get("bio"));
            String linkedin = optionalString(data.get("linkedin"));
            java.util.List<String> availability = data.get("availability") instanceof java.util.List<?> av ? av.stream().map(String::valueOf).toList() : java.util.Collections.emptyList();
            MockDataStore.MockMentor mentor = new MockDataStore.MockMentor(id, name, expertise, bio, linkedin, availability);
            store.getMentorsById().put(id, mentor);
        });
    }

    private void parseBookings(Object obj) {
        if (!(obj instanceof java.util.List<?> list)) return;
        for (Object raw : list) {
            if (!(raw instanceof Map<?,?> data)) continue;
            String id = stringVal(data.get(ID_KEY));
            String studentId = optionalString(data.get("studentId"));
            String mentorId = optionalString(data.get("mentorId"));
            String date = optionalString(data.get("date"));
            java.time.Instant createdAt = data.get(CREATED_AT_KEY) == null ? java.time.Instant.now() : java.time.Instant.parse(String.valueOf(data.get(CREATED_AT_KEY)));
            String status = optionalString(data.get("status"));
            String meetingLink = optionalString(data.get("meetingLink"));
            MockDataStore.MockBooking booking = new MockDataStore.MockBooking(id, studentId.isBlank()?null:studentId, mentorId, date, createdAt, status, meetingLink);
            store.getBookingsByMentorId().computeIfAbsent(mentorId, k -> new java.util.ArrayList<>()).add(booking);
            if (studentId != null && !studentId.isBlank()) store.getBookingsByStudentId().computeIfAbsent(studentId, k -> new java.util.ArrayList<>()).add(booking);
        }
    }

    @PreDestroy
    public void save() {
        try {
            Map<String,Object> root = new HashMap<>();
            Map<String,Object> students = new HashMap<>();
            store.getStudentsByEmail().forEach((email, s) -> {
                Map<String,Object> val = new HashMap<>();
                val.put(ID_KEY, s.getId());
                val.put("email", email);
                val.put(NAME_KEY, s.getName());
                val.put(GRADE_LEVEL_KEY, s.getGradeLevel());
                val.put(CREATED_AT_KEY, s.getCreatedAt().toString());
                students.put(email, val);
            });
            root.put(STUDENTS_KEY, students);
            root.put(PROFILES_KEY, new HashMap<>(store.getProfiles()));
            // mentors
            Map<String,Object> mentors = new HashMap<>();
            store.getMentorsById().forEach((id, m) -> {
                Map<String,Object> val = new HashMap<>();
                val.put(NAME_KEY, m.getName());
                val.put("expertise", m.getExpertise());
                val.put("bio", m.getBio());
                val.put("linkedin", m.getLinkedin());
                val.put("availability", m.getAvailability());
                mentors.put(id, val);
            });
            root.put(MENTORS_KEY, mentors);
            // bookings
            java.util.List<Map<String,Object>> bookings = new java.util.ArrayList<>();
            store.getBookingsByMentorId().values().forEach(list -> list.forEach(b -> {
                Map<String,Object> val = new HashMap<>();
                val.put(ID_KEY, b.getId());
                val.put("studentId", b.getStudentId());
                val.put("mentorId", b.getMentorId());
                val.put("date", b.getDate());
                val.put(CREATED_AT_KEY, b.getCreatedAt().toString());
                val.put("status", b.getStatus());
                val.put("meetingLink", b.getMeetingLink());
                bookings.add(val);
            }));
            root.put(BOOKINGS_KEY, bookings);
            Map<String,Object> auth = new HashMap<>();
            store.getAuthUsers().forEach((email, u) -> {
                Map<String,Object> val = new HashMap<>();
                val.put(ID_KEY, u.getId());
                val.put("email", email);
                val.put(NAME_KEY, u.getName());
                val.put(PASSWORD_KEY, u.getPassword());
                val.put(CREATED_AT_KEY, u.getCreatedAt().toString());
                auth.put(email, val);
            });
            root.put(AUTH_USERS_KEY, auth);
            String json = new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsString(root);
            Files.writeString(file, json);
            log.info("[MockPersist] Saved mock store file: {}", file.toAbsolutePath());
        } catch (IOException e) {
            log.error("[MockPersist] Failed to save mock data store", e);
        }
    }

    private java.time.LocalDateTime parseDate(Object val) {
        if (val == null) return java.time.LocalDateTime.now();
        try { return java.time.LocalDateTime.parse(String.valueOf(val)); } catch (Exception e) { return java.time.LocalDateTime.now(); }
    }

    private String stringVal(Object o) { return String.valueOf(o); }
    private String optionalString(Object o) { return o == null ? "" : String.valueOf(o); }
}
