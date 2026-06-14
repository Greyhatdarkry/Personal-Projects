// Encapsulates the details of a Thrift Shop item.
public class Item {
    private String name;
    private double price;
    private String category; // "Men" or "Women"
    private String description;

    public Item(String name, double price, String category, String description) {
        this.name = name;
        this.price = price;
        this.category = category;
        this.description = description;
    }

    // encapsulation
    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    public String getCategory() {
        return category;
    }

    public String getDescription() {
        return description;
    }

    @Override
    public String toString() {
        return String.format("%s (₱%.2f) - %s", name, price, category);
    }
}
