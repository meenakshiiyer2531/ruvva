package com.ruvaa.backend.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Mentor {

    private Long id;
    private String name;
    private String specialization;
    private String philosophy;
    private String bio;
    private String experience;
    private String education;
    private String contact;
    private Double rating;
    private Double hourlyRate;
    private String availableSlots;
}