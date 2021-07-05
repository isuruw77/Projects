package controller;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import model.interfaces.GameEngine;
import view.DropDownMenu;

public class RollDie implements ActionListener {
	private GameEngine gameEngine;
	private DropDownMenu menu;
	
	public RollDie(GameEngine gameEngine, DropDownMenu menu) {
		this.gameEngine = gameEngine;
		this.menu = menu;
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		String item =  menu.getSelectedItem().toString();
		
		for(int i = 0; i < gameEngine.getAllPlayers().size(); ++i) {
			String id = String.valueOf(i);
			if(gameEngine.getPlayer(id).getPlayerName().equals(item)) {
				System.out.println(gameEngine.getPlayer(id).getPlayerId());
				gameEngine.rollPlayer(gameEngine.getPlayer(id), 100, 1000, 100, 50, 500, 50);
			}
		}

	}

}
