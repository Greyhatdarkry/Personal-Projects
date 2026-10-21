import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.ArrayList;
import java.util.List;

/**
 * CartDialog provides a dark-mode modal dialog displaying the customer's shopping cart.
 * Users can select specific items for checkout, remove individual or selected items,
 * and proceed to the CheckoutDialog.
 * 
 * Implements ActionListener and ItemListener directly to avoid anonymous inner classes ($1.class).
 */
public class CartDialog extends JDialog implements ActionListener, ItemListener {
    private JFrame parentFrame;
    private ShopPanel shopPanel;
    private List<CartItem> cart;

    private List<JCheckBox> itemCheckboxes;
    private JPanel itemsContainer;
    private JScrollPane scrollPane;
    private JLabel totalSelectedLabel;
    private JLabel countLabel;

    private static final Color BG_COLOR = new Color(18, 18, 18);
    private static final Color CARD_COLOR = new Color(30, 30, 30);
    private static final Color TEXT_COLOR = Color.WHITE;
    private static final Color ACCENT_COLOR = new Color(74, 144, 226);
    private static final Color ACCENT_HOVER = new Color(100, 160, 240);
    private static final Color PH_PESO_COLOR = new Color(255, 193, 7);
    private static final Color DANGER_COLOR = new Color(200, 50, 50);
    private static final Color DANGER_HOVER = new Color(230, 70, 70);
    private static final Color MUTED_COLOR = new Color(150, 150, 150);

