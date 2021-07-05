package client;

import javax.swing.SwingUtilities;

import controller.AddPlayer;
import model.GameEngineImpl;
import model.SimplePlayer;
import model.interfaces.GameEngine;
import model.interfaces.Player;
import validate.Validator;
import view.DiceGameFrame;
import view.GameEngineCallbackGUI;
import view.GameEngineCallbackImpl;

/**
 * Simple console client for FP assignment 1, 2020
 * NOTE: This code will not compile until you have implemented stubs for the supplied interfaces!
 * 
 * You must be able to compile your code WITHOUT modifying this class.
 * Additional testing should be done by copying and extending this class while ensuring this class still works.
 * 
 * @author Caspar Ryan
 * 
 */
public class SimpleTestClient
{
   public static void main(String args[])
   {
      // instantiate the GameEngine so we can make calls
      final GameEngine gameEngine = new GameEngineImpl();
      
   
      new DiceGameFrame(gameEngine);
      
      gameEngine.addGameEngineCallback(new GameEngineCallbackGUI());

      // call method in Validator.jar to test *structural* correctness
      // just passing this does not mean it actually works .. you need to test yourself!
      // pass false if you want to show minimal logging (pass/fail) .. (i.e. ONLY once it passes)
      Validator.validate(false);

      // create two test players (NOTE: you will need to implement the 3 arg contructor in SimplePlayer)
//      Player[] players = new Player[] { new SimplePlayer("1", "The Roller", 5000), new SimplePlayer(
//         "2", "The Loser", 500) };

      // register the callback for notifications (all logging output is done by GameEngineCallbackImpl)
      // see provided skeleton class GameEngineCallbackImpl.java
     
//      new Thread()
//      {
//      @Override
//      public void run()
//      	{
//    	  gameEngine.addGameEngineCallback(new GameEngineCallbackImpl());
//
//          // main loop to add players from our collection
//          for (Player player : players)
//             gameEngine.addPlayer(player);
//
//          // use the gameEngine to place a bet and roll for each Player
//          for (Player player : gameEngine.getAllPlayers())
//          {
//             gameEngine.placeBet(player, 100);
//             gameEngine.rollPlayer(player, 100, 1000, 100, 50, 500, 50);
//          }
//
//          // all players have rolled so now house rolls (GameEngineCallBack is
//          // called) and results are calculated
//          gameEngine.rollHouse(100, 1000, 200, 50, 500, 25);
//      	}
//      }.start();

   
   }

}
