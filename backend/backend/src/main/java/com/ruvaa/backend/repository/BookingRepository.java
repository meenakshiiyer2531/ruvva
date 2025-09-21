package com.ruvaa.backend.repository;

import com.ruvaa.backend.entity.Booking;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.entity.Mentor;
import java.util.List;
import java.util.Optional;

public interface BookingRepository {
    List<Booking> findByUserOrderByBookingDateDesc(User user);
    List<Booking> findByMentorOrderByBookingDateDesc(Mentor mentor);
    List<Booking> findByUserAndStatusOrderByBookingDateDesc(User user, Booking.BookingStatus status);
    Booking save(Booking booking);
    Optional<Booking> findById(Long id);
    void deleteById(Long id);
}