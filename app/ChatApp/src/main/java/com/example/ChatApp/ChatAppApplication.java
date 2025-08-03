package com.example.ChatApp;

import org.springframework.amqp.rabbit.annotation.EnableRabbit;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

import lombok.extern.slf4j.Slf4j;

@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
@Slf4j
@EnableRabbit
public class ChatAppApplication {

	public static void main(String[] args) {
		SpringApplication.run(ChatAppApplication.class, args);
		
		log.info("Backend Server started on port 8080");
	}
}
