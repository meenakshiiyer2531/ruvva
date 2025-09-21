package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.ProfileRequest;
import com.ruvaa.backend.dto.ProfileResponse;
import com.ruvaa.backend.service.ProfileService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/profile")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class ProfileController {

    private final ProfileService profileService;

    @GetMapping
    public ResponseEntity<ProfileResponse> getProfile(Authentication authentication) {
        try {
            String username = authentication != null ? authentication.getName() : "anonymous";
            ProfileResponse profile = profileService.getProfile(username);
            return ResponseEntity.ok(profile);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @PostMapping
    public ResponseEntity<ProfileResponse> updateProfile(@RequestBody ProfileRequest request,
                                                        Authentication authentication) {
        try {
            String username = authentication != null ? authentication.getName() : "anonymous";
            ProfileResponse profile = profileService.updateProfile(username, request);
            return ResponseEntity.ok(profile);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
}