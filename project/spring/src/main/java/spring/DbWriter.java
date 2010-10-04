package spring;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.namedparam.SqlParameterSource;
import org.springframework.jdbc.core.namedparam.SqlParameterSourceUtils;
import org.springframework.jdbc.core.simple.SimpleJdbcTemplate;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;

/**
 * Created by IntelliJ IDEA.
 * User: Sike Huang
 * Date: Aug 30, 2010
 * Time: 11:15:44 PM
 * To change this template use File | Settings | File Templates.
 */
@Component(value = "dbWriter")
public class DbWriter implements Writer {
    @Autowired
    private DataSource dataSource;

    @Transactional
    public void write(Product... products) {
        SimpleJdbcTemplate template = new SimpleJdbcTemplate(dataSource);
        SqlParameterSource[] batch = SqlParameterSourceUtils.createBatch(products);
        template.batchUpdate("insert into product_id (pid) values(:id)", batch);
        template.batchUpdate("insert into product (pname) values(:name)", batch);
    }
}
