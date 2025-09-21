package com.ruvaa.backend.service;

import com.ruvaa.backend.dto.CareerDto;
import com.ruvaa.backend.dto.ProfileRequest;
import com.ruvaa.backend.dto.ProfileResponse;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

@Service
public class ProfileService {

    private final Map<String, ProfileResponse> profiles = new HashMap<>();

    public ProfileResponse getProfile(String username) {
        return profiles.getOrDefault(username, createDefaultProfile());
    }

    public ProfileResponse updateProfile(String username, ProfileRequest request) {
        ProfileResponse profile = new ProfileResponse();
        profile.setName(request.getName());
        profile.setStudentClass(request.getStudentClass());
        profile.setLocation(request.getLocation());
        profile.setAspirations(request.getAspirations());
        profile.setSavedCareers(request.getSavedCareers() != null ? request.getSavedCareers() : new ArrayList<>());

        profiles.put(username, profile);
        return profile;
    }

    private ProfileResponse createDefaultProfile() {
        ProfileResponse profile = new ProfileResponse();
        profile.setName("");
        profile.setStudentClass("");
        profile.setLocation("");
        profile.setAspirations("");
        profile.setSavedCareers(new ArrayList<>());
        return profile;
    }
}