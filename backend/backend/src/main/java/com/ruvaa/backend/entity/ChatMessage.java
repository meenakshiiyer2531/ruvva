package com.ruvaa.backend.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatMessage {

    private Long id;
    private User user;
    private Long userId; // For Firebase relationships
    private String message;
    private String response;
    private Boolean isFromUser;
    private LocalDateTime createdAt;

    public void onCreate() {
        createdAt = LocalDateTime.now();
    }
}