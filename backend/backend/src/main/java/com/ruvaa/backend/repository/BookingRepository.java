package com.ruvaa.backend.repository;

import com.ruvaa.backend.entity.Booking;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.entity.Mentor;
import java.util.List;
import java.util.Optional;

public interface BookingRepository {
    List<Booking> findByUserOrderByBookingDateDesc(String userId);
    List<Booking> findByMentorOrderByBookingDateDesc(String mentorId);
    List<Booking> findByUserAndStatusOrderByBookingDateDesc(String userId, Booking.BookingStatus status);
    Booking save(Booking booking);
    Optional<Booking> findById(String id);
    void deleteById(String id);
}