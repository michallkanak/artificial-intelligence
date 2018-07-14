/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package SI3;

import java.awt.Color;
import javax.swing.AbstractButton;
import javax.swing.JButton;
import javax.swing.JLabel;

import java.util.ArrayList;
import java.util.List;
import javax.swing.JOptionPane;
/**
 *
 * @author piotr
 */
public class Game {

    private JButton btn[][];
    public ArrayList<ArrayList<Field>> tab;
    private JLabel label1;    
    private JLabel label2;
    private int diagonPoint;
    private Player turn;
    Player p1 = new Player(Color.GREEN);
    Player p2 = new Player(Color.BLACK);
    private MinMax m_minMax = null;
    
    public Game(JButton b[][], JLabel label1, JLabel label2) {
        this.turn = p1;
        this.label1 = label1;
        this.label2 = label2;        
        btn = b;
        intralizeBoard(btn.length);
        diagonPoint = -1;
        m_minMax = new MinMax();
    }

    private void intralizeBoard(int x) {
        this.tab = new ArrayList(new ArrayList(btn.length));       
        for (int i = 0; i < x; i++) {
            ArrayList temp = new ArrayList<Field>(x);
            for (int j = 0; j < x; j++) {
                temp.add(j, new Field(i,j,false));
            }
            this.tab.add(i, temp);
        }
    }

    private void print() {
        for (int i = 0; i < tab.size(); i++) {
            for (int j = 0; j < tab.get(0).size(); j++) {
                System.out.println(tab.get(i).get(j).Column + " " + tab.get(i).get(j).Row);
            }
            System.out.println();
        }
        System.out.println();
    }

    public void setFlag(AbstractButton b) {
        int points = 0;
        for (int i = 0; i < btn.length; i++) {
            for (int j = 0; j < btn.length; j++) {
                if (btn[i][j] == b) {
                    this.tab.get(i).get(j).IsSelected = true;
                    btn[i][j].setBackground(turn.color);
                    int checkColVal = checkCol(j);
                    int checkRowVal = checkRow(i);
                    int checkDiagonalRightVal = checkDiagonalRight(i, j);
                    int checkDiagonalLeftVal = checkDiagonalLeft(i, j);
                    
                    if (checkColVal > 0) {
                        System.out.println("kolumna zamknięta " + checkColVal);
                        points += checkColVal;
                    }
                    if (checkRowVal > 0) {
                        System.out.println("Wiersz zamknięty " + checkRowVal);
                        points += checkRowVal;
                    }
                    diagonPoint = -1;
                    if (checkDiagonalRightVal > 0) {
                        System.out.println("przekątna zamknięta " + diagonPoint + "points:" + checkDiagonalRight(i, j));
                        points += checkDiagonalRightVal;
                    }
                    diagonPoint = -1;
                    if (checkDiagonalLeftVal > 0) {
                        System.out.println("przekątna zamknięta " + diagonPoint + "points:" + checkDiagonalLeft(i, j));
                        points += checkDiagonalLeftVal;
                    }
                    turn.score += points;
                }
            }
        }
        print();
        changeTurn();
        
    }

    public boolean isFree(AbstractButton b) {
        for (int i = 0; i < btn.length; i++) {
            for (int j = 0; j < btn.length; j++) {
                if (btn[i][j] == b && tab.get(i).get(j).IsSelected == true) {
                    return false;
                }
            }
        }
        return true;
    }

    private int checkRow(int x) {
        int count = 0;
        for (int i = 0; i < tab.size(); i++) {
            if (tab.get(x).get(i).IsSelected == false) {
                return 0;
            }
            count++;
        }
        return count;
    }

    private int checkCol(int y) {
        int count = 0;
        for (int i = 0; i < tab.size(); i++) {
            if (tab.get(i).get(y).IsSelected == false) {
                return 0;
            }
            count++;
        }
        return count;
    }

    private int checkDiagonalRight(int x, int y) {
        int count = 0;
        if ((x == 0 && y == tab.size()-1) || (x == tab.size()-1 && y == 0)) {
            return count;
        }
        if (checkDiagonalRightMinus(x, y, count) > 0) {
            return checkDiagonalRightPlus(x, y, checkDiagonalRightMinus(x, y, count)-1);
        }
        diagonPoint = -1;
        return 0;
    }

