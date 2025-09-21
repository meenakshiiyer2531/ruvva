package com.ruvaa.backend.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Career {

    private Long id;
    private String name;
    private String icon;
    private String description;
    private String requiredSkills;
    private String salaryRange;
    private String growthProspects;
    private String category;
}