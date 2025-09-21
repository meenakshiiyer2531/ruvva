package com.ruvaa.backend.controller;

import com.ruvaa.backend.entity.Career;
import com.ruvaa.backend.repository.CareerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/careers")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class CareerController {

    private final CareerRepository careerRepository;

    @GetMapping("/recommendations")
    public ResponseEntity<List<Career>> getRecommendations() {
        List<Career> careers = careerRepository.findAll();
        return ResponseEntity.ok(careers);
    }

    @GetMapping("/search")
    public ResponseEntity<List<Career>> searchCareers(@RequestParam String query) {
        List<Career> careers = careerRepository.searchCareers(query);
        return ResponseEntity.ok(careers);
    }

    @GetMapping("/category/{category}")
    public ResponseEntity<List<Career>> getCareersByCategory(@PathVariable String category) {
        List<Career> careers = careerRepository.findByCategory(category);
        return ResponseEntity.ok(careers);
    }
}