    private int checkDiagonalRightMinus(int x, int y, int count) {
        if (x > tab.size()-1 || x < 0 || y > tab.size()-1 || y < 0) {
            return count;
        }
        if (tab.get(x).get(y).IsSelected == true) {
            diagonPoint++;
            count++;
            return checkDiagonalRightMinus(x - 1, y - 1, count);
        }
        return 0;
    }

    private int checkDiagonalRightPlus(int x, int y, int count) {
        if (x > tab.size()-1 || x < 0 || y > tab.size()-1 || y < 0) {
            return count;
        }
        if (tab.get(x).get(y).IsSelected == true) {
            diagonPoint++;
            count++;
            return checkDiagonalRightPlus(x + 1, y + 1, count);
        }
        return 0;
    }

    private int checkDiagonalLeft(int x, int y) {
        int count = 0;
        if ((x == 0 && y == 0) || (x == tab.size()-1 && y == tab.size()-1)) {
            return count;
        }
        if (checkDiagonalLeftMinus(x, y, count) > 0) {
            return checkDiagonalLeftPlus(x, y, checkDiagonalLeftMinus(x, y, count) -1);
        }
        diagonPoint = -1;
        return 0;
    }

    private int checkDiagonalLeftMinus(int x, int y, int count) {
        if (x > tab.size()-1 || x < 0 || y > tab.size()-1 || y < 0) {
            return count;
        }
        if (tab.get(x).get(y).IsSelected == true) {
            diagonPoint++;
            count++;
            return checkDiagonalLeftMinus(x - 1, y + 1, count);
        }
        return 0;
    }

    private int checkDiagonalLeftPlus(int x, int y, int count) {
        if (x > tab.size()-1 || x < 0 || y > tab.size()-1 || y < 0) {
            return count;
        }
        if (tab.get(x).get(y).IsSelected == true) {
            diagonPoint++;
            count++;
            return checkDiagonalLeftPlus(x + 1, y - 1, count);
        }
        return 0;
    }

    private void changeTurn() {
        
        if (turn.equals(p1)) {
            this.label1.setText(Integer.toString(turn.score));
            turn = p2;
            
            if (m_minMax.CountPossibleMoves(this.tab) == 0) {
                JOptionPane panel = new JOptionPane();
                panel.createDialog("KONIEC GRY!");
                return;
            }
            Field field = m_minMax.Proceed(this.tab, turn.score);
            System.out.println(" "+field.getColumn() +" "+ field.getRow() +" ");
            this.tab.get(field.Row).get(field.Column).IsSelected = true;
            btn[field.Row][field.Column].setBackground(turn.color);
            turn.score = turn.score + m_minMax.CalculateScore(this.tab, this.tab.get(field.Row).get(field.Column));
            this.label2.setText(Integer.toString(turn.score));   
            turn = p1;
            
        }
    }
    
    public void autoTurn() {
            if (m_minMax.CountPossibleMoves(this.tab) == 0) {
                JOptionPane panel = new JOptionPane();                
                panel.createDialog("KONIEC GRY!");
                return;
            }
            Field field = m_minMax.Proceed(this.tab, turn.score);
            System.out.println(" "+field.getColumn() +" "+ field.getRow() +" ");
            this.tab.get(field.Row).get(field.Column).IsSelected = true;
            btn[field.Row][field.Column].setBackground(turn.color);
            turn.score = turn.score + m_minMax.CalculateScore(this.tab, this.tab.get(field.Row).get(field.Column));
            this.label1.setText(Integer.toString(turn.score));   
            turn = p2;
            if (m_minMax.CountPossibleMoves(this.tab) == 0) {
                JOptionPane panel = new JOptionPane();                
                panel.createDialog("KONIEC GRY!");
                return;
            }
            Field field2 = m_minMax.Proceed(this.tab, turn.score);
            System.out.println(" "+field2.getColumn() +" "+ field2.getRow() +" ");
            this.tab.get(field2.Row).get(field2.Column).IsSelected = true;
            btn[field2.Row][field2.Column].setBackground(turn.color);
            turn.score = turn.score + m_minMax.CalculateScore(this.tab, 
                this.tab.get(field2.Row).get(field2.Column));
            this.label2.setText(Integer.toString(turn.score));   
            turn = p1;
            Object d = new Object();
            try        
            {
                d.wait(4000);
            } 
            catch(Exception ex) 
            {
            }
            autoTurn();
    }
}
