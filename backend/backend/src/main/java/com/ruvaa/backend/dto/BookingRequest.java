package com.ruvaa.backend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.time.LocalDateTime;

@Data
public class BookingRequest {
    
    @NotNull(message = "Mentor ID is required")
    private Long mentorId;
    
    @NotNull(message = "Booking date is required")
    private LocalDateTime bookingDate;
    
    private Integer sessionDuration;
    private String notes;
}