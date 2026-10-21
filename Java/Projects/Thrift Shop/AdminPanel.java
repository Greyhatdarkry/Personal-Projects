import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat;
import java.util.List;

/**
 * AdminPanel provides an administrative dashboard to monitor store sales,
 * review order transactions, and manage store inventory in real-time.
 * 
 * Implements ActionListener directly to avoid anonymous inner classes ($1.class).
 */
public class AdminPanel extends JPanel implements ActionListener {
    private Thriftshop mainFrame;
    private ShopPanel shopPanel;
    private List<SaleRecord> salesHistory;

    private JLabel totalSalesLabel;
    private JLabel totalOrdersLabel;
    private JLabel totalInventoryLabel;

    private DefaultTableModel salesTableModel;
    private JTable salesTable;

    private DefaultTableModel inventoryTableModel;
    private JTable inventoryTable;

    private SimpleDateFormat dateFormat;

    private static final Color BG_COLOR = new Color(18, 18, 18);
    private static final Color CARD_COLOR = new Color(30, 30, 30);
    private static final Color TEXT_COLOR = Color.WHITE;
    private static final Color ACCENT_COLOR = new Color(74, 144, 226);
    private static final Color ACCENT_HOVER = new Color(100, 160, 240);
    private static final Color PH_PESO_COLOR = new Color(255, 193, 7);
    private static final Color DANGER_COLOR = new Color(200, 50, 50);
    private static final Color DANGER_HOVER = new Color(230, 70, 70);
    private static final Color SUCCESS_COLOR = new Color(40, 167, 69);
    private static final Color SUCCESS_HOVER = new Color(55, 195, 85);
    private static final Color MUTED_COLOR = new Color(160, 160, 160);

    public AdminPanel(Thriftshop mainFrame, ShopPanel shopPanel, List<SaleRecord> salesHistory) {
        this.mainFrame = mainFrame;
        this.shopPanel = shopPanel;
        this.salesHistory = salesHistory;
        this.dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm");

        setLayout(new BorderLayout(0, 20));
        setBackground(BG_COLOR);
        setBorder(new EmptyBorder(25, 35, 25, 35));

        // Header Panel
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setOpaque(false);

        JPanel titleBlock = new JPanel(new GridLayout(2, 1, 0, 5));
        titleBlock.setOpaque(false);

        JLabel title = new JLabel("ADMINISTRATIVE DASHBOARD");
        title.setFont(new Font("Segoe UI", Font.BOLD, 28));
        title.setForeground(TEXT_COLOR);

        JLabel subtitle = new JLabel("Thrift Shop Operations, Sales Analytics & Inventory Control");
        subtitle.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        subtitle.setForeground(MUTED_COLOR);

        titleBlock.add(title);
        titleBlock.add(subtitle);
        headerPanel.add(titleBlock, BorderLayout.WEST);

        JButton backBtn = new RoundedButton("RETURN TO SHOP", 10, ACCENT_COLOR, ACCENT_HOVER);
        backBtn.setFont(new Font("Segoe UI", Font.BOLD, 14));
        backBtn.setActionCommand("BACK_TO_SHOP");
        backBtn.addActionListener(this);
        headerPanel.add(backBtn, BorderLayout.EAST);

        add(headerPanel, BorderLayout.NORTH);

        // Center: KPI metrics + Tabbed content
        JPanel centerContainer = new JPanel(new BorderLayout(0, 20));
        centerContainer.setOpaque(false);

        // KPI Metric Cards Row
        JPanel kpiRow = new JPanel(new GridLayout(1, 3, 20, 0));
        kpiRow.setOpaque(false);
        kpiRow.setPreferredSize(new Dimension(0, 100));

        totalSalesLabel = new JLabel("\u20B10.00");
        kpiRow.add(createKpiCard("TOTAL REVENUE", totalSalesLabel, PH_PESO_COLOR));

        totalOrdersLabel = new JLabel("0");
        kpiRow.add(createKpiCard("TOTAL TRANSACTIONS", totalOrdersLabel, ACCENT_COLOR));

        totalInventoryLabel = new JLabel("0");
        kpiRow.add(createKpiCard("INVENTORY ITEMS", totalInventoryLabel, SUCCESS_COLOR));

        centerContainer.add(kpiRow, BorderLayout.NORTH);

        // Tabbed Panel
        UIManager.put("TabbedPane.contentOpaque", false);
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.setBackground(CARD_COLOR);
        tabbedPane.setForeground(TEXT_COLOR);
        tabbedPane.setFont(new Font("Segoe UI", Font.BOLD, 14));

        tabbedPane.addTab("SALES HISTORY", createSalesTab());
        tabbedPane.addTab("INVENTORY MANAGEMENT", createInventoryTab());

        centerContainer.add(tabbedPane, BorderLayout.CENTER);
        add(centerContainer, BorderLayout.CENTER);

        refreshData();
    }

