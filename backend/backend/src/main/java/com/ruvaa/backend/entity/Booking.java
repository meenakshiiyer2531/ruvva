package com.ruvaa.backend.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import com.google.cloud.Timestamp;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Booking {

    private String id;

    private String userId; // For Firebase relationships
    private String mentorId; // For Firebase relationships
    private com.google.cloud.Timestamp bookingDate;
    private Integer sessionDuration; // in minutes
    private BookingStatus status;
    private String notes;
    private com.google.cloud.Timestamp createdAt;
    private com.google.cloud.Timestamp updatedAt;

    public void onCreate() {
        createdAt = com.google.cloud.Timestamp.now();
        updatedAt = com.google.cloud.Timestamp.now();
        if (status == null) {
            status = BookingStatus.PENDING;
        }
    }

    public void onUpdate() {
        updatedAt = com.google.cloud.Timestamp.now();
    }
    
    public enum BookingStatus {
        PENDING, CONFIRMED, COMPLETED, CANCELLED
    }
}