import java.io.*;

public class Fib {
    private int num1, num2, num3;

    public Fib() {
        //read from numbers.txt
        try {
            BufferedReader reader = new BufferedReader(new FileReader("numbers.txt"));
            num1 = Integer.parseInt(reader.readLine());
            num2 = Integer.parseInt(reader.readLine());
            num3 = Integer.parseInt(reader.readLine());
            reader.close();
        } 
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void WriteIntoDatafile() {
        //write to numbers.txt
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter("numbers.txt"));
            writer.write(num1 + "\n");
            writer.write(num2 + "\n");
            writer.write(num3 + "\n");
            writer.close();
        } 
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void CalculateNextFib() {
        //calculate next fib number
        int nextFib = num1 + num2 ;
        num1 = num2;
        num2 = num3;
        num3 = nextFib;
        WriteIntoDatafile();
    }

    public void CalculatePrevFib() {
        //calculate previous fib number
        int prevFib = num3 - num2;
        num3 = num2;
        num2 = num1;
        num1 = prevFib;
        WriteIntoDatafile();
    }
}
