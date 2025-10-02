package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.BookingRequest;
import com.ruvaa.backend.entity.Booking;
import com.ruvaa.backend.entity.Mentor;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.repository.BookingRepository;
import com.ruvaa.backend.repository.MentorRepository;
import com.ruvaa.backend.repository.UserRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

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
            User user = userRepository.findByUsername(authentication.getName())
                    .orElseThrow(() -> new RuntimeException("User not found"));

            Mentor mentor = mentorRepository.findById(request.getMentorId())
                    .orElseThrow(() -> new RuntimeException("Mentor not found"));

            Booking booking = new Booking();
            booking.setUser(user);
            booking.setMentor(mentor);
            booking.setBookingDate(request.getBookingDate());
            booking.setSessionDuration(request.getSessionDuration() != null ? request.getSessionDuration() : 60);
            booking.setNotes(request.getNotes());

            Booking savedBooking = bookingRepository.save(booking);
            return ResponseEntity.ok(savedBooking);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/bookings")
    public ResponseEntity<List<Booking>> getUserBookings(Authentication authentication) {
        try {
            User user = userRepository.findByUsername(authentication.getName())
                    .orElseThrow(() -> new RuntimeException("User not found"));

            List<Booking> bookings = bookingRepository.findByUserOrderByBookingDateDesc(user);
            return ResponseEntity.ok(bookings);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
}