    private JPanel createKpiCard(String title, JLabel valueLabel, Color valueColor) {
        RoundedPanel card = new RoundedPanel(15, CARD_COLOR);
        card.setLayout(new BorderLayout());
        card.setBorder(new EmptyBorder(15, 20, 15, 20));

        JLabel titleLabel = new JLabel(title);
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        titleLabel.setForeground(MUTED_COLOR);
        card.add(titleLabel, BorderLayout.NORTH);

        valueLabel.setFont(new Font("Segoe UI", Font.BOLD, 26));
        valueLabel.setForeground(valueColor);
        card.add(valueLabel, BorderLayout.CENTER);

        return card;
    }

    private JPanel createSalesTab() {
        JPanel panel = new JPanel(new BorderLayout(0, 10));
        panel.setOpaque(false);
        panel.setBorder(new EmptyBorder(15, 10, 10, 10));

        String[] columns = {"Date & Time", "Customer Name", "Items Count", "Items Purchased", "Total Amount"};
        salesTableModel = new NonEditableTableModel(columns, 0);

        salesTable = new JTable(salesTableModel);
        styleTable(salesTable);

        JScrollPane scrollPane = new JScrollPane(salesTable);
        scrollPane.setBorder(BorderFactory.createLineBorder(new Color(45, 45, 45)));
        scrollPane.getViewport().setBackground(CARD_COLOR);
        panel.add(scrollPane, BorderLayout.CENTER);

        JPanel controls = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        controls.setOpaque(false);

        JButton viewDetailsBtn = new RoundedButton("View Order Receipt", 8, ACCENT_COLOR, ACCENT_HOVER);
        viewDetailsBtn.setActionCommand("VIEW_SALE_DETAILS");
        viewDetailsBtn.addActionListener(this);

        JButton refreshSalesBtn = new RoundedButton("Refresh History", 8, new Color(60, 60, 60), new Color(80, 80, 80));
        refreshSalesBtn.setActionCommand("REFRESH");
        refreshSalesBtn.addActionListener(this);

        controls.add(viewDetailsBtn);
        controls.add(refreshSalesBtn);
        panel.add(controls, BorderLayout.SOUTH);

        return panel;
    }

