package com.ruvaa.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class UserDto {
    private String id;  // Changed to String to support Firebase UIDs
    private String username;
    private String name;
    private String email;
    private String phone;
    private Integer age;
    private String location;
    private String education;
    private String interests;
    private LocalDateTime createdAt;
}