import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main
{
    public static String read(String filePath)throws IOException
    {
        StringBuilder continut=new StringBuilder();
        try(BufferedReader x = new BufferedReader (new FileReader(filePath)))
        {
            String line;
            while((line=x.readLine())!=null)
            {
                continut.append(line).append("\n");
            }
        }
        return continut.toString();
    }

    public static String rmv_semne_pct(String text)
    {
        return text.replaceAll("[^a-zA-Z0-9\\s]","");
    }

    public static String lowerCase(String text)
    {
        return text.toLowerCase();
    }

    public static void main(String[] args)
    {
        try
        {
            String filePath="fisier.txt";
            String continut=read(filePath);
            System.out.println("Continut initial:\n"+continut);
            continut=rmv_semne_pct(continut);
            System.out.println("Continutul dupa eliminarea semnelor de punctuatie:\n"+continut);
            continut=lowerCase(continut);
            System.out.println("Continutul dupa transformarea caracterelor mari in caractere mici:\n"+continut);
        }
        catch(IOException e)
        {
            e.printStackTrace();
        }
    }
}