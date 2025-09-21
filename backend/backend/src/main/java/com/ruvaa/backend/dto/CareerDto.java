package com.ruvaa.backend.dto;

import lombok.Data;
import java.util.List;

@Data
public class CareerDto {
    private String id;
    private String title;
    private String desc;
    private String category;
    private List<String> tags;
    private Double scoreMatch;
    private List<LearningStepDto> learningPath;
}