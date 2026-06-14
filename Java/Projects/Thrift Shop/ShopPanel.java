import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
import java.util.Comparator;

public class ShopPanel extends JPanel implements ActionListener {
    private List<Item> inventory;
    private List<CartItem> cart;
    private List<SaleRecord> salesHistory;
    private JLabel totalLabel;
    private double currentTotal = 0.0;
    
    private JTabbedPane tabbedPane;
    private JTextField searchField;
    private RoundedPanel receiptPanel;
    private JTextArea receiptText;

    private static final Color BG_COLOR = new Color(18, 18, 18);
    private static final Color CARD_COLOR = new Color(30, 30, 30);
    private static final Color ACCENT_COLOR = new Color(74, 144, 226);
    private static final Color TEXT_COLOR = Color.WHITE;
    private static final Color PH_PESO_COLOR = new Color(255, 193, 7);

    public ShopPanel() {
        inventory = new ArrayList<>();
        cart = new ArrayList<>();
        salesHistory = new ArrayList<>();
        setupInventory();

        setLayout(new BorderLayout());
        setBackground(BG_COLOR);

        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(BG_COLOR);
        header.setBorder(new EmptyBorder(20, 40, 20, 40));

        JLabel title = new JLabel("JASON'S THRIFT SHOP");
        title.setFont(new Font("Segoe UI", Font.BOLD, 32));
        title.setForeground(TEXT_COLOR);
        header.add(title, BorderLayout.WEST);

        // Search Bar and Admin Button
        JPanel controls = new JPanel(new FlowLayout(FlowLayout.RIGHT, 15, 0));
        controls.setOpaque(false);

        searchField = new JTextField(15);
        searchField.setBackground(CARD_COLOR);
        searchField.setForeground(TEXT_COLOR);
        searchField.setCaretColor(TEXT_COLOR);
        searchField.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(ACCENT_COLOR, 1),
            BorderFactory.createEmptyBorder(5, 10, 5, 10)
        ));
        searchField.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                performSearch();
            }
        });
        
        JLabel searchIcon = new JLabel("Search: ");
        searchIcon.setForeground(Color.LIGHT_GRAY);
        
        JLabel sortLbl = new JLabel(" Sort: ");
        sortLbl.setForeground(Color.LIGHT_GRAY);
        String[] sortOptions = {"Default", "Price: Low to High", "Price: High to Low", "Name: A-Z"};
        final JComboBox<String> sortBox = new JComboBox<>(sortOptions);
        sortBox.setBackground(CARD_COLOR);
        sortBox.setForeground(TEXT_COLOR);
        sortBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                performSort((String)sortBox.getSelectedItem());
            }
        });

        JButton adminBtn = new RoundedButton("ADMIN", 8, new Color(50, 50, 60), new Color(70, 70, 80));
        adminBtn.setActionCommand("ADMIN_LOGIN");
        adminBtn.addActionListener(this);

        controls.add(searchIcon);
        controls.add(searchField);
        controls.add(sortLbl);
        controls.add(sortBox);
        controls.add(adminBtn);
        header.add(controls, BorderLayout.EAST);

        add(header, BorderLayout.NORTH);

        UIManager.put("TabbedPane.contentOpaque", false);
        tabbedPane = new JTabbedPane();
        tabbedPane.setBackground(CARD_COLOR);
        tabbedPane.setForeground(TEXT_COLOR);
        tabbedPane.setFont(new Font("Segoe UI", Font.BOLD, 14));
        tabbedPane.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        tabbedPane.addTab("ALL ITEMS", createTabContent("All"));
        tabbedPane.addTab("MEN'S COLLECTION", createTabContent("Men"));
        tabbedPane.addTab("WOMEN'S COLLECTION", createTabContent("Women"));

        add(tabbedPane, BorderLayout.CENTER);

        JPanel sidebar = new JPanel();
        sidebar.setLayout(new BoxLayout(sidebar, BoxLayout.Y_AXIS));
        sidebar.setBackground(CARD_COLOR);
        sidebar.setPreferredSize(new Dimension(350, 0));
        sidebar.setBorder(new EmptyBorder(30, 20, 30, 20));

        JLabel cartHeader = new JLabel("ORDER SUMMARY");
        cartHeader.setFont(new Font("Segoe UI", Font.BOLD, 22));
        cartHeader.setForeground(TEXT_COLOR);
        cartHeader.setAlignmentX(Component.CENTER_ALIGNMENT);
        sidebar.add(cartHeader);
        sidebar.add(Box.createVerticalStrut(30));

        totalLabel = new JLabel("Total: \u20B10.00");
        totalLabel.setFont(new Font("Segoe UI", Font.BOLD, 28));
        totalLabel.setForeground(PH_PESO_COLOR);
        totalLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        sidebar.add(totalLabel);
        sidebar.add(Box.createVerticalStrut(15));

        receiptPanel = new RoundedPanel(10, Color.WHITE);
        receiptPanel.setLayout(new BorderLayout());
        receiptPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        receiptPanel.setVisible(false);
        receiptPanel.setMaximumSize(new Dimension(300, 250));
        
        receiptText = new JTextArea();
        receiptText.setEditable(false);
        receiptText.setFont(new Font("Monospaced", Font.PLAIN, 11));
        receiptText.setForeground(Color.BLACK);
        receiptText.setBackground(Color.WHITE);
        
        JScrollPane receiptScroll = new JScrollPane(receiptText);
        receiptScroll.setBorder(null);
        receiptPanel.add(receiptScroll, BorderLayout.CENTER);
        
        JPanel receiptButtonsPanel = new JPanel(new GridLayout(1, 2, 5, 0));
        receiptButtonsPanel.setOpaque(false);
        
        JButton printReceiptBtn = new RoundedButton("Print", 8, new Color(50, 150, 50), new Color(80, 180, 80));
        printReceiptBtn.setActionCommand("PRINT_RECEIPT");
        printReceiptBtn.addActionListener(this);
        receiptButtonsPanel.add(printReceiptBtn);
        
        JButton closeReceiptBtn = new RoundedButton("Close", 8, new Color(200, 50, 50), new Color(220, 80, 80));
        closeReceiptBtn.setActionCommand("CLOSE_RECEIPT");
        closeReceiptBtn.addActionListener(this);
        receiptButtonsPanel.add(closeReceiptBtn);
        
        receiptPanel.add(receiptButtonsPanel, BorderLayout.SOUTH);
        
        sidebar.add(receiptPanel);

        sidebar.add(Box.createVerticalGlue());

        JButton viewCartBtn = new RoundedButton("VIEW CART", 10, new Color(50, 50, 50), new Color(80, 80, 80));
        viewCartBtn.setMaximumSize(new Dimension(Integer.MAX_VALUE, 50));
        viewCartBtn.setActionCommand("VIEW_CART");
        viewCartBtn.addActionListener(this);
        sidebar.add(viewCartBtn);
        sidebar.add(Box.createVerticalStrut(15));

        JButton checkoutBtn = new RoundedButton("CHECKOUT", 10, ACCENT_COLOR, new Color(100, 160, 240));
        checkoutBtn.setMaximumSize(new Dimension(Integer.MAX_VALUE, 50));
        checkoutBtn.setActionCommand("CHECKOUT");
        checkoutBtn.addActionListener(this);
        sidebar.add(checkoutBtn);

        add(sidebar, BorderLayout.EAST);
    }

    private void setupInventory() {
        inventory.add(new Item("Vintage Leather Jacket", 1500.00, "Men", "Classic 90s leather jacket."));
        inventory.add(new Item("Striped Cotton Shirt", 450.00, "Men", "Lightweight breathable cotton."));
        inventory.add(new Item("Denim Jeans (Regular Fit)", 850.00, "Men", "Durable denim for daily wear."));
        inventory.add(new Item("Woolen Sweater", 1200.00, "Men", "Cozy wool for cold nights."));
        inventory.add(new Item("Oversized Graphic Hoodie", 650.00, "Men", "Comfortable streetwear hoodie."));
        inventory.add(new Item("Cargo Pants", 700.00, "Men", "Utility pants with multiple pockets."));
        inventory.add(new Item("Plaid Flannel Shirt", 350.00, "Men", "Soft brushed cotton flannel."));
        inventory.add(new Item("Retro Windbreaker", 800.00, "Men", "Neon colors 80s style jacket."));
        inventory.add(new Item("Tailored Chinos", 600.00, "Men", "Smart casual slim fit trousers."));
        inventory.add(new Item("Basic Plain Tee", 250.00, "Men", "Essential everyday white t-shirt."));
        inventory.add(new Item("Distressed Denim Shorts", 450.00, "Men", "Perfect for summer casual outings."));

        inventory.add(new Item("Floral Summer Dress", 750.00, "Women", "Elegant floral print for summer."));
        inventory.add(new Item("Silk Evening Blouse", 900.00, "Women", "Smooth silk blouse for formal events."));
        inventory.add(new Item("High-Waist Pleated Skirt", 600.00, "Women", "Fashionable pleats in pastel pink."));
        inventory.add(new Item("Cashmere Cardigan", 1850.00, "Women", "Premium soft cashmere wool."));
        inventory.add(new Item("Cropped Denim Jacket", 800.00, "Women", "Stylish cropped fit jacket."));
        inventory.add(new Item("Vintage Boho Maxi Dress", 950.00, "Women", "Flowy bohemian style maxi."));
        inventory.add(new Item("Turtleneck Ribbed Knit", 550.00, "Women", "Warm and snug fitting top."));
        inventory.add(new Item("Wide-Leg Linen Pants", 750.00, "Women", "Breathable fabric for warm weather."));
        inventory.add(new Item("Satin Slip Dress", 850.00, "Women", "Chic and minimalist evening wear."));
        inventory.add(new Item("Oversized Blazer", 1100.00, "Women", "Structured fit for an office look."));
        inventory.add(new Item("Mom Jeans", 850.00, "Women", "Classic 90s high-waisted denim."));
    }

    private JScrollPane createTabContent(String filter) {
        JPanel grid = new JPanel(new GridBagLayout());
        grid.setBackground(BG_COLOR);
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(15, 15, 15, 15);
        gbc.gridx = 0;
        gbc.gridy = 0;

        int columns = 3;

        for (Item item : inventory) {
            if (filter.equals("All") || item.getCategory().equalsIgnoreCase(filter)) {
                grid.add(createItemCard(item), gbc);
                gbc.gridx++;
                if (gbc.gridx >= columns) {
                    gbc.gridx = 0;
                    gbc.gridy++;
                }
            }
        }
        
        gbc.gridx = 0;
        gbc.gridy++;
        gbc.weighty = 1.0;
        grid.add(Box.createVerticalGlue(), gbc);

        JScrollPane scrollPane = new JScrollPane(grid);
        scrollPane.setBorder(null);
        scrollPane.getVerticalScrollBar().setUnitIncrement(16);
        scrollPane.getViewport().setBackground(BG_COLOR);
        return scrollPane;
    }

    private JPanel createItemCard(Item item) {
        RoundedPanel card = new RoundedPanel(15, CARD_COLOR);
        card.setLayout(new BorderLayout());
        card.setPreferredSize(new Dimension(250, 320));
        card.setBorder(new EmptyBorder(15, 15, 15, 15));

        JLabel catTag = new JLabel(item.getCategory().toUpperCase());
        catTag.setFont(new Font("Segoe UI", Font.BOLD, 10));
        catTag.setForeground(ACCENT_COLOR);
        card.add(catTag, BorderLayout.NORTH);

        JPanel infoPanel = new JPanel(new GridLayout(3, 1));
        infoPanel.setOpaque(false);

        JLabel nameLabel = new JLabel("<html><body style='width: 150px'>" + item.getName() + "</body></html>");
        nameLabel.setFont(new Font("Segoe UI", Font.BOLD, 18));
        nameLabel.setForeground(TEXT_COLOR);

        JLabel priceLabel = new JLabel("\u20B1" + String.format("%.2f", item.getPrice()));
        priceLabel.setFont(new Font("Segoe UI", Font.BOLD, 22));
        priceLabel.setForeground(PH_PESO_COLOR);

        JLabel descLabel = new JLabel("<html><body style='width: 150px; color: #888888; font-size: 10px'>"
                + item.getDescription() + "</body></html>");

        infoPanel.add(nameLabel);
        infoPanel.add(priceLabel);
        infoPanel.add(descLabel);
        card.add(infoPanel, BorderLayout.CENTER);

        JButton addBtn = new RoundedButton("ADD TO CART", 8, new Color(50, 50, 50), new Color(80, 80, 80));
        addBtn.setActionCommand("ADD_" + item.getName());
        addBtn.addActionListener(this);
        card.add(addBtn, BorderLayout.SOUTH);

        return card;
    }

    public void updateCart() {
        currentTotal = 0;
        for (CartItem i : cart) {
            currentTotal += i.getPrice();
        }
        totalLabel.setText("Total: \u20B1" + String.format("%.2f", currentTotal));
    }

    public void recordSale(List<CartItem> purchasedItems, double total, String customerName) {
        salesHistory.add(new SaleRecord(customerName, new ArrayList<>(purchasedItems), total));
    }

    public void showReceipt(List<CartItem> purchasedItems, double total, String customerName) {
        StringBuilder sb = new StringBuilder();
        sb.append("----- JASON'S THRIFT SHOP -----\n");
        sb.append("Customer: ").append(customerName).append("\n");
        sb.append("-------------------------------\n");
        for (CartItem item : purchasedItems) {
            String name = item.getName();
            if (name.length() > 20) name = name.substring(0, 17) + "...";
            sb.append(String.format("%-20s P%.2f\n", name, item.getPrice()));
            sb.append("  Size: ").append(item.getSize()).append("\n");
        }
        sb.append("-------------------------------\n");
        sb.append(String.format("TOTAL:               P%.2f\n", total));
        sb.append("-------------------------------\n");
        sb.append("    THANK YOU FOR SHOPPING!    \n");
        
        receiptText.setText(sb.toString());
        receiptPanel.setVisible(true);
        revalidate();
        repaint();
    }

    private void performSort(String criteria) {
        if (criteria.equals("Price: Low to High")) {
            Collections.sort(inventory, new Comparator<Item>() {
                @Override
                public int compare(Item a, Item b) {
                    return Double.compare(a.getPrice(), b.getPrice());
                }
            });
        } else if (criteria.equals("Price: High to Low")) {
            Collections.sort(inventory, new Comparator<Item>() {
                @Override
                public int compare(Item a, Item b) {
                    return Double.compare(b.getPrice(), a.getPrice());
                }
            });
        } else if (criteria.equals("Name: A-Z")) {
            Collections.sort(inventory, new Comparator<Item>() {
                @Override
                public int compare(Item a, Item b) {
                    return a.getName().compareToIgnoreCase(b.getName());
                }
            });
        } else {
            Collections.sort(inventory, new Comparator<Item>() {
                @Override
                public int compare(Item a, Item b) {
                    return a.getName().compareToIgnoreCase(b.getName());
                }
            });
        }
        refreshUI();
    }

    public void refreshUI() {
        tabbedPane.removeAll();
        tabbedPane.addTab("ALL ITEMS", createTabContent("All"));
        tabbedPane.addTab("MEN'S COLLECTION", createTabContent("Men"));
        tabbedPane.addTab("WOMEN'S COLLECTION", createTabContent("Women"));
        revalidate();
        repaint();
    }

    private void performSearch() {
        String query = searchField.getText().toLowerCase();
        if (query.isEmpty()) {
            refreshUI();
            return;
        }

        JPanel grid = new JPanel(new GridBagLayout());
        grid.setBackground(BG_COLOR);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(15, 15, 15, 15);
        gbc.gridx = 0; gbc.gridy = 0;

        for (Item item : inventory) {
            if (item.getName().toLowerCase().contains(query) || item.getCategory().toLowerCase().contains(query)) {
                grid.add(createItemCard(item), gbc);
                gbc.gridx++;
                if (gbc.gridx >= 3) { gbc.gridx = 0; gbc.gridy++; }
            }
        }

        JScrollPane scrollPane = new JScrollPane(grid);
        scrollPane.setBorder(null);
        scrollPane.getViewport().setBackground(BG_COLOR);

        tabbedPane.removeAll();
        tabbedPane.addTab("SEARCH RESULTS: " + query.toUpperCase(), scrollPane);
        revalidate();
        repaint();
    }

    public List<Item> getInventory() { return inventory; }
    public List<SaleRecord> getSalesHistory() { return salesHistory; }

    @Override
    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        if (cmd.equals("ADMIN_LOGIN")) {
            showAdminLogin();
        } else if (cmd.equals("CLOSE_RECEIPT")) {
            receiptPanel.setVisible(false);
            revalidate();
            repaint();
        } else if (cmd.equals("PRINT_RECEIPT")) {
            try {
                receiptText.print();
            } catch (java.awt.print.PrinterException ex) {
                JOptionPane.showMessageDialog(this, "Failed to print receipt: " + ex.getMessage(), "Print Error", JOptionPane.ERROR_MESSAGE);
            }
        } else if (cmd.equals("VIEW_CART") || cmd.equals("CHECKOUT")) {
            if (cart.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Your cart is empty!", "Cart", JOptionPane.INFORMATION_MESSAGE);
            } else {
                new CartDialog((JFrame) SwingUtilities.getWindowAncestor(this), this, cart).setVisible(true);
            }
        } else if (cmd.startsWith("ADD_")) {
            String itemName = cmd.substring(4);
            Item foundItem = null;
            for (Item item : inventory) {
                if (item.getName().equals(itemName)) {
                    foundItem = item;
                    break;
                }
            }
            if (foundItem != null) {
                String[] sizes = {"Small", "Medium", "Large", "XL", "Free Size"};
                String selectedSize = (String) JOptionPane.showInputDialog(
                        this,
                        "Select Size for " + foundItem.getName() + ":",
                        "Choose Size",
                        JOptionPane.QUESTION_MESSAGE,
                        null,
                        sizes,
                        sizes[1]);

                if (selectedSize != null && !selectedSize.trim().isEmpty()) {
                    cart.add(new CartItem(foundItem, selectedSize));
                    updateCart();
                }
            }
        }
    }

    private void showAdminLogin() {
        JPanel loginPanel = new JPanel(new GridLayout(2, 2, 10, 10));
        loginPanel.setOpaque(false);
        
        JTextField usernameField = new JTextField();
        JPasswordField passwordField = new JPasswordField();
        
        loginPanel.add(new JLabel("Username:"));
        loginPanel.add(usernameField);
        loginPanel.add(new JLabel("Password:"));
        loginPanel.add(passwordField);

        int result = JOptionPane.showConfirmDialog(this, loginPanel, "Admin Login", JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
        
        if (result == JOptionPane.OK_OPTION) {
            String user = usernameField.getText();
            String pass = new String(passwordField.getPassword());
            
            if (user.equals("admin") && pass.equals("admin123")) {
                Thriftshop frame = (Thriftshop) SwingUtilities.getWindowAncestor(this);
                frame.showAdmin(this, salesHistory);
            } else {
                JOptionPane.showMessageDialog(this, "Invalid credentials!", "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
}
