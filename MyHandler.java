import java.io.*;
import com.sun.net.httpserver.*;
import java.net.*;
import java.util.*;

public class MyHandler implements HttpHandler{

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        //set response headers
        exchange.getResponseHeaders().set("Content-Type", "text/html");
        exchange.sendResponseHeaders(200, 0);

        //get fib numbers from numbers.txt
        

    }
    
}
