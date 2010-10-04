package spring;

import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageCreator;
import org.springframework.amqp.core.SimpleMessageProperties;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitMessageProperties;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Created by IntelliJ IDEA.
 * User: Sike Huang
 * Date: Aug 31, 2010
 * Time: 11:05:24 PM
 * To change this template use File | Settings | File Templates.
 */
@Component(value = "fileWriter")
public class FileWriter implements Writer {
    @Value("#{config.prefix}")
    private String prefix;
    @Value("#{config.suffix}")
    private String suffix;
    @Autowired
    private ConnectionFactory connectionFactory;

    public void write(Product... products) {
        AmqpTemplate template = new RabbitTemplate(connectionFactory);
        for (Product product : products) {
            final String file = prefix + product + suffix;
            template.send(new MessageCreator() {
                public Message createMessage() {
                    return new Message(file.getBytes(), new RabbitMessageProperties());
                }
            });
        }
    }
}

