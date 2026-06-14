import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.geom.RoundRectangle2D;

public class RoundedButton extends JButton implements MouseListener {
    private int radius;
    private Color defaultColor;
    private Color hoverColor;
    private boolean isHovered = false;

    public RoundedButton(String text, int radius, Color defaultColor, Color hoverColor) {
        super(text);
        this.radius = radius;
        this.defaultColor = defaultColor;
        this.hoverColor = hoverColor;
        setContentAreaFilled(false);
        setFocusPainted(false);
        setBorderPainted(false);
        setForeground(Color.WHITE);
        setFont(new Font("Segoe UI", Font.BOLD, 14));

        addMouseListener(this);
    }

    @Override
    public void mouseEntered(MouseEvent evt) {
        isHovered = true;
        repaint();
    }

    @Override
    public void mouseExited(MouseEvent evt) {
        isHovered = false;
        repaint();
    }

    @Override
    public void mouseClicked(MouseEvent evt) {}

    @Override
    public void mousePressed(MouseEvent evt) {}

    @Override
    public void mouseReleased(MouseEvent evt) {}

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        if (isHovered) {
            g2.setColor(hoverColor);
        } else {
            g2.setColor(defaultColor);
        }
        
        g2.fill(new RoundRectangle2D.Double(0, 0, getWidth(), getHeight(), radius, radius));
        
        g2.setColor(getForeground());
        FontMetrics fm = g2.getFontMetrics();
        int x = (getWidth() - fm.stringWidth(getText())) / 2;
        int y = (getHeight() - fm.getHeight()) / 2 + fm.getAscent();
        g2.drawString(getText(), x, y);
        
        g2.dispose();
    }
}
