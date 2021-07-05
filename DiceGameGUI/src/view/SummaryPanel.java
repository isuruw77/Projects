package view;


import java.awt.GridLayout;

import javax.swing.BorderFactory;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class SummaryPanel extends JPanel {
	
	public SummaryPanel() {
		setBorder(BorderFactory.createTitledBorder("Summary Panel"));
		setLayout(new GridLayout(0,1));
//		add(summary);
//		add(new PlayerSummary());
	}
}
