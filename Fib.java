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
        int prevFib = num2 - num1;
        num3 = num2;
        num2 = num1;
        num1 = prevFib;
        if(num2 < num1) {
            int temp = num1;
            num1 = num2;
            num2 = temp;
        }
        
        WriteIntoDatafile();
    }

    public void Refresh() {
        num1 = 0;
        num2 = 1;
        num3 = 1;
        WriteIntoDatafile();
    }

    public String getNumbers() {
        ReadFromDataFile();
        return "<tr><td>" + num1 + "</td><td>" + num2 + "</td><td>" + num3 + "</td></tr>";
    }

}
