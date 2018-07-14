/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package SI3;

/**
 *
 * @author Michal
 */
public class Field 
{
    public int Row;
    public int Column;
    public boolean IsSelected;

    public Field(int Row, int Column,  boolean IsSelected) {
        this.Row = Row;
        this.Column = Column;
        this.IsSelected = IsSelected;
    }

    public int getRow() {
        return Row;
    }

    public void setRow(int Row) {
        this.Row = Row;
    }

    public int getColumn() {
        return Column;
    }

    public void setColumn(int Column) {
        this.Column = Column;
    }

    public boolean isIsSelected() {
        return IsSelected;
    }

    public void setIsSelected(boolean IsSelected) {
        this.IsSelected = IsSelected;
    }
    
}