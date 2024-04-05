import java.io.*;
import com.sun.net.httpserver.*;

public class ErrorHandler implements HttpHandler{

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "text/html");
        exchange.sendResponseHeaders(404, 0);

        OutputStream os = exchange.getResponseBody();
        PrintWriter out = new PrintWriter(os);

        out.println("<!DOCTYPE html>");
        out.println("<html>");
        out.println("<head><title>404 Not Found</title></head>");
        out.println("<body>");
        out.println("<h1>404 Not Found</h1>");
        out.println("<p>The page you are looking for is not found.</p>");
        out.println("</body>");
        out.println("</html>");

        out.flush();
        out.close();
        os.close();
    }
    
}
