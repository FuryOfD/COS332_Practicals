import java.io.*;
import java.net.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        try{
            ServerSocket server = new ServerSocket(55555);

            while (true){
                Socket client = server.accept();
                
            }

        }
        catch(Exception e){
            e.printStackTrace();
        }
    }
}
