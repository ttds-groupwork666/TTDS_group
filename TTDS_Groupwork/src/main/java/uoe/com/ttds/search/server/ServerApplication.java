package uoe.com.ttds.search.server;
import controller.*;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ServerApplication {

    public static void main(String[] args) {

        //SpringApplication.run(ServerApplication.class, args);
        SpringApplication.run(server.class,args);
    }

}
