import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;

public class CheckoutDialog extends JDialog implements ActionListener {
    private ShopPanel shopPanel;
    private List<CartItem> cart;
    private List<CartItem> selectedItems;
    
    private CardLayout cardLayout;
    private JPanel mainContainer;
    
    private double totalAmount = 0.0;
    private JLabel loadingLabel;

    private JTextField nameFieldDetails;
    private JTextField phoneFieldDetails;
    private JRadioButton cashlessRadio;
    private JTextField nameFieldCard;
    private JTextField numberFieldCard;

    private JCheckBox receiptCheckboxCashless;
    private JCheckBox receiptCheckboxCash;

    private Timer timer1;
    private Timer timer2;
    private Timer timer3;

    private static final Color BG_COLOR = new Color(18, 18, 18);
    private static final Color CARD_COLOR = new Color(30, 30, 30);
    private static final Color TEXT_COLOR = Color.WHITE;
    private static final Color ACCENT_COLOR = new Color(74, 144, 226);

    public CheckoutDialog(JFrame parent, ShopPanel shopPanel, List<CartItem> cart, List<CartItem> selectedItems) {
        super(parent, "Checkout", true);
        this.shopPanel = shopPanel;
        this.cart = cart;
        this.selectedItems = selectedItems;

        for (CartItem item : selectedItems) {
            totalAmount += item.getPrice();
        }

        setSize(400, 550);
        setLocationRelativeTo(parent);
        setUndecorated(true);

        cardLayout = new CardLayout();
        mainContainer = new RoundedPanel(20, BG_COLOR);
        mainContainer.setLayout(cardLayout);
        mainContainer.setBorder(new EmptyBorder(20, 20, 20, 20));

        mainContainer.add(createDetailsPanel(), "DETAILS");
        mainContainer.add(createPaymentModePanel(), "PAYMENT_MODE");
        mainContainer.add(createCashlessPanel(), "CASHLESS");
        mainContainer.add(createCashPanel(), "CASH");
        mainContainer.add(createLoadingPanel(), "LOADING");

        timer1 = new Timer(2000, this); timer1.setActionCommand("TIMER_1"); timer1.setRepeats(false);
        timer2 = new Timer(2500, this); timer2.setActionCommand("TIMER_2"); timer2.setRepeats(false);
        timer3 = new Timer(2000, this); timer3.setActionCommand("TIMER_3"); timer3.setRepeats(false);

        setContentPane(mainContainer);
    }

    private JPanel createDetailsPanel() {
        JPanel panel = new JPanel(new BorderLayout(0, 20));
        panel.setOpaque(false);

        JLabel title = new JLabel("RECIPIENT DETAILS");
        title.setFont(new Font("Segoe UI", Font.BOLD, 22));
        title.setForeground(TEXT_COLOR);
        title.setHorizontalAlignment(SwingConstants.CENTER);
        panel.add(title, BorderLayout.NORTH);

        JPanel form = new JPanel(new GridLayout(4, 1, 0, 10));
        form.setOpaque(false);

        JLabel nameLbl = new JLabel("Full Name:");
        nameLbl.setForeground(Color.LIGHT_GRAY);
        nameFieldDetails = new JTextField();
        nameFieldDetails.setBackground(CARD_COLOR);
        nameFieldDetails.setForeground(TEXT_COLOR);
        nameFieldDetails.setCaretColor(Color.WHITE);

        JLabel phoneLbl = new JLabel("Contact Number:");
        phoneLbl.setForeground(Color.LIGHT_GRAY);
        phoneFieldDetails = new JTextField();
        phoneFieldDetails.setBackground(CARD_COLOR);
        phoneFieldDetails.setForeground(TEXT_COLOR);
        phoneFieldDetails.setCaretColor(Color.WHITE);

        form.add(nameLbl);
        form.add(nameFieldDetails);
        form.add(phoneLbl);
        form.add(phoneFieldDetails);
        
        panel.add(form, BorderLayout.CENTER);

        JPanel bottom = new JPanel(new GridLayout(1, 2, 10, 0));
        bottom.setOpaque(false);
        JButton cancel = new RoundedButton("CANCEL", 10, new Color(80, 80, 80), new Color(100, 100, 100));
        cancel.setActionCommand("CANCEL");
        cancel.addActionListener(this);

        JButton next = new RoundedButton("NEXT", 10, ACCENT_COLOR, new Color(100, 160, 240));
        next.setActionCommand("NEXT_DETAILS");
        next.addActionListener(this);

        bottom.add(cancel);
        bottom.add(next);
        panel.add(bottom, BorderLayout.SOUTH);

        return panel;
    }