    public CartDialog(JFrame parent, ShopPanel shopPanel, List<CartItem> cart) {
        super(parent, "Shopping Cart", true);
        this.parentFrame = parent;
        this.shopPanel = shopPanel;
        this.cart = cart;
        this.itemCheckboxes = new ArrayList<>();

        setSize(520, 620);
        setLocationRelativeTo(parent);
        setUndecorated(true);

        RoundedPanel mainContainer = new RoundedPanel(20, BG_COLOR);
        mainContainer.setLayout(new BorderLayout(0, 15));
        mainContainer.setBorder(new EmptyBorder(25, 25, 25, 25));

        // Header
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setOpaque(false);

        JLabel titleLabel = new JLabel("SHOPPING CART");
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 22));
        titleLabel.setForeground(TEXT_COLOR);
        headerPanel.add(titleLabel, BorderLayout.WEST);

        countLabel = new JLabel(cart.size() + " item(s)");
        countLabel.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        countLabel.setForeground(MUTED_COLOR);
        headerPanel.add(countLabel, BorderLayout.EAST);

        mainContainer.add(headerPanel, BorderLayout.NORTH);

        // Center: Scrollable Item List
        itemsContainer = new JPanel();
        itemsContainer.setLayout(new BoxLayout(itemsContainer, BoxLayout.Y_AXIS));
        itemsContainer.setBackground(BG_COLOR);

        scrollPane = new JScrollPane(itemsContainer);
        scrollPane.setBorder(null);
        scrollPane.getViewport().setBackground(BG_COLOR);
        scrollPane.getVerticalScrollBar().setUnitIncrement(16);
        mainContainer.add(scrollPane, BorderLayout.CENTER);

        // South: Actions & Totals
        JPanel southPanel = new JPanel();
        southPanel.setLayout(new BoxLayout(southPanel, BoxLayout.Y_AXIS));
        southPanel.setOpaque(false);

        // Selection buttons row
        JPanel selectionRow = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 5));
        selectionRow.setOpaque(false);

        JButton selectAllBtn = new RoundedButton("Select All", 8, new Color(50, 50, 50), new Color(70, 70, 70));
        selectAllBtn.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        selectAllBtn.setActionCommand("SELECT_ALL");
        selectAllBtn.addActionListener(this);

        JButton deselectAllBtn = new RoundedButton("Deselect All", 8, new Color(50, 50, 50), new Color(70, 70, 70));
        deselectAllBtn.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        deselectAllBtn.setActionCommand("DESELECT_ALL");
        deselectAllBtn.addActionListener(this);

        JButton removeSelectedBtn = new RoundedButton("Remove Selected", 8, DANGER_COLOR, DANGER_HOVER);
        removeSelectedBtn.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        removeSelectedBtn.setActionCommand("REMOVE_SELECTED");
        removeSelectedBtn.addActionListener(this);

        selectionRow.add(selectAllBtn);
        selectionRow.add(deselectAllBtn);
        selectionRow.add(removeSelectedBtn);
        southPanel.add(selectionRow);
        southPanel.add(Box.createVerticalStrut(10));

        // Subtotal row
        JPanel totalRow = new JPanel(new BorderLayout());
        totalRow.setOpaque(false);

        JLabel totalText = new JLabel("Selected Subtotal:");
        totalText.setFont(new Font("Segoe UI", Font.BOLD, 16));
        totalText.setForeground(TEXT_COLOR);
        totalRow.add(totalText, BorderLayout.WEST);

        totalSelectedLabel = new JLabel("\u20B10.00");
        totalSelectedLabel.setFont(new Font("Segoe UI", Font.BOLD, 22));
        totalSelectedLabel.setForeground(PH_PESO_COLOR);
        totalRow.add(totalSelectedLabel, BorderLayout.EAST);

        southPanel.add(totalRow);
        southPanel.add(Box.createVerticalStrut(15));

        // Bottom dialog buttons (Close & Checkout)
        JPanel buttonRow = new JPanel(new GridLayout(1, 2, 15, 0));
        buttonRow.setOpaque(false);

        JButton closeBtn = new RoundedButton("CONTINUE SHOPPING", 10, new Color(70, 70, 70), new Color(90, 90, 90));
        closeBtn.setActionCommand("CLOSE");
        closeBtn.addActionListener(this);

        JButton checkoutBtn = new RoundedButton("PROCEED TO CHECKOUT", 10, ACCENT_COLOR, ACCENT_HOVER);
        checkoutBtn.setActionCommand("CHECKOUT");
        checkoutBtn.addActionListener(this);

        buttonRow.add(closeBtn);
        buttonRow.add(checkoutBtn);
        southPanel.add(buttonRow);

        mainContainer.add(southPanel, BorderLayout.SOUTH);

        setContentPane(mainContainer);

        renderCartItems();
    }

    private void renderCartItems() {
        itemsContainer.removeAll();
        itemCheckboxes.clear();

        if (cart.isEmpty()) {
            JPanel emptyPanel = new JPanel(new GridBagLayout());
            emptyPanel.setOpaque(false);
            JLabel emptyLabel = new JLabel("Your cart is currently empty.");
            emptyLabel.setFont(new Font("Segoe UI", Font.ITALIC, 16));
            emptyLabel.setForeground(MUTED_COLOR);
            emptyPanel.add(emptyLabel);
            itemsContainer.add(emptyPanel);
        } else {
            for (int i = 0; i < cart.size(); i++) {
                CartItem item = cart.get(i);
                itemsContainer.add(createItemRow(item, i));
                itemsContainer.add(Box.createVerticalStrut(10));
            }
        }

        countLabel.setText(cart.size() + " item(s)");
        calculateSelectedTotal();
        itemsContainer.revalidate();
        itemsContainer.repaint();
    }

    private JPanel createItemRow(CartItem item, int index) {
        RoundedPanel card = new RoundedPanel(12, CARD_COLOR);
        card.setLayout(new BorderLayout(15, 0));
        card.setBorder(new EmptyBorder(12, 15, 12, 15));
        card.setMaximumSize(new Dimension(Integer.MAX_VALUE, 75));

        // Checkbox on the left
        JCheckBox checkBox = new JCheckBox();
        checkBox.setSelected(true);
        checkBox.setOpaque(false);
        checkBox.addItemListener(this);
        itemCheckboxes.add(checkBox);
        card.add(checkBox, BorderLayout.WEST);

        // Center item info
        JPanel infoPanel = new JPanel(new GridLayout(2, 1, 0, 4));
        infoPanel.setOpaque(false);

        JLabel nameLabel = new JLabel(item.getName());
        nameLabel.setFont(new Font("Segoe UI", Font.BOLD, 15));
        nameLabel.setForeground(TEXT_COLOR);

        JLabel detailsLabel = new JLabel("Category: " + item.getCategory() + "  |  Size: " + item.getSize());
        detailsLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        detailsLabel.setForeground(MUTED_COLOR);

        infoPanel.add(nameLabel);
        infoPanel.add(detailsLabel);
        card.add(infoPanel, BorderLayout.CENTER);

        // Right panel with price and remove button
        JPanel rightPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 15, 5));
        rightPanel.setOpaque(false);

        JLabel priceLabel = new JLabel("\u20B1" + String.format("%.2f", item.getPrice()));
        priceLabel.setFont(new Font("Segoe UI", Font.BOLD, 16));
        priceLabel.setForeground(PH_PESO_COLOR);

        JButton removeBtn = new RoundedButton("X", 8, DANGER_COLOR, DANGER_HOVER);
        removeBtn.setPreferredSize(new Dimension(30, 30));
        removeBtn.setFont(new Font("Segoe UI", Font.BOLD, 12));
        removeBtn.setActionCommand("REMOVE_" + index);
        removeBtn.addActionListener(this);

        rightPanel.add(priceLabel);
        rightPanel.add(removeBtn);
        card.add(rightPanel, BorderLayout.EAST);

        return card;
    }

    private void calculateSelectedTotal() {
        double total = 0.0;
        int checkedCount = 0;
        for (int i = 0; i < itemCheckboxes.size(); i++) {
            if (itemCheckboxes.get(i).isSelected() && i < cart.size()) {
                total += cart.get(i).getPrice();
                checkedCount++;
            }
        }
        totalSelectedLabel.setText("\u20B1" + String.format("%.2f", total));
    }

    @Override
    public void itemStateChanged(ItemEvent e) {
        calculateSelectedTotal();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();

        if (cmd.equals("CLOSE")) {
            dispose();
        } else if (cmd.equals("SELECT_ALL")) {
            for (JCheckBox cb : itemCheckboxes) {
                cb.setSelected(true);
            }
            calculateSelectedTotal();
        } else if (cmd.equals("DESELECT_ALL")) {
            for (JCheckBox cb : itemCheckboxes) {
                cb.setSelected(false);
            }
            calculateSelectedTotal();
        } else if (cmd.equals("REMOVE_SELECTED")) {
            List<CartItem> toRemove = new ArrayList<>();
            for (int i = 0; i < itemCheckboxes.size(); i++) {
                if (itemCheckboxes.get(i).isSelected() && i < cart.size()) {
                    toRemove.add(cart.get(i));
                }
            }
            if (toRemove.isEmpty()) {
                JOptionPane.showMessageDialog(this, "No items selected to remove.", "Notice", JOptionPane.INFORMATION_MESSAGE);
                return;
            }
            cart.removeAll(toRemove);
            shopPanel.updateCart();
            renderCartItems();
        } else if (cmd.startsWith("REMOVE_")) {
            try {
                int index = Integer.parseInt(cmd.substring(7));
                if (index >= 0 && index < cart.size()) {
                    cart.remove(index);
                    shopPanel.updateCart();
                    renderCartItems();
                }
            } catch (NumberFormatException ignored) {}
        } else if (cmd.equals("CHECKOUT")) {
            List<CartItem> selectedItems = new ArrayList<>();
            for (int i = 0; i < itemCheckboxes.size(); i++) {
                if (itemCheckboxes.get(i).isSelected() && i < cart.size()) {
                    selectedItems.add(cart.get(i));
                }
            }

            if (selectedItems.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please select at least one item to proceed to checkout.", "No Items Selected", JOptionPane.WARNING_MESSAGE);
                return;
            }

            dispose();
            new CheckoutDialog(parentFrame, shopPanel, cart, selectedItems).setVisible(true);
        }
    }
}