    private JPanel createInventoryTab() {
        JPanel panel = new JPanel(new BorderLayout(0, 10));
        panel.setOpaque(false);
        panel.setBorder(new EmptyBorder(15, 10, 10, 10));

        String[] columns = {"Item Name", "Category", "Price", "Description"};
        inventoryTableModel = new NonEditableTableModel(columns, 0);

        inventoryTable = new JTable(inventoryTableModel);
        styleTable(inventoryTable);

        JScrollPane scrollPane = new JScrollPane(inventoryTable);
        scrollPane.setBorder(BorderFactory.createLineBorder(new Color(45, 45, 45)));
        scrollPane.getViewport().setBackground(CARD_COLOR);
        panel.add(scrollPane, BorderLayout.CENTER);

        JPanel controls = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        controls.setOpaque(false);

        JButton addItemBtn = new RoundedButton("Add New Item", 8, SUCCESS_COLOR, SUCCESS_HOVER);
        addItemBtn.setActionCommand("ADD_ITEM");
        addItemBtn.addActionListener(this);

        JButton deleteItemBtn = new RoundedButton("Delete Selected Item", 8, DANGER_COLOR, DANGER_HOVER);
        deleteItemBtn.setActionCommand("DELETE_ITEM");
        deleteItemBtn.addActionListener(this);

        JButton refreshInvBtn = new RoundedButton("Refresh Inventory", 8, new Color(60, 60, 60), new Color(80, 80, 80));
        refreshInvBtn.setActionCommand("REFRESH");
        refreshInvBtn.addActionListener(this);

        controls.add(addItemBtn);
        controls.add(deleteItemBtn);
        controls.add(refreshInvBtn);
        panel.add(controls, BorderLayout.SOUTH);

        return panel;
    }

    private void styleTable(JTable table) {
        table.setBackground(CARD_COLOR);
        table.setForeground(TEXT_COLOR);
        table.setGridColor(new Color(45, 45, 45));
        table.setRowHeight(32);
        table.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        table.setSelectionBackground(new Color(55, 65, 80));
        table.setSelectionForeground(TEXT_COLOR);

        table.getTableHeader().setBackground(new Color(25, 25, 25));
        table.getTableHeader().setForeground(TEXT_COLOR);
        table.getTableHeader().setFont(new Font("Segoe UI", Font.BOLD, 13));
        table.getTableHeader().setReorderingAllowed(false);

        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(SwingConstants.CENTER);
        centerRenderer.setOpaque(false);
    }

    public void refreshData() {
        // Refresh Sales Table
        salesTableModel.setRowCount(0);
        double totalRevenue = 0.0;
        for (SaleRecord record : salesHistory) {
            totalRevenue += record.getTotalAmount();

            StringBuilder itemsSummary = new StringBuilder();
            List<CartItem> items = record.getItems();
            if (items != null) {
                for (int i = 0; i < items.size(); i++) {
                    CartItem ci = items.get(i);
                    itemsSummary.append(ci.getName()).append(" (").append(ci.getSize()).append(")");
                    if (i < items.size() - 1) itemsSummary.append(", ");
                }
            }

            salesTableModel.addRow(new Object[]{
                dateFormat.format(record.getDate()),
                record.getCustomerName(),
                (items != null ? items.size() : 0),
                itemsSummary.toString(),
                String.format("\u20B1%.2f", record.getTotalAmount())
            });
        }

        // Refresh Inventory Table
        inventoryTableModel.setRowCount(0);
        List<Item> inventory = shopPanel.getInventory();
        for (Item item : inventory) {
            inventoryTableModel.addRow(new Object[]{
                item.getName(),
                item.getCategory(),
                String.format("\u20B1%.2f", item.getPrice()),
                item.getDescription()
            });
        }

        // Update KPI Cards
        totalSalesLabel.setText(String.format("\u20B1%.2f", totalRevenue));
        totalOrdersLabel.setText(String.valueOf(salesHistory.size()));
        totalInventoryLabel.setText(String.valueOf(inventory.size()));
    }

