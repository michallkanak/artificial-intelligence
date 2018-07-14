/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package SI3;

import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
/**
 *
 * @author Michal
 */

public class MinMax
   {
       private Field m_selectedField = null;
       private int m_MaxExecutionTime;
       private List<PossibleMove> m_movesPossible;
       private Object m_lock = new Object();
       private int m_workersFinished = 0;

       public Field Proceed(ArrayList<ArrayList<Field>> board, int depth)
       {
           m_movesPossible = new ArrayList<PossibleMove>();
           ArrayList<ArrayList<Field>> boardCopy =  new ArrayList(new ArrayList(board.size()));//(btn.length);        

           for (int i = 0; i < board.size(); i++)
           {
               ArrayList row = new ArrayList<Field>(board.size());
               for (int column = 0; column < board.size(); column++)
               {
                    row.add(column, new Field(board.get(i).get(column).Row,
                            board.get(i).get(column).Column,
                            board.get(i).get(column).IsSelected));
               }

               boardCopy.add(row);
           }

           AlfaBeta alfaBeta = new AlfaBeta();
           alfaBeta.Value = 0;
           alfaBeta.Alpha = 0;
           alfaBeta.Beta = 0;  

           PossibleMove move = RunMinMax(boardCopy, true, -1, alfaBeta, null);

           return board.get(move.Field.Row).get(move.Field.Column);
       }

       public PossibleMove RunMinMax(ArrayList<ArrayList<Field>> board, 
               boolean isPlayer, 
               int depth, 
               AlfaBeta alfabeta, 
               Field selectedField)
       {
           depth++;

            try
            {
                int score = CalculateScore(board, selectedField);
                if (score > 0)
                {
                    if (isPlayer)
                    {
                       return new PossibleMove(selectedField, score - depth);
                    }

                   return new PossibleMove(selectedField, depth - score);
                }
            }
            catch(Exception e)
            {

            }           
           
           int possibleMovesCount = CountPossibleMoves(board);
           if (possibleMovesCount == 0)
           {
               int score = CalculateScore(board, selectedField);
               if (score > 0)
               {
                   if (isPlayer)
                   {
                       return new PossibleMove(selectedField, score - depth);
                   }

                   return new PossibleMove(selectedField, depth - score);
               }

               return new PossibleMove(selectedField, depth);
           }

           List<Field> possibleMoves = new ArrayList<Field>();
           for (ArrayList<Field> row : board)
           {
               for (Field field : row)
               {
                   if (field.IsSelected == false)
                   {
                       possibleMoves.add(field);
                   }
               }
           }

           List<PossibleMove> results = new ArrayList<PossibleMove>();
            for (Field possibleField : possibleMoves)
            {
                possibleField.IsSelected = true;

                PossibleMove possibleMove = RunMinMax(board, !isPlayer, depth, alfabeta, possibleField);
                if (isPlayer)
                {
                    if (possibleMove.Value > alfabeta.Value)
                    {
                        alfabeta.Value = possibleMove.Value;
                    }

                    if (possibleMove.Value >= alfabeta.Beta)
                    {
                        return possibleMove;
                    }

                    if (possibleMove.Value > alfabeta.Alpha)
                    {
                        alfabeta.Alpha = possibleMove.Value;
                    }

                    if (possibleMove.Value < alfabeta.Beta)
                    {
                        alfabeta.Beta = possibleMove.Value;
                    }
                }
                else
                {
                    if (possibleMove.Value < alfabeta.Value)
                    {
                        alfabeta.Value = possibleMove.Value;
                    }

                    if (possibleMove.Value <= alfabeta.Alpha)
                    {
                        return possibleMove;
                    }

                    if (possibleMove.Value < alfabeta.Beta)
                    {
                        alfabeta.Beta = possibleMove.Value;
                    }

                    if (possibleMove.Value > alfabeta.Alpha)
                    {
                        alfabeta.Alpha = possibleMove.Value;
                    }
                }

                results.add(possibleMove);
                possibleField.IsSelected = false;
            }
           

            if (results.size() == 0)
            {
                int score = CalculateScore(board, selectedField);
                if (score > 0)
                {
                    if (isPlayer)
                    {
                        return new PossibleMove(selectedField, score - depth);
                    }

                    return new PossibleMove(selectedField, depth - score);
                }

                return new PossibleMove(selectedField, 0);
}

           if (isPlayer)
           {
               PossibleMove max = Collections.max(results, new comparatorArray());
               //System.out.println("max:" + max.Value);
               return max;
           }
           else
           {
               PossibleMove min = Collections.min(results, new comparatorArray());
               //System.out.println("min:" + min.Value);
               return min;
           }
       }

       public int CountPossibleMoves(ArrayList<ArrayList<Field>> board)
       {
           int possibleMoves = 0;
           for (ArrayList<Field> row : board)
           {
               for (Field field : row)
               {
                   if (field.IsSelected == false)
                   {
                       possibleMoves++;
                   }
               }
           }

           return possibleMoves;
       }

       public int CalculateScore(ArrayList<ArrayList<Field>> board, Field selectedField)
       {
           GamePointsCalculator calc = new GamePointsCalculator(board.size(), board);
           int points = 0;
           points += calc.CheckColumn(selectedField);
           points += calc.CheckLeftDiagonal(selectedField);
           points += calc.CheckRightDiagonal(selectedField);
           points += calc.CheckRow(selectedField);

           return points;
       }
}