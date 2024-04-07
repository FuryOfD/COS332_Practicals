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

        exchange.getResponseHeaders().set("Content-Type", "text/html");
        exchange.sendResponseHeaders(200, 0);

        String response = fib.getNumbers();

        OutputStream os = exchange.getResponseBody();
        PrintWriter out = new PrintWriter(os);

        out.println("<!DOCTYPE html>");
        out.println("<html>");
        out.println("<head>");
        out.println("<title>Fibonacci Sequence</title>");
        out.println("<meta http-equiv=\"Cache-Control\" content=\"no-store, no-cache, must-revalidate, max-age=0\">");
        out.println("<style>");
        out.println("* {");
        out.println("    font-family: 'Courier New', Courier, monospace;");
        out.println("}");
        out.println(".center {");
        out.println("    display: flex;");
        out.println("    justify-content: center;");
        out.println("    align-items: center;");
        out.println("    height: 100px;");
        out.println("}");
        out.println(".table {");
        out.println("    font-size: 30px;");
        out.println("    display: flex;");
        out.println("    flex-direction: column; ");
        out.println("    align-items: center;");
        out.println("    border: 1px solid;");
        out.println("}");
        out.println(".tr {");
        out.println("    padding: 10px;");
        out.println("    border: 1px solid;");
        out.println("}");
        out.println(".table td {");
        out.println("    padding: 10px;");
        out.println("    border: 1px solid;");
        out.println("}");
        out.println(".prev {");
        out.println("    padding: 10px;");
        out.println("    border: 1px solid;");
        out.println("    color: #ff0000;");
        out.println("}");
        out.println(".nothing {");
        out.println("    padding: 10px;");
        out.println("}");
        out.println(".next {");
        out.println("    padding: 10px;");
        out.println("    border: 1px solid;");
        out.println("    color: #ff0000;");
        out.println("}");
        out.println("</style>");
        out.println("</head>");
        out.println("<body>");

        out.println("<div class=\"center\">");
        out.println("<h1>Fibonacci Sequence</h1>");
        out.println("</div>");
        //out.println("<p class=\"nothing\">    </p>");
        out.println("<div class=\"center\">");
        out.println("<table class=\"table\">");
        out.println("<tr><th>Fn-1</th><th>Fn</th><th>Fn+1</th></tr>");
        out.println(response);
        out.println("</table>");
        out.println("</div>");

        out.println("<div class=\"center\">");
        out.println("<p class=\"prev\"> <a href=\"/prev\">Previous</a> </p>");
        out.println("<p class=\"nothing\">    </p>");
        out.println("<p class=\"next\"> <a href=\"/next\">Next</a> </p>");
        out.println("</div>");
        out.println("</body>");
        out.println("</html>");

        out.flush();
        out.close();
        os.close();
    }
}
