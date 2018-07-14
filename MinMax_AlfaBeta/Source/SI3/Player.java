/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package SI3;

import java.awt.Color;

/**
 *
 * @author Michal
 */
public class Player {

   public int score;
   public Color color;
   /** Constructor with reference to game board */
   public Player(Color color) {
      this.color = color;
   }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public Color getColor() {
        return color;
    }

    public void setColor(Color color) {
        this.color = color;
    }
   
}