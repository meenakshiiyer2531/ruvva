package com.ruvaa.backend.mock;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Shared in-memory data store for mock mode (firebase.enabled=false).
 * Keeps student and profile data consistent across controllers.
 */
@Component
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "false", matchIfMissing = true)
public class MockDataStore {

    // email -> student record
    private final Map<String, MockStudent> studentsByEmail = new ConcurrentHashMap<>();
    // id -> student record
    private final Map<String, MockStudent> studentsById = new ConcurrentHashMap<>();
    // id -> profile map
    private final Map<String, Map<String, Object>> profiles = new ConcurrentHashMap<>();
    // id -> list of assessment runs (each run is a Map<String,Object>)
    private final Map<String, java.util.List<Map<String,Object>>> assessmentHistory = new ConcurrentHashMap<>();
    // email -> raw user auth record (for /auth endpoints)
    private final Map<String, MockUserAuth> authUsers = new ConcurrentHashMap<>();
    // mentorId -> mentor record
    private final Map<String, MockMentor> mentorsById = new ConcurrentHashMap<>();
    // studentId -> list of bookings
    private final Map<String, java.util.List<MockBooking>> bookingsByStudentId = new ConcurrentHashMap<>();
    // mentorId -> list of bookings
    private final Map<String, java.util.List<MockBooking>> bookingsByMentorId = new ConcurrentHashMap<>();
    // notifications removed per latest requirement (legacy structure retained for compatibility but unused)
    @Deprecated
    private final Map<String, java.util.List<MockNotification>> notificationsByStudentId = new ConcurrentHashMap<>();

    public Map<String, MockStudent> getStudentsByEmail() { return studentsByEmail; }
    public Map<String, MockStudent> getStudentsById() { return studentsById; }
    public Map<String, Map<String, Object>> getProfiles() { return profiles; }
    public Map<String, java.util.List<Map<String,Object>>> getAssessmentHistory() { return assessmentHistory; }
    public Map<String, MockUserAuth> getAuthUsers() { return authUsers; }
    public Map<String, MockMentor> getMentorsById() { return mentorsById; }
    public Map<String, java.util.List<MockBooking>> getBookingsByStudentId() { return bookingsByStudentId; }
    public Map<String, java.util.List<MockBooking>> getBookingsByMentorId() { return bookingsByMentorId; }
    @Deprecated
    public Map<String, java.util.List<MockNotification>> getNotificationsByStudentId() { return notificationsByStudentId; }

    // --- DTO inner classes (simple POJOs) ---
    public static class MockStudent {
        private final String id;
        private final String email;
        private String name;
        private String gradeLevel;
        private final java.time.LocalDateTime createdAt;
        public MockStudent(String id, String email, String name, String gradeLevel, java.time.LocalDateTime createdAt) {
            this.id = id; this.email = email; this.name = name; this.gradeLevel = gradeLevel; this.createdAt = createdAt;
        }
        public String getId() { return id; }
        public String getEmail() { return email; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getGradeLevel() { return gradeLevel; }
        public void setGradeLevel(String gradeLevel) { this.gradeLevel = gradeLevel; }
        public java.time.LocalDateTime getCreatedAt() { return createdAt; }
    }

    public static class MockUserAuth {
        private final String id;
        private final String email;
        private String password;
        private String name;
        private final java.time.LocalDateTime createdAt;
        public MockUserAuth(String id, String email, String password, String name, java.time.LocalDateTime createdAt) {
            this.id = id; this.email = email; this.password = password; this.name = name; this.createdAt = createdAt;
        }
        public String getId() { return id; }
        public String getEmail() { return email; }
        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public java.time.LocalDateTime getCreatedAt() { return createdAt; }
    }

    // --- Mentor / Booking / Notification POJOs ---
    public static class MockMentor {
        private final String id;
        private final String name;
        private final java.util.List<String> expertise;
        private final String bio;
        private final String linkedin;
        private final java.util.List<String> availability; // ISO date strings
        public MockMentor(String id, String name, java.util.List<String> expertise, String bio, String linkedin, java.util.List<String> availability) {
            this.id = id; this.name = name; this.expertise = expertise; this.bio = bio; this.linkedin = linkedin; this.availability = availability;
        }
        public String getId() { return id; }
        public String getName() { return name; }
        public java.util.List<String> getExpertise() { return expertise; }
        public String getBio() { return bio; }
        public String getLinkedin() { return linkedin; }
        public java.util.List<String> getAvailability() { return availability; }
    }

