import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

/**
 * Thriftshop is the top-level window for the Thrift Shop application.
 * It encapsulates the frame configuration and ensures a full-screen experience.
 */
public class Thriftshop extends JFrame implements KeyListener {
    private JPanel mainContainer;
    private CardLayout cardLayout;
    private ShopPanel shopPanel;

    public Thriftshop() {
        setTitle("Jason's - Thrift Shop");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        // Remove title bar for true full screen experience
        setUndecorated(false);
        setExtendedState(MAXIMIZED_BOTH);
        
        cardLayout = new CardLayout();
        mainContainer = new JPanel(cardLayout);
        
        // Shop interface
        shopPanel = new ShopPanel();
        mainContainer.add(shopPanel, "SHOP");

        add(mainContainer);

        // Show the window
        setVisible(true);

        // Use implement KeyListener instead of anonymous inner class to prevent $1.class
        addKeyListener(this);

        // Ensure focus for key listener
        setFocusable(true);
        requestFocusInWindow();
    }

    @Override
    public void keyTyped(KeyEvent e) {}

    @Override
    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {
            int confirm = JOptionPane.showConfirmDialog(
                    this,
                    "Are you sure you want to exit?",
                    "Exit Application",
                    JOptionPane.YES_NO_OPTION);
            if (confirm == JOptionPane.YES_OPTION) {
                System.exit(0);
            }
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {}

    public void showAdmin(ShopPanel shopPanel, java.util.List<SaleRecord> salesHistory) {
        AdminPanel adminPanel = new AdminPanel(this, shopPanel, salesHistory);
        mainContainer.add(adminPanel, "ADMIN");
        cardLayout.show(mainContainer, "ADMIN");
    }

    public void showShop() {
        cardLayout.show(mainContainer, "SHOP");
    }

    public static void main(String[] args) {
        // Use the look and feel of the system or CrossPlatform
        try {
            UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Use AppRunner class instead of anonymous inner class to prevent $1.class
        SwingUtilities.invokeLater(new AppRunner());
    }
}
