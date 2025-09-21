package com.ruvaa.backend.repository;

import com.ruvaa.backend.entity.College;
import java.util.List;
import java.util.Optional;

public interface CollegeRepository {
    List<College> searchColleges(String search);
    List<College> findByLocation(String location);
    College save(College college);
    Optional<College> findById(Long id);
    void deleteById(Long id);
    List<College> findAll();
    long count();
}