package com.ruvaa.backend.dto;

import lombok.Data;
import java.util.List;

@Data
public class ProfileResponse {
    private String name;
    private String studentClass;
    private String location;
    private String aspirations;
    private List<CareerDto> savedCareers;
}