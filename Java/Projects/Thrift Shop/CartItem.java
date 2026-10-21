/**
 * CartItem represents an item added to the shopping cart,
 * associating an Item with the customer's selected size.
 */
public class CartItem {
    private Item item;
    private String size;

    public CartItem(Item item, String size) {
        this.item = item;
        this.size = size;
    }

    public Item getItem() {
        return item;
    }

    public String getSize() {
        return size;
    }

    public void setSize(String size) {
        this.size = size;
    }

    public String getName() {
        return (item != null) ? item.getName() : "";
    }

    public double getPrice() {
        return (item != null) ? item.getPrice() : 0.0;
    }

    public String getCategory() {
        return (item != null) ? item.getCategory() : "";
    }

    public String getDescription() {
        return (item != null) ? item.getDescription() : "";
    }

    @Override
    public String toString() {
        return String.format("%s (%s) - \u20B1%.2f", getName(), size, getPrice());
    }
}
