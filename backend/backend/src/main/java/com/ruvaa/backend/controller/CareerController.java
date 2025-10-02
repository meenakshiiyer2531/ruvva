package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.CareerDto;
import com.ruvaa.backend.service.CareerService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/careers")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class CareerController {

    private final CareerService careerService;

    @PostMapping("/recommendations")
    public ResponseEntity<List<CareerDto>> getRecommendations(@RequestBody(required = false) java.util.Map<String, Object> profileData) {
        List<CareerDto> careers = careerService.getAllCareers();
        return ResponseEntity.ok(careers);
    }

    @GetMapping("/search")
    public ResponseEntity<List<CareerDto>> searchCareers(@RequestParam String query) {
        List<CareerDto> careers = careerService.searchCareers(query);
        return ResponseEntity.ok(careers);
    }

    @GetMapping("/category/{category}")
    public ResponseEntity<List<CareerDto>> getCareersByCategory(@PathVariable String category) {
        List<CareerDto> careers = careerService.getCareersByCategory(category);
        return ResponseEntity.ok(careers);
    }
}