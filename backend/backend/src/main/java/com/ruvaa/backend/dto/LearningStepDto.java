package com.ruvaa.backend.dto;

import lombok.Data;
import java.util.List;

@Data
public class LearningStepDto {
    private String step;
    private List<String> resources;
}