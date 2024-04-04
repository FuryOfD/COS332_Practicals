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

        Fib fib = new Fib();
        String response = fib.getNumbers();

        OutputStream os = exchange.getResponseBody();
        PrintWriter out = new PrintWriter(os);

        out.println("<!DOCTYPE html>");
        out.println("<html>");
        out.println("<head><title>Fibonacci Sequence</title></head>");
        out.println("<body>");
        out.println("<h1>Fibonacci Sequence</h1>");
        out.println("<table>");
        out.println("<tr><th>Fn-1</th><th>Fn</th><th>Fn+1</th></tr>");
        out.println(response);

        out.println("</table>");
        out.println("<a href=\"/next\">Next</a>");
        out.println("<a href=\"/prev\">Previous</a>");
        out.println("</body>");
        out.println("</html>");

        out.flush();
        out.close();
        os.close();
        

    }
    
}
