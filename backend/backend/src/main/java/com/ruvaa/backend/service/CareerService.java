package com.ruvaa.backend.service;

import com.ruvaa.backend.dto.CareerDto;
import com.ruvaa.backend.dto.LearningStepDto;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class CareerService {

    private final List<CareerDto> careers = createMockCareers();

    public List<CareerDto> getAllCareers() {
        return careers;
    }

    public List<CareerDto> searchCareers(String query) {
        if (query == null || query.trim().isEmpty()) {
            return careers;
        }

        String lowerQuery = query.toLowerCase();
        return careers.stream()
                .filter(career ->
                    career.getTitle().toLowerCase().contains(lowerQuery) ||
                    career.getDesc().toLowerCase().contains(lowerQuery) ||
                    career.getTags().stream().anyMatch(tag -> tag.toLowerCase().contains(lowerQuery))
                )
                .collect(Collectors.toList());
    }

    public List<CareerDto> getCareersByCategory(String category) {
        return careers.stream()
                .filter(career -> category.equalsIgnoreCase(career.getCategory()))
                .collect(Collectors.toList());
    }

    private List<CareerDto> createMockCareers() {
        List<CareerDto> careers = new ArrayList<>();

        // Software Engineer
        CareerDto softwareEngineer = new CareerDto();
        softwareEngineer.setId("c1");
        softwareEngineer.setTitle("Software Engineer");
        softwareEngineer.setDesc("Designs, develops, and maintains software applications and systems. They write code, test software, and collaborate on project teams.");
        softwareEngineer.setCategory("Technology");
        softwareEngineer.setTags(Arrays.asList("Programming", "Computer Science", "Technology"));
        softwareEngineer.setScoreMatch(0.95);

        List<LearningStepDto> softwareSteps = new ArrayList<>();
        LearningStepDto step1 = new LearningStepDto();
        step1.setStep("Learn programming basics (e.g., Python, JavaScript)");
        step1.setResources(Arrays.asList("https://www.freecodecamp.org/", "https://www.theodinproject.com/"));
        softwareSteps.add(step1);

        LearningStepDto step2 = new LearningStepDto();
        step2.setStep("Master Data Structures & Algorithms");
        step2.setResources(Arrays.asList("https://www.geeksforgeeks.org/data-structures/", "https://leetcode.com/"));
        softwareSteps.add(step2);

        softwareEngineer.setLearningPath(softwareSteps);
        careers.add(softwareEngineer);

        // Data Scientist
        CareerDto dataScientist = new CareerDto();
        dataScientist.setId("c2");
        dataScientist.setTitle("Data Scientist");
        dataScientist.setDesc("Analyzes and interprets complex data to help organizations make better decisions. They use statistical methods and machine learning.");
        dataScientist.setCategory("Technology");
        dataScientist.setTags(Arrays.asList("Data", "Analytics", "AI", "Statistics", "Technology"));
        dataScientist.setScoreMatch(0.92);

        List<LearningStepDto> dataSteps = new ArrayList<>();
        LearningStepDto dataStep1 = new LearningStepDto();
        dataStep1.setStep("Learn statistics and probability");
        dataStep1.setResources(Arrays.asList("https://www.coursera.org/courses?query=introduction%20to%20statistics", "https://www.khanacademy.org/math/statistics-probability"));
        dataSteps.add(dataStep1);

        dataScientist.setLearningPath(dataSteps);
        careers.add(dataScientist);

        // UX/UI Designer
        CareerDto uxDesigner = new CareerDto();
        uxDesigner.setId("c3");
        uxDesigner.setTitle("UX/UI Designer");
        uxDesigner.setDesc("Focuses on the user experience (UX) and user interface (UI) of digital products. They create intuitive, accessible, and enjoyable designs.");
        uxDesigner.setCategory("Design");
        uxDesigner.setTags(Arrays.asList("Design", "User Experience", "Creativity", "Technology"));
        uxDesigner.setScoreMatch(0.88);

        List<LearningStepDto> uxSteps = new ArrayList<>();
        LearningStepDto uxStep1 = new LearningStepDto();
        uxStep1.setStep("Understand design principles and user psychology");
        uxStep1.setResources(Arrays.asList("https://www.nngroup.com/articles/usability-101-introduction-to-usability/", "https://www.interaction-design.org/literature/topics/usability-101"));
        uxSteps.add(uxStep1);

        uxDesigner.setLearningPath(uxSteps);
        careers.add(uxDesigner);

        // Add more careers as needed...
        return careers;
    }
}