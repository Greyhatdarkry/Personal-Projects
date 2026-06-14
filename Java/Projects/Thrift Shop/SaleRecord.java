import java.util.List;
import java.util.Date;

public class SaleRecord {
    private String customerName;
    private List<CartItem> items;
    private double totalAmount;
    private Date date;

    public SaleRecord(String customerName, List<CartItem> items, double totalAmount) {
        this.customerName = customerName;
        this.items = items;
        this.totalAmount = totalAmount;
        this.date = new Date();
    }

    public String getCustomerName() { return customerName; }
    public List<CartItem> getItems() { return items; }
    public double getTotalAmount() { return totalAmount; }
    public Date getDate() { return date; }
}