    private void handleAddItem() {
        JPanel form = new JPanel(new GridLayout(4, 2, 10, 12));
        form.setOpaque(false);

        JTextField nameField = new JTextField();
        String[] categories = {"Men", "Women"};
        JComboBox<String> categoryCombo = new JComboBox<>(categories);
        JTextField priceField = new JTextField();
        JTextField descField = new JTextField();

        form.add(new JLabel("Item Name:"));
        form.add(nameField);
        form.add(new JLabel("Category:"));
        form.add(categoryCombo);
        form.add(new JLabel("Price (\u20B1):"));
        form.add(priceField);
        form.add(new JLabel("Description:"));
        form.add(descField);

        int result = JOptionPane.showConfirmDialog(
            this, form, "Add New Inventory Item",
            JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE
        );

        if (result == JOptionPane.OK_OPTION) {
            String name = nameField.getText().trim();
            String cat = (String) categoryCombo.getSelectedItem();
            String priceStr = priceField.getText().trim();
            String desc = descField.getText().trim();

            if (name.isEmpty() || priceStr.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Name and Price are required.", "Input Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            try {
                double price = Double.parseDouble(priceStr);
                Item newItem = new Item(name, price, cat, desc);
                shopPanel.getInventory().add(newItem);
                shopPanel.refreshUI();
                refreshData();
                JOptionPane.showMessageDialog(this, "Item successfully added to inventory!", "Success", JOptionPane.INFORMATION_MESSAGE);
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Invalid price format. Please enter a valid number.", "Number Format Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void handleDeleteItem() {
        int selectedRow = inventoryTable.getSelectedRow();
        if (selectedRow < 0) {
            JOptionPane.showMessageDialog(this, "Please select an item from the table to delete.", "No Selection", JOptionPane.WARNING_MESSAGE);
            return;
        }

        String itemName = (String) inventoryTableModel.getValueAt(selectedRow, 0);
        int confirm = JOptionPane.showConfirmDialog(
            this,
            "Are you sure you want to delete \"" + itemName + "\" from inventory?",
            "Confirm Delete",
            JOptionPane.YES_NO_OPTION,
            JOptionPane.QUESTION_MESSAGE
        );

        if (confirm == JOptionPane.YES_OPTION) {
            List<Item> inventory = shopPanel.getInventory();
            if (selectedRow < inventory.size()) {
                inventory.remove(selectedRow);
                shopPanel.refreshUI();
                refreshData();
            }
        }
    }

    private void handleViewSaleDetails() {
        int selectedRow = salesTable.getSelectedRow();
        if (selectedRow < 0) {
            JOptionPane.showMessageDialog(this, "Please select a transaction to view details.", "No Selection", JOptionPane.WARNING_MESSAGE);
            return;
        }

        if (selectedRow < salesHistory.size()) {
            SaleRecord record = salesHistory.get(selectedRow);
            StringBuilder sb = new StringBuilder();
            sb.append("----- TRANSACTION RECEIPT -----\n");
            sb.append("Date: ").append(dateFormat.format(record.getDate())).append("\n");
            sb.append("Customer: ").append(record.getCustomerName()).append("\n");
            sb.append("-------------------------------\n");
            if (record.getItems() != null) {
                for (CartItem ci : record.getItems()) {
                    sb.append(String.format("%-20s \u20B1%.2f (Size: %s)\n", ci.getName(), ci.getPrice(), ci.getSize()));
                }
            }
            sb.append("-------------------------------\n");
            sb.append(String.format("TOTAL: \u20B1%.2f\n", record.getTotalAmount()));

            JTextArea textArea = new JTextArea(sb.toString());
            textArea.setEditable(false);
            textArea.setFont(new Font("Monospaced", Font.PLAIN, 12));

            JOptionPane.showMessageDialog(this, new JScrollPane(textArea), "Transaction Details", JOptionPane.PLAIN_MESSAGE);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();

        if (cmd.equals("BACK_TO_SHOP")) {
            mainFrame.showShop();
        } else if (cmd.equals("REFRESH")) {
            refreshData();
        } else if (cmd.equals("ADD_ITEM")) {
            handleAddItem();
        } else if (cmd.equals("DELETE_ITEM")) {
            handleDeleteItem();
        } else if (cmd.equals("VIEW_SALE_DETAILS")) {
            handleViewSaleDetails();
        }
    }

    private static class NonEditableTableModel extends DefaultTableModel {
        public NonEditableTableModel(Object[] columnNames, int rowCount) {
            super(columnNames, rowCount);
        }

        @Override
        public boolean isCellEditable(int row, int column) {
            return false;
        }
    }
}
