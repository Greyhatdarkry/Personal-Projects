import javax.swing.*;
import java.awt.*;
import java.awt.geom.RoundRectangle2D;

public class CustomUI {

    /**
     * A JPanel with rounded corners and optional drop shadow/border.
     */
    public static class RoundedPanel extends JPanel {
        private int radius;
        private Color backgroundColor;

        public RoundedPanel(int radius, Color bgColor) {
            super();
            this.radius = radius;
            this.backgroundColor = bgColor;
            setOpaque(false);
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g.create();
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            
            if (backgroundColor != null) {
                g2.setColor(backgroundColor);
            } else {
                g2.setColor(getBackground());
            }
            
            g2.fill(new RoundRectangle2D.Double(0, 0, getWidth(), getHeight(), radius, radius));
            g2.dispose();
        }
    }

    /**
     * A JPanel with a smooth gradient background.
     */
    public static class GradientPanel extends JPanel {
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

    /**
     * A custom JButton with rounded corners and hover effects.
     */
    public static class RoundedButton extends JButton {
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

            addMouseListener(new java.awt.event.MouseAdapter() {
                @Override
                public void mouseEntered(java.awt.event.MouseEvent evt) {
                    isHovered = true;
                    repaint();
                }

                @Override
                public void mouseExited(java.awt.event.MouseEvent evt) {
                    isHovered = false;
                    repaint();
                }
            });
        }

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
            
            // Draw text
            g2.setColor(getForeground());
            FontMetrics fm = g2.getFontMetrics();
            int x = (getWidth() - fm.stringWidth(getText())) / 2;
            int y = (getHeight() - fm.getHeight()) / 2 + fm.getAscent();
            g2.drawString(getText(), x, y);
            
            g2.dispose();
        }
    }
}
