package com.ruvaa.backend.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class College {

    private Long id;
    private String name;
    private String location;
    private String programs;
    private String website;
    private String contact;
    private String type;
    private String affiliation;
    private String description;
    private String admissionCriteria;
}