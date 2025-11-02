package com.ruvaa.backend.controller;

import com.ruvaa.backend.mock.MockDataStore;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.constraints.NotBlank;
import java.util.*;

/**
 * Mock Mentor Controller (active only in mock mode) providing mentor catalog and bookings.
 * Notifications removed per updated requirements. Provides booking detail with meeting link.
 */
@Slf4j
@RestController
@RequestMapping("/mentors")
@Validated
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "false", matchIfMissing = true)
public class MentorController {

    private final MockDataStore store;
    private static final String SUCCESS_KEY = "success";
    private static final String MESSAGE_KEY = "message";
    private static final String DATA_KEY = "data";
    private static final String MENTOR_NOT_FOUND_PREFIX = "Mentor not found: ";
    private static final String DATE_REQUIRED_MESSAGE = "Date is required";

    public MentorController(MockDataStore store) { this.store = store; }

    // --- Catalog ---
    @GetMapping
    public ResponseEntity<Map<String,Object>> listMentors() {
        List<Map<String,Object>> list = new ArrayList<>();
        for (MockDataStore.MockMentor m : store.getMentorsById().values()) {
            list.add(mentorToMap(m));
        }
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(DATA_KEY,list);
        resp.put(MESSAGE_KEY,"Mentors listed (mock mode)");
        return ResponseEntity.ok(resp);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Map<String,Object>> getMentor(@PathVariable String id) {
        MockDataStore.MockMentor m = store.getMentorsById().get(id);
        if (m == null) return notFound(MENTOR_NOT_FOUND_PREFIX + id);
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(DATA_KEY, mentorToMap(m));
        resp.put(MESSAGE_KEY,"Mentor retrieved (mock mode)");
        return ResponseEntity.ok(resp);
    }

    @GetMapping("/{id}/availability")
    public ResponseEntity<Map<String,Object>> availability(@PathVariable String id) {
        MockDataStore.MockMentor m = store.getMentorsById().get(id);
        if (m == null) return notFound(MENTOR_NOT_FOUND_PREFIX + id);
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(DATA_KEY, m.getAvailability());
        resp.put(MESSAGE_KEY,"Availability retrieved (mock mode)");
        return ResponseEntity.ok(resp);
    }

    // --- Booking Creation ---
    @PostMapping("/{id}/bookings")
    public ResponseEntity<Map<String,Object>> book(@PathVariable String id, @RequestBody BookingRequest req) {
        MockDataStore.MockMentor mentor = store.getMentorsById().get(id);
        if (mentor == null) return notFound(MENTOR_NOT_FOUND_PREFIX + id);
        if (req == null || req.getDate() == null || req.getDate().isBlank()) return badRequest(DATE_REQUIRED_MESSAGE);

        String studentId = resolveStudent(req.getStudentId(), req.getStudentEmail());

        // Conflict check
        boolean conflict = store.getBookingsByMentorId().getOrDefault(id, Collections.emptyList())
            .stream().anyMatch(b -> b.getDate().equals(req.getDate()) && !"CANCELLED".equalsIgnoreCase(b.getStatus()));
        if (conflict) {
            return conflictResponse("Slot already booked for that date");
        }

        MockDataStore.MockBooking booking = new MockDataStore.MockBooking(
            "booking-" + System.currentTimeMillis(),
            studentId,
            mentor.getId(),
            req.getDate(),
            java.time.Instant.now(),
            "BOOKED",
            generateMeetLink()
        );
        store.getBookingsByMentorId().computeIfAbsent(mentor.getId(), k -> new ArrayList<>()).add(booking);
        if (studentId != null) store.getBookingsByStudentId().computeIfAbsent(studentId, k -> new ArrayList<>()).add(booking);

        Map<String,Object> data = bookingToMap(booking, mentor);
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(DATA_KEY,data);
        resp.put(MESSAGE_KEY,"Booking created (mock mode)");
        return ResponseEntity.status(HttpStatus.CREATED).body(resp);
    }

    // --- Listing ---
    @GetMapping("/{id}/bookings")
    public ResponseEntity<Map<String,Object>> listMentorBookings(@PathVariable String id) {
        MockDataStore.MockMentor mentor = store.getMentorsById().get(id);
        if (mentor == null) return notFound(MENTOR_NOT_FOUND_PREFIX + id);
        List<MockDataStore.MockBooking> list = store.getBookingsByMentorId().getOrDefault(id, Collections.emptyList());
        List<Map<String,Object>> dto = new ArrayList<>();
        list.forEach(b -> dto.add(bookingToMap(b, mentor)));
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(DATA_KEY,dto);
        resp.put(MESSAGE_KEY,"Mentor bookings listed (mock mode)");
        return ResponseEntity.ok(resp);
    }

    @GetMapping("/students/{studentId}/bookings")
    public ResponseEntity<Map<String,Object>> listStudentBookings(@PathVariable String studentId) {
        List<MockDataStore.MockBooking> list = store.getBookingsByStudentId().getOrDefault(studentId, Collections.emptyList());
        List<Map<String,Object>> dto = new ArrayList<>();
        for (MockDataStore.MockBooking b : list) {
            MockDataStore.MockMentor mentor = store.getMentorsById().get(b.getMentorId());
            dto.add(bookingToMap(b, mentor));
        }
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(DATA_KEY,dto);
        resp.put(MESSAGE_KEY,"Student bookings listed (mock mode)");
        return ResponseEntity.ok(resp);
    }

    // --- Booking Detail ---
    @GetMapping("/bookings/{bookingId}")
    public ResponseEntity<Map<String,Object>> getBooking(@PathVariable String bookingId) {
        MockDataStore.MockBooking found = store.getBookingsByMentorId().values().stream()
            .flatMap(List::stream)
            .filter(b -> b.getId().equals(bookingId))
            .findFirst().orElse(null);
        if (found == null) return notFound("Booking not found: " + bookingId);
        MockDataStore.MockMentor mentor = store.getMentorsById().get(found.getMentorId());
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(DATA_KEY, bookingToMap(found, mentor));
        resp.put(MESSAGE_KEY,"Booking retrieved (mock mode)");
        return ResponseEntity.ok(resp);
    }

    // Legacy endpoint supporting existing frontend POST /mentors/book
    @PostMapping("/book")
    public ResponseEntity<Map<String,Object>> legacyBook(@RequestBody LegacyBookingRequest legacy) {
        if (legacy == null || legacy.getDate() == null || legacy.getDate().isBlank()) return badRequest(DATE_REQUIRED_MESSAGE);
        MockDataStore.MockMentor mentor = resolveMentor(legacy.getMentorId(), legacy.getMentorName());
        if (mentor == null) return notFound("Mentor not found for legacy booking");
        String studentId = resolveStudentByName(legacy.getStudentName());
        boolean conflict = store.getBookingsByMentorId().getOrDefault(mentor.getId(), Collections.emptyList()).stream()
            .anyMatch(b -> b.getDate().equals(legacy.getDate()) && !"CANCELLED".equalsIgnoreCase(b.getStatus()));
        if (conflict) return conflictResponse("Slot already booked for that date");
        MockDataStore.MockBooking booking = new MockDataStore.MockBooking(
            "booking-" + System.currentTimeMillis(),
            studentId,
            mentor.getId(),
            legacy.getDate(),
            java.time.Instant.now(),
            "BOOKED",
            generateMeetLink()
        );
        store.getBookingsByMentorId().computeIfAbsent(mentor.getId(), k -> new ArrayList<>()).add(booking);
        if (studentId != null) store.getBookingsByStudentId().computeIfAbsent(studentId, k -> new ArrayList<>()).add(booking);
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,true);
        resp.put(DATA_KEY, bookingToMap(booking, mentor));
        resp.put(MESSAGE_KEY, "Legacy booking created (mock mode)");
        return ResponseEntity.status(HttpStatus.CREATED).body(resp);
    }

