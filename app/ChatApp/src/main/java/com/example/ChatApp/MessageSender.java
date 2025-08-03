package com.example.ChatApp;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

import lombok.extern.slf4j.Slf4j;


@Component
@Slf4j
public class MessageSender {

    private final RabbitTemplate rabbitTemplate;

    public MessageSender(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    @EventListener(ApplicationReadyEvent.class)
    public void sendMessage() {
        String message = "Hello from Spring Boot!";
        rabbitTemplate.convertAndSend(RabbitMqConfig.QUEUE, message);
        log.info("[x] Sent: " + message);
    }


}
