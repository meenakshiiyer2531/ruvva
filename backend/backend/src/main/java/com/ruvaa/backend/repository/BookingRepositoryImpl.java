package com.ruvaa.backend.repository;

import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.Query;
import com.google.cloud.firestore.QueryDocumentSnapshot;
import com.ruvaa.backend.entity.Booking;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.entity.Mentor;
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
public class BookingRepositoryImpl implements BookingRepository {

    private final Firestore firestore;
    private static final String COLLECTION_NAME = "bookings";

    @Override
    public List<Booking> findByUserOrderByBookingDateDesc(User user) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("userId", user.getId())
                    .orderBy("bookingDate", Query.Direction.DESCENDING)
                    .get()
                    .get();

            List<Booking> bookings = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Booking booking = document.toObject(Booking.class);
                booking.setId(Long.parseLong(document.getId()));
                bookings.add(booking);
            }
            return bookings;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding bookings by user: {}", user.getId(), e);
            return new ArrayList<>();
        }
    }

    @Override
    public List<Booking> findByMentorOrderByBookingDateDesc(Mentor mentor) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("mentorId", mentor.getId())
                    .orderBy("bookingDate", Query.Direction.DESCENDING)
                    .get()
                    .get();

            List<Booking> bookings = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Booking booking = document.toObject(Booking.class);
                booking.setId(Long.parseLong(document.getId()));
                bookings.add(booking);
            }
            return bookings;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding bookings by mentor: {}", mentor.getId(), e);
            return new ArrayList<>();
        }
    }

    @Override
    public List<Booking> findByUserAndStatusOrderByBookingDateDesc(User user, Booking.BookingStatus status) {
        try {
            var query = firestore.collection(COLLECTION_NAME)
                    .whereEqualTo("userId", user.getId())
                    .whereEqualTo("status", status.name())
                    .orderBy("bookingDate", Query.Direction.DESCENDING)
                    .get()
                    .get();

            List<Booking> bookings = new ArrayList<>();
            for (QueryDocumentSnapshot document : query.getDocuments()) {
                Booking booking = document.toObject(Booking.class);
                booking.setId(Long.parseLong(document.getId()));
                bookings.add(booking);
            }
            return bookings;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding bookings by user and status: {} {}", user.getId(), status, e);
            return new ArrayList<>();
        }
    }

    @Override
    public Booking save(Booking booking) {
        try {
            if (booking.getId() == null) {
                booking.setId(System.currentTimeMillis());
            }

            firestore.collection(COLLECTION_NAME)
                    .document(booking.getId().toString())
                    .set(booking)
                    .get();

            return booking;
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error saving booking: {}", booking.getId(), e);
            throw new RuntimeException("Failed to save booking", e);
        }
    }

    @Override
    public Optional<Booking> findById(Long id) {
        try {
            var document = firestore.collection(COLLECTION_NAME)
                    .document(id.toString())
                    .get()
                    .get();

            if (document.exists()) {
                Booking booking = document.toObject(Booking.class);
                booking.setId(id);
                return Optional.of(booking);
            }
            return Optional.empty();
        } catch (InterruptedException | ExecutionException e) {
            log.error("Error finding booking by id: {}", id, e);
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
            log.error("Error deleting booking by id: {}", id, e);
            throw new RuntimeException("Failed to delete booking", e);
        }
    }
}