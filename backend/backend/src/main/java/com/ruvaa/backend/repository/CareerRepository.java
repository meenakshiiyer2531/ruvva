package com.ruvaa.backend.repository;

import com.ruvaa.backend.entity.Career;
import java.util.List;
import java.util.Optional;

public interface CareerRepository {
    List<Career> searchCareers(String search);
    List<Career> findByCategory(String category);
    Career save(Career career);
    Optional<Career> findById(Long id);
    void deleteById(Long id);
    List<Career> findAll();
    long count();
}