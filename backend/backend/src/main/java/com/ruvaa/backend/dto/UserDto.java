package com.ruvaa.backend.dto;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class UserDto {
    private Long id;
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