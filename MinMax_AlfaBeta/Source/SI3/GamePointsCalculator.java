/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package SI3;

import java.util.ArrayList;

/**
 *
 * @author Michal
 */
public class GamePointsCalculator {

    private int m_mapSize;
    private ArrayList<ArrayList<Field>> m_fields;

    public GamePointsCalculator(int mapSize, ArrayList<ArrayList<Field>> fields) {
        m_mapSize = mapSize-1;
        m_fields = fields;
    }

    public int CheckColumn(Field selectedField) {
        int points = 0;
        int column = selectedField.Column;
        for (int row = 0; row < m_fields.size(); row++) {
            Field fieldToCheck = m_fields.get(row).get(column);
            if (!fieldToCheck.IsSelected) {
                return 0;
            }

            points++;
        }

        if (points < 2) {
            return 0;
        }

        return points;
    }

    public int CheckRow(Field selectedField) {
        int points = 0;
        int row = selectedField.Row;
        for (int column = 0; column < m_fields.size(); column++) {
            Field fieldToCheck = m_fields.get(row).get(column);
            if (!fieldToCheck.IsSelected) {
                return 0;
            }

            points++;
        }

        if (points < 2) {
            return 0;
        }

        return points;
    }

    public int CheckLeftDiagonal(Field selectedField) {
        int x = selectedField.Row;
        int y = selectedField.Column;

        int count = 0;
        if ((x == 0 && y == 0) || (x == m_mapSize && y == m_mapSize)) {
            return count;
        }
        if (checkDiagonalLeftMinus(x, y, count) > 0) {
            return checkDiagonalLeftPlus(x, y, checkDiagonalLeftMinus(x, y, count) -1);
        }
        
        return 0;
    }
    private int checkDiagonalLeftMinus(int x, int y, int count) {
        if (x > m_mapSize || x < 0 || y > m_mapSize || y < 0) {
            return count;
        }
        if (m_fields.get(x).get(y).IsSelected == true) {
            count++;
            return checkDiagonalLeftMinus(x - 1, y + 1, count);
        }
        return 0;
    }

    private int checkDiagonalLeftPlus(int x, int y, int count) {
        if (x > m_mapSize || x < 0 || y > m_mapSize || y < 0) {
            return count;
        }
        if (m_fields.get(x).get(y).IsSelected == true) {
            count++;
            return checkDiagonalLeftPlus(x + 1, y - 1, count);
        }
        return 0;
    }

    public int CheckRightDiagonal(Field selectedField) {
        int x = selectedField.Row;
        int y = selectedField.Column;
        int count = 0;
        if ((x == 0 && y == m_fields.size()-1) || (x == m_fields.size()-1 && y == 0)) {
            return count;
        }
        if (checkDiagonalRightMinus(x, y, count) > 0) {
            return checkDiagonalRightPlus(x, y, checkDiagonalRightMinus(x, y, count)-1);
        }
        return 0;
    }
    private int checkDiagonalRightMinus(int x, int y, int count) {
        if (x > m_fields.size()-1 || x < 0 || y > m_fields.size()-1 || y < 0) {
            return count;
        }
        if (m_fields.get(x).get(y).IsSelected == true) {
            count++;
            return checkDiagonalRightMinus(x - 1, y - 1, count);
        }
        return 0;
    }

    private int checkDiagonalRightPlus(int x, int y, int count) {
        if (x > m_fields.size()-1 || x < 0 || y > m_fields.size()-1 || y < 0) {
            return count;
        }
        if (m_fields.get(x).get(y).IsSelected == true) {
            count++;
            return checkDiagonalRightPlus(x + 1, y + 1, count);
        }
        return 0;
    }

}