    // --- Helpers ---
    private Map<String,Object> mentorToMap(MockDataStore.MockMentor m) {
        Map<String,Object> map = new HashMap<>();
        map.put("id", m.getId());
        map.put("name", m.getName());
        map.put("expertise", m.getExpertise());
        map.put("bio", m.getBio());
        map.put("linkedin", m.getLinkedin());
        map.put("availability", m.getAvailability());
        return map;
    }

    private Map<String,Object> bookingToMap(MockDataStore.MockBooking b, MockDataStore.MockMentor mentor) {
        Map<String,Object> map = new HashMap<>();
        map.put("id", b.getId());
        map.put("mentorId", b.getMentorId());
        if (mentor != null) {
            map.put("mentorName", mentor.getName());
            map.put("mentorBio", mentor.getBio());
            map.put("mentorExpertise", mentor.getExpertise());
            map.put("mentorLinkedin", mentor.getLinkedin());
        }
        map.put("date", b.getDate());
        map.put("status", b.getStatus());
        map.put("createdAt", b.getCreatedAt().toString());
        map.put("meetingLink", b.getMeetingLink());
        return map;
    }

    private String resolveStudent(String studentId, String studentEmail) {
        if (studentId != null && store.getStudentsById().containsKey(studentId)) return studentId;
        if (studentEmail != null && store.getStudentsByEmail().containsKey(studentEmail)) {
            return store.getStudentsByEmail().get(studentEmail).getId();
        }
        return null;
    }

    private String resolveStudentByName(String name) {
        if (name == null) return null;
        return store.getStudentsByEmail().values().stream()
            .filter(s -> s.getName() != null && s.getName().equalsIgnoreCase(name))
            .map(MockDataStore.MockStudent::getId)
            .findFirst().orElse(null);
    }

    private MockDataStore.MockMentor resolveMentor(String id, String name) {
        MockDataStore.MockMentor mentor = null;
        if (id != null) mentor = store.getMentorsById().get(id);
        if (mentor == null && name != null) {
            mentor = store.getMentorsById().values().stream()
                .filter(m -> m.getName().equalsIgnoreCase(name))
                .findFirst().orElse(null);
        }
        return mentor;
    }


    private String generateMeetLink() {
        String token = java.util.UUID.randomUUID().toString().substring(0,8);
        return "https://meet.google.com/" + token;
    }

    private ResponseEntity<Map<String,Object>> notFound(String msg) {
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,false);
        resp.put(MESSAGE_KEY,msg);
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(resp);
    }
    private ResponseEntity<Map<String,Object>> badRequest(String msg) {
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,false);
        resp.put(MESSAGE_KEY,msg);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(resp);
    }
    private ResponseEntity<Map<String,Object>> conflictResponse(String msg) {
        Map<String,Object> resp = new HashMap<>();
        resp.put(SUCCESS_KEY,false);
        resp.put(MESSAGE_KEY,msg);
        return ResponseEntity.status(HttpStatus.CONFLICT).body(resp);
    }

    // --- DTO ---
    @Data
    public static class BookingRequest {
        @NotBlank
        private String date; // ISO yyyy-MM-dd
        private String studentId; // optional
        private String studentEmail; // alternative resolution
    }

    @Data
    public static class LegacyBookingRequest {
        private String mentorId;
        private String mentorName;
        private String studentName;
        private String date;
    }
}