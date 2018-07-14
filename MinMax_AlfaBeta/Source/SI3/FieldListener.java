/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package SI3;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.AbstractButton;

/**
 *
 * @author piotr
 */
public class FieldListener implements ActionListener {

    private Game game;

    @Override
    public void actionPerformed(ActionEvent e) {
        AbstractButton btn = (AbstractButton) e.getSource();
        if (game.isFree(btn)) {
            game.setFlag(btn);
        } else {
            System.out.println("zajęte");
        }
       

    }

    public void setGame(Game g) {
        game = g;
    }
}
