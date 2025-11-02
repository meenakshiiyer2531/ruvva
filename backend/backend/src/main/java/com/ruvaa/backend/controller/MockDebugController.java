package com.ruvaa.backend.controller;

import com.ruvaa.backend.mock.MockDataStore;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/debug/mock-store")
@RequiredArgsConstructor
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "false", matchIfMissing = true)
public class MockDebugController {

    private final MockDataStore store;

    @GetMapping
    public ResponseEntity<Map<String, Object>> snapshot() {
        return ResponseEntity.ok(Map.of(
            "studentsByEmailCount", store.getStudentsByEmail().size(),
            "authUsersCount", store.getAuthUsers().size(),
            "profilesCount", store.getProfiles().size(),
            "studentsEmails", store.getStudentsByEmail().keySet(),
            "authEmails", store.getAuthUsers().keySet()
        ));
    }
}
