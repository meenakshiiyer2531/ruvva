package com.ruvaa.backend.config;

import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

import java.time.Duration;

/**
 * Google Gemini AI Configuration for CareerConnect
 * 
 * Configures Gemini AI client with proper rate limiting, timeouts,
 * and connection pooling for production use.
 */
@Slf4j
@Configuration
@ConfigurationProperties(prefix = "gemini")
@Data
public class GeminiConfig {

    private String apiKey;
    private String baseUrl;
    private String model;
    private Integer maxTokens;
    private Double temperature;
    private RateLimit rateLimit = new RateLimit();

    @Data
    public static class RateLimit {
        private Integer requestsPerMinute = 60;
        private Integer burstCapacity = 10;
    }

    /**
     * Check if Gemini is properly configured
     */
    public boolean isGeminiConfigured() {
        return apiKey != null && !apiKey.isBlank() && 
               baseUrl != null && !baseUrl.isBlank() &&
               model != null && !model.isBlank();
    }

    /**
     * Configure WebClient for Gemini AI API calls with production settings.
     */
    @Bean("geminiWebClient")
    public WebClient geminiWebClient() {
        if (apiKey == null || apiKey.isBlank()) {
            log.warn("Gemini API key not configured - AI features will be disabled");
            return null;
        }

        log.info("Configuring Gemini AI client for model: {}", model);

        // Configure connection provider with pooling
        ConnectionProvider connectionProvider = ConnectionProvider.builder("gemini-pool")
            .maxConnections(50)
            .maxIdleTime(Duration.ofSeconds(20))
            .maxLifeTime(Duration.ofSeconds(60))
            .pendingAcquireTimeout(Duration.ofSeconds(60))
            .evictInBackground(Duration.ofSeconds(120))
            .build();

        // Configure HTTP client with timeouts
        HttpClient httpClient = HttpClient.create(connectionProvider)
            .responseTimeout(Duration.ofSeconds(30))
            .option(io.netty.channel.ChannelOption.CONNECT_TIMEOUT_MILLIS, 10000);

        return WebClient.builder()
            .baseUrl(baseUrl)
            .clientConnector(new ReactorClientHttpConnector(httpClient))
            .defaultHeader("Content-Type", "application/json")
            .defaultHeader("x-goog-api-key", apiKey)
            .codecs(configurer -> {
                configurer.defaultCodecs().maxInMemorySize(2 * 1024 * 1024); // 2MB buffer
            })
            .build();
    }

    /**
     * Validate Gemini configuration on startup.
     */
    @Bean
    public GeminiConfigValidator geminiConfigValidator() {
        return new GeminiConfigValidator(this);
    }

    /**
     * Inner class for configuration validation.
     */
    @Slf4j
    public static class GeminiConfigValidator {
        private final GeminiConfig config;

        public GeminiConfigValidator(GeminiConfig config) {
            this.config = config;
            validateConfiguration();
        }

        private void validateConfiguration() {
            if (config.getApiKey() == null || config.getApiKey().isBlank()) {
                log.warn("Gemini API key is not configured. AI features will be disabled.");
                return;
            }

            if (config.getBaseUrl() == null || config.getBaseUrl().isBlank()) {
                throw new IllegalArgumentException("Gemini base URL must be configured");
            }

            if (config.getModel() == null || config.getModel().isBlank()) {
                throw new IllegalArgumentException("Gemini model must be configured");
            }

            if (config.getMaxTokens() == null || config.getMaxTokens() <= 0) {
                config.setMaxTokens(2048);
                log.warn("Invalid max tokens configured, defaulting to 2048");
            }

            if (config.getTemperature() == null || config.getTemperature() < 0 || config.getTemperature() > 1) {
                config.setTemperature(0.7);
                log.warn("Invalid temperature configured, defaulting to 0.7");
            }

            log.info("Gemini configuration validated successfully");
        }
    }

}