package com.ruvaa.backend.controller;

import com.ruvaa.backend.entity.College;
import com.ruvaa.backend.repository.CollegeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/colleges")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class CollegeController {

    private final CollegeRepository collegeRepository;

    @GetMapping("/list")
    public ResponseEntity<List<College>> getAllColleges() {
        List<College> colleges = collegeRepository.findAll();
        return ResponseEntity.ok(colleges);
    }

    @GetMapping("/search")
    public ResponseEntity<List<College>> searchColleges(@RequestParam String query) {
        List<College> colleges = collegeRepository.searchColleges(query);
        return ResponseEntity.ok(colleges);
    }

    @GetMapping("/location/{location}")
    public ResponseEntity<List<College>> getCollegesByLocation(@PathVariable String location) {
        List<College> colleges = collegeRepository.findByLocation(location);
        return ResponseEntity.ok(colleges);
    }
}