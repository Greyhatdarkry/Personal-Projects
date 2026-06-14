import javax.swing.*;
import java.awt.*;

public class GradientPanel extends JPanel {
    private Color startColor;
    private Color endColor;
    private boolean vertical;

    public GradientPanel(Color startColor, Color endColor, boolean vertical) {
        this.startColor = startColor;
        this.endColor = endColor;
        this.vertical = vertical;
        setOpaque(false);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        GradientPaint gp;
        if (vertical) {
            gp = new GradientPaint(0, 0, startColor, 0, getHeight(), endColor);
        } else {
            gp = new GradientPaint(0, 0, startColor, getWidth(), 0, endColor);
        }
        
        g2.setPaint(gp);
        g2.fillRect(0, 0, getWidth(), getHeight());
        g2.dispose();
    }
}
