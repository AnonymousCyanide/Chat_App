package com.example.ChatApp;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.amqp.core.Queue;


@Configuration
public class RabbitMqConfig {

    public static final String QUEUE = "demo-queue";

    @Bean
    public Queue demoQueue() {
        return new Queue(QUEUE, false);
    }
}
