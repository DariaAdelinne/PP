import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.*;
import java.util.Stack;

public class Calculator extends JFrame{
    JButton digits[] ={
            new JButton(" 0 "),
            new JButton(" 1 "),
            new JButton(" 2 "),
            new JButton(" 3 "),
            new JButton(" 4 "),
            new JButton(" 5 "),
            new JButton(" 6 "),
            new JButton(" 7 "),
            new JButton(" 8 "),
            new JButton(" 9 ")
    };

    JButton operators[] ={
            new JButton(" + "),
            new JButton(" - "),
            new JButton(" * "),
            new JButton(" / "),
            new JButton(" = "),
            new JButton(" C "),
            new JButton(" ( "), //adaugare butoane pentru paranteze
            new JButton(" ) ")
    };

    String oper_values[] ={"+", "-", "*", "/", "=", "", "(", ")"};

    JTextArea area = new JTextArea(3, 5);

    public static void main(String[] args){
        Calculator calculator = new Calculator();
        calculator.setSize(300, 250);
        calculator.setTitle(" Java-Calc, PP Lab1 ");
        calculator.setResizable(false);
        calculator.setVisible(true);
        calculator.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public Calculator(){
        add(new JScrollPane(area), BorderLayout.NORTH);
        JPanel buttonpanel = new JPanel();
        buttonpanel.setLayout(new FlowLayout());

        for (int i = 0; i < 10; i++)
            buttonpanel.add(digits[i]);

        for (int i = 0; i <8; i++)//modificare dimensiune vector
            buttonpanel.add(operators[i]);

        add(buttonpanel, BorderLayout.CENTER);
        area.setForeground(Color.BLACK);
        area.setBackground(Color.WHITE);
        area.setLineWrap(true);
        area.setWrapStyleWord(true);
        area.setEditable(false);

        for (int i = 0; i < 10; i++){
            int fI = i;
            digits[i].addActionListener(new ActionListener(){
                @Override
                public void actionPerformed(ActionEvent actionEvent){
                    area.append(Integer.toString(fI));
                }
            });
        }

        for (int i = 0; i < 8; i++){
            int fI = i;
            operators[i].addActionListener(new ActionListener(){
                @Override
                public void actionPerformed(ActionEvent actionEvent){
                    if (fI == 5)
                        area.setText("");
                    else if (fI == 4){
                        try{
                            String expresie = area.getText();
                            String expresiePol = Poloneza(expresie);
                            double rez = Rezultat(expresiePol);
                            area.append(" = " + rez);
                        } catch (Exception e){
                            area.setText(" !!!Probleme!!! ");
                        }
                    } else{
                        area.append(oper_values[fI]);
                    }
                }
            });
        }
    }

    public boolean isOperator(char operator)
    {
        return operator=='+' || operator=='-' || operator=='*' || operator=='/';
    }

    public int priority(char operator)
    {
        if(operator=='*' || operator=='/')
            return 1;
        return 0;
    }

    public String Poloneza(String expresie)
    {
        StringBuilder rez = new StringBuilder();
        Stack<Character> operatori = new Stack<>();
        int i;
        for(i=0;i<expresie.length();i++)
        {
            char c=expresie.charAt(i);
            if(Character.isDigit(c))
            {
                StringBuilder numar=new StringBuilder();
                while(i<expresie.length() && Character.isDigit(expresie.charAt(i)))
                {
                    numar.append(expresie.charAt(i));
                    i++;
                }
                i--;
                rez.append(numar.toString()).append(" ");
            }
            else if(c=='(')
            {
                operatori.push(c);
            }
            else if(c==')')
            {
                while(!operatori.isEmpty() && operatori.peek()!='(')
                {
                    rez.append(operatori.pop()).append(" ");
                }
                operatori.pop();
            }
            else if(isOperator(c))
            {
                while(!operatori.isEmpty() && operatori.peek()!='(' && priority(operatori.peek())>=priority(c))
                {
                    rez.append(operatori.pop()).append(" ");
                }
                operatori.push(c);
            }
        }
        while(!operatori.isEmpty())
        {
            rez.append(operatori.pop()).append(" ");
        }
        return rez.toString();
    }

    public double Rezultat(String expresie){
        Stack<Double> rez = new Stack<>();
        String[] p = expresie.split(" ");
        for (String subs : p) {
            if (subs.isEmpty()) {
                continue; // Sărim peste spații goale
            }
            if (Character.isDigit(subs.charAt(0))) {
                rez.push(Double.parseDouble(subs));
            } else if (isOperator(subs.charAt(0))) {
                double op2 = rez.pop(); // Al doilea operand
                double op1 = rez.pop(); // Primul operand
                switch (subs.charAt(0)) {
                    case '+':
                        rez.push(op1 + op2);
                        break;
                    case '-':
                        rez.push(op1 - op2);
                        break;
                    case '*':
                        rez.push(op1 * op2);
                        break;
                    case '/':
                        rez.push(op1 / op2);
                        break;
                }
            }
        }
        return rez.pop();
    }
}