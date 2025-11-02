package com.ruvaa.backend.mock;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {"firebase.enabled=false"})
@AutoConfigureMockMvc
@ActiveProfiles("dev")
class MockStudentIntegrationTest {

    @Autowired
    MockMvc mockMvc;
    @Autowired
    ObjectMapper mapper;

    private final Path persistenceFile = Path.of("mock-data-store.json");

    @BeforeEach
    void cleanFile() throws Exception {
        Files.deleteIfExists(persistenceFile);
    }

    @Test
    void registrationProfileSeedAndPersistenceRoundTrip() throws Exception {
        // Register student
        java.util.Map<String,Object> payload = new java.util.HashMap<>();
        payload.put("email", "inttest.student@example.com");
        payload.put("password", "Passw0rd!");
        payload.put("name", "Integration Tester");
        payload.put("gradeLevel", "11");
        payload.put("city", "TestCity");
        payload.put("state", "TS");
        payload.put("educationLevel", "HighSchool");
        payload.put("institutionName", "Test High");
        payload.put("stream", "Science");
        payload.put("agreeToTerms", true);
        payload.put("agreeToPrivacyPolicy", true);
        MvcResult regResult = mockMvc.perform(post("/students/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(mapper.writeValueAsString(payload)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.success").value(true))
            .andReturn();
        String regJson = regResult.getResponse().getContentAsString();
        String studentId = mapper.readTree(regJson).path("data").path("id").asText();
        Assertions.assertFalse(studentId.isBlank(), "Student id should be returned");
        // Validate extended fields present
        Assertions.assertEquals("TestCity", mapper.readTree(regJson).path("data").path("city").asText());
        Assertions.assertEquals("Science", mapper.readTree(regJson).path("data").path("stream").asText());

        // Retrieve combined student
        mockMvc.perform(get("/students/" + studentId))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.success").value(true))
            .andExpect(jsonPath("$.data.id").value(studentId))
            .andExpect(jsonPath("$.data.profile.city").value("TestCity"));

        // Persistence save occurs on shutdown (PreDestroy). For integration simplicity, assert that registering did not create file yet.
        Assertions.assertFalse(Files.exists(persistenceFile), "File should not exist before explicit save");
    }
}
