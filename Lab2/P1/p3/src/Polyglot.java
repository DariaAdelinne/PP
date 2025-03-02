import org.graalvm.polyglot.*;

public class Polyglot {
    public static void main(String[] args) {
        Context context = Context.newBuilder().allowAllAccess(true).build();
        String pythonCode =
                "def f1():\n" +
                        "n=input('Introduceti numarul de aruncari: ')\n" +
                        "x=input('Introduceti numarul x: ')\n" +
                        "return n,x\n" +
                        "f1()";
        Value pyResult=context.eval("python", pythonCode);
        int n=pyResult.getArrayElement(0).asInt();
        int x=pyResult.getArrayElement(1).asInt();
        String rCode=
                "f2 <- function(n, x) {\n" +
                        "prob <- pbinom(x,size = n,prob = 0.5)\n" +
                        "return(prob)\n" +
                        "}\n" +
                        "f2(" + n + ", " + x + ")";
        Value rResult=context.eval("R",rCode);
        double prob=rResult.asDouble();
        System.out.println("Probabilitatea este: "+ prob);

    }
}