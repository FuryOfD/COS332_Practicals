import java.io.*;
import java.net.*;
import com.sun.net.httpserver.*;

public class Server {
    public static void initiliazeServer(int port) {
        try {
            HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
            server.createContext("/", new MyHandler());
            server.setExecutor(null);
            server.start();
            System.out.println("Server started on port " + port);
            
        } 
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