    private JPanel createPaymentModePanel() {
        JPanel panel = new JPanel(new BorderLayout(0, 20));
        panel.setOpaque(false);

        JLabel title = new JLabel("MODE OF PAYMENT");
        title.setFont(new Font("Segoe UI", Font.BOLD, 22));
        title.setForeground(TEXT_COLOR);
        title.setHorizontalAlignment(SwingConstants.CENTER);
        panel.add(title, BorderLayout.NORTH);

        JPanel options = new JPanel(new GridLayout(2, 1, 0, 15));
        options.setOpaque(false);

        JRadioButton cashRadio = new JRadioButton("Cash on Delivery / Pickup");
        cashRadio.setForeground(TEXT_COLOR);
        cashRadio.setOpaque(false);
        cashRadio.setSelected(true);

        cashlessRadio = new JRadioButton("Cashless (Credit/Debit Card)");
        cashlessRadio.setForeground(TEXT_COLOR);
        cashlessRadio.setOpaque(false);

        ButtonGroup bg = new ButtonGroup();
        bg.add(cashRadio);
        bg.add(cashlessRadio);

        options.add(cashRadio);
        options.add(cashlessRadio);
        
        panel.add(options, BorderLayout.CENTER);

        JPanel bottom = new JPanel(new GridLayout(1, 2, 10, 0));
        bottom.setOpaque(false);
        JButton back = new RoundedButton("BACK", 10, new Color(80, 80, 80), new Color(100, 100, 100));
        back.setActionCommand("BACK_TO_DETAILS");
        back.addActionListener(this);

        JButton next = new RoundedButton("PROCEED", 10, ACCENT_COLOR, new Color(100, 160, 240));
        next.setActionCommand("PROCEED_PAYMENT_MODE");
        next.addActionListener(this);

        bottom.add(back);
        bottom.add(next);
        panel.add(bottom, BorderLayout.SOUTH);

        return panel;
    }

    private JPanel createCashlessPanel() {
        GradientPanel panel = new GradientPanel(new Color(40, 40, 60), new Color(20, 20, 30), true);
        panel.setLayout(new BorderLayout(0, 15));
        panel.setBorder(new EmptyBorder(20, 20, 20, 20));

        JLabel title = new JLabel("CARD DETAILS");
        title.setFont(new Font("Segoe UI", Font.BOLD, 22));
        title.setForeground(Color.WHITE);
        title.setHorizontalAlignment(SwingConstants.CENTER);
        panel.add(title, BorderLayout.NORTH);

        JPanel form = new JPanel(new GridLayout(8, 1, 0, 5));
        form.setOpaque(false);

        form.add(createWhiteLabel("Card Type:"));
        JComboBox<String> cardType = new JComboBox<>(new String[]{"Debit Card", "Credit Card"});
        form.add(cardType);

        form.add(createWhiteLabel("Card Holder Name:"));
        nameFieldCard = new JTextField();
        form.add(nameFieldCard);

        form.add(createWhiteLabel("Card Number:"));
        numberFieldCard = new JTextField();
        form.add(numberFieldCard);

        JPanel split = new JPanel(new GridLayout(1, 2, 10, 0));
        split.setOpaque(false);
        JPanel cvcPanel = new JPanel(new BorderLayout()); cvcPanel.setOpaque(false);
        cvcPanel.add(createWhiteLabel("CVC/CVV:"), BorderLayout.NORTH);
        cvcPanel.add(new JTextField(), BorderLayout.CENTER);
        
        JPanel expPanel = new JPanel(new BorderLayout()); expPanel.setOpaque(false);
        expPanel.add(createWhiteLabel("Expiry (MM/YY):"), BorderLayout.NORTH);
        expPanel.add(new JTextField(), BorderLayout.CENTER);
        
        split.add(cvcPanel);
        split.add(expPanel);

        form.add(split);
        panel.add(form, BorderLayout.CENTER);

        JPanel bottom = new JPanel(new GridLayout(1, 2, 10, 0));
        bottom.setOpaque(false);
        JButton back = new RoundedButton("BACK", 10, new Color(80, 80, 80), new Color(100, 100, 100));
        back.setActionCommand("BACK_TO_PAYMENT_MODE");
        back.addActionListener(this);

        JButton pay = new RoundedButton("PAY \u20B1" + String.format("%.2f", totalAmount), 10, new Color(46, 204, 113), new Color(39, 174, 96));
        pay.setActionCommand("PAY_CASHLESS");
        pay.addActionListener(this);

        bottom.add(back);
        bottom.add(pay);

        receiptCheckboxCashless = new JCheckBox("Generate Receipt (Uncheck to save paper)");
        receiptCheckboxCashless.setForeground(Color.LIGHT_GRAY);
        receiptCheckboxCashless.setOpaque(false);
        receiptCheckboxCashless.setSelected(true);
        receiptCheckboxCashless.setHorizontalAlignment(SwingConstants.CENTER);

        JPanel bottomWrapper = new JPanel(new BorderLayout(0, 10));
        bottomWrapper.setOpaque(false);
        bottomWrapper.add(receiptCheckboxCashless, BorderLayout.NORTH);
        bottomWrapper.add(bottom, BorderLayout.CENTER);

        panel.add(bottomWrapper, BorderLayout.SOUTH);

        return panel;
    }

