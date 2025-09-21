package com.ruvaa.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class ChatResponse {
    private String message;
    private String response;
    private Boolean isFromUser;
    private LocalDateTime timestamp;
}