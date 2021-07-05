package view;

import model.interfaces.DicePair;
import model.interfaces.Die;
import model.interfaces.GameEngine;
import model.interfaces.Player;
import view.interfaces.GameEngineCallback;

public class GameEngineCallbackGUI implements GameEngineCallback {

	@Override
	public void playerDieUpdate(Player player, Die die, GameEngine gameEngine) {
		System.out.println("Called");
	}

	@Override
	public void houseDieUpdate(Die die, GameEngine gameEngine) {
		// TODO Auto-generated method stub

	}

	@Override
	public void playerResult(Player player, DicePair result, GameEngine gameEngine) {
		System.out.println(result.getDie1().getValue());
	}

	@Override
	public void houseResult(DicePair result, GameEngine gameEngine) {
		// TODO Auto-generated method stub

	}

}
