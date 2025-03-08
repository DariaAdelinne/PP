import org.graalvm.polyglot.*;
import java.io.*;
public class RegresieLiniara
{
    public static void main(String[] args) throws IOException
    {
        try{
            String date;//Citirea datelor
            try(BufferedReader x=new BufferedReader(new FileReader("date.txt")))
            {
                date=x.readLine();
                if(date==null)
                {
                    throw new IOException("Fisierul date.txt este gol");
                }
                date=date.trim();
            }
            String dateIesire;//Citim numele fisierul de iesire
            try(BufferedReader y=new BufferedReader(new FileReader("dateIesire.txt")))
            {
                dateIesire=y.readLine();
                if(dateIesire==null)
                {
                    throw new IOException("Fisierul dateIesire.txt este gol");
                }
                dateIesire=dateIesire.trim();
            }
            String outputPath="out";//Directorul de iesire
            Context polyglot=Context.newBuilder().allowAllAccess(true).build();//Creearea contextului

            BufferedReader z=new BufferedReader(new InputStreamReader(System.in));//Citirea culorii
            System.out.print("Introduceti culoarea: ");
            String culoare=z.readLine();

            String rCode=String.format(
                    "library(lattice)\n"+//biblioteca pentru plotare
                            "data <- read.table('%s', header=TRUE,sep=',')\n"+//citirea datelor
                            "print(data)\n"+
                            "png(file=file.path('%s', '%s'), width=800, height=600)\n"+//deschiderea fisierului png pentru plotare
                            "plot <- xyplot(y ~ x, data=data, type=c('p', 'r'), col='%s', main='Regresie Liniara')\n"+//creearea graficului; y~x ->relatia de regresie
                            "print(plot)\n"+//desenarea garficului
                            "dev.off()\n"+//inchide si salveaza fisierul
                            "system(paste('open', file.path('%s', '%s')))",//deschide png
                    date,outputPath,dateIesire,culoare,outputPath,dateIesire);
            polyglot.eval("R",rCode);//executarea codului  inR
        }
        catch(IOException e)
        {
            e.printStackTrace();
        }
    }
}