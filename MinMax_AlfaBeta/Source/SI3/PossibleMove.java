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
public class PossibleMove
{
    public int Value;
    public Field Field;

    public PossibleMove(Field Field, int Value) {
        this.Value = Value;
        this.Field = Field;
    }

    public int getValue() {
        return Value;
    }

    public void setValue(int Value) {
        this.Value = Value;
    }

    public Field getField() {
        return Field;
    }

    public void setField(Field Field) {
        this.Field = Field;
    }
    
    
}
