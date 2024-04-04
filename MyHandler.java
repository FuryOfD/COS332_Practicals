import java.io.*;
import com.sun.net.httpserver.*;

public class MyHandler implements HttpHandler{
    private Fib fib;

    public MyHandler() {
        fib = new Fib();
    }


    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        if (path.equals("/next")) {
            fib.CalculateNextFib();
        } else if (path.equals("/prev")) {
            fib.CalculatePrevFib();
        }

        //set response headers
        exchange.getResponseHeaders().set("Content-Type", "text/html");
        exchange.sendResponseHeaders(200, 0);

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
        out.println("<a href=\"/prev\">Previous</a>");
        out.println("<a href=\"/next\">Next</a>");
        out.println("</body>");
        out.println("</html>");

        out.flush();
        out.close();
        os.close();
    }
}
