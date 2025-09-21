package com.ruvaa.backend.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.util.List;

@Data
public class AssessmentRequest {
    
    @NotNull(message = "Answers are required")
    private List<AnswerDto> answers;
    
    @Data
    public static class AnswerDto {
        private String question;
        private String answer;
        private Integer points;
    }
}