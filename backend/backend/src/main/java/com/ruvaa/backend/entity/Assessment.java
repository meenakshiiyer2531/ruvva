package com.ruvaa.backend.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Assessment {

    private Long id;
    private User user;
    private Long userId; // For Firebase relationships
    private Integer totalScore;
    private Integer maxScore;
    private String answers;
    private String recommendations;
    private LocalDateTime createdAt;

    public void onCreate() {
        createdAt = LocalDateTime.now();
    }
}