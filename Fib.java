import java.io.*;

public class Fib {
    private int num1, num2, num3;

    public Fib() {
        ReadFromDataFile();
    }

    private void ReadFromDataFile() {
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
        ReadFromDataFile();
        //calculate next fib number
        int nextFib = num2 + num3;
        num1 = num2;
        num2 = num3;
        num3 = nextFib;
        WriteIntoDatafile();
    }

    public void CalculatePrevFib() {
        ReadFromDataFile();
        //calculate previous fib number
        int prevFib = num2 - num1;
        num3 = num2;
        num2 = num1;
        num1 = prevFib;
        WriteIntoDatafile();
    }

    //return the 3 numbers
    public String getNumbers() {
        ReadFromDataFile();
        return "<tr><td>" + num1 + "</td><td>" + num2 + "</td><td>" + num3 + "</td></tr>";
    }

}