    private JLabel createWhiteLabel(String text) {
        JLabel l = new JLabel(text);
        l.setForeground(Color.LIGHT_GRAY);
        return l;
    }

    private JPanel createCashPanel() {
        JPanel panel = new JPanel(new BorderLayout(0, 20));
        panel.setOpaque(false);

        JLabel title = new JLabel("CASH PAYMENT");
        title.setFont(new Font("Segoe UI", Font.BOLD, 22));
        title.setForeground(TEXT_COLOR);
        title.setHorizontalAlignment(SwingConstants.CENTER);
        panel.add(title, BorderLayout.NORTH);

        JLabel info = new JLabel("<html><center>Total Amount to Pay:<br><br><font size='+3' color='#FFC107'><b>\u20B1" 
                                 + String.format("%.2f", totalAmount) + "</b></font><br><br>Please prepare exact amount if possible.</center></html>");
        info.setForeground(TEXT_COLOR);
        info.setHorizontalAlignment(SwingConstants.CENTER);
        panel.add(info, BorderLayout.CENTER);

        JPanel bottom = new JPanel(new GridLayout(1, 2, 10, 0));
        bottom.setOpaque(false);
        JButton back = new RoundedButton("BACK", 10, new Color(80, 80, 80), new Color(100, 100, 100));
        back.setActionCommand("BACK_TO_PAYMENT_MODE");
        back.addActionListener(this);

        JButton confirm = new RoundedButton("CONFIRM ORDER", 10, new Color(46, 204, 113), new Color(39, 174, 96));
        confirm.setActionCommand("CONFIRM_CASH");
        confirm.addActionListener(this);

        bottom.add(back);
        bottom.add(confirm);

        receiptCheckboxCash = new JCheckBox("Generate Receipt (Uncheck to save paper)");
        receiptCheckboxCash.setForeground(Color.LIGHT_GRAY);
        receiptCheckboxCash.setOpaque(false);
        receiptCheckboxCash.setSelected(true);
        receiptCheckboxCash.setHorizontalAlignment(SwingConstants.CENTER);

        JPanel bottomWrapper = new JPanel(new BorderLayout(0, 10));
        bottomWrapper.setOpaque(false);
        bottomWrapper.add(receiptCheckboxCash, BorderLayout.NORTH);
        bottomWrapper.add(bottom, BorderLayout.CENTER);

        panel.add(bottomWrapper, BorderLayout.SOUTH);

        return panel;
    }

    private JPanel createLoadingPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setOpaque(false);

        loadingLabel = new JLabel("Processing order...");
        loadingLabel.setFont(new Font("Segoe UI", Font.BOLD, 18));
        loadingLabel.setForeground(ACCENT_COLOR);
        loadingLabel.setHorizontalAlignment(SwingConstants.CENTER);
        panel.add(loadingLabel, BorderLayout.CENTER);

        return panel;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        if (cmd.equals("CANCEL")) {
            dispose();
        } else if (cmd.equals("NEXT_DETAILS")) {
            if (nameFieldDetails.getText().trim().isEmpty() || phoneFieldDetails.getText().trim().isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please fill in all details.");
                return;
            }
            cardLayout.show(mainContainer, "PAYMENT_MODE");
        } else if (cmd.equals("BACK_TO_DETAILS")) {
            cardLayout.show(mainContainer, "DETAILS");
        } else if (cmd.equals("PROCEED_PAYMENT_MODE")) {
            if (cashlessRadio.isSelected()) {
                cardLayout.show(mainContainer, "CASHLESS");
            } else {
                cardLayout.show(mainContainer, "CASH");
            }
        } else if (cmd.equals("BACK_TO_PAYMENT_MODE")) {
            cardLayout.show(mainContainer, "PAYMENT_MODE");
        } else if (cmd.equals("PAY_CASHLESS")) {
            if (nameFieldCard.getText().isEmpty() || numberFieldCard.getText().isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please fill in required fields.");
                return;
            }
            cardLayout.show(mainContainer, "LOADING");
            timer1.start();
        } else if (cmd.equals("CONFIRM_CASH")) {
            cardLayout.show(mainContainer, "LOADING");
            timer1.start();
        } else if (cmd.equals("TIMER_1")) {
            loadingLabel.setText("<html><center>Thank you for purchasing<br>please come again!</center></html>");
            timer2.start();
        } else if (cmd.equals("TIMER_2")) {
            loadingLabel.setText("Going back in the items...");
            timer3.start();
        } else if (cmd.equals("TIMER_3")) {
            boolean wantsReceipt = cashlessRadio.isSelected() ? receiptCheckboxCashless.isSelected() : receiptCheckboxCash.isSelected();
            cart.removeAll(selectedItems);
            shopPanel.updateCart();
            
            // Record the sale in admin records
            shopPanel.recordSale(selectedItems, totalAmount, nameFieldDetails.getText());
            
            if (wantsReceipt) {
                shopPanel.showReceipt(selectedItems, totalAmount, nameFieldDetails.getText());
            }
            dispose();
        }
    }
}
