package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.BookingRequest;
import com.ruvaa.backend.entity.Booking;
import com.ruvaa.backend.entity.Mentor;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.model.entity.Student;
import com.ruvaa.backend.repository.BookingRepository;
import com.ruvaa.backend.repository.MentorRepository;
import com.ruvaa.backend.repository.UserRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.time.ZoneOffset;

@Slf4j
@RestController
@RequestMapping("/mentors")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class MentorController {

    private final MentorRepository mentorRepository;
    private final BookingRepository bookingRepository;
    private final UserRepository userRepository;

    @GetMapping("/list")
    public ResponseEntity<List<Mentor>> getAllMentors() {
        List<Mentor> mentors = mentorRepository.findAll();
        return ResponseEntity.ok(mentors);
    }

    @GetMapping("/specialization/{specialization}")
    public ResponseEntity<List<Mentor>> getMentorsBySpecialization(@PathVariable String specialization) {
        List<Mentor> mentors = mentorRepository.findBySpecialization(specialization);
        return ResponseEntity.ok(mentors);
    }

    @PostMapping("/book")
    public ResponseEntity<Booking> bookMentor(@Valid @RequestBody BookingRequest request,
                                            Authentication authentication) {
        try {
            Student student = (Student) authentication.getPrincipal();

            Mentor mentor = mentorRepository.findById(request.getMentorId())
                    .orElseThrow(() -> new RuntimeException("Mentor not found"));

            Booking booking = new Booking();
            booking.setUserId(student.getId());
            booking.setMentorId(request.getMentorId().toString()); // Convert Long to String

            booking.setBookingDate(com.google.cloud.Timestamp.of(java.util.Date.from(request.getBookingDate().toInstant(java.time.ZoneOffset.UTC))));
            booking.setSessionDuration(request.getSessionDuration() != null ? request.getSessionDuration() : 60);
            booking.setNotes(request.getNotes());

            Booking savedBooking = bookingRepository.save(booking);
            return ResponseEntity.ok(savedBooking);
        } catch (Exception e) {
            log.error("Failed to book mentor: {}", e.getMessage());
            return ResponseEntity.badRequest().body(null); // Return null body for 400
        }
    }

    @GetMapping("/bookings")
    public ResponseEntity<List<Booking>> getUserBookings(Authentication authentication) {
        try {
            Student student = (Student) authentication.getPrincipal();

            List<Booking> bookings = bookingRepository.findByUserOrderByBookingDateDesc(student.getId());
            return ResponseEntity.ok(bookings);
        } catch (Exception e) {
            log.error("Failed to get user bookings: {}", e.getMessage());
            return ResponseEntity.badRequest().body(null);
        }
    }
}