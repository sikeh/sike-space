import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import spring.Product;
import spring.Writer;

/**
 * Created by IntelliJ IDEA.
 * User: Sike Huang
 * Date: Aug 30, 2010
 * Time: 11:04:47 PM
 * To change this template use File | Settings | File Templates.
 */
public class Launcher {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext("spring.xml");
        Writer writer = context.getBean("fileWriter", Writer.class);
        writer.write(createProduct(), createProduct(), createProduct(), createBadProduct());
    }

    private static Product createProduct() {
        Product product = new Product();
        product.setId("34324");
        product.setName("PC");
        return product;
    }

    private static Product createBadProduct() {
        Product product = new Product();
        product.setId("loooooooooooooooooooooooooooooooooooooooooong id");
        product.setName("loooooooooooooooooooooooooooooooooooooooooong name");
        return product;
    }
}