    public static class MockBooking {
        private final String id;
        private final String studentId; // may be null if resolution failed
        private final String mentorId;
        private final String date; // ISO date
        private final java.time.Instant createdAt;
        private String status; // BOOKED / CANCELLED
        private final String meetingLink; // Google Meet style link
        public MockBooking(String id, String studentId, String mentorId, String date, java.time.Instant createdAt, String status, String meetingLink) {
            this.id = id; this.studentId = studentId; this.mentorId = mentorId; this.date = date; this.createdAt = createdAt; this.status = status; this.meetingLink = meetingLink;
        }
        public String getId() { return id; }
        public String getStudentId() { return studentId; }
        public String getMentorId() { return mentorId; }
        public String getDate() { return date; }
        public java.time.Instant getCreatedAt() { return createdAt; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        public String getMeetingLink() { return meetingLink; }
    }

    public static class MockNotification {
        private final String id;
        private final String studentId;
        private final String type; // BOOKING_CONFIRMED, BOOKING_CONFLICT, GENERAL
        private final String message;
        private final java.time.Instant createdAt;
        private boolean read;
        public MockNotification(String id, String studentId, String type, String message, java.time.Instant createdAt) {
            this.id = id; this.studentId = studentId; this.type = type; this.message = message; this.createdAt = createdAt; this.read = false;
        }
        public String getId() { return id; }
        public String getStudentId() { return studentId; }
        public String getType() { return type; }
        public String getMessage() { return message; }
        public java.time.Instant getCreatedAt() { return createdAt; }
        public boolean isRead() { return read; }
        public void markRead() { this.read = true; }
    }

    // Seed mentors if empty (simple inline seeding; could be moved to persistence later)
    @jakarta.annotation.PostConstruct
    public void seedMentors() {
        if (!mentorsById.isEmpty()) return;
        java.util.List<MockMentor> seed = java.util.List.of(
            new MockMentor("mentor-1","Dr. Ananya Gupta", java.util.List.of("Career Counseling","Educational Psychology","Motivation"), "Licensed counseling psychologist with 12+ years helping students clarify academic & career direction.", "https://www.linkedin.com/in/ananya-gupta", java.util.List.of("2025-11-03","2025-11-05","2025-11-07")),
            new MockMentor("mentor-2","Prof. Rohan Mehta", java.util.List.of("Artificial Intelligence","Machine Learning","Data Science"), "University professor & applied ML researcher focusing on ethical AI and student mentorship.", "https://www.linkedin.com/in/rohan-mehta", java.util.List.of("2025-11-04","2025-11-06","2025-11-08")),
            new MockMentor("mentor-3","Ms. Kavya Rao", java.util.List.of("UX Design","Product Strategy","Innovation"), "Senior product designer at a SaaS scale-up, coaching on user research and portfolio building.", "https://www.linkedin.com/in/kavya-rao", java.util.List.of("2025-11-03","2025-11-05","2025-11-09")),
            new MockMentor("mentor-4","Mr. Arvind Singh", java.util.List.of("Cybersecurity","Cloud Security","Python"), "Security analyst focused on threat modeling & secure architecture reviews; mentor for security career transitions.", "https://www.linkedin.com/in/arvind-singh", java.util.List.of("2025-11-04","2025-11-07","2025-11-10")),
            new MockMentor("mentor-5","Dr. Neha Joshi", java.util.List.of("Robotics","Automation","STEM Outreach"), "Robotics researcher leading university-industry collaborations; passionate about hands-on STEM mentoring.", "https://www.linkedin.com/in/neha-joshi", java.util.List.of("2025-11-03","2025-11-06","2025-11-08"))
        );
        seed.forEach(m -> mentorsById.put(m.getId(), m));
    }
}
