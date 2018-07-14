/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package SI3;

import java.util.Comparator;

public class comparatorArray implements Comparator<PossibleMove> {
    public int compare(PossibleMove a, PossibleMove b) {
        if (a.getValue() > b.getValue())
            return -1; // highest value first
        if (a.getValue() == b.getValue())
            return 0;
        return 1;
    }
}