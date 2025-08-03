package com.example.ChatApp;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

import lombok.extern.slf4j.Slf4j;

@Component
@Slf4j
public class MessageListener {

    @RabbitListener(queues = RabbitMqConfig.QUEUE)
    public void receiveMessage(String message) {
        log.info("[x] Received: " + message);
    }
}
